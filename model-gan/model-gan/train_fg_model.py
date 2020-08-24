# TPU imports
import warnings
import torch_xla
import torch_xla.debug.metrics as met
import torch_xla.distributed.data_parallel as dp
import torch_xla.distributed.parallel_loader as pl
import torch_xla.utils.utils as xu
import torch_xla.core.xla_model as xm
import torch_xla.distributed.xla_multiprocessing as xmp
import torch_xla.test.test_utils as test_utils
import torch_xla.utils.serialization as xser
import warnings

warnings.filterwarnings("ignore")

#Original Imports
import argparse
import os, time
from shutil import copyfile
import torch
import torch.nn as nn
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
from torchvision import transforms
from torch.utils.data import DataLoader, DistributedSampler #Added DistributedSamplerfor TPU purposes
from torch.autograd import Variable
from data_loader_fg_model import CocoData
from utils import  show_result, mse_loss
from networks import Discriminator, Generator_FG
from Feature_Matching import VGGLoss

parser = argparse.ArgumentParser()

parser.add_argument('--log_dir', type=str, default='log',
help='Name of the log folder')
parser.add_argument('--save_models', type=bool, default=True,
help='Set True if you want to save trained models')
parser.add_argument('--pre_trained_model_path', type=str, default=None,
help='Pre-trained model path')
parser.add_argument('--pre_trained_model_epoch', type=str, default=None,
help='Pre-trained model epoch e.g 200')
parser.add_argument('--train_imgs_path', type=str, default='coco/images/train2017',
help='Path to training images')
parser.add_argument('--train_annotation_path', type=str, default='coco/annotations/instances_train2017.json',
help='Path to annotation file, .json file')
parser.add_argument('--category_names', type=str, default='giraffe,elephant,zebra,sheep,cow,bear',
help='List of categories in MS-COCO dataset')
parser.add_argument('--num_test_img', type=int, default=16,
help='Number of images saved during training')
parser.add_argument('--img_size', type=int, default=128,
help='Generated image size')
parser.add_argument('--local_patch_size', type=int, default=128,
help='Image size of instance images after interpolation')
parser.add_argument('--batch_size', type=int, default=16,
help='Mini-batch size')
parser.add_argument('--train_epoch', type=int, default=100, #Originally set at 400
help='Maximum training epoch')
parser.add_argument('--lr', type=float, default=0.0002,
help='Initial learning rate')
parser.add_argument('--optim_step_size', type=int, default=20, #Originally set at 80
help='Learning rate decay step size')
parser.add_argument('--optim_gamma', type=float, default=0.5,
help='Learning rate decay ratio')
parser.add_argument('--critic_iter', type=int, default=5,
help='Number of discriminator update against each generator update')
parser.add_argument('--noise_size', type=int, default=128,
help='Noise vector size')
parser.add_argument('--lambda_FM', type=float, default=1,
help='Trade-off param for feature matching loss')
parser.add_argument('--lambda_recon', type=float, default=0.00001,
help='Trade-off param for reconstruction loss')
parser.add_argument('--num_res_blocks', type=int, default=5,
help='Number of residual block in generator network')
parser.add_argument('--trade_off_G', type=float, default=0.1,
help='Trade-off parameter which controls gradient flow to generator from D_local and D_glob')
parser.add_argument('--num_workers', type=int, default=4, #Added for TPU purposes
help='Number of workers to be utilized on device')
parser.add_argument('--num_cores', type=int, default=8, #Added for TPU purposes
help='Number of cores to be on device')
    
opt = parser.parse_args()
FLAGS = vars(opt) #Added for TPU purposes
print(opt)

def main(rank):
    
    #Seed - Added for TPU purposes
    torch.manual_seed(1)
       
    #Create log folder
    root = 'result_fg/'
    model = 'coco_model_'
    result_folder_name = 'images_' + FLAGS['log_dir']
    model_folder_name = 'models_' + FLAGS['log_dir']
    if not os.path.isdir(root):
        os.mkdir(root)
    if not os.path.isdir(root + result_folder_name):
        os.mkdir(root + result_folder_name)
    if not os.path.isdir(root + model_folder_name):
        os.mkdir(root + model_folder_name)
    
    #Save the script
    copyfile(os.path.basename(__file__), root + result_folder_name + '/' + os.path.basename(__file__))
    
    #Define transformation for dataset images - e.g scaling
    transform = transforms.Compose(
        [
            transforms.Scale((FLAGS['img_size'],FLAGS['img_size'])),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ]
    ) 
    #Load dataset
    category_names = FLAGS['category_names'].split(',')
    
    #Serial Executor - This is needed to spread inside TPU for memory purposes
    SERIAL_EXEC = xmp.MpSerialExecutor()
    
    #Define Dataset
    dataset = SERIAL_EXEC.run(
        lambda: CocoData(
            root = FLAGS['train_imgs_path'],
            annFile = FLAGS['train_annotation_path'],
            category_names = category_names,
            transform=transform,
            final_img_size=FLAGS['img_size']
        )
    )
    
    #Discard images contain very small instances  
    dataset.discard_small(min_area=0.03, max_area=1)
    
    #Define data sampler - Added for TPU purposes
    train_sampler = DistributedSampler(
        dataset,
        num_replicas=xm.xrt_world_size(),
        rank=xm.get_ordinal(),
        shuffle=True
    )

    #Define data loader
    train_loader = DataLoader( #Modified for TPU purposes
        dataset,
        batch_size=FLAGS['batch_size'],
        sampler=train_sampler,
        num_workers=FLAGS['num_workers']
        # shuffle=True
    )

    #Define device - Added for TPU purposes
    device = xm.xla_device(devkind='TPU')

    #For evaluation define fixed masks and noises
    data_iter = iter(train_loader)
    sample_batched = data_iter.next()  
    x_fixed = sample_batched['image'][0:FLAGS['num_test_img']]
    x_fixed = Variable(x_fixed.to(device))
    y_fixed = sample_batched['single_fg_mask'][0:FLAGS['num_test_img']]
    y_fixed = Variable(y_fixed.to(device))
    z_fixed = torch.randn((FLAGS['num_test_img'],FLAGS['noise_size']))
    z_fixed = Variable(z_fixed.to(device))
    
    #Define networks
    generator = Generator_FG(
        z_dim=FLAGS['noise_size'],
        label_channel=len(category_names),
        num_res_blocks=FLAGS['num_res_blocks']
    )

    discriminator_glob = Discriminator(
        channels=3+len(category_names)
    )

    discriminator_instance = Discriminator(
        channels=3+len(category_names),
        input_size=FLAGS['local_patch_size']
    )

    WRAPPED_GENERATOR = xmp.MpModelWrapper(generator) #Added for TPU purposes
    WRAPPED_DISCRIMINATOR_GLOB = xmp.MpModelWrapper(discriminator) #Added for TPU purposes
    WRAPPED_DISCRIMINATOR_INSTANCE = xmp.MpModelWrapper(discriminator) #Added for TPU purposes

    G_fg = WRAPPED_GENERATOR.to(device) #Modified for TPU purposes
    D_glob = WRAPPED_DISCRIMINATOR.to(device) #Modified for TPU purposes
    D_instance = WRAPPED_DISCRIMINATOR.to(device) #Modified for TPU purposes
    
    #Load parameters from pre-trained models
    if FLAGS['pre_trained_model_path'] != None and FLAGS['pre_trained_model_epoch'] != None:
        try:
            G_fg.load_state_dict(xser.load(FLAGS['pre_trained_model_path'] + 'G_fg_epoch_' + FLAGS['pre_trained_model_epoch']))
            D_glob.load_state_dict(xser.load(FLAGS['pre_trained_model_path'] + 'D_glob_epoch_' + FLAGS['pre_trained_model_epoch']))
            D_instance.load_state_dict(xser.load(FLAGS['pre_trained_model_path'] + 'D_local_epoch_' + FLAGS['pre_trained_model_epoch']))
  
            xm.master_print('Parameters are loaded!')
        except:
            xm.master_print('Error: Pre-trained parameters are not loaded!')
            pass
    
    #Define interpolation operation
    up_instance =  nn.Upsample(
        size=(FLAGS['local_patch_size'],FLAGS['local_patch_size']),
        mode='bilinear'
    )
    
    #Define pooling operation for the case that image size and local patch size are mismatched
    pooling_instance = nn.Sequential()
    if FLAGS['local_patch_size']!=FLAGS['img_size']:
        pooling_instance.add_module(
            '0',
            nn.AvgPool2d(int(FLAGS['img_size']/FLAGS['local_patch_size']))
        )
        
    #Define training loss function - binary cross entropy
    BCE_loss = nn.BCELoss()
    
    #Define feature matching loss
    criterionVGG = VGGLoss()
    criterionVGG = criterionVGG.to(device) #Modified for TPU Purposes
         
    #Define optimizer
    G_local_optimizer = optim.Adam(
        G_fg.parameters(),
        lr=FLAGS['lr'],
        betas=(0.0, 0.9)
    )
    D_local_optimizer = optim.Adam(
        list(filter(lambda p: p.requires_grad, D_glob.parameters())) + list(filter(lambda p: p.requires_grad, D_instance.parameters())),
        lr=FLAGS['lr'],
        betas=(0.0,0.9)
    )

    #Deine learning rate scheduler
    scheduler_G = lr_scheduler.StepLR(
        G_local_optimizer,
        step_size=FLAGS['optim_step_size'],
        gamma=FLAGS['optim_gamma']
    )
    scheduler_D = lr_scheduler.StepLR(
        D_local_optimizer,
        step_size=FLAGS['optim_step_size'],
        gamma=FLAGS['optim_gamma']
    )
    
    #----------------------------TRAIN-----------------------------------------
    xm.master_print('training start!')
    tracker = xm.RateTracker() #Added for TPU reasons
    start_time = time.time()
    
    for epoch in range(FLAGS['train_epoch']):
        epoch_start_time = time.time()
        para_loader = pl.ParallelLoader(train_loader, [device]) #Added for TPU purposes
        loader = para_loader.per_device_loader(device) #Added for TPU purposes
         
        D_local_losses = []
        G_local_losses = []
    
        y_real_ = torch.ones(FLAGS['batch_size'])
        y_fake_ = torch.zeros(FLAGS['batch_size'])
        y_real_ = Variable(y_real_.to(device)) #Modified for TPU purposes
        y_fake_ = Variable(y_fake_.to(device)) #Modified for TPU purposes

        data_iter = iter(loader)
        num_iter = 0

        while num_iter < len(loader): #Modified for TPU purposes 
            j=0
            while j < FLAGS['critic_iter'] and num_iter < len(loader):
                j += 1
                sample_batched = data_iter.next()  
                num_iter += 1

                x_ = sample_batched['image']
                x_ = Variable(x_.to(device)) #Modified for TPU purposes

                y_ = sample_batched['single_fg_mask']
                y_ = Variable(y_.to(device)) #Modified for TPU purposes

                fg_mask = sample_batched['seg_mask']
                fg_mask = Variable(fg_mask.to(device)) #Modified for TPU purposes

                y_instances = sample_batched['mask_instance']
                bbox = sample_batched['bbox']
                
                mini_batch = x_.size()[0]
                if mini_batch != FLAGS['batch_size']:
                    break
                
                #Update discriminators - D 
                #Real examples
                D_glob.zero_grad()
                D_instance.zero_grad()
                    
                y_reduced = torch.sum(y_,1).clamp(0,1).view(y_.size(0),1,FLAGS['img_size'],FLAGS['img_size'])
                
                x_d = torch.cat([x_,fg_mask],1)
                
                x_instances = torch.zeros((FLAGS['batch_size'],3,FLAGS['local_patch_size'],FLAGS['local_patch_size']))
                x_instances = Variable(x_instances.to(device))
                y_instances = Variable(y_instances.to(device))
                y_instances = pooling_instance(y_instances)
                G_instances = torch.zeros((FLAGS['batch_size'],3,FLAGS['local_patch_size'],FLAGS['local_patch_size']))
                G_instances = Variable(G_instances.to(device))
                      
                #Obtain instances
                for t in range(x_d.size()[0]):
                    x_instance = x_[t,0:3,bbox[0][t]:bbox[1][t],bbox[2][t]:bbox[3][t]] 
                    x_instance = x_instance.contiguous().view(1,x_instance.size()[0],x_instance.size()[1],x_instance.size()[2]) 
                    x_instances[t] = up_instance(x_instance)
                    
                D_result_instance = D_instance(torch.cat([x_instances,y_instances],1)).squeeze()       
                D_result = D_glob(x_d).squeeze()
                D_real_loss = BCE_loss(D_result, y_real_) +  BCE_loss(D_result_instance, y_real_)
                D_real_loss.backward()
                
                #Fake examples
                z_ = torch.randn((mini_batch,FLAGS['noise_size']))
                z_ = Variable(z_.to(device))
    
                #Generate fake images
                G_fg_result = G_fg(z_,y_, torch.mul(x_,(1-y_reduced)))
                G_result_d = torch.cat([G_fg_result,fg_mask],1) 
                            
                #Obtain fake instances
                for t in range(x_d.size()[0]):
                    G_instance = G_result_d[t,0:3,bbox[0][t]:bbox[1][t],bbox[2][t]:bbox[3][t]] 
                    G_instance = G_instance.contiguous().view(1,G_instance.size()[0],G_instance.size()[1],G_instance.size()[2]) 
                    G_instances[t] = up_instance(G_instance)
                
                
                D_result_instance = D_instance(torch.cat([G_instances,y_instances],1).detach()).squeeze() 
                D_result = D_glob(G_result_d.detach()).squeeze() 
                D_fake_loss = BCE_loss(D_result, y_fake_) +  BCE_loss(D_result_instance, y_fake_)
                D_fake_loss.backward()

                xm.optimizer_step(D_local_optimizer) #Modified for TPU purposes
                
                D_train_loss = D_real_loss + D_fake_loss
                D_local_losses.append(D_train_loss.data[0])
    
            if mini_batch != FLAGS['batch_size']:
                break  
            
            #Update generator G
            G_fg.zero_grad()   
            D_result = D_glob(G_result_d).squeeze() 
            D_result_instance = D_instance(torch.cat([G_instances,y_instances],1)).squeeze() 
            G_train_loss = (1-FLAGS['trade_off_G'])*BCE_loss(D_result, y_real_) + FLAGS['trade_off_G']*BCE_loss(D_result_instance, y_real_) 
            
            #Feature matching loss between generated image and corresponding ground truth
            FM_loss = criterionVGG(G_fg_result, x_)
            
            #Reconstruction loss
            Recon_loss = mse_loss(torch.mul(x_,(1-y_reduced) ), torch.mul(G_fg_result,(1-y_reduced))  )
    
            total_loss = G_train_loss + FLAGS['lambda_FM']*FM_loss + FLAGS['lambda_recon']*Recon_loss
            total_loss.backward() 

            xm.optimizer_step(G_local_optimizer)

            G_local_losses.append(G_train_loss.data[0])
    
            xm.master_print('loss_d: %.3f, loss_g: %.3f' % (D_train_loss.data[0],G_train_loss.data[0]))
            if (num_iter % 100) == 0:
                xm.master_print('%d - %d complete!' % ((epoch+1), num_iter))
                xm.master_print(result_folder_name)

        #Modified location of the scheduler step to avoid warning
        scheduler_G.step()
        scheduler_D.step()

        epoch_end_time = time.time()
        per_epoch_ptime = epoch_end_time - epoch_start_time
        xm.master_print('[%d/%d] - ptime: %.2f, loss_d: %.3f, loss_g: %.3f' % ((epoch + 1), FLAGS['train_epoch'], per_epoch_ptime, torch.mean(torch.FloatTensor(D_local_losses)), torch.mean(torch.FloatTensor(G_local_losses))))
    
        #Save images
        G_fg.eval()
        
        if epoch == 0:
            show_result(
                (epoch+1),
                x_fixed,
                save=True,
                path=root + result_folder_name+ '/' + model + str(epoch + 1 ) + '_gt.png'
            )
            for t in range(y_fixed.size()[1]):
                show_result(
                    (epoch+1),
                    y_fixed[:,t:t+1,:,:],
                    save=True,
                    path=root + result_folder_name+ '/' + model + str(epoch + 1 ) +'_'+ str(t) +'_masked.png'
                )
            
        show_result(
            (epoch+1),
            G_fg(
                z_fixed,
                y_fixed,
                torch.mul(
                    x_fixed,
                    (1-torch.sum(y_fixed,1).view(y_fixed.size(0),1,FLAGS['img_size'],FLAGS['img_size']))
                )
            ),
            save=True,
            path=root + result_folder_name+ '/' + model + str(epoch + 1 ) + '_fg.png'
        )
        
        G_fg.train()
        
        #Save model params
        if FLAGS['save_models'] and (epoch>11 and epoch % 10 == 0 ):
            xser.save(
                G_fg.state_dict(),
                root + model_folder_name + '/' + model + 'G_fg_epoch_'+str(epoch)+'.pth'
                master_only=True
            )
            xser.save(
                D_glob.state_dict(),
                root + model_folder_name + '/' + model + 'D_glob_epoch_'+str(epoch)+'.pth'
                master_only=True
            )
            xser.save(
                D_instance.state_dict(),
                root + model_folder_name + '/' + model + 'D_local_epoch_'+str(epoch)+'.pth'
                master_only=True
            )
                         
    end_time = time.time()
    total_ptime = end_time - start_time
    xm.master_print("Training finish!... save training results")
    xm.master_print('Training time: ' + str(total_ptime))


if __name__ == '__main__':
    # main()
        def _mp_fn(rank, flags):
        global FLAGS
        FLAGS = flags
        torch.set_default_tensor_type('torch.FloatTensor')
        main(rank)

    xmp.spawn(_mp_fn, args=(FLAGS,), nprocs=FLAGS['num_cores'], start_method='fork')