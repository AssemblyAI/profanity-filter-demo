How to Detect and Censor Profanities
--

This is an example of how you can use AssemblyAI's [Profanity Filter](https://www.assemblyai.com/docs/core-transcription#profanity-filtering) feature to automatically detect profanities and replace them in your audio file. 

## Quick Setup

* Download project files by running `git clone https://github.com/AssemblyAI/speaker-diarization.git`
* Navigate to the project folder
* Create a new [virtual environment](https://docs.python.org/3/library/venv.html)
* Activate the new virtual environment and run `pip install -r requirements.txt` to install project dependencies
* Run the application using the `streamlit run profanity_filter.py`

## How it Works

The YouTube video from the link you submitted is downloaded and then uploaded to AssemblyAI's servers for transcription with `filter_profanity` set to `true`. When the transcript is complete, a regex search for all words that start with a letter followed by asterisks identifies the timestamps in the original audio with profanity. The original audio is removed and replaced with the censor of the user's choice.

## Main Dependencies

* [Streamlit](https://pypi.org/project/streamlit/) The fastest way to build data apps in Python
* [youtube_dl](https://pypi.org/project/youtube_dl/) Command-line program to download videos from YouTube.com
* [pydub](https://pypi.org/project/pydub/) Manipulate audio with an simple and easy high level interface.

Contact Us
--
If you have any questions, please feel free to reach out to our Support team - support@assemblyai.com!