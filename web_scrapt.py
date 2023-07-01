from bs4 import BeautifulSoup
import requests
#import nltk
#nltk.download("punkt")
from tokencount import counter

import sys
import openai
import tiktoken

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_completion_and_token_count(messages, #Here I can count the number of tokens
                                   model="gpt-3.5-turbo-0613", 
                                   temperature=0, 
                                   max_tokens=1000):
    
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

def parser(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    
    #Get the tokens of the text
    count_model = "gpt-3.5-turbo-0613"
    tokens = counter(text,count_model)

    return tokens, text

def curate(url, topic, intro):
    tokens, entra = parser(url)
    #return f"{entra}"
    if tokens > 2500:
        response = f"CONTENT HAS {tokens}. THEY ARE TOO MANY!"
    else:
        #text = f"""Is this content relevant to {topic}? If it is, provide a summary of about 100 words {entra}"""
        #text = f"""Take the main ideas from the text and write a segment for a podcast of about 100 words. Mention the website {url} in a concise and reader-friendly way at the beginning of the segment, and refer to it as the source of the information that follows. This is not the fist segment of the episode. The information is: {entra}"""
        #text = f"""Take the text in backticks and write a segment to be included in the middle of a podcast script. The segment has to have around 200 words. ```{entra}```"""
        text = f"""Write a script for an episode of a podcast named Your Wellness Journey. The host's name is Veronica, and there are no guests in the podcast. The topic of the episode is {topic}.

Introduction:

- Briefly introduce the podcast and its focus on wellness. Mention that the content and voice are generated by Artificial intelligence.

Part 1 (Around 500 words):

- Introduce the main topic of the episode related to {topic}.
- Discuss key points, insights, or strategies related to {topic}.
- Encourage listeners to engage with the content and apply it to their own lives.

Part 2 (Around 500 words):
- Start Part2 following this example: {intro}
- Mention the website {url} in a concise and reader-friendly way at the beginning. Avoid writting the full url: {url}.
- Mention that the link to the website can be found in the description of the episode.
- Extract and present the main ideas from ```{entra}```.
- Provide a one sententence mention about Part 3.

Write a script for the Part 2 that is a continuation of Part 1. The content should be around 500 words. Remove any last paragraphs that attempt to finish the script.
Avoid using any sentence that implies welcoming the listener back or expressing pleasure in their return.
        """
        messages = [
            {'role': 'system',
             'content': "You are a content curation assistant."},
             #'content': "You are a podcast script writer"},
            {'role': 'user', 'content': text},
        ]
        response, token_dict = get_completion_and_token_count(messages, temperature=0)
        #text = f"""write a small segment for a podcast from text. The segment is about 100 words. text: {response}"""
        #messages = [
        #    {'role': 'system',
        #     #'content': "You are a content curation assistant."},
        #     'content': "You are a popular podcaster."},
        #    {'role': 'user', 'content': text},
        #]
        #response, token_dict = get_completion_and_token_count(messages, temperature=0)

    return response


def main():
    #parser(url)
    curate(url, topic)

if __name__ == "__main__":
    main()