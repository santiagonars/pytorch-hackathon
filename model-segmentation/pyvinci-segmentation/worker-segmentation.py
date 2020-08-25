#SEGMENTATION MODEL
from model import segmentation
from model.segmentation import SegmentationModel
from model.segmentation import ImagePreProcessing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import Base, Jobs, Image
import datetime
import pickle
import time
import os


DATABASE_URL = os.getenv('WORKER_DATABASE_URL')
SEGMENTATION_INTERVAL = int(os.getenv('SEGMENTATION_INTERVAL')) # in seconds (defaults=120)
JOBS_LIMIT = int(os.getenv('JOBS_LIMIT')) # set between 0 and 3 (default=1)
USING_CPU = os.getenv('USING_CPU') # set to 'False' to run on GPU

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def database_delete(num):
    for i in range(num):
        projectID = str()
        job_record = session.query(Jobs).filter_by(status="COMPLETE").order_by(Jobs.created_at).first()
        projectID = job_record.project_id
        session.delete(job_record)
        session.commit()
        print("Job deleted: {}".format(job_record))
        for image_record in session.query(Image).filter_by(project_id=projectID).all():
            session.delete(image_record)
            session.commit()
            print("Image deleted: {}".format(image_record))
        print("")


def database_read():
    jobIDs = list()
    imageIDs = list()
    imageURLs = list()
    projectID = str()
    # limit_value is sets the number of jobs for worker to do
    if JOBS_LIMIT >= 0 and JOBS_LIMIT <= 3:
        limit_value = JOBS_LIMIT
    else:
        limit_value = 1
    for job_record in session.query(Jobs).filter_by(status="PENDING_LABELS").order_by(Jobs.created_at).limit(limit_value).all():
        projectID = job_record.project_id
        jobIDs.append(job_record.id)
        for image_record in session.query(Image).filter_by(project_id=projectID).all():
            imageIDs.append([image_record.id, job_record.id])
            imageURLs.append(image_record.url)
    return (jobIDs, imageIDs, imageURLs)


def database_update_image(image_id, labels_things_pred, labels_stuff_pred, masks_labels_pred, masks_nparr_pred):
    img_labels_completed = session.query(Image).filter_by(id=image_id).one()
    img_labels_completed.labels_things = labels_things_pred
    img_labels_completed.labels_stuff = labels_stuff_pred
    img_labels_completed.masks_labels = masks_labels_pred
    img_labels_completed.masks = pickle.dumps(masks_nparr_pred)
    img_labels_completed.updated_at = datetime.datetime.now()
    session.add(img_labels_completed)
    session.commit()
    print('Image segmentation completed:{}'.format(img_labels_completed))


def database_update_job(job_id):
    job_completed = session.query(Jobs).filter_by(id=job_id).first()
    job_completed.status = 'COMPLETE'
    job_completed.updated_at = datetime.datetime.now()
    session.add(job_completed)
    session.commit()
    print('Job for image segmentation completed:{}'.format(job_completed))


def worker():
    jobIDs, imageIDs, imagesURLs = database_read()
    model = SegmentationModel()
    if USING_CPU == 'false':
        predictor = model.builtModel(UsingCPU=False)
    else:
        predictor = model.builtModel(UsingCPU=True)

    image_preprocessing = ImagePreProcessing()
    for img in imagesURLs:
        image_preprocessing.loadImage(img)
    imageProcessedData = image_preprocessing.getImages()

    for i in range(len(jobIDs)):
        for j in range(len(imageIDs)):
            if imageIDs[j][1] == jobIDs[i]:
                image_url, image = imageProcessedData[j]
                prediction = model.getPrediction(predictor, image)
                labels_things_pred, labels_stuff_pred = model.getLabels_PanopticSeg(prediction)
                masks_labels_pred, masks_nparr_pred = model.getMasks_InstanceSeg(prediction, labels=True)
                #for index in range(len(masks_labels_pred)):
                #    masks_labels_pred[index] = str(masks_labels_pred[index]) + "_" + str(index)
                database_update_image(imageIDs[j][0], labels_things_pred, labels_stuff_pred, masks_labels_pred, masks_nparr_pred)
        database_update_job(jobIDs[i])


if __name__ == "__main__":
    while True:
        worker()
        default_interval = 120
        print('Starting to wait...')
        if SEGMENTATION_INTERVAL != None:
            default_interval = SEGMENTATION_INTERVAL
        time.sleep(default_interval)


