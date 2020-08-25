import React from 'react';
import styles from './CreateJobButton.module.css'

export default function CreateJobButton({postJob, disabled}) {

    const onClick = () => {
        postJob()
    }

    return (
        <div className={styles.container}>
            <button onClick={onClick} disabled={disabled}>Begin modeling</button>
        </div>
    )
};