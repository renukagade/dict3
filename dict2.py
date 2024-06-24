import streamlit as st
import requests

# Function to fetch word details from WordsAPI
def fetch_word_details(word, language="en"):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}"
    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "YOUR_RAPIDAPI_KEY"
    }
    params = {"language": language}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to check grammar using LanguageTool API
def check_grammar(text, language="en"):
    url = "https://languagetool.org/api/v2/check"
    params = {"text": text, "language": language}
    response = requests.post(url, data=params)
    return response.json()

# Function to fetch synonyms and antonyms using WordsAPI
def fetch_synonyms_antonyms(word, language="en"):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "YOUR_RAPIDAPI_KEY"
    }
    params = {"language": language}
    synonyms_response = requests.get(url, headers=headers, params=params)
    synonyms = synonyms_response.json().get("synonyms", [])

    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/antonyms"
    antonyms_response = requests.get(url, headers=headers, params=params)
    antonyms = antonyms_response.json().get("antonyms", [])

    return synonyms, antonyms

# Streamlit interface
st.title("Dictionary Bot")
word = st.text_input("Enter a word:")

if st.button("Search"):
    if word:
        # Fetch word details
        details = fetch_word_details(word)
        if "success" in details and details["success"] is False:
            st.error("Word not found. Please try another word.")
        else:
            st.subheader(f"Meaning of '{word}':")
            st.write(details.get("results", {}).get("definition", "Not available"))

            st.subheader("Parts of Speech:")
            st.write(details.get("results", {}).get("partOfSpeech", "Not available"))

            examples = details.get("results", {}).get("examples", [])
            if examples:
                st.subheader("Example Usage:")
                for example in examples:
                    st.write(f"- {example}")

            st.subheader("Origin of the word:")
            st.write(details.get("results", {}).get("origin", "Not available"))

            # Check grammar
            st.subheader("Grammar Check:")
            grammar_check = check_grammar(word)
            if grammar_check.get("matches"):
                for match in grammar_check["matches"]:
                    st.write(f"Message: {match['message']}")
                    st.write(f"Replacements: {match['replacements']}")

            # Fetch synonyms and antonyms
            synonyms, antonyms = fetch_synonyms_antonyms(word)
            st.subheader("Synonyms:")
            st.write(", ".join(synonyms) if synonyms else "Not available")

            st.subheader("Antonyms:")
            st.write(", ".join(antonyms) if antonyms else "Not available")
    else:
        st.warning("Please enter a word to search.")
