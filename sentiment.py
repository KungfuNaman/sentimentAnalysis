import time
import openai

def analyze_sentiment(conversation, retries=3):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"""Given the following conversation, provide a sentiment analysis, including emotional states and psychological insights for each speaker separately in bullet points. Assign a happiness rating from 1 to 5. Present the response in a Array of JSON format only without any extra text with each entry containing 'speaker', 'emotional_states', 'psychological_insights', and 'happy_rating' as keys. All values should be strings."""}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError as e:
        if retries > 0:
            print(f"Rate limit exceeded, retrying in 30 seconds... (Retries left: {retries})")
            time.sleep(30)  # Wait for 30 seconds before retrying
            return analyze_sentiment(conversation, retries-1)
        else:
            raise Exception("Rate limit exceeded, no retries left.")





        


        
