import streamlit as st
import requests
from googletrans import Translator

BASE_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

def get_word_data(word):
    url = f"{BASE_URL}{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            return data[0]
        else:
            return None
    else:
        return None

def get_word_meanings(data):
    meanings = []
    if 'meanings' in data:
        for meaning in data['meanings']:
            meanings.append({
                'part_of_speech': meaning.get('partOfSpeech', 'Unknown'),
                'definitions': [defn['definition'] for defn in meaning.get('definitions', [])],
                'examples': [defn['example'] for defn in meaning.get('definitions', []) if 'example' in defn]
            })
    return meanings

def get_word_pronunciation(data):
    if 'phonetics' in data:
        return data['phonetics'][0]['text']
    return "No pronunciation found."

def get_word_origin(data):
    if 'origin' in data:
        return data['origin']
    return "Origin not available."

def get_related_words(data):
    related = []
    if 'meanings' in data:
        for meaning in data['meanings']:
            for definition in meaning.get('definitions', []):
                if 'derivativeOf' in definition:
                    related.extend(definition['derivativeOf'])
                if 'hasTypes' in definition:
                    related.extend(definition['hasTypes'])
    return related

def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

# Streamlit UI
st.title("Enhanced Multilingual Dictionary Bot")
st.write("Enter a word to get its meaning and more.")

word = st.text_input("Enter a word:")
language = st.selectbox('Select language:', ['English', 'French', 'Hindi','Telugu'])
    
if st.button('Lookup'):
    translate_text(word,language)

if word:
    word_data = get_word_data(word)
    if word_data:
        meanings = get_word_meanings(word_data)
        pronunciation = get_word_pronunciation(word_data)
        origin = get_word_origin(word_data)
        related_words = get_related_words(word_data)

        st.write(f"Word: {word}")
        st.write(f"Pronunciation: {pronunciation}")
        st.write(f"Origin: {origin}")

        for idx, meaning in enumerate(meanings, start=1):
            st.write(f"\nMeaning {idx}:")
            st.write(f"Part of Speech: {meaning['part_of_speech']}")
            if meaning['definitions']:
                st.write("Definitions:")
                for definition in meaning['definitions']:
                    st.write(f"- {definition}")
            if meaning['examples']:
                st.write("Examples:")
                for example in meaning['examples']:
                    st.write(f"- {example}")

        if related_words:
            st.write("\nRelated Words:")
            st.write(", ".join(related_words))

        dest_lang = st.selectbox("Translate to language:", ["english", "french","Hindi","Telugu"])
        translated_definitions = []
        for meaning in meanings:
            for definition in meaning['definitions']:
                translated_definition = translate_text(definition, dest_lang)
                translated_definitions.append(translated_definition)
        st.write(f"\nTranslated Definitions:")
        for idx, trans_def in enumerate(translated_definitions, start=1):
            st.write(f"Definition {idx}: {trans_def}")

    else:
        st.write("No data found for the given word.")
