# Segmentation prediction modules
from model import segmentation
from model.segmentation import SegmentationModel
from model.segmentation import ImagePreProcessing

# Database modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import Base, Jobs
import datetime
import pickle
# ---------WIll NEED this below to save/ load NP_ARRAY (masks) using PICKLE:----------
# https://stackoverflow.com/questions/60278766/best-way-to-insert-python-numpy-array-into-postgresql-database
# https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.PickleType


# ----------------Establish Database Connection:----------------
engine = create_engine('postgres+psycopg2://postgres:root@localhost:5432/pyvinci')
# Bind the engine to the metadata of the Base class
Base.metadata.bind = engine

# A DBSession() instance establishes all communications with the database
DBSession = sessionmaker(bind=engine)

# session.commit() => use to make any changes in the database
# session.rollback() => use to revert all changes back to the the last commit
session = DBSession()

def database_insertion():
    # To add an imageurl, need to update status, created_at, updated_at
    # imageURL = "https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg"
    newjob = Jobs(image_url=imageURL, status="new", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
    session.add(newjob)
    session.commit()
    print('New Job added; Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

# main uses this function
def database_read():
    # TODO: need to set it so it finds a job with the status set to new
    resultQuery = session.query(Jobs).first()
    # print(('id: {}\nimage_url: {}\nstatus: {}').format(resultQuery.id, resultQuery.image_url, resultQuery.status))
    return resultQuery.image_url

# main uses this function
def database_update(image_url, labels_things_pred, labels_stuff_pred, masks_labels_pred, masks_nparr_pred):
    statusUpdate = session.query(Jobs).filter_by(image_url=image_url).one()
    # statusUpdate.labels_things = labels_things_pred
    # statusUpdate.labels_stuff = labels_stuff_pred
    # statusUpdate.mask_labels = masks_labels_pred
    # statusUpdate.masks_nparr = pickle.dumps(masks_nparr_pred) # pickle converts numpy array to binary
    statusUpdate.status = 'completed'
    statusUpdate.updated_at = datetime.datetime.now()
    session.add(statusUpdate)
    session.commit()
    print('Job completed')


def database_delete():
    # need to add matching array to label_things
    valueToDelete = session.query(Jobs).filter_by(labels_things='some array').one()
    session.delete(valueToDelete)
    session.commit


def main():

    # imageURL1 = "https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg"

    imageURL1 = database_read()

    # Create model
    model = SegmentationModel()
    predictor = model.builtModel(UsingCPU=True)

    # Make list of images to run
    image_preprocessing = ImagePreProcessing()
    image_preprocessing.loadImage(imageURL1)
    imageList = image_preprocessing.getImages()

    # Perform prediction for every image
    for imageData in imageList:
        image_url, image = imageData
        prediction = model.getPrediction(predictor, image)
        print("Image URL:", image_url)

        labels_things_pred, labels_stuff_pred = model.getLabels_PanopticSeg(prediction)

        masks_nparr_pred, masks_labels_pred = model.getMasks_InstanceSeg(prediction, labels=True)

        # Add predictions to database
        database_update(image_url, labels_things_pred, labels_stuff_pred, masks_labels_pred, masks_nparr_pred)


if __name__ == "__main__":
    main()
    # database_insertion()
    # database_read() # main uses
    # database_update() # main uses
    # database_delete():