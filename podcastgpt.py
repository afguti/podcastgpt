#!/usr/bin/env python3
import sys
import openai
import tiktoken

#lines below are to add api key as an env variable
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, #Using this function I can setup the max number of tokens
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=1000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
    )
    return response.choices[0].message["content"]

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

def remove_text(text):
    # Remove "VERONICA: "
    text = text.replace("VERONICA: ", "")
    
    # Remove words enclosed in []
    import re
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove empty lines
    text = "\n".join(line for line in text.split("\n") if line.strip())
    
    # Remove last 2 lines
    lines = text.split('\n')
    text = '\n'.join(lines[:-2])
    
    # Replace \n with ". "
    text = text.replace('\n', ' ')
    
    return text

def default():
	print("Empty!")

def execute():
	entra = sys.argv[1]
	text = f"""{entra}"""
	messages =  [  
	{'role':'system', 
	 'content':"""You are a podcast script writter."""},    
	{'role':'user', 'content':text},  
	] 
	response, token_dict = get_completion_and_token_count(messages, temperature=0)

	#prompt = f"""Execute the prompt delimited by the backticks. ```{text}```"""
	#response = get_completion(prompt)
	response = remove_text(response)
	print(response)  # The output
	print(token_dict)  # Print the number of tokens used


def main():
	if len(sys.argv) < 2:	
		default()
	else:
		execute()

if __name__ == "__main__":
	main()
