from flask import Flask, request, render_template, redirect, url_for
from sentiment import analyze_sentiment
import os
from pydub import AudioSegment
import boto3
import whisper
import json
# import ssl
# import certifi

# ssl_context = ssl.create_default_context(cafile=certifi.where())
# ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_to_wav(filepath):
    if filepath.endswith('.mp3'):
        path, _ = os.path.splitext(filepath)
        new_filepath = path + '.wav'
        sound = AudioSegment.from_mp3(filepath)
        sound.export(new_filepath, format="wav")
        return new_filepath
    else:
        return filepath

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('transcribe', filename=filename))
    return render_template('index.html')

@app.route('/transcribe/<filename>')
def transcribe(filename):
    try:
        # original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # print("starting to convert to wa",filepath)
        # filepath = convert_to_wav(original_filepath)
        # print("convert to wav result",filepath)

        # model = whisper.load_model("base")  
        # result = model.transcribe(filepath)
        # print("whisper response",result)

        # text = result["text"]
        # sentiment_analysis = analyze_sentiment(text)

        # print("analyze_sentiment response",sentiment_analysis)

        # aws_access_key_id = os.getenv('aws_access_key_id')
        # aws_secret_access_key = os.getenv('aws_secret_access_key')
        # aws_default_region = os.getenv('aws_default_region')
        # s3 = boto3.client(
        #     's3',
        #     aws_access_key_id=aws_access_key_id,
        #     aws_secret_access_key=aws_secret_access_key,
        #     region_name=aws_default_region
        # )
        # bucket_name = 'myaudiosentimentbucket'
        # object_key = f'sentimentanalysis/{filename}.json'



        # sentiment_analysis = sentiment_analysis.strip('```json\n').rstrip('```')

        # s3_response = s3.put_object(
        #     Bucket=bucket_name,
        #     Key=object_key,
        #     Body=str({
        #         # 'transcription': text,
        #         'sentiment_analysis': sentiment_analysis
        #     }).encode()
        # )
        
        print("s3_resposponse",s3_response)
        sentiment_analysis=json.loads(sentiment_analysis)
        return render_template('transcribe.html', transcription="hello", sentiment_analysis="yo")
    except Exception as e:
        # Log and print the error
        app.logger.error(f'Error processing {filename}: {str(e)}', exc_info=True)
        print(f'Error processing {filename}: {str(e)}')
        # Optionally, return an error page or message
        return render_template('error.html'), 500

if __name__ == "__main__":
    app.run()
