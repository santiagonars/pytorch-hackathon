# from model import segmentation
# from model.segmentation import SegmentationModel
# from model.segmentation import ImagePreProcessing
# import numpy as np
import psycopg2
from psycopg2 import sql
import pickle


def testdatabase():
    connection = psycopg2.connect(database="postgres", user="postgres", password="root", host="127.0.0.1", port="5432")
    # another option:
    # conn_str = "dbname=%s user=%s password=%s host=%s port=%s" % ("postgres","postgres","root","127.0.0.1", "5432")
    # connection = None
    # connection = psycopg2.connect(conn_str)

    # connection.set_session(autocommit=True)
    cursor = connection.cursor()
    
    # cursor.execute("SELECT * FROM pyvinci.user_record")
    cursor.execute(sql.SQL("SELECT * FROM {}.{}").format(
        sql.Identifier('pyvinci'),
        sql.Identifier('user_record')))

    print("id | username | password | created_at | updated_at")
    print("--------------------------") 
    rows = cursor.fetchall()
    for row in rows:
        print(row[0],' ',str(row[2]).strip(),'      ',row[1].strip())

    connection.close()


    # some_uuid = '1'
    # image_url = 'https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg'
    # cursor.execute(
    #     """
    #     INSERT INTO jobs (id, image_url) 
    #     VALUES (%s, %s)
    #     """,
    #     (some_uuid, image_url)   
    # )





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
    testdatabase()