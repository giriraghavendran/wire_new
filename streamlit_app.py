import pandas as pd
import streamlit as st
import pyttsx3

# Streamlit app setup
st.title("Wire Detail Search")
speaker = pyttsx3.init()
speaker.setProperty('rate', 95)

# Initialize or update persistent session state for search history
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Display searched wire names in sidebar
st.sidebar.write("Wires you have searched:")
for item in st.session_state.search_history:
    st.sidebar.write(item)

# File uploader for Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    search_text = st.text_input("Enter the wire name:", key="wirename")

    if search_text:
        normalized_search_text = search_text.strip().upper()
        if normalized_search_text and normalized_search_text not in st.session_state.search_history:
            st.session_state.search_history.append(normalized_search_text)

        # Perform search only within the 'Wir' column
        matches = df[df['Wir'].astype(str).str.upper().str.contains(normalized_search_text, na=False)]

        if not matches.empty:
            match_index = st.number_input("Select match index:", min_value=0, max_value=len(matches) - 1, step=1)
            match = matches.iloc[match_index]
            color_map = {'GY': 'gray', 'BL': 'black', 'B': 'blue', 'R': 'red'}
            color = color_map.get(match['Cir'], match['Cir'])  # Default to original if not mapped

            # Display wire details
            st.write(f"S.No: {match['S.N']}")
            st.write(f"Size: {match['siz']}")
            st.write(f"Color: {color}")
            st.write(f"Wire Name: {match['Wir']}")
            st.write(f"Starting Equipment: {match['Eq.F']}")
            st.write(f"Terminal 1: {match['Ter-F']}")
            st.write(f"Ending Equipment: {match['Eq.T']}")
            st.write(f"Terminal 2: {match['Ter-T']}")

            # Speaking functionality
            details = f"Serial Number {match['S.N']}, Size {match['siz']}, Color {color}, Wire {match['Wir']}, Starting equipment {match['Eq.F']}, Terminal {match['Ter-F']}, Ending equipment {match['Eq.T']}, Terminal {match['Ter-T']}"
            st.write(details)
            speaker.say(details)

            if len(matches) > 1:
                speaker.say("Another wire named {0} found. Click plus to proceed.".format(match['Wir']))
            speaker.runAndWait()
        else:
            st.write("No matches found.")
            speaker.say("No matches found.")
            speaker.runAndWait()


