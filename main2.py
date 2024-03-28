# from flask import Flask, request, render_template, redirect, url_for
# from sentiment import analyze_sentiment
# import speech_recognition as sr
# import os
# from pydub import AudioSegment
# import boto3
# from botocore.exceptions import ClientError

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# def convert_to_wav(filepath):
#     if filepath.endswith('.mp3'):
#         path, _ = os.path.splitext(filepath)
#         new_filepath = path + '.wav'
#         sound = AudioSegment.from_mp3(filepath)
#         sound.export(new_filepath, format="wav")
#         return new_filepath
#     else:
#         return filepath

# @app.route("/", methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files.get('file')
#         if file and allowed_file(file.filename):
#             filename = file.filename
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             return redirect(url_for('transcribe', filename=filename))
#     return render_template('index.html')

# @app.route('/transcribe/<filename>')
# def transcribe(filename):
#     try:
#         # Download the audio file from S3
#         s3 = boto3.client(
#             's3',
#             aws_access_key_id='AKIAZI2LEQUR7HG2W3CB',
#             aws_secret_access_key='Qj6GSYLwzV5ntR+h6GAt9d9QuJWryOib6OtHsBK8'
#         )
#         response = s3.get_object(
#             Bucket='myaudiosentimentbucket',  # Replace with your bucket name
#             Key=filename
#         )
#         audio_data = response['Body'].read()

#         # Perform transcription and sentiment analysis
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(audio_data) as source:  # This line might need adjustment
#             audio_data = recognizer.record(source)
#             try:
#                 text = recognizer.recognize_google(audio_data)
#                 # Perform sentiment analysis on the transcribed text
#                 sentiment_analysis = analyze_sentiment(text)
#             except sr.UnknownValueError:
#                 text = "Audio was not understood"
#                 sentiment_analysis = "Sentiment analysis could not be performed."
#             except sr.RequestError as e:
#                 text = f"Could not request results; {e}"
#                 sentiment_analysis = "Sentiment analysis could not be performed."
#             except Exception as e:
#                 text = f"An error occurred: {str(e)}"
#                 sentiment_analysis = "Sentiment analysis could not be performed."
#     except ClientError as e:
#         # Handle exceptions related to S3 operations
#         error_message = e.response['Error']['Message']
#         return f"An error occurred: {error_message}"
    
#     return render_template('transcribe.html', transcription=text, sentiment_analysis=sentiment_analysis)

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import speech_recognition as sr
import boto3
from botocore.exceptions import ClientError
import tempfile
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Boto3 S3 initialization
s3 = boto3.client('s3')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            local_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_filepath)
            
            # Define S3 bucket name
            bucket_name = 'your_bucket_name'
            
            # Upload the file to S3
            try:
                response = s3.upload_file(local_filepath, bucket_name, filename)
            except ClientError as e:
                logging.error(e)
                return f"Failed to upload file to S3: {e}"
            
            return redirect(url_for('transcribe', filename=filename))
    return render_template('index.html')

@app.route('/transcribe/<filename>')
def transcribe(filename):
    # Define S3 bucket name
    bucket_name = 'myaudiosentimentbucket'
    
    try:
        # Generate the URL for the file
        file_url = s3.generate_presigned_url('get_object', 
                                             Params={'Bucket': bucket_name, 'Key': filename},
                                             ExpiresIn=300)
                                             
        # Perform transcription
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(suffix='.wav') as tmpfile:
            # Download file from S3 to tmpfile
            with open(tmpfile.name, 'wb') as f:
                s3.download_fileobj(bucket_name, filename, f)
            with sr.AudioFile(tmpfile.name) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                except sr.UnknownValueError:
                    text = "Audio was not understood."
                except sr.RequestError as e:
                    text = f"Could not request results; {e}"
                except Exception as e:
                    text = f"An error occurred: {str(e)}"
    except ClientError as e:
        logging.error(e)
        return f"Failed to process file from S3: {e}"

    return render_template('transcribe.html', transcription=text)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
