import pandas as pd
import streamlit as st
from gtts import gTTS
import os

# Load the Excel file
@st.cache
def load_data(file_path):
    return pd.read_excel(file_path)

df = load_data('C:/wireproject/.venv/WIRE_DETAIL.xlsx')

# Streamlit user interface for input
wir_input = st.text_input("Enter the Wire ID (Wir) to search: ").upper()

if wir_input:
    # Find the rows that match the 'Wir' input
    matching_rows = df[df['Wir'].astype(str) == wir_input]

    # Check if there's at least one match
    if not matching_rows.empty:
        # Iterate over each matching row
        for index, row in matching_rows.iterrows():
            # Select specific columns and rename for clear text output
            selected_data = row[['siz', 'Cir', 'Wir', 'Eq.F', 'Ter-F', 'Eq.T', 'Ter-T']].fillna('Missing')
            selected_data.index = ['Size', 'Color', 'Wire Number', 'Starting Equipment', 'Terminal', 'Ending Equipment', 'Terminal']

            # Convert the series to a string with descriptive labels
            text_to_speak = '. '.join([f"{idx} {val}" for idx, val in selected_data.items()])

            # Replace specific abbreviations or terms for correct pronunciation
            replacements = {
                'GY': 'Grey',
                'siz': 'size',
                'Cir': 'color',
                'Wir': 'wire number',
                'Eq.F': 'starting equipment',
                'Ter-F': 'terminal',
                'Eq.T': 'ending equipment',
                'Ter-T': 'terminal'
            }
            for key, value in replacements.items():
                text_to_speak = text_to_speak.replace(key, value)

            # Display selected data as a table in Streamlit
            st.write(selected_data.to_frame().T)

            # Language for the TTS
            language = 'en'

            # Create the gTTS object
            tts = gTTS(text=text_to_speak, lang=language, slow=False)

            # Save the spoken text to an MP3 file
            audio_file_path = f'wir_details_audio_{index}.mp3'
            tts.save(audio_file_path)

            # Provide download link for the audio file
            with open(audio_file_path, "rb") as file:
                btn = st.download_button(
                    label="Download audio file",
                    data=file,
                    file_name=audio_file_path,
                    mime="audio/mp3"
                )

            # Optionally, display a button to play the audio directly in the browser
            st.audio(audio_file_path)
    else:
        st.write("No matching entry found for Wir:", wir_input)
