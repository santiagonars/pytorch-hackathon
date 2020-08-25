import React from 'react';
import styles from './ProjectsList.module.css'
import ProjectsListProject from './ProjectsListProject/ProjectsListProject';

export default function ProjectsList({projects}) {

    const projectsListProjects = projects?.map((project, index) =>
        <ProjectsListProject
            key={index}
            project={project}
        />
    );

    return (
        <div className={styles.container}>    
            <h2>Your projects:</h2> 
            {projects?.length ? 
                <div>
                    {projectsListProjects}
                </div>
                :
                <div>
                    No projects available to display
                </div>
            }
        </div>
    )
};