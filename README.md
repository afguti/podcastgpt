# Your Wellness Journey Podcast

## Introduction
This repository contains the scripts for the episodes of the "Your Wellness Journey" podcast. The podcast is hosted by Veronica and focuses on various wellness topics. The scripts are generated using artificial intelligence to provide engaging and informative content to the listeners.

## Scripts
The repository includes four main scripts:

1. `podcastgpt.py`: This script generates the main content for an episode based on a given topic. It includes an introduction, Part 1, and the summary.

2. `web_scrapt.py`: This script scrapes information from a website related to the given topic and curates it for Part 2 of the episode.

3. `summary.py`: This script generates the concluding part of the episode, summarizing the main ideas and inviting listeners to the next episode.

4. `tokencount.py`: This script contains a function to count the number of tokens in a given text, which is used in other scripts for token tracking.

5. `speech.py`: Text to speech script. 
    Notes: IAM identity has to be created and in Permissions policies "AmazonPollyFullAccess" as well as "AmazonS3FullAccess" has to be added.
    Sample of command:
    tts(engine="neural", region='ap-northeast-1', endpoint_url='https://polly.ap-northeast-1.amazonaws.com/', output_format='mp3', bucket_name='podcast-wellness-e1', s3_key_prefix='prueba', voice_id='Ruth', text_file_path='./wellness3')
    Source:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
    https://docs.aws.amazon.com/polly/latest/dg/API_StartSpeechSynthesisTask.html
    https://stackoverflow.com/questions/50100221/download-file-from-aws-s3-using-python
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/start_speech_synthesis_task.html#Polly.Client.start_speech_synthesis_task
    https://stackoverflow.com/questions/73533742/start-speech-synthesis-task-to-mp3-amazon-polly?rq=1


## Usage
To use the scripts and generate an episode script, follow these steps:

1. Set up the environment by installing the required dependencies and setting the OpenAI API key as an environment variable.

2. Run the `podcastgpt.py` script with the desired topic as a command-line argument. The script will generate the content for the introduction and Part 1, and save it to a file.

3. Run the `web_scrapt.py` script with the generated URL and topic as arguments. This script will scrape information from the website and curate it for Part 2, which will be appended to the previously generated file.

4. Run the `summary.py` script with the content file from the previous steps and the topic for the next episode as arguments. This script will generate the concluding part of the episode and append it to the content file.

5. The final script can be converted into speech using text-to-speech tools or further processed as needed.

Please ensure that you have the necessary permissions and comply with any usage guidelines or terms of service when using external websites or APIs for content curation.

## Dependencies
The scripts rely on the following dependencies:

- Python 3
- OpenAI Python Library
- BeautifulSoup (for web scraping)
- dotenv (for loading environment variables)

Please refer to the `requirements.txt` file for the specific versions of the dependencies used in this project.

## Current challenges and goals
1. We found that the urls that are selected contain very little reading material which reflect in poor content and short episode. For now, we might need a human to revise the URL before it is used.

2. We have to keep looking for more realistic voice and audio.

3. The content has to last for more than an hour.

4. The podcast has to have a host and a guest.

5. Automate tasks that currently require human intervention.

6. automate audio upload.

7. keep track of visited websites, to avoid repetition.

8. keep track of topics discussed, to avoid repetition.

9. Automate the creation of a short description of episode of around 100 words.

10. Automate image creation.

11. Incorporate LangChain and agents for further automation.

## Example Workflow
Here is a visualization of the workflow:

```mermaid
graph TB
    A[Agent create a list of episodes topic1 topic2 ...]
    A --> B[Generate the introduction based on topicX]
    B --> C[Search the web for topicX]
    C --> D[Get a list of 10 URLs. Remove those with content length that cannot be proceed. From the remaining, pick the most relevant.]
    D --> E{Was the URL visited before?}
    E --> |Yes|F[Take the next most relevant URL from the list]
    E --> |No|H[Repeat for Part 3, but look in news.]
    H --> D
    F --> G{Is the list empty?}
    G --> |Yes|I[Look for the next 10 URLs]
    H --> J[Create the summary and consider topicX+1]
    I --> D
    D --> G
    H --> K[Create 100 word episode description]
    J <--> L((Verify that the content fits a podcast script))
    K <--> L
    L --> M[Clean up and generate text for audio processing]
    M --> O[Audio creation]
    M <--> N((Human revision))
    O <--> N
    N <--> P[Generate the image for the episode]
    O --> Q[Upload episode]
    P --> Q
    Q --> R[Promote in social media]
    G --> |No|H
    B --> |Append|S[Output text]
    H --> |Append Part2 and Part3|S
    J --> |Append|S
    N <--> K


