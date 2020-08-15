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


# ----------------Establish Database Connection:----------------
engine = create_engine('postgres+psycopg2://postgres:root@localhost:5432/pyvinci')
# Bind the engine to the metadata of the Base class
Base.metadata.bind = engine

# A DBSession() instance establishes all communications with the database
DBSession = sessionmaker(bind=engine)

# session.commit() => use to make any changes in the database
# session.rollback() => use to revert all changes back to the the last commit
session = DBSession()


# Use database_insert() to add new jobs to database
def database_insert():
    newJobs = list()
    newJobs.append('https://storage.googleapis.com/segmentation-testing/testing_images1/bikes.jpeg')
    newJobs.append('https://storage.googleapis.com/segmentation-testing/testing_images1/beach.jpeg')
    newJobs.append('https://storage.googleapis.com/segmentation-testing/testing_images1/buildings.JPG')
    newJobs.append('https://storage.googleapis.com/segmentation-testing/testing_images1/dog.jpeg')
    newJobs.append('https://storage.googleapis.com/segmentation-testing/testing_images1/snow_statue.JPG')
    newJobs.append('https://storage.googleapis.com/segmentation-testing/testing_images1/trees_buildings.JPG')
    newJobs.append('https://storage.googleapis.com/segmentation-testing/testing_images1/bike.jpeg')
    for imageURL in newJobs:
        # New job requires image_url, update status, created_at, updated_at (values cannot be NULL)
        job_new = Jobs(image_url=imageURL, status="PENDING", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        session.add(job_new)
        session.commit()
        # print('New job added for image_url{}; Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(job_new))
        print('New job added: {}'.format(job_new))


# Use database_delete() to remove records
def database_delete():
    # query all completed records to be deleted in database
    for record in session.query(Jobs).filter_by(status="COMPLETE").all():
        session.delete(record)
        session.commit()
        print("Record deleted: {}".format(record))


# Used by main() at the beginning
def database_read():
    jobIDs = list()
    imageURLs = list()
    # Set limit_value to set the number of jobs to complete
    limit_value = 3
    for job_id, image_url in session.query(Jobs.id, Jobs.image_url).filter_by(status="PENDING").order_by(Jobs.created_at).limit(limit_value).all():
        jobIDs.append(job_id)
        imageURLs.append(image_url)
    return (jobIDs, imageURLs)


# Used by main() at the end of function
def database_update(job_id, image_url, labels_things_pred, labels_stuff_pred, masks_labels_pred, masks_nparr_pred):
    job_completed = session.query(Jobs).filter_by(id=job_id).first()
    job_completed.labels_things = labels_things_pred
    job_completed.labels_stuff = labels_stuff_pred
    job_completed.mask_labels = masks_labels_pred
    job_completed.masks_nparr = pickle.dumps(masks_nparr_pred) # pickle converts numpy array to binary. # Load Example=> some_array = pickle.loads(cursor.fetchone()[0])
    job_completed.status = 'COMPLETE'
    job_completed.updated_at = datetime.datetime.now()
    session.add(job_completed)
    session.commit()
    print('Job completed:{}'.format(job_completed))


def main():
    # Get list of jobs and corresponding model input data
    jobIDs, imagesURLs = database_read()
    # Create model
    model = SegmentationModel()
    predictor = model.builtModel(UsingCPU=True)
    # Create image preprocessor
    image_preprocessing = ImagePreProcessing()
    # load images to be processed
    for img in imagesURLs:
        image_preprocessing.loadImage(img)
    imageProcessedData = image_preprocessing.getImages()

    # Perform prediction for every image
    for i in range(len(jobIDs)):
        image_url, image = imageProcessedData[i]
        prediction = model.getPrediction(predictor, image)
        # get labels from panoptic segmentation predictions
        labels_things_pred, labels_stuff_pred = model.getLabels_PanopticSeg(prediction)
        # get masks and corresponding labels from instance segmentation predictions
        masks_nparr_pred, masks_labels_pred = model.getMasks_InstanceSeg(prediction, labels=True)
        # add predictions to database
        database_update(jobIDs[i], image_url, labels_things_pred, labels_stuff_pred, masks_labels_pred, masks_nparr_pred)


if __name__ == "__main__":
    main()
    # database_insert()
    # database_delete()