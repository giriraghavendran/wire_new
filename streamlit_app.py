import pandas as pd
import streamlit as st
from gtts import gTTS
import os

# Streamlit user interface for file upload
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Load the data into a pandas DataFrame
    df = pd.read_excel(uploaded_file)

    # Text input for the 'Wir' column to search
    wir_input = st.text_input("Enter the Wire ID (Wir) to search: ").upper()

    if wir_input:
        # Find the rows that match the 'Wir' input
        matching_rows = df[df['Wir'].astype(str) == wir_input]

        # Check if there's at least one match
        if not matching_rows.empty:
            for index, row in matching_rows.iterrows():
                selected_data = row[['siz', 'Cir', 'Wir', 'Eq.F', 'Ter-F', 'Eq.T', 'Ter-T']].fillna('Missing')
                selected_data.index = ['Size', 'Color', 'Wire Number', 'Starting Equipment', 'Terminal', 'Ending Equipment', 'Terminal']

                text_to_speak = '. '.join([f"{idx} {val}" for idx, val in selected_data.items()])
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

                language = 'en'
                tts = gTTS(text=text_to_speak, lang=language, slow=False)
                audio_file_path = f'wir_details_audio_{index}.mp3'
                tts.save(audio_file_path)

                # Display data and provide download link for the audio file
                st.write(selected_data.to_frame().T)
                with open(audio_file_path, "rb") as file:
                    st.download_button(
                        label="Download audio file",
                        data=file,
                        file_name=audio_file_path,
                        mime="audio/mp3"
                    )

                # Play audio in the browser
                st.audio(audio_file_path)
        else:
            st.write("No matching entry found for Wir:", wir_input)
