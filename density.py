import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
from nltk import ngrams

# Function to fetch and clean text from a webpage
def get_page_text(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all the text from the page
        text = soup.get_text()

        # Clean the text by removing non-alphabetic characters (optional)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
        text = text.lower()
        return text
    except Exception as e:
        st.error(f"Error fetching or processing the URL: {e}")
        return ""

# Function to generate n-grams
def get_ngrams(text, n):
    words = text.split()  # Tokenize the text into words
    n_grams = ngrams(words, n)  # Generate n-grams
    ngram_counts = Counter(n_grams)  # Count frequency of n-grams
    return {' '.join(ngram): count for ngram, count in ngram_counts.items()}

# Streamlit App
st.title("Keyword Phrase Analysis Tool")

# User Input for URL
url = st.text_input("Enter the URL of the website", "")

if url:
    st.write(f"Analyzing the website: {url}")

    # Get and process the webpage text
    text = get_page_text(url)

    if text:
        # Generate n-grams for 2, 3, and 4 words
        bigrams = get_ngrams(text, 2)
        trigrams = get_ngrams(text, 3)
        fourgrams = get_ngrams(text, 4)

        # Filter n-grams with count > 1
        bigrams = {phrase: count for phrase, count in bigrams.items() if count > 1}
        trigrams = {phrase: count for phrase, count in trigrams.items() if count > 1}
        fourgrams = {phrase: count for phrase, count in fourgrams.items() if count > 1}

        # Display results
        st.subheader("2-word Phrases (Bigrams)")
        if bigrams:
            st.write(bigrams)
        else:
            st.write("No repeated bigrams found.")

        st.subheader("3-word Phrases (Trigrams)")
        if trigrams:
            st.write(trigrams)
        else:
            st.write("No repeated trigrams found.")

        st.subheader("4-word Phrases (Fourgrams)")
        if fourgrams:
            st.write(fourgrams)
        else:
            st.write("No repeated fourgrams found.")

        # Additional Keyword Analysis
        keyword = st.text_input("Enter a specific keyword/phrase to analyze its density (optional)", "")
        if keyword:
            keyword_length = len(keyword.split())
            ngrams_for_keyword = get_ngrams(text, keyword_length)
            keyword_count = ngrams_for_keyword.get(keyword.lower(), 0)
            total_words = len(text.split())
            density = (keyword_count / total_words) * 100 if total_words > 0 else 0

            st.subheader(f"Keyword Analysis for '{keyword}'")
            if keyword_count > 0:
                st.write(f"Occurrences: {keyword_count}")
                st.write(f"Density: {density:.2f}%")
            else:
                st.write("The specified keyword/phrase was not found on the webpage.")
