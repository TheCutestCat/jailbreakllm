from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")
base_url= os.getenv("OPENAI_BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url)

def openai_wrapper(system_messages,input_messages,response_format):
    system_messages = {"role": "system", "content": f"{system_messages}"}
    input_messages = {"role": "user", "content": f"{input_messages}"}
    
    messages = [system_messages]
    messages.append(input_messages)
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=response_format,
    )
    completion_result = completion.choices[0].message

    if completion_result.parsed:
        result = completion_result.parsed
        return result
    else:
        print(completion_result.refusal)


def chat_completion(system_message,user_message,model):
    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user","content": user_message}
    ])

    return completion.choices[0].message.content