  import React, { useState } from 'react';
  import axios from 'axios';
  import Uploadpage from './Uploadpage';
  import "./Upload.css";
  import instructions from './instructions';
  const Upload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [res, setRes] = useState("");

    const handleFileChange = (event) => {
      setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
      if (!selectedFile) {
        alert('Please select a file.');
        return;
      }

      const formData = new FormData();
      formData.append('file', selectedFile);

      try {
        const response = await axios.post('http://localhost:8000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        setRes(response.data);
        console.log(res);
        // Handle the response from the back-end
      } catch (error) {
        // Handle any errors that occur
        console.error('Error:', error);
      }
    };

    return (
      <div>
        <div className='maegin'>
          <div className="scantitle">
            <p>Scan your network logs here</p>
          </div>
          <p></p>
          <p className='info' >
            We have duly furnished the necessary instructions on generating the CSV file containing the local network logs.
            You may access the information <a href="/instructions">here</a>.
          </p>
        </div>

        <div className="uploadtotal">
          <div className="upload-box">
            <form className="form">
              <span className="form-title">Upload your file</span>
              <p className="form-paragraph">File should be a .csv file</p>
              <label htmlFor="file-input" className="drop-container">
                <span className="drop-title">Drop files here</span>
                or
                <input type="file" accept=".csv" required id="file-input" onChange={handleFileChange} />
              </label>
            </form>
          </div>
          <div className='upbtn'>
            <button className="uploadbtn" onClick={handleUpload}>Upload</button>
          </div>
        </div>

        {res && (
          <div>
            {res.Prediction}
            {res.nonmal}
            {res.mal}
            {res.attack}
          </div>
        )}

        <Uploadpage />
      </div>
    );
  };

  export default Upload;
