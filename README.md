# ProjectDZD
ZeroDay-attack detection project
# zero-day_model(prototype)
This is just a prototype of our Project i.e Project DZD (Detective Zero Day).
These files contain the codes and models that are used to built our WebApplication.
This WebApp is just a prototype.

**FRONT-END**
Our front end is not completely done.
We have just used ReactJS so far. 
where we'll be running "npm start" to run the frontend server. 
Then later on we will be adding CSS, and other styling for a good UserInterface.

**BACK-END**
The backend of the project is done using FastAPI and deploying all the models in backend.
To run the backend successfully without any exceptions we'll have to install the requirements "requirements.txt" by running the command "pip install -r requirements.txt". 
Then start the backend server using the command "uvicorn mlapi:app --reload" .
After starting the backend and frontend servers successfully. use the given sample CSV files to upload to the website to obtain results.

**NOTE:** make sure you update the port number of your backend server in the ./zeroday/src/App.js if it is other than localhost:8000. _(generally, backend servers run on localhost:8000)_

**Steps to be followed :**
Firstly, install all the required prerequisites mentioned above
    In the front end folder, run the npm start command
    In the backend folder, run the command: "uvicorn mlapiLSTM:app --port 8000"
    The backend will be running in the 8000 port.
    Now, you have to get your network logs using CICFlowmeter.
    Or just use the csv files provided in the "sample csvs" file.
    Click on the "choose file" botton, select the csv and click on the "Upload button"
    You will get the results along with a Chatgpt response containing details of the type of attack.
    
 **_contact:_**_kapardhikannekanti@gmail.com_
