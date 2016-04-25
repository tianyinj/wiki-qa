from bs4 import BeautifulSoup
import nltk
import re
from nltk.tokenize import sent_tokenize


# -*- coding: utf-8 -*-
 
import sys  
import os

reload(sys)
sys.setdefaultencoding('utf-8')


def parse_txt(filename):
	sent_detector = nltk.data.load(filename)
	sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', sent_detector)
	return sentences
