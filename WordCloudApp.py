import pandas as pd
from textblob import Word, TextBlob
import string
import re
from nltk.corpus import stopwords
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import streamlit as st
import time
import nltk

nltk.download('stopwords')
# Load the spacy model from the installed package

def clean(text):

	#Remove emojis and special elements
	text = text.encode('ascii', 'ignore').decode('ascii')

	#Lower case
	text = text.lower()

	#Remove punctuation
	for p in string.punctuation:
		text = text.replace(p, " ")
	

	# Remove additional spaces
	text = re.sub(r'\s+', ' ', text)

	# Remove stop words
	text = " ".join([x for x in text.split() if x not in stopwords.words('english')])
	

	#Lemmatization

	# Load the English language model
	nlp = spacy.load("en_core_web_sm")

	# Process the text
	doc = nlp(text)

	# Perform lemmatization
	text = " ".join([token.lemma_ for token in doc])

	# Filter out words of length less than 3
	text = " ".join([x for x in text.split() if len(x) >= 3])



	return text


# change the value to black
def black_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return "#000000"


def create_wordcloud(text):

	frequency = pd.Series(text.split()).value_counts()

	# Create a wordcloud object
	wordcloud = WordCloud(
					    	width=3000, 
					    	height=2000, 
					    	background_color='#ffffff', 
					    	max_words=1000,
					    	font_path='Oswald-VariableFont_wght.ttf'
					    	).generate_from_frequencies(frequency)

	# set the word color to black
	wordcloud.recolor(color_func = black_color_func)
	wordcloud.to_file("wordcloud.png")

	return wordcloud






st.sidebar.title("Word Cloud Generator")

text = st.sidebar.text_area(label="Paste your text here", height=300)

button = st.sidebar.button('Generate')

if button:
	if text:
		placeholder1 = st.empty()
		with st.spinner('Cleaning text...'):
			cleaned_text = clean(text)
		placeholder1.success('Text cleaning done!')
		
		placeholder2 = st.empty()
		with st.spinner("Generating word cloud..."):
			wordcloud = create_wordcloud(cleaned_text)
		placeholder1.empty()
		placeholder2.success('Word Cloud generation done!')
		time.sleep(1.5)
		st.image("wordcloud.png")
		placeholder2.empty()
