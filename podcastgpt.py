#!/usr/bin/env python3
import sys
import openai
import tiktoken

#my scripts
from web_scrapt import curate
from summary import outtro

#lines below are to add api key as an env variable
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

#n is the number of lines to remove from the top, and m is the number of lines to remove from bottom.
def remove_text(text,n: int,m: int):
    # Remove "VERONICA: or Veronica: "
    text = text.replace("VERONICA: ", "")
    text = text.replace("Veronica: ", "")

    # Remove words enclosed in []
    import re
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove empty lines
    text = "\n".join(line for line in text.split("\n") if line.strip())
    
    if n != 0 or m != 0:
        # Remove the first n lines, and last m lines
        lines = text.split('\n')
        text = '\n'.join(lines[n:-m])
    
    #Replace \n with ". "
    text = text.replace('\n', '\n<break time="500ms"/>\n')
    
    return text

#Create the file where the output is saved
def save_output(filename: str, texto: str):
    directory = './'

    file_path = os.path.join(directory, filename)

    if not os.path.exists(file_path):
        # File does not exist, create it
        with open(file_path, 'w') as file:
            pass  # This creates an empty file

    with open(file_path, 'a') as file:
        # Append text to the file
        file.write("\n"+texto)
    return f"Content saved to {file_path}."

#It returns Empty when no argument is given to podcastgpt.py
def default():
	print("Empty!")

def execute():
	entra = sys.argv[1]
	text = f"""Write a script for an episode of a podcast named Your Wellness Journey. The host's name is Veronica, and there are no guests in the podcast. The topic of the episode is {entra}.

Introduction:

- Briefly introduce the podcast and its focus on wellness. Mention that the content and voice are generated by Artificial intelligence.

Part 1 (Around 500 words):

- Introduce the main topic of the episode related to {entra}
- Discuss key points, insights, or strategies related to {entra}.
- Encourage listeners to engage with the content and apply it to their own lives.

Write a script for the Introduction and Part 1. The content should be around 500 words. Remove any last paragraphs that attempt to finish the script. Replace welcome back with just welcome."""
	messages =  [  
	{'role':'system', 
	 'content':"""You are a podcast script writter."""},    
	{'role':'user', 'content':text},  
	] 
	response, token_dict = get_completion_and_token_count(messages, temperature=0)
	
	save_output("tocompare", response) #for test purpose
	response = remove_text(response,0,2)  #Part1
	save_output("wellness3", response)
	
    #Section 2 picks up any website related to the topic
	url = "https://www.verywellmind.com/self-care-strategies-overall-stress-reduction-3144729" #URL for topic: self-care
	#url = "https://www.goalcast.com/wellness/" #URL for the concept of wellness
	intro = "Now in this section of the podcast we will review information we found in a web site."
	part2 = curate(url, entra, intro)
	save_output("tocompare", part2) #for test purpose
	if len(part2) < 100:
	    print("Something went wrong. Check output file!")
	else:
	    print("All seems good!")
	    part2 = remove_text(part2,1,2) #Part2
	save_output("wellness3", part2)

    #Section 3 will pick up a news article
	url = "https://www.forbes.com/sites/kathymillerperkins/2023/06/27/radical-self-care-how-to-redefine-boundaries-between-career-and-life/?sh=23e2f83d4dd6" #URL for topic: self-care in the news
	#url = "https://www.bbc.co.uk/programmes/articles/558FD1c2hXHCh1wJfN6lkKS/how-wellness-became-big-business" #URL for the concept of wellness in the news
	intro1 = f"Now in this section of the podcast we will review the news about {entra}"
	part3 = curate(url, entra, intro1)
	save_output("tocompare", part3) #for test purpose
	if len(part3) < 100:
	    print("Something went wrong. Check output file!")
	else:
	    print("All seems good!")
	    part3 = remove_text(part3,1,2) #Part3
	save_output("wellness3", part3)

	#Summary:
	path = "./wellness3"
	with open(path, 'r') as file:
	    content = file.read()
	part4 = outtro(content, "Mindfulness") #here we need to input the topic of the next episode
	save_output("tocompare", part4) #for text purpose
	part4 = remove_text(part4,0,0)    
	save_output("wellness3", part4)
	with open(path, 'r') as file:
	    content = file.read()
	polly = f"<speak>\n{content}\n</speak>"
	save_output("forpolly", polly)

			
def main():
	if len(sys.argv) < 2:	
		default()
	else:
		execute()

if __name__ == "__main__":
	main()
