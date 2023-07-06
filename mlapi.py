from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import pandas as pd
import io
import pickle
import openai 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = pickle.load(open('./Models/RandomForestmodel', 'rb'))
botmodel = pickle.load(open('./Models/bot_model.pkl', 'rb'))
ddos_model = pickle.load(open('./Models/ddos_model.pkl', 'rb'))
ddoshulk_model = pickle.load(open('./Models/ddoshulk_model.pkl', 'rb'))
dos_goldeneye_model = pickle.load(open('./Models/dos_goldeneye_model.pkl', 'rb'))
dos_slowhttptest_model = pickle.load(open('./Models/dos_slowhttptest_model.pkl', 'rb'))
dos_slowloris_model = pickle.load(open('./Models/dos_slowloris_model.pkl', 'rb'))
ftppatator_model = pickle.load(open('./Models/FTP- PATATOR_model.pkl', 'rb'))
infiltration_model = pickle.load(open('./Models/infiltration_model.pkl', 'rb'))
ssh_patator_model = pickle.load(open('./Models/ssh_patator_model.pkl', 'rb'))
webattack_bruteforce_model = pickle.load(open('./Models/webattack_bruteforce_model.pkl', 'rb'))
webattack_sqlinjection_model = pickle.load(open('./Models/webattack_sqlinjection_model.pkl', 'rb'))

known_attack_models = {botmodel: "Bot",ddos_model: "DDoS", ddoshulk_model: "DoS hulk", dos_goldeneye_model: "DoS goldeneye", dos_slowhttptest_model: "DoS slowhttptest", dos_slowloris_model: "DoS_slowloris", ftppatator_model: "FTP Patator", infiltration_model: "Infiltration", ssh_patator_model: "SSH Patator", webattack_bruteforce_model: "Webattack Bruteforce", webattack_sqlinjection_model: "Webattack SQL Injection"}
print(len(known_attack_models))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    x = await file.read()
    df = pd.read_csv(io.BytesIO(x))

    ###RAW FROM CICFLOWMETER-------------------------------------
    # reqcols = [4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 40, 61, 62, 63, 64, 65, 66, 67, 68, 69,72, 75, 76, 78, 79, 80, 81, 82]
    # traincols = [' Destination Port', ' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets', 'Total Length of Fwd Packets', ' Total Length of Bwd Packets', ' Fwd Packet Length Max', ' Fwd Packet Length Min', ' Fwd Packet Length Mean', ' Fwd Packet Length Std', 'Bwd Packet Length Max', ' Bwd Packet Length Min', ' Bwd Packet Length Mean', ' Bwd Packet Length Std', 'Flow Bytes/s', ' Flow Packets/s', ' Flow IAT Mean', ' Flow IAT Std', ' Flow IAT Max', ' Flow IAT Min', 'Fwd IAT Total', ' Fwd IAT Mean', ' Fwd IAT Std', ' Fwd IAT Max', ' Fwd IAT Min', 'Bwd IAT Total', ' Bwd IAT Mean', ' Bwd IAT Std', ' Bwd IAT Max', ' Bwd IAT Min', 'Fwd PSH Flags', ' Bwd PSH Flags', ' Bwd URG Flags', 'Fwd Packets/s', ' Bwd Packets/s', ' Min Packet Length', ' Max Packet Length', ' Packet Length Mean', ' Packet Length Std', ' Packet Length Variance', 'FIN Flag Count', ' SYN Flag Count', ' RST Flag Count', ' PSH Flag Count', ' ACK Flag Count', ' URG Flag Count', ' CWE Flag Count', ' Down/Up Ratio', ' Average Packet Size', ' Avg Fwd Segment Size', ' Avg Bwd Segment Size', ' Fwd Header Length.1', 'Fwd Avg Bytes/Bulk', ' Fwd Avg Packets/Bulk', ' Fwd Avg Bulk Rate', ' Bwd Avg Bytes/Bulk', ' Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', ' Subflow Fwd Bytes', ' Subflow Bwd Packets', ' Init_Win_bytes_backward', 'Active Mean', ' Active Std', ' Active Min', 'Idle Mean', ' Idle Std', ' Idle Max', ' Idle Min', ' Label']
    # df = df.iloc[:,reqcols]
    # df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]
    # col_dict = dict(zip(df.columns, traincols))
    # df = df.rename(columns = col_dict)
    # print(df.head())


    ###CICIDS2017-------------------------------------------

    
    df.drop(df.columns[0],axis=1, inplace = True)

    prediction = model.predict(df)
    prediction = (prediction > 0.5).astype(int)
    prediction = list(prediction)

    result = ''
    count_0, count_1 = prediction.count(0), prediction.count(1)

    if count_0 > count_1:
        result = "Not Malicious"
        return {"Prediction": result, "nonmal" : count_0, "mali" : count_1, "attack": "NA" , "isMalicious" : False}
    else:
        type_of_the_attack = ""
        no_of_records = len(df)

        for i in known_attack_models:
            whichpred = i.predict(df)
            inliers = list(whichpred).count(1)
            if inliers > (no_of_records//2):
                type_of_the_attack = known_attack_models[i]
                break
        if type_of_the_attack=="":
            type_of_the_attack="Zero-day"


        # response = getchatgpt(type_of_the_attack)
        print(type_of_the_attack)
        return {"Prediction": "Malicious", "nonmal" : count_0, "mali" : count_1, "attack": type_of_the_attack, "isMalicious": True}#"info": response
    
