from model import segmentation
from model.segmentation import SegmentationModel
from model.segmentation import ImagePreProcessing


def main():

    imageURL1 = "https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg"
    # imageURL2 = "https://storage.googleapis.com/segmentation-testing/testing_images1/beach.jpeg"
    # imageURL3 = "https://storage.googleapis.com/segmentation-testing/testing_images1/buildings.JPG"
    # create model
    model = SegmentationModel()
    predictor = model.builtModel(UsingCPU=True) #set to False when using a GPU
    # make list of images to run
    image_preprocessing = ImagePreProcessing()
    image_preprocessing.loadImage(imageURL1)
    # image_preprocessing.loadImage(imageURL2)
    # image_preprocessing.loadImage(imageURL3)
    imageList = image_preprocessing.getImages()
    # perform prediction for every image
    for imageData in imageList:
        imageURL, image = imageData
        prediction = model.getPrediction(predictor, image)
        print("Image URL:", imageURL)
        # print(">>> Instance segmentation classes prediction:\n", prediction["instances"].pred_classes)
        # print(">>> Instance segmentation mask prediction:\n", prediction["instances"].pred_masks)
        # print(">>> Panoptic segmentation mask prediction:\n", prediction["panoptic_seg"][1])
        labels_things, labels_stuff = model.getLabels_PanopticSeg(prediction)
        print(">>>Panoptic Seg (things) labels:", labels_things)
        print(">>>Panoptic Seg (stuff) labels:", labels_stuff)
        masks, mask_labels = model.getMasks_InstanceSeg(prediction, labels=True)
        print(">>>Instance Seg (things) mask labels:", mask_labels)
        for i in range(0, len(masks)):
            print("Label:", mask_labels[i])
            print(masks[i])

if __name__ == "__main__":
    main()