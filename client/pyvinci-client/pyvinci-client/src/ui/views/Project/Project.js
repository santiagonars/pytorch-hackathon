import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom';
import './Project.css';
import ApiService from '../../../services/ApiService';
import ProjectInfo from '../../components/ProjectInfo/ProjectInfo';
import ImageUploader from '../../components/ImageUploader/ImageUploader';
import ProjectImages from '../../components/ProjectImages/ProjectImages';
import CreateJobButton from '../../components/CreateJobButton/CreateJobButton';
import ProjectStatus from '../../components/ProjectStatus/ProjectStatus';

export function Project() {

    const {id: projectId} = useParams();
    
    const [project, setProject] = useState();
    const [images, setImages] = useState([]);

    const fetchProject = () => {
        return ApiService.getProject(projectId)
        .then(data => {
            setProject(data)
        })
    }
    
    const fetchImages = () => {
        ApiService.getImages(projectId)
        .then(data => {
            setImages(data)
        })
    }
    
    const uploadImages = (images) => {
        ApiService.postImages(projectId, images)
        .then(res => {
            // Get images after uploading
            fetchImages()
        })
    }
    
    const deleteImage = (imageId) => {
        ApiService.deleteImage(projectId, imageId)
        .then(data => {
            // Get images after deleting
            fetchImages()
        })
    }
    
    const onImageClick = (index) => {
        console.log("Clicked image: ", images[index])
    }

    const postJob = () => {
        // console.log("postJob")
        ApiService.postJob(projectId)
        .then(res => {
            // console.log("fetchProject after postJob")
            fetchProject()
            // .then(res =>{
                // console.log("fetchProject after postJob response")
            // })
        })
    }

    // Get project data
    useEffect(() => {
        fetchProject()
    }, [projectId]);

    // Get project images
    useEffect(() => {
        fetchImages()
    }, [projectId]);

    const [interval, setTheInterval] = useState()

    useEffect(() => {

        // console.log("Interval effect")

        if(project?.status == "PENDING_LABELS"){

            // console.log("Status is pending..")

            if(!interval){
                setTheInterval(
                    setInterval(() => {
                        // console.log('Interval..');
                        fetchProject()
                    }, 2000)
                )
            }
        } else {

            // console.log("Status is not pending..")

            if(interval){
                // console.log("Clear interval")
                clearInterval(interval)
                // console.log("Get your data!")
                fetchImages()
            }
        }
    }, [project])

    const hasImages = images.length > 0
    const isModelling = project?.status == "PENDING_LABELS"
    const isModellingComplete = project?.status == "COMPLETE"
    const hasModellingStarted = isModellingComplete || isModellingComplete

    return (
        <div className="Project">
            {project ? 
                <div>
                    <ProjectInfo project={project} />
                    {!hasModellingStarted && <ImageUploader upload={uploadImages}/>}
                    <ProjectImages images={images} onClick={onImageClick} deleteImage={deleteImage}/>
                    <ProjectStatus project={project} images={images} isModellingComplete={isModellingComplete}/>
                    {!isModelling && !isModellingComplete && <CreateJobButton project={project} postJob={postJob} disabled={!hasImages}/>}
                </div> :
                <div>
                    Loading...
                </div>
            }
        </div>
    )
}