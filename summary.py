import requests
from tokencount import counter

import sys
import openai
import tiktoken

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_completion_and_token_count(messages, #Here I can count the number of tokens
                                   model="gpt-3.5-turbo-16k", 
                                   temperature=0, 
                                   max_tokens=10000):
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    
    content = response.choices[0].message["content"]
    
    token_dict = {
'prompt_tokens':response['usage']['prompt_tokens'],
'completion_tokens':response['usage']['completion_tokens'],
'total_tokens':response['usage']['total_tokens'],
    }

    return content, token_dict

def outtro(content, next_episode):
    tokens = counter(content, "gpt-3.5-turbo-16k")
    if tokens > 15000:
        response = f"CONTENT HAS {tokens}. THEY ARE TOO MANY!"
    else:
        text = f"""The text enclosed in angle brackets is the episode of a podcast. List the key points and main ideas that capture the essence of the episode.
        Determine the central theme or topic that the episode explores.
        Identify the most important takeaways or insights from the episode.
        Episode:
        <{content}>
        
        Tasks:
        - Based on the list of main ideas, central theme, and the takeaways, Write an engaging last section of a script of a podcast episode.
        - Start the section with: Now, before we finish this episode lets review the main takeaways.
        - Finish the section inviting listeners to tune for the next episode in which we will discuss about {next_episode}.
        - The section has to be concise. Aim for a lenght of about 200 words."""
        messages = [
            {'role': 'system',
             'content': "You are a content curation assistant."},
            {'role': 'user', 'content': text},
        ]
        response, token_dict = get_completion_and_token_count(messages, temperature=0)

    return response

def main():
    curate(url, topic)

if __name__ == "__main__":
    main()