from flask import Flask, request, render_template, jsonify
import boto3
import os

app = Flask(__name__)

# Configuration AWS
AWS_REGION = 'your-aws-region'
LAMBDA_FUNCTION_NAME = 'your-lambda-function-name'

# Client Lambda
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    audio_data = audio_file.read()

    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=audio_data
    )

    response_payload = response['Payload'].read().decode('utf-8')

    return jsonify(response_payload)

if __name__ == '__main__':
    app.run(debug=True)
