from mutagen.mp3 import MP3 #pip install mutagen
from pydub import AudioSegment, silence #for mp3 manipulation. pip install pydub

#from podcastgpt import remove_text, save_output
from speech import tts
from bsoundprompt import prompt
from filehandle import remove_text, save_output

#Font colors
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreenIn(skk): input("\033[92m {}\033[00m" .format(skk))

def audio(resp: str, ch: int):
	with open(resp, 'r') as file:
		content = file.read()
	resp1 = remove_text(content,0,0,1) #Part1 for tts
	resp1 = '<speak>\n'+resp1+'\n</speak>'
	save_output(f"resp{ch}_2.txt", resp1) #Part1 for tts
	prGreenIn(f"\nREVIEW resp{ch}_2.txt FOR tts AND PRESS ENTER TO CONTINUE")
	tts(engine="neural", region='ap-northeast-1', endpoint_url='https://polly.ap-northeast-1.amazonaws.com/', output_format='mp3', 
	bucket_name='podcast-wellness-e1', s3_key_prefix='prueba', voice_id='Ruth', text_file_path=f'./resp{ch}_2.txt', output_path=f'./part{ch}.mp3')
	audio = MP3(f"part{ch}.mp3")
	audio_lenght=int(audio.info.length)+6
	prRed(f'\naudio lenght for Part{ch}: {audio_lenght} seconds\n')
	prompt1 = prompt(content)
	lines = prompt1.split('\n')
	last_two = lines[-2:]
	last_lines = "\n".join(last_two)
	prRed(f'\nPrompt to generate Part{ch} background sound: ')
	print(last_lines+"\n")
	#we use the Colab from https://github.com/facebookresearch/audiocraft to generate background audio
	prGreenIn(f"\nNOW BASED ON THE PROMPT ABOVE, GENERATE BACKGROUND SOUND, NAME IT background{ch}.mp4, AND PRESS ENTER TO CONTINUE") #Need to automate this part
	backg = AudioSegment.from_file(f"./background{ch}.mp4", format="mp4")
	backg = backg - 18 #Here we can adjust the volume of the background sound
	backg = backg * (int(audio_lenght)+1)
	backg = backg[0:audio_lenght*1000]
	faded_sound = backg.fade_out(3000) #Fade out the background audio the last 3 seconds
	talk = AudioSegment.from_file(f"./part{ch}.mp3", format="mp3")
	talk = talk + 8
	overlay1 = faded_sound.overlay(talk, position=3000)
	file_handle = overlay1.export(f'final_p{ch}.mp3', format='mp3')
	prRed(f"\nPART {ch} IS COMPLETED!")
	return None
