// src/components/DocumentViewer.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const DocumentViewer = () => {
    const { id } = useParams();
    const [document, setDocument] = useState(null);

    useEffect(() => {
        const fetchDocument = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}/documents/${id}/`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                setDocument(response.data);
            } catch (error) {
                console.error('Error fetching document', error);
            }
        };

        fetchDocument();
    }, [id]);

    if (!document) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Document Viewer</h2>
            <div>
                <h3>Original Document</h3>
                <p>{document.original_file}</p>
            </div>
            <div>
                <h3>Improved Document</h3>
                <p>{document.improved_content}</p>
            </div>
        </div>
    );
};

export default DocumentViewer;
