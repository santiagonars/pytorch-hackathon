
# import common libraries
import requests
from requests.exceptions import HTTPError, Timeout


class GanModel():
    pass




class ImagePreProcessing():
    def __init__(self):
        self.images = list()

    def getImages(self):
        return self.images

    def loadImage(self, imageUrl):
        self.url = imageUrl
        # Use requests to issue a standard HTTP GET 
        try:
            image_response = requests.get(imageUrl ,timeout=15)
            # raise_for_status will throw an exception if an HTTP error
            image_response.raise_for_status
            print('image received: {}'.format(image_response))
            # get image as numpy array
            image_NumpyArray = np.frombuffer(image_response.content, np.uint8)
            image = cv2.imdecode(image_NumpyArray, cv2.IMREAD_COLOR)
            # append to images to be run on model
            self.images.append([imageUrl, image])

        except HTTPError as err:
            print("Error: {0}".format(err))
        except Timeout as err:
            print("Request time out {0}".format(err))


if __name__ == "gan":
    pass