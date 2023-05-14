import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [res, setres] = useState("");

  const handleChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        mode: 'no-cors'
      });
      setres(response.data);
      console.log(res);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>

    <form onSubmit={handleSubmit}>
      <input type="file" onChange={handleChange} />
      <button type="submit">Check</button>
      {res && (
      <div>
        <p>Result: {res.Prediction}</p>
        <p>Non - malicious Samples: {res.nonmal}</p>
        <p>Malicious Samples: {res.mali}</p>
        <p>Type of the attack: {res.attack}</p>
        <p>More information:{res.info}</p>
      </div>
    )}
    </form>
    </div>
  );
}

export default FileUpload;
