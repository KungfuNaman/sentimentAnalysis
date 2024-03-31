# audio-sentiment-analysis
Audio Sentiment Analysis Project
A web app leveraging Flask, Whisper, and OpenAI for sentiment analysis of audio conversations. It transcribes dialogues, extracts emotional and psychological insights, and presents them through a user-friendly interface, offering a unique perspective on interpersonal communications.
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
Set the environment variable OPENAI_API_KEY with your API key.
AWS Credentials:
Set up your AWS access key ID, secret access key, and default region as environment variables:
aws_access_key_id = ''
aws_secret_access_key = ''
aws_default_region = ''
SSL Certificate Verification (optional):
The project configures SSL to use a default unverified context for development purposes. For production, ensure proper SSL certificate verification
Access the web application at "http://localhost:3000".
