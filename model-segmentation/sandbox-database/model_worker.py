# from model import segmentation
# from model.segmentation import SegmentationModel
# from model.segmentation import ImagePreProcessing


# import pickle


def test_sqlAlchemy():
    
    pass





""" import datetime

print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())) """


def main():

    imageURL1 = "https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg"

    # Create model
    model = SegmentationModel()
    predictor = model.builtModel(UsingCPU=True)

    # Make list of images to run
    image_preprocessing = ImagePreProcessing()
    image_preprocessing.loadImage(imageURL1)
    imageList = image_preprocessing.getImages()

    # Perform prediction for every image
    for imageData in imageList:
        imageURL, image = imageData
        prediction = model.getPrediction(predictor, image)
        print("Image URL:", imageURL)

        labels_things, labels_stuff = model.getLabels_PanopticSeg(prediction)

        masks_nparr, mask_labels = model.getMasks_InstanceSeg(prediction, labels=True)

        # Here add output to database


if __name__ == "__main__":
    # main()
    test_sqlAlchemy()