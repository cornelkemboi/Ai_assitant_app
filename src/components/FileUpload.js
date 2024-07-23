import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('original_file', file);

    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        }
      });
      alert('File uploaded successfully');
    } catch (error) {
      console.error('File upload error', error);
      alert('File upload failed');
    }
  };

  return (
    <form onSubmit={handleFileUpload} className="file-upload-form">
      <input type="file" onChange={handleFileChange} />
      <button type="submit">Upload</button>
    </form>
  );
};

export default FileUpload;

// import React, { useState, useEffect } from 'react';
// import axios from 'axios';

// const FileUpload = () => {
//     const [file, setFile] = useState(null);
//     const [csrfToken, setCsrfToken] = useState('');

//     useEffect(() => {
//         // Fetch CSRF token from Django backend
//         const fetchCsrfToken = async () => {
//             try {
//                 const response = await axios.get('/api/csrf/', { withCredentials: true });
//                 setCsrfToken(response.data.csrfToken);
//             } catch (error) {
//                 console.error('Failed to fetch CSRF token', error);
//             }
//         };

//         fetchCsrfToken();
//     }, []);

//     const handleFileChange = (e) => {
//         setFile(e.target.files[0]);
//     };

//     const handleFileUpload = async (e) => {
//         e.preventDefault();
//         const formData = new FormData();
//         formData.append('original_file', file);

//         try {
//             await axios.post(
//                 `${process.env.REACT_APP_API_URL}/upload/`, 
//                 formData, 
//                 {
//                     headers: {
//                         'Content-Type': 'multipart/form-data',
//                         'X-CSRFToken': csrfToken,
//                         'Authorization': `Bearer ${localStorage.getItem('token')}`,
//                     }
//                 }
//             );
//             alert('File uploaded successfully');
//         } catch (error) {
//             console.error('File upload error', error);
//             alert('File upload failed');
//         }
//     };

//     return (
//         <form onSubmit={handleFileUpload}>
//             <input type="file" onChange={handleFileChange} />
//             <button type="submit">Upload</button>
//         </form>
//     );
// };

// export default FileUpload;
