import React, {useState} from 'react'
import styles from './ImageUploader.css'

export default function ImageUploader({upload}) {

    const [file, setFile] = useState();

    const fileChangedHandler = (event) => {
        const file = event.target.files[0]
        setFile(file)
    }

    const uploadHandler = () => {
        upload(file)
    }

    return (
        <div className={styles.container}>
            <div>Upload image:</div>
            <input type="file" onChange={fileChangedHandler}/>
            <button onClick={uploadHandler}>Upload</button>
        </div>
    )
};