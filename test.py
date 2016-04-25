import nltk
from nltk.tokenize import MWETokenizer
from nltk.parse import stanford
import re
import os
import string
import gettext


cwd = os.getcwd()

os.environ['CLASSPATH'] = cwd + '/stanford/'
os.environ['STANFORD_MODELS'] = cwd + '/stanford/'

# print os.environ["CLASSPATH"]
# print os.getcwd()

def tokenizeSentences(text):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = sent_detector.tokenize(text.strip())
	return sentences

def tokenizeWords(sentence):
	tokens = nltk.word_tokenize(sentence)
	tokens = nltk.pos_tag(tokens)
	return tokens

def neTag(tokens):
	neTagged = nltk.ne_chunk(tokens)
	return neTagged

def parseSentence(sentence):
	parser = stanford.StanfordParser(model_path=cwd + "/stanford/englishPCFG.ser.gz")
	result = parser.raw_parse_sents((sentence,))
	for line in result:
		for res in line:
			return res

def tagSentence(sentence):
	tokens = tokenizeWords(sentence)
	neTagged = neTag(tokens)
	return neTagged

def getText(filename):
	f = open(filename)
	htmlText = f.read()
	htmlParser = gettext.MyHTMLParser()
	htmlParser.feed(htmlText)
	textdict = htmlParser.d
	# neDict = dict()
	# parseDict = dict()
	# print textdict
	for key in textdict:
		# if key == '': continue
	# 	neDict[key] = []
	# 	parseDict[key] = []
		text = textdict[key]
		sentences = tokenizeSentences(text)
		textdict[key] = sentences
	# 	# for sentence in sentences:
	# 	# 	tokens = tokenizeWords(sentence)
	# 	# 	# print tokens
	# 	# 	neTagged = neTag(tokens)
	# 	# 	neDict[key].append(neTagged)
			
	# 	for sentence in sentences:
	# 		parser = stanford.StanfordParser(model_path=cwd + "/stanford/englishPCFG.ser.gz")
	# 		result = parser.raw_parse_sents((sentence,))
	# 		for line in result:
	# 			for res in line:
	# 				print res
	# 				parseDict[key].append(res)
	return textdict

text = getText('a1.html')

sentences = text[(u'Clint Dempsey', u'Club career', u'Seattle Sounders FC')]
print(sentences)
sentence = sentences[0]
#parseSentence(sentence).draw()
#tagSentence(sentence).draw()
# sentence = text[]