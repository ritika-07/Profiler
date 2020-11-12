# Core Packages
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import *
from tkinter import ttk #for tab creation using tkinter
import tkinter.filedialog

# Other pkg
import time

# NLP Pkgs
from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
from gensim.summarization import summarize
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

# Web Scraping Pkg
from urllib.request import urlopen
from bs4 import BeautifulSoup

#Personality Pkgs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
import re
import tweepy
import nltk 
import sys
import pandas as pd
import os
import string
import numpy as np
from unidecode import unidecode
import csv
from itertools import islice
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

def sumy_summary(docx):
	parsed_text = PlaintextParser.from_string(docx, Tokenizer("english"))
	summary_lexrank = LexRankSummarizer()
	summary = summary_lexrank(parsed_text.document, 3)
	summary_list = [str(sentence) for sentence in summary_lexrank]
	result=''.join(summary_list)
	return result

 # Structure and Layout
window = Tk()
window.title("Candidate Profiler For Job Screening")
window.geometry("900x600")
window.config(background='black')

style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn') #tabs positioned west-north
timestr = time.strftime("%Y%m%d-%H%M%S")

# TAB LAYOUT
tab_control = ttk.Notebook(window,style='lefttab.TNotebook')
 
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)
tab6 = ttk.Frame(tab_control)

# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text=f'{"Home":^40s}')
tab_control.add(tab2, text=f'{"Social Media Personality":^29s}')
tab_control.add(tab3, text=f'{"Candidate Information":^30s}')
tab_control.add(tab4, text=f'{"Canditate File":^37s}')
tab_control.add(tab5, text=f'{"Candidate URLs":^33s}')
tab_control.add(tab6, text=f'{"Alternate Algorithms":^32s}')

label1 = Label(tab1, text= 'About',padx=5, pady=5)
label1.grid(column=1, row=0, pady=5)
 
label2 = Label(tab2, text= 'Twitter Psychatric Evaluation',padx=5, pady=5)
label2.grid(column=1, row=0, pady=5)

label3 = Label(tab3, text= 'Candidate Resumé and Information Summarizer',padx=5, pady=5)
label3.grid(column=1, row=0, pady=5)

label4 = Label(tab4, text= 'Candidate File Summarizer',padx=5, pady=5)
label4.grid(column=1, row=0, pady=5)

label5 = Label(tab5, text= 'Candidate Web Presence Analysis',padx=5, pady=5)
label5.grid(column=1, row=0, pady=5)

label6 = Label(tab6, text= 'Multi-Algorithm Comparison',padx=5, pady=5)
label6.grid(column=1, row=0, pady=5)

tab_control.pack(expand=1, fill='both')


#####
# Personality tab functions
def exec_twt():
	ckey='YvQZ4wcEhYo4F4Lj8PQqj500d'
	csecret='nDMvzbvQxt2zW9GZOalnOikeDcwGwPwvi2USOD5phJCmw5e9wD'
	atoken='994417184322433025-anaAEWzZErK5h8CGTxEgJMPFwfRoMNA'
	asecret='M2RwOR7CaWHMO7d83iWuKhHmEtgyaomobBNt9bsJhSF3i'
	authenticate=tweepy.OAuthHandler(ckey, csecret)
	authenticate.set_access_token(atoken, asecret)
	api=tweepy.API(authenticate)

	emoji = r"""
	    (?:
	        [:=;] # Eyes
	        [oO\-]? # Nose (optional)
	        [D\)\]\(\]/\\OpP] # Mouth
	    )"""

	emoji_pattern = re.compile("["
	        u"\U0001F600-\U0001F64F"  # emoticons
	        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
	        u"\U0001F680-\U0001F6FF"  # transport & map symbols
	        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
	                           "]+", flags=re.UNICODE)


	regex_str = [
	    emoji,
	    r'<[^>]+>',  # HTML tags
	    r'(?:@[\w_]+)',  # @-mentions
	    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
	    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

	    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
	    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
	    r'(?:[\w_]+)',  # other words
	    r'(?:\S)'  # anything else
	]

	tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
	emoticon_re = re.compile(r'^' + emoji + '$', re.VERBOSE | re.IGNORECASE)


	def tokenize(s):
	    return tokens_re.findall(s)


	def preprocess(s, lowercase=False):
	    tokens = tokenize(s)
	    if lowercase:
	        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	    return tokens
	def preproc(s):
		
		s= unidecode(s)
		Tag_POS=preprocess(s)
		

		tweet=' '.join(Tag_POS)
		sw = set(stopwords.words('english'))
		word_tokens = word_tokenize(tweet)
		
		filtered_sentence = []
		for w in Tag_POS:
		    if w not in sw:
		        filtered_sentence.append(w)
		
		stemmed_sentence=[]
		stemmed_output = SnowballStemmer("english", ignore_stopwords=True)
		for w in filtered_sentence:
			stemmed_sentence.append(stemmed_output.stem(w))
		

		var = ' '.join(c for c in stemmed_sentence if c not in string.punctuation) 
		preProcessed=var.split(" ")
		final=[]
		for i in preProcessed:
			if i not in final:
				if i.isdigit():
					pass
				else:
					if 'http' not in i:
						final.append(i)
		var1=' '.join(c for c in final)
		return var1

	def getTweets(user):
		csvFile = open('user.csv', 'a', newline='')
		csvWriter = csv.writer(csvFile)
		try:
			for i in range(0,4):
				tweets=api.user_timeline(screen_name = user, count = 1000, include_rts=True, page=i)
				for status in tweets:
					tw=preproc(status.text)
					if tw.find(" ") == -1:
						tw="blank"
					csvWriter.writerow([tw])
		except tweepy.TweepError:
			print("Failed to run the command on that user, Skipping...")
		csvFile.close()



	username=str(e1.get('1.0',tk.END))
	getTweets(username)
	with open('user.csv','rt') as f:
		csvReader=csv.reader(f)
		tweetList=[rows[0] for rows in csvReader]
	os.remove('user.csv')
	with open('CSV_Data/newfrequency300.csv','rt') as f:
		csvReader=csv.reader(f)
		mydict={rows[1]: int(rows[0]) for rows in csvReader}

	vectorizer=TfidfVectorizer(vocabulary=mydict,min_df=1)
	x=vectorizer.fit_transform(tweetList).toarray()
	df=pd.DataFrame(x)


	model_IE = pickle.load(open("Pickle_Data/BNIEFinal.sav", 'rb'))
	model_SN = pickle.load(open("Pickle_Data/BNSNFinal.sav", 'rb'))
	model_TF = pickle.load(open('Pickle_Data/BNTFFinal.sav', 'rb'))
	model_PJ = pickle.load(open('Pickle_Data/BNPJFinal.sav', 'rb'))

	answer=[]
	IE=model_IE.predict(df)
	SN=model_SN.predict(df)
	TF=model_TF.predict(df)
	PJ=model_PJ.predict(df)


	b = Counter(IE)
	value=b.most_common(1)
	#print(value)
	if value[0][0] == 1.0:
		answer.append("I")
	else:
		answer.append("E")

	b = Counter(SN)
	value=b.most_common(1)
	#print(value)
	if value[0][0] == 1.0:
		answer.append("S")
	else:
		answer.append("N")

	b = Counter(TF)
	value=b.most_common(1)
	#print(value)
	if value[0][0] == 1:
		answer.append("T")
	else:
		answer.append("F")

	b = Counter(PJ)
	value=b.most_common(1)
	#print(value)
	if value[0][0] == 1:
		answer.append("P")
	else:
		answer.append("J")
	mbti="".join(answer)

	# Classifying Personality's ==========================================>

	if mbti == 'ENFJ':
		result="Username: " + username + "\n\n" + mbti + "- The Giver :-\nThey are extroverted, idealistic, charismatic, outspoken, \n highly principled and ethical, and usually know how to connect \n with others no matter their background or personality.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ISTJ':
		result="Username: " + username + "\n\n" + mbti + "- The Inspector :-\nThey appear serious, formal, and proper. They also love \n traditions and old-school values that uphold patience, hard work,\n honor, and social and cultural responsibility. They are reserved, calm, quiet, and upright.\n\n"
		tab2_display.insert(tk.END,result)
	

	elif mbti == 'INFJ':
		result="Username: " + username + "\n\n" + mbti + "- The Counselor :-\nThey have a different, and usually more profound, way of\n looking at the world. They have a substance and depth in the way \n they think, never taking anything at surface level or accepting things the way they are.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'INTJ':
		result="Username: " + username + "\n\n" + mbti + "- The Mastermind :-\nThey are usually self-sufficient and would rather work \n alone than in a group. Socializing drains an introvert’s energy, \n causing them to need to recharge.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ISTP':
		result="Username: " + username + "\n\n" + mbti + "- The Craftsman :-\nThey are mysterious people who are usually very rational\n and logical, but also quite spontaneous and enthusiastic. Their \n personality traits are less easily recognizable than those of other \n types, and even people who know them well can’t always anticipate \n their reactions. Deep down, ISTPs are spontaneous, unpredictable individuals,\n but they hide those traits from the outside world, often very successfully.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ESFJ':
		result="Username: " + username + "\n\n" + mbti + "- The Provider :-\nThey are social butterflies, and their need to interact\n with others and make people happy usually ends up making them popular.\n The ESFJ usually tends to be the cheerleader or sports hero in high school\n and college. Later on in life, they continue to revel in the \n spotlight, and are primarily focused on organizing social events for their families,\n friends and communities.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'INFP':
		result="Username: " + username + "\n\n" + mbti + "- The Idealist :-\nThey prefer not to talk about themselves, especially in \n the first encounter with a new person. They like spending time alone in \n quiet places where they can make sense of what is happening around them. \n They love analyzing signs and symbols, and consider them to be \n metaphors that have deeper meanings related to life.\n\n"
		tab2_display.insert(tk.END,result)

	elif mbti == 'ESFP':
		result="Username: " + username + "\n\n" + mbti + "- The Performer :-\nThey have an Extraverted, Observant, Feeling and Perceiving \n personality, and are commonly seen as Entertainers. Born to be in \n front of others and to capture the stage, ESFPs love the spotlight. ESFPs \n are thoughtful explorers who love learning and sharing what they \n learn with others. ESFPs are “people people” with strong interpersonal skills.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ENFP':
		result="Username: " + username + "\n\n" + mbti + "- The Champion :-\nThey have an Extraverted, Intuitive, Feeling and Perceiving \n personality. This personality type is highly individualistic and \n Champions strive toward creating their own methods, looks, actions, habits, \n and ideas — they do not like cookie cutter people and hate when they \n are forced to live inside a box.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ESTP':
		result="Username: " + username + "\n\n" + mbti + "- The Doer :-\nThey have an Extraverted, Sensing, Thinking, and Perceptive\n personality. ESTPs are governed by the need for social interaction,\n feelings and emotions, logical processes and reasoning, along with a need \n for freedom.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ESTJ':
		result="Username: " + username + "\n\n" + mbti + "- The Supervisor :-\nThey are organized, honest, dedicated, dignified, traditional,\n and are great believers of doing what they believe is right and \n socially acceptable. Though the paths towards “good” and “right” are difficult,\n they are glad to take their place as the leaders of the pack. \n They are the epitome of good citizenry.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ENTJ':
		result="Username: " + username + "\n\n" + mbti + "- The Commander :-\nTheir secondary mode of operation is internal, where intuition \n and reasoning take effect. ENTJs are natural born leaders among \n the 16 personality types and like being in charge. They live in a world of \n possibilities and they often see challenges and obstacles as great \n opportunities to push themselves.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'INTP':
		result="Username: " + username + "\n\n" + mbti + "- The Thinker :-\nThey are well known for their brilliant theories and unrelenting\n logic, which makes sense since they are arguably the most logical \n minded of all the personality types. They love patterns, have a keen eye \n for picking up on discrepancies, and a good ability to read people, \n making it a bad idea to lie to an INTP.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ISFJ':
		result="Username: " + username + "\n\n" + mbti + "- The Nurturer :-\nThey are philanthropists and they are always ready to give back \n and return generosity with even more generosity. The people \n and things they believe in will be upheld and supported with enthusiasm\n  and unselfishness.\n\n"
		tab2_display.insert(tk.END,result)
	
	elif mbti == 'ENTP':
		result="Username: " + username + "\n\n" + mbti + "- The Visionary :-\nThose with the ENTP personality are some of the rarest in the world,\n  which is completely understandable. Although they are \n extroverts, they don’t enjoy small talk and may not thrive in many social \n situations, especially those that involve people who are too different\n from the ENTP. ENTPs are intelligent and knowledgeable need to \n be constantly mentally stimulated.\n\n"
		tab2_display.insert(tk.END,result)
	
	else :
		result="Username: " + username + "\n\n" + mbti + "- The Composer :-\nThey are introverts that do not seem like introverts. It is \n because even if they have difficulties connecting to other people\n at first, they become warm, approachable, and friendly eventually. They \n are fun to be with and very spontaneous, which makes them the perfect \n friend to tag along in whatever activity, regardless if planned \n or unplanned. ISFPs want to live their life to the fullest and embrace the\n present, so they make sure they are always out to explore new things and \n discover new experiences.\n\n"
		tab2_display.insert(tk.END,result)
	

def clear_username():
	e1.delete('1.0',END)

def clear_personality():
	tab2_display.delete('1.0',END)

def twt_save():
	raw_text = str(tab2_display.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	file_name = 'CandidatePersonality_'+ timestr + '.txt'
	with open(file_name, 'w') as f:
		f.write(final_text)
	result = '\nName of file: {}.'.format(file_name)
	tab2_display.insert(tk.END,result)



######
# Functions for candidate information tab
def get_summary():
	raw_text = str(entry.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSummary:{}'.format(final_text)
	tab3_display.insert(tk.END,result)

def clear_text():
	entry.delete('1.0',END)

def clear_display_result():
	tab3_display.delete('1.0',END)

def save_summary():
	raw_text = str(entry.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	file_name = 'CandidateInfo_'+ timestr + '.txt'
	with open(file_name, 'w') as f:
		f.write(final_text)
	result = '\nName of file: {}'.format(file_name)
	tab3_display.insert(tk.END,result)

#####
#Functions for candidate file tab
def openfiles():
	file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
	read_text = open(file1).read()
	displayed_file.insert(tk.END,read_text)

# for reset button
def clear_text_file():
	displayed_file.delete('1.0',END)

# Clear Result of Functions
def clear_text_result():
	tab4_display_text.delete('1.0',END)

def get_file_summary():
	raw_text = displayed_file.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab4_display_text.insert(tk.END,result)

#####
#Functions for Candidate URL TAB
def clear_url_entry():
	url_entry.delete(0,END)

def clear_url_display():
	tab5_display_text.delete('1.0',END)

# Fetch Text From Url
def get_text():
	raw_text = str(url_entry.get())
	page = urlopen(raw_text)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	url_display.insert(tk.END,fetched_text)

def get_url_summary():
	raw_text = url_display.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab5_display_text.insert(tk.END,result)	

#####
# COMPARER FUNCTIONS
def clear_compare_text():
	entry1.delete('1.0',END)

def clear_compare_display_result():
	tab6_display.delete('1.0',END)

def use_spacy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSpacy Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)

def use_nltk():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = nltk_summarizer(raw_text)
	print(final_text)
	result = '\nNLTK Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)

def use_gensim():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = summarize(raw_text)
	print(final_text)
	result = '\nGensim Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)

def use_sumy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = sumy_summary(raw_text)
	print(final_text)
	result = '\nSumy Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)
		

# Home tab
about_label = Label(tab1,text="Our Project:\n\nCandidate Profiler\n\nIn a fast paced world like today’s, where the competition for jobs is on the rise, \nit becomes a challenge to judge a candidate quickly. \nIn order to fit in a company’s atmosphere and be able to work with other employees, \nit is crucial to determine what type of personality a candidate possesses. \nSince it is easy for a candidate to showcase only the \n“good” aspects of their personality during an interview, \nit is not the best judgement. \nTherefore, in order to combat this problem, \nwe have developed a personality assessment tool that determines a personality based on \npsychiatric analysis of the candidate’s tweets. \nOur project also aims to summarise the vast amounts of \nclient data available on the internet \nin order to make the recruiter’s job easier. \nThis helps us automate and identify the ideal candidate for a particular job.",pady=5,padx=5)
about_label.grid(column=1,row=1, pady=5)
about_label = Label(tab1,text="Made By:\n1. Ritika Kayal - 18BCE2518\n2. Sidharth Patil - 18BCB0149",pady=5,padx=5)
about_label.grid(column=1,row=2, pady=5)

#BUTTONS
b0=Button(tab1,text="Close", width=12,command=window.destroy)
b0.grid(row=4,column=1,padx=10,pady=10)


#####
#Personality tab
l1=Label(tab2,text="Enter Twitter Username")
l1.grid(row=3,column=0)

l2=Label(tab2,text="Type of Personality")
l2.grid(row=5,column=1)

e1=Text(tab2,height=1, width=40)
e1.grid(row=3,column=1)

#BUTTONS
button1=Button(tab2,text="Submit",command=exec_twt, width=12)
button1.grid(row=3,column=2,padx=10,pady=10)

button2=Button(tab2,text="Reset Username",command=clear_username, width=12)
button2.grid(row=4,column=0,padx=10,pady=10)

button3=Button(tab2,text="Clear",command=clear_personality, width=12)
button3.grid(row=4,column=1,padx=10,pady=10)

button4=Button(tab2,text="Save",command=twt_save, width=12)
button4.grid(row=4,column=2,padx=10,pady=10)

# Display Screen For Personality
tab2_display = ScrolledText(tab2,height=20)
tab2_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


# Candidate Information Tab
l1=Label(tab3,text="Enter Text To Summarize")
l1.grid(row=2,column=1)

entry=ScrolledText(tab3,height=10)
entry.grid(row=3,column=0,columnspan=3,padx=5,pady=5)

# BUTTONS
button1=Button(tab3,text="Reset",command=clear_text, width=12)
button1.grid(row=5,column=0,padx=10,pady=10)

button2=Button(tab3,text="Summarize",command=get_summary, width=12)
button2.grid(row=5,column=1,padx=10,pady=10)

button3=Button(tab3,text="Clear Result", command=clear_display_result, width=12)
button3.grid(row=5,column=2,padx=10,pady=10)

button4=Button(tab3,text="Save", command=save_summary, width=12)
button4.grid(row=6,column=1,padx=10,pady=10)

# Display Screen For Result
tab3_display = ScrolledText(tab3, height=10)
tab3_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


#Candidate file processing tab
l1=Label(tab4,text="Open File To Summarize")
l1.grid(row=1,column=1)

displayed_file = ScrolledText(tab4,height=10)
displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=5)

# BUTTONS FOR SECOND TAB/FILE READING TAB
b0=Button(tab4,text="Open File", width=12, command=openfiles)
b0.grid(row=4,column=0,padx=10,pady=10)

b1=Button(tab4,text="Reset", width=12,command=clear_text_file)
b1.grid(row=4,column=1,padx=10,pady=10)

b2=Button(tab4,text="Summarize", width=12,command=get_file_summary)
b2.grid(row=5,column=1,padx=10,pady=10)

b3=Button(tab4,text="Clear Result", width=12,command=clear_text_result)
b3.grid(row=4,column=2,padx=10,pady=10)

# Display Screen
tab4_display_text = ScrolledText(tab4,height=10)
tab4_display_text.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

# Allows you to edit
tab4_display_text.config(state=NORMAL)


# Candidate URL TAB
l1=Label(tab5,text="Enter URL To Summarize")
l1.grid(row=1,column=0)

raw_entry=StringVar()
url_entry=Entry(tab5,textvariable=raw_entry,width=30)
url_entry.grid(row=1,column=1)

# BUTTONS
button1=Button(tab5,text="Reset",command=clear_url_entry, width=12,bg='#03A9F4')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab5,text="Get Text",command=get_text, width=12,bg='#03A9F4')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab5,text="Clear Result", command=clear_url_display,width=12,bg='#03A9F4')
button3.grid(row=4,column=2,padx=10,pady=10)

button4=Button(tab5,text="Summarize",command=get_url_summary, width=12,bg='#03A9F4')
button4.grid(row=5,column=1,padx=10,pady=10)

# Display Screen For Result
url_display = ScrolledText(tab5,height=10)
url_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


tab5_display_text = ScrolledText(tab5,height=10)
tab5_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)


# Alternate algorithms tab
l1=Label(tab6,text="Enter Text To Summarize")
l1.grid(row=1,column=1)

entry1=ScrolledText(tab6,height=10)
entry1.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

# BUTTONS
button1=Button(tab6,text="Reset",command=clear_compare_text, width=12,bg='#03A9F4')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab6,text="SpaCy",command=use_spacy, width=12,bg='red')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab6,text="Clear Result", command=clear_compare_display_result,width=12,bg='#03A9F4')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab6,text="NLTK",command=use_nltk, width=12,bg='#03A9F4')
button4.grid(row=4,column=2,padx=10,pady=10)

button4=Button(tab6,text="Gensim",command=use_gensim, width=12,bg='#03A9F4')
button4.grid(row=5,column=1,padx=10,pady=10)

button4=Button(tab6,text="Sumy",command=use_sumy, width=12,bg='#03A9F4')
button4.grid(row=5,column=2,padx=10,pady=10)


# Display Screen For Result
tab6_display = ScrolledText(tab6,height=10)
tab6_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


window.mainloop()