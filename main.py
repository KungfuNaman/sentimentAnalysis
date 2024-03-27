from flask import Flask, request, render_template, redirect, url_for
from sentiment import analyze_sentiment
import speech_recognition as sr
import os
from pydub import AudioSegment

app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template('index.html')

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
    original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    filepath = convert_to_wav(original_filepath)
    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            # Perform sentiment analysis on the transcribed text
            sentiment_analysis = analyze_sentiment(text)
        except sr.UnknownValueError:
            text = "Audio was not understood"
            sentiment_analysis = "Sentiment analysis could not be performed."
        except sr.RequestError as e:
            text = f"Could not request results; {e}"
            sentiment_analysis = "Sentiment analysis could not be performed."
        except Exception as e:
            text = f"An error occurred: {str(e)}"
            sentiment_analysis = "Sentiment analysis could not be performed."


    return render_template('transcribe.html', transcription=text, sentiment_analysis=sentiment_analysis)
    

# if __name__ == "__main__":
#     app.run()
if __name__ == "__main__":
    app.run(debug=True, port=3000)

