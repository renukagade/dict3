import streamlit as st
import requests

# Function to fetch word details from API
def fetch_word_details(word, language='en'):
    
    url = f'https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}'
   
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to get meanings and examples
def get_meanings_and_examples(details):
    meanings_list = []
    for entry in details:
        for meaning in entry['meanings']:
            meanings = []
            for definition in meaning['definitions']:
                meaning_text = f"**{definition['partOfSpeech']}**: {definition['definition']}"
                if 'example' in definition:
                    meaning_text += f"\n*Example*: {definition['example']}"
                meanings.append(meaning_text)
            meanings_list.append({
                'word': entry['word'],
                'meanings': meanings
            })
    return meanings_list

# Function to get word origin
def get_word_origin(details):
    origins = []
    for entry in details:
        if 'origin' in entry:
            origins.append({
                'word': entry['word'],
                'origin': entry['origin']
            })
    return origins

# Streamlit app
def main():
    st.title('Dictionary Bot')
    word = st.text_input('Enter a word:')
    language = st.selectbox('Select language:', ['English', 'French', 'Spanish'])
    
    if st.button('Lookup'):
        if word:
            if language == 'English':
                details = fetch_word_details(word, 'en')
                if details:
                    meanings = get_meanings_and_examples(details)
                    origins = get_word_origin(details)
                    
                    for meaning in meanings:
                        st.header(f"Meaning ({meaning['word']})")
                        for definition in meaning['meanings']:
                            st.markdown(f"- {definition}")
                        st.markdown("---")
                    
                    if origins:
                        st.header(f"Origin of '{origins[0]['word']}'")
                        st.markdown(origins[0]['origin'])
                        st.markdown("---")
                else:
                    st.error(f"Word '{word}' not found in the dictionary.")
            # Implement similar logic for other languages using respective APIs
        else:
            st.warning("Please enter a word to lookup.")

if __name__ == '__main__':
    main()
