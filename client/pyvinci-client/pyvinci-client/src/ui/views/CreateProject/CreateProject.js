import React, {useState} from 'react'
import styles from './CreateProject.module.css'
import ApiService from '../../../services/ApiService';

import { Redirect } from 'react-router-dom';

//TODO: Prevent double submissions. Add loading state and disable when waiting.
//TODO: Show error details
export function CreateProject() {

    const [projectName, setProjectName] = useState("");
    const [success, setSuccess] = useState(false)
    // const [waiting, setWaiting] = useState(false);
    // const [error, setError] = useState(false);
    // const [errorDetails, setErrorDetails] = useState("")

    function handleProjectNameChange(event) {
        setProjectName(event.target.value)
    }

    function handleSubmit(event) {
        ApiService.createProject(projectName)
            .then(project => {
                setSuccess(true)
            })
        event.preventDefault();
    }

    return (
        <div className={styles.container}>

            {success ? <Redirect to='/home' /> : null}

            <form onSubmit={handleSubmit}>
                <label>
                    Project Name:
                    <input value={projectName} onChange={handleProjectNameChange} />
                </label>
                <input type="submit" value="Create project" />
            </form>
        </div>
    )
}