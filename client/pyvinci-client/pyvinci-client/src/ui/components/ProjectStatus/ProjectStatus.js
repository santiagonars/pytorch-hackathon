import React from 'react';
import styles from './ProjectStatus.module.css'

export default function ProjectStatus({project, images, isModellingComplete}) {
    
    const status = project?.status

    const hasImages = images.length > 0

    const isReadyToModel = project.status == "" && hasImages

    let statusText
    switch(status) {
        case "":
          statusText = "Pending model"
          break;
        case "PENDING_LABELS":
          statusText = "Modeling in progress.."
          break;
        case "COMPLETED":
          statusText = "Modeling completed"
          break;
        default:
          statusText = status
    }

    return (
        <div className={styles.container}>
            <div>
                <p>
                    Status: {statusText}
                </p>
                
                <p>
                    {!(images.length > 0) && <b>Add images to your project to begin.</b>}
                </p>

                <p>
                    {isReadyToModel && <b>Ready to model! Add more images or click the "Begin modeling" button to proceed!</b>}
                </p>

                {isModellingComplete &&
                    <div>
                        <p>
                            Your labels produced by Pytorch are available under their respective source images! <b>Create a new project in Home to try again.</b>
                        </p>

                        <h4>Coming soon:</h4>

                        <p>
                            You will be able to select labels from the available options and use another model that uses your label selection and the images of the project to generate new images using AI.
                        </p>
                    </div>
                }

            </div>
        </div>
    )
};