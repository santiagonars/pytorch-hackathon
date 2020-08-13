from model import segmentation
from model.segmentation import SegmentationModel
from model.segmentation import ImagePreProcessing
import json

from flask import Flask, jsonify, request
# NOTE: This implementation only works for one image per call

app = Flask(__name__)
model = SegmentationModel()                                   # Create model object
predictor = model.builtModel(UsingCPU=True)                   # Set to False when using a GPU


# Pre-Process the image(s) to get ready to as input format for model
def preprocess_data(imageURL):
    image_preprocessing = ImagePreProcessing()                # Create object to pre-process image
    image_preprocessing.loadImage(imageURL)                   # Load image to be processed (this can be done multiple times)
    imageList = image_preprocessing.getImages()               # Get image(s)
    return imageList


# Run the model to make a prediction
def get_prediction(imageList):
    for imageData in imageList:                               # Get prediction for every image
        imageURL, image = imageData
        prediction = model.getPrediction(predictor, image)    # Run model to get image prediction
    return prediction


# Make a readable prediction (Only get the prediction data that is needed)
def render_prediction(prediction):
    labels_things, labels_stuff = model.getLabels_PanopticSeg(prediction)
    masks, mask_labels = model.getMasks_InstanceSeg(prediction, labels=True)
    return (labels_things, labels_stuff, masks, mask_labels)


@app.route('/', methods=['GET'])
def root():
    return jsonify({'msg' : 'hello there!!'})


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # file = request.data['imageURL']
        # if file is not None:
        # dictdata = request.data
        data = json.loads(request.data)
        print(data)
        imageURL = data['imageURL']
        imageList = preprocess_data(imageURL)
        prediction = get_prediction(imageList)
        labels_things, labels_stuff, masks, mask_labels = render_prediction(prediction)
        
        # response =  {'imageURL': imageURL, 'labels_things': labels_things, 'labels_stuff': labels_stuff, 'masks': masks, 'mask_labels': mask_labels}
        # response = {
        #     'imageURL': imageURL,
        #     'labels_things': labels_things,
        #     'labels_stuff' : labels_stuff,
        #     'masks': masks,
        #     'mask_labels': mask_labels
        # }

        # return jsonify(response)
        # return jsonify({'imageURL': imageURL, 'labels_things': labels_things, 'labels_stuff': labels_stuff, 'masks': masks, 'mask_labels': mask_labels})
        
        # TODO: need to serialize mask from nparray to json => below works, just not yet for masks.
        return jsonify({'labels_things': list(labels_things), 'labels_stuff': list(labels_stuff), 'mask_labels': list(mask_labels)})

if __name__ == '__main__':
    app.run()