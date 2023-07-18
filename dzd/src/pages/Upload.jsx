import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Uploadpage from './Uploadpage';
import './Upload.css';
import Ddosgoldeneye from './attackinfos/ddosgoldeneye';
import Bot from './attackinfos/Bot';
import Ddos from './attackinfos/Ddos';
import Ddoshulk from './attackinfos/Ddoshulk';
import Ddosslowhttptest from './attackinfos/Ddosslowhttptest';
import Ddosslowloris from './attackinfos/Ddosslowloris';
import Ftppatator from './attackinfos/Ftppatator';
import Infiltration from './attackinfos/Infiltration';
import Sshpatator from './attackinfos/Sshpatator';
import Webbruteforce from './attackinfos/Webbruteforce';
import Websqlinjection from './attackinfos/Websqlinjection';
import Zeroday from './attackinfos/Zeroday';
 
const Upload = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [isMalicious, setIsMalicious] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [res, setRes] = useState("");
  const [isBlinking, setIsBlinking] = useState(false);
  const [fileName, setFileName] = useState("");
  const [showKnowMore, setShowKnowMore] = useState("");
  const [currentAttribute, setCurrentAttribute] = useState("nonmal");

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setFileName(file.name);
  };

  const handleKnowMore = (value) => {
    setShowKnowMore(value);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('username', localStorage.getItem("username"));
    console.log(localStorage.getItem("username"));

    try {
      setIsLoading(true);

      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setRes(response.data);
      setIsMalicious(response.data.isMalicious);
      console.log(response.data.isMalicious) // Assuming the response contains the isMalicious flag
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
      setShowResult(true);
    }
  };

  useEffect(() => {
    setIsBlinking(showResult);
  }, [showResult]);

  useEffect(() => {
    if (isBlinking) {
      const timer = setTimeout(() => {
        setIsBlinking(false);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [isBlinking]);

  useEffect(() => {
    // Start the attribute change loop
    const interval = setInterval(() => {
      setCurrentAttribute((prevAttribute) => {
        if (prevAttribute === "nonmal") {
          return "mali";
        } else if (prevAttribute === "mali") {
          return "attack";
        } else {
          return "nonmal";
        }
      });
    }, 2000); // Interval between attribute changes in milliseconds

    // Clean up the interval when component unmounts
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="maegin">
        <div className="scantitle">
          <p>Scan your network logs here</p>
        </div>
        <p></p>
        <p className="info">
          We have duly furnished the necessary instructions on generating the CSV file containing the local network logs.
          You may access the information <a href="/instructions">here</a>.
        </p>
      </div>

      <div className="uploadtotal">
        <div className="upload-box">
          <form className="form">
            <span className="form-title">Upload your file</span>
            <p className="form-paragraph"><i>File should be a .csv file</i></p>
            <label htmlFor="file-input" className="drop-container">
              <span className="drop-title">{fileName ? fileName : 'Drop files here'}</span>

              <input type="file" accept=".csv" required id="file-input" onChange={handleFileChange} />
            </label>
          </form>
        </div>
        <div className="upbtn">
          <button className="uploadbtn" onClick={handleUpload}>
            {isLoading ? '' : 'Upload'}
            {isLoading && <span className="loading-symbol">Loading...</span>}
          </button>
        </div>
      </div>

      <div className="Check">
        {res && !showResult && (
          <button className={`check-result-btn ${isBlinking ? 'blink' : ''}`} onClick={() => setShowResult(true)}>
            Check Your Result
          </button>
        )}

        
      </div>
      {showResult && (
          <div className="res">
            <p className={`malors ${isBlinking ? 'blink' : ''}`} style={{ color: isMalicious ? 'red' : 'green ' , marginLeft:'40%'}}>
              Your Network is {isMalicious === true ? 'Malicious' : 'Safe'}
            </p>
            {showKnowMore ? (
              <div className="knowmore">
                {/* {currentAttribute === "attack" && <p className="slide-from-left attack">Attack: {res.attack}</p>} */}
                {res.attack === 'zeroday' && <Zeroday />}
                {res.attack === 'bot' && <Bot />}
                {res.attack === 'ddos' && <Ddos />}
                {res.attack === 'ddoshulk' && <Ddoshulk />}
                {res.attack === 'ddosgoldeneye' && <Ddosgoldeneye />}
                {res.attack === 'dosslowhttptest' && <Ddosslowhttptest />}
                {res.attack === 'dosslowloris' && <Ddosslowloris />}
                {res.attack === 'ftppatator' && <Ftppatator />}
                {res.attack === 'infiltration' && <Infiltration />}
                {res.attack === 'sshpatator' && <Sshpatator />}
                {res.attack === 'webattackbruteforce' && <Webbruteforce />}
                {res.attack === 'webattacksqlinjection' && <Websqlinjection />}
              </div>
            ) : (
              <button className="knowmore" onClick={() => handleKnowMore(true)}>Know More</button>
            )}
          </div>
        )}

      <Uploadpage />
    </div>
  );
};

export default Upload;
