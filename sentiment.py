import time
import openai

def analyze_sentiment(conversation, retries=3):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Given the following conversation, provide a sentiment analysis, including emotional states and psychological insights for each speaker seperately in bullet points:\n\n{conversation}"}
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

if __name__ == "__main__":
    sample_conversation = """
    [Speaker_1]: Hello Dave. How are you?
    [Speaker_2]: Hi Joseph. I’m good. Yesterday went for a run. What about you?
    [Speaker_1]: I’m fine. Today I will read a book. I like reading.
    """
    try:
        insights = analyze_sentiment(sample_conversation)
        print("Sentiment Analysis Insights:")
        print(insights)
    except Exception as e:
        print(f"Failed to get insights: {str(e)}")



        


        
