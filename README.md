Audio Sentiment Analysis Project
A web app leveraging Flask, Whisper, and OpenAI for sentiment analysis of audio conversations. It transcribes dialogues, extracts emotional and psychological insights, and presents them through a user-friendly interface, offering a unique perspective on interpersonal communications.
=======

# Features
Audio file upload and storage
Audio to text transcription using OpenAI's Whisper model
Sentiment analysis and happiness rating using OpenAI's GPT-3.5
Storage of analysis results in AWS S3
# Technology Stack
Flask: A lightweight WSGI web application framework
OpenAI Whisper: For audio file transcription
OpenAI GPT-3.5: For sentiment analysis
PyDub: For audio file format conversion
Boto3: For interacting with AWS S3
SSL and Certifi: For secure requests
# Prerequisites
Before running this project, ensure you have the following installed:
Python 3.12.2
Pip
Virtual environment
# Configuration
To run this project, you need to set up several environment variables for OpenAI API, AWS S3, and SSL verification:
OpenAI API Key:
OPENAI_API_KEY=''
AWS Credentials:
aws_access_key_id = ''
aws_secret_access_key = ''
aws_default_region = ''
SSL Certificate Verification (optional):
The project configures SSL to use a default unverified context for development purposes. For production, ensure proper SSL certificate verification
Set the environment variable OPENAI_API_KEY with your API key.
Set up your AWS access key ID, secret access key, and default region as environment variables.
# AWS S3 Storage Integration
This application utilizes Amazon Web Services (AWS) S3 for secure storage of audio analysis results. Each analysis result is saved as a JSON file in a designated S3 bucket, organized by the date and time of analysis.
# Accessing Stored Analysis Results
Bucket Structure: Analysis results are stored in the `myaudiosentimentbucket` bucket.
# Running the Application
Step 1: Clone the Repository:"https://github.com/prachimanocha/audio-sentiment-analysis"
Command- git clone https://github.com/prachimanocha/audio-sentiment-analysis
Command- cd audio-sentiment-analysis
Step 2: Set Up Python Environment
Command- python -m venv venv
Command- source venv/bin/activate
Step 3: Install Dependencies
Command- pip install -r requirements.txt
Step 4: Configure Environment Variables
export OPENAI_API_KEY=your_openai_api_key_here
export AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
export AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
export AWS_DEFAULT_REGION=your_aws_region_here
Step 5: Run the Flask Application
Command- python main.py
Step 6: Access the Application
This command starts the server on http://127.0.0.1:3000, where you can access the web application

# Access the web application at "http://localhost:3000".

# Challenges Faced

Developing this Flask-based audio sentiment analysis application presented several significant challenges, including:

# Dynamic Responses from OpenAI's GPT API:
  - The variability in the structure and format of responses from OpenAI's GPT API.
  - With the variability of the AI's responses,devised a solution to instruct the model to return the output in a predefined format.

# Secure Management of Sensitive Keys:
  - Initially faced a risk of hardcoding sensitive information, such as the OpenAI API key and AWS Access Keys, directly into the source code, which could lead to potential security vulnerabilities.
  - Implemented a secure strategy using environment variables for storing these keys, preventing them from being exposed in the project's version-controlled source code.
  - This approach highlighted the critical importance of security best practices in protecting sensitive information from unauthorized access.
# SSL Certificate Error with Whisper Model:
- Encountered SSL certificate verification errors when attempting to use OpenAI's Whisper model for audio transcription.

>>>>>>> sentimentBranch
