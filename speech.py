import boto3

def start_polly_synthesis_task(region, endpoint_url, output_format, bucket_name, s3_key_prefix, voice_id, tex
t_file_path):
    # Create a Boto3 client for Polly
    polly_client = boto3.client('polly', region_name=region, endpoint_url=endpoint_url)
    # Read the text content from the file
    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        text = text_file.read()
    # Start the speech synthesis task
    response = polly_client.start_speech_synthesis_task(
        OutputFormat=output_format,
        OutputS3BucketName=bucket_name,
        OutputS3KeyPrefix=s3_key_prefix,
        VoiceId=voice_id,
        Text=text
    )
    return response['SynthesisTask']['TaskId'] 

#pending: How to define the language?
region = 'ap-northeast-1'
endpoint_url = 'https://polly.ap-northeast-1.amazonaws.com/'
output_format = 'mp3'
bucket_name = 'podcast-wellness-e1' #a bucket was created manually. This can be automated
s3_key_prefix = 'prueba' #This is a folder inside the bucket
voice_id = 'Joanna'
text_file_path = './input.txt' #The input in the current directory

task_id = start_polly_synthesis_task(region, endpoint_url, output_format, bucket_name, s3_key_prefix, voice_id, text_file_path)

print(f'Started Polly speech synthesis task with ID: {task_id}')

def check_task_status(region, task_id):
    # Create a Boto3 client for Polly
    polly_client = boto3.client('polly', region_name=region)

    # Check the status of the synthesis task
    response = polly_client.get_speech_synthesis_task(TaskId=task_id)
    status = response['SynthesisTask']['TaskStatus']

    return status

while True:
    status = check_task_status(region, task_id)
    if status == 'completed':
        print('Speech synthesis task is completed.')
        break
    elif status == 'failed':
        print('Speech synthesis task failed.')
        break
    elif status == 'inProgress':
        print('Speech synthesis task is still in progress. Waiting...')
        time.sleep(5)  # Wait for a few seconds before checking again
    else:
        print('Unexpected task status:', status)
        break

your_bucket = s3.Bucket(bucket_name)

for s3_file in your_bucket.objects.all():
    print(s3_file.key)

your_bucket.download_file('prueba.f7869603-2cfa-47de-964e-c32bc6942e4c.mp3','./salida.mp3')

your_bucket.download_file(f'{s3_key_prefix}.{task_id}.mp3','./output.mp3')

