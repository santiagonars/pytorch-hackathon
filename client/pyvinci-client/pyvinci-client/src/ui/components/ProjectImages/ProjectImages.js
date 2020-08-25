import React, { useCallback } from 'react';
import styles from './ProjectImages.css'

export default function ProjectImages({images, onClick, deleteImage}) {

    const handleOnClick = useCallback((index) => (e) => {
        e.stopPropagation()
        e.preventDefault()
        if (onClick) {
            onClick(index);
        }
    });

    const handleDeleteClick = useCallback((id) => (e) => {
        e.stopPropagation()
        e.preventDefault()
        deleteImage(id)
    })
    const imageElements = (
        <ul className="card-list">
            {images.map((image, index) => {
                const url = image.url

                const labelWordElements = image.labels?.map((label, index) => {
                    return (
                        <b key={index}>
                            {label},&nbsp;
                        </b>
                    )
                })

                return (
                    <li className="card" key={index} onClick={handleOnClick(index)}>
                        <div>
                            <a 
                                className="card-image" 
                                href={url} 
                            >
                                <img 
                                    src={url} 
                                    alt={"Uploaded photo"}
                                />
                            </a>
                            <button onClick={handleDeleteClick(image.id)}>Delete</button>

                            <div className="labels-container">
                                {labelWordElements}
                            </div>

                        </div>
                    </li>
                )
            })}
        </ul>
    )

    return (
        <div className={styles.container}>
            Images:
            { images.length ?
                <div>
                    {imageElements}
                </div>
            :
                <div>
                    No images available to display
                </div>
            }
        </div>
    )
};