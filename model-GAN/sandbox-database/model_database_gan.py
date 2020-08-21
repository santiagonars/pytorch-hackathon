# Segmentation prediction modules
from model import gan
from model.gan import GanModel
from model.gan import ImagePreProcessing

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


# Used by main() to get the labels and masks for that GAN model will use as input
def database_read():
    jobIDs = list()
    labels = list()
    masks = list()
    # Set limit_value to set the number of jobs to use for GAN model input
    limit_value = 3
    for job_id, mask_labels, masks_nparr in session.query(Jobs.id, Jobs.mask_labels, Jobs.masks_nparr).filter_by(status="COMPLETE", ).order_by(Jobs.created_at).limit(limit_value).all():
        jobIDs.append(job_id)
        labels.append(mask_labels)
        masks.append(pickle.loads(masks_nparr)) # *Load binary data, also? => some_array = pickle.loads(cursor.fetchone()[0])
    # print(len(jobIDs))
    # print(len(labels))
    # print(len(masks))
    # print(labels[0])
    # print(masks[0])
    return (jobIDs, labels, masks)


# TODO: Might need to update to work architecture
# Used by main() at the end to load model prediction(s)
def database_update(job_id, result_image_url):
    job_completed = session.query(Jobs).filter_by(id=job_id).first()
    # job_completed.status = 'COMPLETE'
    job_completed.updated_at = datetime.datetime.now()
    session.add(job_completed)
    session.commit()
    print('Job completed:{}'.format(job_completed))




# Store image on the cloud storage and get a url
def store_image_in_cloud(image_generated):
    pass
    # TODO: Create function to load image to S3 (AWS) to get a URL (in Python)


def main():
    # Get list of jobs and corresponding model input data from database
    jobIDs, labels, masks = database_read()
    # TODO: 1.) Whatever label(s) gets selected by user, use index(es) of label(s) to pass corresponding mask to model
    # TODO: 2.) might need to do another query to pull background label


    # imageGeneratedList = list()

    """ 
    # Store image on the cloud storage and get a url
    result_image_url = store_image_in_cloud(image_generated)

    # Load generated image url to database
    database_update(jobIDs[i], result_image_url)
    """

if __name__ == "__main__":
    main()
    # database_insert()
    # database_delete()