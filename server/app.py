from flask import Flask, request, render_template, jsonify
import boto3
import os
import base64
import json

app = Flask(__name__)

# Configuration AWS
AWS_REGION = 'us-east-1'
LAMBDA_FUNCTION_NAME = 'speech_to_text'

# Client Lambda
boto3.setup_default_session(profile_name='dev')
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    audio_data = audio_file.read()
        

    print("save")

    with open('uploaded_audio.wav', 'wb') as f:
        f.write(audio_data)

    print("encode")
    
    
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    payload = json.dumps({'body': json.dumps({'audio': audio_base64})})

    print("call with payload ", payload)
    #response = lambda_client.invoke(
    #    FunctionName=LAMBDA_FUNCTION_NAME,
    #    InvocationType='RequestResponse',
    #    Payload=audio_data
    #)


    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=payload
    )
    print("call success")
    response_payload = response['Payload'].read().decode('utf-8')

    return jsonify(response_payload)
    
if __name__ == '__main__':
    app.run(debug=True)
