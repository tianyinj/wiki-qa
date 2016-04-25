import os
from nltk.parse.stanford import StanfordParser
from nltk.tag import StanfordNERTagger
stanford_path = '/var/nlp/spring16/libs/stanford-corenlp-full-2015-12-09'
parser = StanfordParser(os.path.join(stanford_path, "stanford-corenlp-3.6.0.jar"), os.path.join(stanford_path, "stanford-corenlp-3.6.0-models.jar"))
st = StanfordNERTagger('/var/nlp/spring16/teams/Catsman/classifiers/english.muc.7class.distsim.crf.ser.gz', os.path.join(stanford_path, "stanford-corenlp-3.6.0.jar"))