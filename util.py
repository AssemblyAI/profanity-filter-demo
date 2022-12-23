import re
import youtube_dl  
import streamlit as st
import requests
from pydub import AudioSegment
import time

# CONSTANTS and SETTINGS
ydl_opts = {
   'format': 'bestaudio/best',
   'postprocessors': [{
       'key': 'FFmpegExtractAudio',
       'preferredcodec': 'mp3',
       'preferredquality': '192',
   }],
   'ffmpeg-location': './',
   'outtmpl': "./%(id)s.%(ext)s",
   # 'nocheckcertificate': True
}

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'

CHUNK_SIZE = 5242880

def get_vid(link):
    _id = link.strip()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(_id)

def read_file(filename):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(CHUNK_SIZE)
            if not data:
                break
            yield data

# a function to upload a given file to AssemblyAI's servers
def upload_file(file, auth):
    headers_auth_only = {'authorization': auth}
    upload_response = requests.post(
        upload_endpoint,
        headers=headers_auth_only, 
        data=read_file(file)
	)
    # print('Uploaded to', upload_response.json()['upload_url'])
    return upload_response.json()['upload_url']

# a function that takes a youtube link, downloads the video, uploads it to AssemblyAI's servers and transcribes it
@st.cache
def transcribe_from_link(link, auth):
	headers_auth_only = {'authorization': auth}
    # download the audio of the YouTube video locally
	meta = get_vid(link)
	save_location = meta['id'] + ".mp3"
	# start the transcription of the audio file
	transcript_request = {
		'audio_url': upload_file(save_location, auth),
        "filter_profanity": True
	}

	transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers_auth_only)

	# this is the id of the file that is being transcribed in the AssemblyAI servers
	# we will use this id to access the completed transcription
	transcript_id = transcript_response.json()['id']
	polling_endpoint = transcript_endpoint + "/" + transcript_id
    
	return polling_endpoint, save_location

# return the status of a given transcript 
def get_status(polling_endpoint, auth):
    headers_auth_only = {'authorization': auth}
    polling_response = requests.get(polling_endpoint, headers=headers_auth_only)
    return polling_response.json()['status']

# repeatedly checks the status of a given transcript until the status is completed or error
def poll(polling_endpoint, auth):
    status = get_status(polling_endpoint, auth)
    while status not in ["error", "completed"]:
        time.sleep(10)
        status = get_status(polling_endpoint, auth)

def censor_profanity(transcript, audio_file, beep):
    sound = AudioSegment.from_file(audio_file)
    
    # create output audio
    newsound = AudioSegment.empty()
    #time stamp of the last profanity: 0 by default
    last_vulgarity = 0
    for word in transcript['words']:
        if re.search("[a-zA-Z]\*+", word['text']):
            newsound += sound[last_vulgarity:word['start']]
            newsound += beep[:word['end']-word['start']]
            last_vulgarity = word['end']
    newsound += sound[last_vulgarity:]
    newsound.export("final.mp3", format="mp3")
    return "final.mp3"