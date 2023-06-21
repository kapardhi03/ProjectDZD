import React from 'react';
import './Instructions.css';

function Instructions() {
  return (
    <div className="instructions">
      <h1>Instructions</h1>
      <section>
        <h2>Installation</h2>
        <pre className="code">
          git clone https://gitlab.com/hieulw/cicflowmeter
          <br />
          cd cicflowmeter
          <br />
          python setup.py install
        </pre>
        <p className="or">or</p>
        <pre className="code">pip install cicflowmeter</pre>
      </section>
      <section>
        <h2>Usage</h2>
        <pre className="code">
          usage: cicflowmeter [-h] (-i INPUT_INTERFACE | -f INPUT_FILE) [-c] [-u URL_MODEL] output
          <br />
          positional arguments:
          <br />
          output output file name (in flow mode) or directory (in sequence mode)
          <br />
          optional arguments:
          <br />
          -h, --help show this help message and exit
          <br />
          -i INPUT_INTERFACE capture online data from INPUT_INTERFACE
          <br />
          -f INPUT_FILE capture offline data from INPUT_FILE
          <br />
          -c, --csv, --flow output flows as csv
        </pre>
      </section>
      <section>
        <h3>Convert pcap file to flow csv:</h3>
        <pre className="code">cicflowmeter -f example.pcap -c flows.csv</pre>
        <h3>Sniff packets real-time from interface to flow csv: (need root permission)</h3>
        <pre className="code">cicflowmeter -i eth0 -c flows.csv</pre>
      </section>
      <div className='upload-section'>
        <a href='/upload' className='upload-button'>
          Upload Now
        </a>
      </div>
      <div className="help-section">
        <a href="https://example.com" target="_blank" rel="noopener noreferrer" className="help-button">
          Need Help?
        </a>
      </div>
    </div>
  );
}

export default Instructions;
