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
    df.drop(df.columns[0],axis=1, inplace = True)

    prediction = model.predict(df)
    prediction = (prediction > 0.5).astype(int)
    prediction = list(prediction)

    result = ''
    count_0, count_1 = prediction.count(0), prediction.count(1)

    if count_0 > count_1:
<<<<<<< HEAD
        result = "Not MalicioA"
=======
        result = "Not Malicious"
>>>>>>> 29b4dd63a314a90a91a8cb84542fd0e7307dc748
        return {"Prediction": result, "nonmal" : count_0, "mali" : count_1, "attack": "NA"}
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

<<<<<<< HEAD
        # response = getchatgpt(type_of_the_attack)
        print(type_of_the_attack)
        return {"Prediction": "Malicious", "nonmal" : count_0, "mali" : count_1, "attack": type_of_the_attack}
=======
        response = getchatgpt(type_of_the_attack)
        print(type_of_the_attack)
        return {"Prediction": "Malicious", "nonmal" : count_0, "mali" : count_1, "attack": type_of_the_attack, "info": response}
>>>>>>> 29b4dd63a314a90a91a8cb84542fd0e7307dc748




<<<<<<< HEAD
# def getchatgpt(attack):
    # openai.api_key = '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'

    # Define your chat function
    # def chat_with_gpt(prompt):
        # response = openai.Completion.create(
            # engine='text-davinci-003',  # Specify the GPT-3.5 engine
            # prompt=prompt,
            # max_tokens=500,  # Adjust the response length as needed
            # n=1,  # Number of responses to generate
            # stop=None,  # Optional stopping criteria
            # temperature=0.7,  # Controls the randomness of the output
            # timeout=10,  # Maximum time (in seconds) to wait for a response
        # )

        # if 'choices' in response and len(response['choices']) > 0:
            # return response['choices'][0]['text'].strip()
        # else:
            # return None

    # Example usage
    # prompt = f"Give information of the attack {attack} and suggestions"
    # response = chat_with_gpt(prompt)
    # return response
=======
def getchatgpt(attack):
    openai.api_key = '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'

    # Define your chat function
    def chat_with_gpt(prompt):
        response = openai.Completion.create(
            engine='text-davinci-003',  # Specify the GPT-3.5 engine
            prompt=prompt,
            max_tokens=500,  # Adjust the response length as needed
            n=1,  # Number of responses to generate
            stop=None,  # Optional stopping criteria
            temperature=0.7,  # Controls the randomness of the output
            timeout=10,  # Maximum time (in seconds) to wait for a response
        )

        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['text'].strip()
        else:
            return None

    # Example usage
    prompt = f"Give information of the attack {attack} and suggestions"
    response = chat_with_gpt(prompt)
    return response
>>>>>>> 29b4dd63a314a90a91a8cb84542fd0e7307dc748
    
