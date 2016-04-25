#pipeline.py
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('/Users/tia/stanford-ner-2015-12-09/classifiers/english.conll.4class.distsim.crf.ser.gz','/Users/tia/stanford-ner-2015-12-09/stanford-ner-3.6.0.jar') 


from nltk.parse.stanford import StanfordParser
from nltk.internals import find_jars_within_path


parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


stanford_dir = parser._classpath[0].rpartition('/')[0]
parser._classpath = tuple(find_jars_within_path(stanford_dir))

stanford_dir1 = st._stanford_jar.rpartition('/')[0]
stanford_jars = find_jars_within_path(stanford_dir1)
st._stanford_jar = ':'.join(stanford_jars)

from nltk.tree import *
from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()