import os 
import openai   # pip instal openai
from openai import OpenAI   # 

# Set environment variables
my_api_key = os.environ.get('OPENAI_KEY')

openai.api_key = my_api_key
print(my_api_key)

# Authorization: Bearer my_api_key

# WRITE YOUR CODE HERE


# # Create an OpenAPI client using the key from our environment variable
client = OpenAI(
    api_key= my_api_key,
)

content = "Tell me about myself based on my favorite album:"
content+= "Channel Orange by Frank Ocean"
content+= "I want to know what this says about my: 1. Musical preferences, 2. Personal insights, 3. Personality"

# # Specify the model to use and the messages to send
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a musical genius that's good at reading people."},
        {"role": "user", "content": content}
    ]
)
print(completion.choices[0].message.content)



