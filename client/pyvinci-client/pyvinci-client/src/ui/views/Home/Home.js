import React, {useState, useEffect} from 'react'
import styles from './Home.module.css';
import ProjectsList from '../../components/ProjectsList/ProjectsList';
import { CreateProject } from '../CreateProject/CreateProject';
import ApiService from '../../../services/ApiService';
import { Redirect, Route } from 'react-router-dom';

export function Home() {

    const [projects, setProjects] = useState();

    useEffect(() => {
        ApiService.getProjects()
        .then(projects => {
            setProjects(projects)
        })
    }, []);

    const [navigateToNewProject, setNavigateToNewProject] = useState(false)
    function openCreateProject() {
        setNavigateToNewProject(true)
    }

    return (
        <div className={styles.container}>
            {projects ?
                <div>
                    <ProjectsList projects={projects}/>
                </div> :
                <div>
                    Loading...
                </div>
            }
            <div>
                <button onClick={openCreateProject}>
                    Create New Project
                </button>

                {navigateToNewProject ? <Redirect to='/projects/new' /> : null}
                <Route 
                    path={`/projects/new`}
                    component={CreateProject}
                />
            </div>
        </div>
    );
}