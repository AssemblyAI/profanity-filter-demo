import util
import requests
import streamlit as st
from pydub import AudioSegment

# Title
st.title('Censor profanities in YouTube videos 🧼')

# Captures the user's auth key from AssemblyAI
auth_key = st.text_input("Enter your auth key", type="password")
headers = {'authorization': auth_key}

# Allows the user to choose which censor to use
censor = st.radio("Choose your censor:", ["Beep 🤖", "Dolphin 🐬", "Duck 🐥", "Silence 🤐"])

# Changes the constant variable beep for the user's choice of censor
if censor == "Beep 🤖":
    beep = AudioSegment.from_file('src/beep.m4a')[500:]
elif censor == "Dolphin 🐬":
    beep = AudioSegment.from_file('src/dolphin.m4a')[300:]
elif censor == "Duck 🐥":
    beep = AudioSegment.from_file('src/duck.m4a')[250:450]
elif censor == "Silence 🤐":
    beep = AudioSegment.silent(300)
else:
    beep = AudioSegment.from_file('src/beep.m4a')[500:]

# Captures the YouTube link provided by the user
link = st.text_input('Enter your YouTube video link', 'https://youtu.be/E6M-XUW4xYY')

# Submits the YouTube link to be transcribed by AssemblyAI
polling_endpoint, file = util.transcribe_from_link(link, auth_key)

# Changes status to 'submitted'
st.session_state['status'] = 'submitted'

# Repeatedly poll the transcript until it is completed
util.poll(polling_endpoint, auth_key)

# Sets the 
st.session_state['status'] = util.get_status(polling_endpoint, auth_key)

#
st.text("The transcription is " + st.session_state['status'])

if st.session_state['status']=='completed':
    polling_response = requests.get(polling_endpoint, headers=headers)
    transcript = polling_response.json()
    st.audio(util.censor_profanity(transcript, file, beep))
