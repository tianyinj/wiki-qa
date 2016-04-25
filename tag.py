import os
from nltk.parse.stanford import StanfordParser
from nltk.tag import StanfordNERTagger
stanford_path = '/var/nlp/spring16/libs/stanford-corenlp-full-2015-12-09'
parser = StanfordParser(os.path.join(stanford_path, "stanford-corenlp-3.6.0.jar"), os.path.join(stanford_path, "stanford-corenlp-3.6.0-models.jar"))
st = StanfordNERTagger('/var/nlp/spring16/teams/Catsman/classifiers/english.muc.7class.distsim.crf.ser.gz', os.path.join(stanford_path, "stanford-corenlp-3.6.0.jar"))

from nltk.tree import *
from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()


#grammar.py

sent1_and_sent2 = "(S (S CC S .))"
vp1_and_vp2 = "(S (VP CC VP .))"
p1_comma_p2 = "(S ((NP (NP , NP ,)) VP .))"

be_signal = ["is", "am", "are", "was", "were", "may", "should", "can", "could", "would"]
decoration_adv = ["currently", "suddenly", "actually","basically","completely","constantly","largely","literally","seriously","totally","unusually"]
past_principle = ["hava", "has", "had"]

##Still need to implement
##Compound: semicolon, cc, quotes
##Complex : SBAR, 
#Coreference resolution? (maybe not)

##Implemented
##Complex : appositives

def is_single(tree):
	for child in tree:
		if child.label()[-1] == "S":
			return 0
	return 1

def get_apposition(tree):

	p1 = None
	p2 = None

	single = -1

	for child in tree:
		if child.label() == "NP" and p1 == None:
			p1 = child.leaves()
			single = is_single(child)
		elif child.label() == "NP" and not p1 == None:
			p2 = child.leaves()

	if p1 == None or p2 == None:
		return []
	#Tup;e of phrase list
	if single == 1:
		p1.append("is")
	else:
		p1.append("are")
	return [p1.append(p2)]

def get_subparts(tree):
	s1 = None
	s2 = None

	for child in range(len(tree)):
		if tree[child].label() == "VP" and s1 == None:
			s1 = tree[child].leaves()
		elif tree[child].label() == "VP" and not s1 == None:
			s2 = tree[child].leaves()

	return (s1, s2)


def is_apposition(tree):
	for child in tree:
		if child.label() == "VP":
			return []
		if child.label() == "NP" and len(child)>1:
			return get_apposition(child)
	return []

def is_compounding(tree):

	head = None


	for child in range(len(tree)):

		if tree[child].label() == "VP":
			(sent1, sent2) = get_subparts(tree[child])
			if not sent1 == None and not sent2 == None:
				break
		if tree[child].label() == "NP":
			head = tree[child].leaves()

	if head == None:
		return []
	if sent1 == None or sent2 == None:
		return []
	sent1 = head+sent1
	sent2 = head+sent2

	return [sent1, sent2]


def expandable(trees):
	matches = []

	#Only 1 full sentence
	tree = trees
	appostion_list = is_apposition(tree)
	compounding_list = is_compounding(tree)
	if not appostion_list == []:
		matches+=appostion_list
	elif not compounding_list == []:
		matches+=compounding_list
	return matches



def main(raw_sentences, n):
	result = []
	sent_list = []

	for sentence in raw_sentences:
		if len(sentence) < 5 :
			continue
		trees = list(parser.raw_parse(sentence))
		for tree in trees:
			exp = expandable(tree[0])
			if exp == [] or exp == [None]:
				sent_list.append((sentence, tree))
			else:
				for extra_sent in exp:
					new_sent = ' '.join(extra_sent)
					new_tree = list(parser.raw_parse(new_sent))
					sent_list.append((new_sent, new_tree[0]))

	## sentences in NP+VP. form
	for sent, tree in sent_list:
		tree = tree[0]
		if (len(tree) > 2):
			if tree[1].label() == "ADVP":
				result += " ".join(ask_how(tree))
		#The index of vp in sentence

		for vp_pos in range(len(tree)):
			if tree[vp_pos].label() == "VP":
				break
		if vp_pos == len(tree):
			break

		ner_tags = st.tag(sent.split())
		result.append(" ".join(ask_binary(copy.deepcopy(tree), vp_pos)))
		result += ask_wh(ner_tags, copy.deepcopy(tree))

		if (len(result) >= n):
			break


	#question is a string of plain question
	for question in result:
		print(str.capitalize(question) + "?")

	exit(0)

def have_tag(taggers, search):
	for (word, tag) in taggers:
		if tag == search:
			return True
	return False


def ask_wh(ner_tags, tree):

	result = []
	vp = tree[1]
	np = tree[0]

	question = []

	if len(vp) > 1 and vp[1].label() == "PP":
		if have_tag(ner_tags, "LOCATION"):
			question += ask_where(copy.deepcopy(tree), np, vp)
			result.append(" ".join(question))
		if have_tag(ner_tags, "TIME") or have_tag(ner_tags, "DATE"):
			question += ask_when(copy.deepcopy(tree), np, vp)
			result.append(" ".join(question))
		if vp[1].label() == "NP":
			question += ask_what(copy.deepcopy(tree))
			result.append(" ".join(question))
		if have_tag(ner_tags, "PERSON"):
			question += ask_who(copy.deepcopy(tree), 0)
			result.append(" ".join(question))
	
	return result


###############YES/NO QUESTION################
def ask_binary(tree, index):

	tokens = tree.leaves()
	[verb] = tree[1][0].leaves()

	if verb in be_signal:
		result = generate_binary_be(tree, verb)
	else:
		result = genertate_binary_do(tree, verb)

	return result


def generate_binary_be(tree, verb):
	return [verb] + tree[0].leaves() + tree[1][1].leaves()


def genertate_binary_do(tree, verb):
	result = []
	vp = 1
	np = 0

	for i in range(len(tree[vp])):
		[verb] = tree[1][0].leaves()
		if verb in past_principle:
			if i+1 < len(tree[vp]) and tree[vp][i+1][0].label() == "VBN":
				tree[vp].pop(0)
				result = [verb] + tree[np].leaves() + tree[vp].leaves()
				break

		elif tree[vp][i].label() == "VB" or tree[vp][i].label() == "VBP":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["do"] + tree[np].leaves() + [base] + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["did"] + tree[np].leaves() + [base] + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["does"] + tree[np].leaves() + [base] + tree[vp].leaves()
			break
	return result


###############WHAT QUESTION################

def ask_what(tree):

	tokens = tree.leaves()
	vp = tree[1]
	pos_tag = vp[0].label()

	if vp[0].leaves() in be_signal:
		return generate_be_what(tree, 1, 0)
	else:
		return generate_do_what(tree, 1, 0)

	
def generate_be_what(tree, vp, np):
	result = []
	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["what "+base] + tree[np].leaves() + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["what "+base] + tree[np].leaves() + [base] + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["what "+base] + tree[np].leaves() + [base] + tree[vp].leaves()
			break
	return result


def generate_do_what(tree, vp, np):
	result = []
	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["what do"] + tree[np].leaves() + [base]
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["what did"] + tree[np].leaves() + [base]
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["what does"] + tree[np].leaves() + [base]
			break
	return result



################WHO QUESTION#####################
def ask_who(tree, index):
	tokens = tree.leaves()
	np = tree[0]

	if vp[0].leaves() in be_signal:
		return generate_be_what(tree, 1, 0)
	else:
		return generate_do_what(tree, 1, 0)

	
def generate_be_who(tree, np, vp):
	result = []
	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["who "+base] + tree[np].leaves() + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["who "+base] + tree[np].leaves() + [base] + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["who "+base] + tree[np].leaves() + [base] + tree[vp].leaves()
			break
	return result


def generate_do_who(tree, np, vp):
	result = []
	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["who do"] + tree[np].leaves() + [base]
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["who did"] + tree[np].leaves() + [base]
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["who does"] + tree[np].leaves() + [base]
			break
	return result


def ask_whom(tree, index):
	tokens = tree.leaves()
	np = tree[0]

	result += generate_be_who(tree, 2, 1)
	result += generate_do_who(tree, 2, 1)

	
def generate_be_whom(tree, np, vp):
	result = []
	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["whom "+base] + tree[np].leaves() + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["whom "+base] + tree[np].leaves() + [base] + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["whom "+base] + tree[np].leaves() + [base] + tree[vp].leaves()
			break
	return result


def generate_do_whom(tree, np, vp):
	result = []

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["whom do"] + tree[np].leaves() + [base]
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["whom did"] + tree[np].leaves() + [base]
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["whom does"] + tree[np].leaves() + [base]
			break
	return result

################WHERE QUESTION#####################

def ask_where(tree, index, ner_tags):

	tokens = tree.leaves()
	vp = tree[1]
	pos_tag = vp[0].label()

	if vp[0].leaves() in be_signal:
		return generate_be_where(tree, 0, 1, 2)
	else:

		return generate_do_where(tree, 0, 1, 2)

	
def generate_be_where(tree, np, vp, pp_pos):
	result = []
	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "PP":
			tree[vp].pop(i)

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["where "+verb] + tree[np].leaves() + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["where "+verb] + tree[np].leaves() + [base] + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["where "+verb] + tree[np].leaves() + [base] + tree[vp].leaves()
			break
	return result


def generate_do_where(tree, np, vp, pp_pos):
	result = []

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "PP":
			tree[vp].pop(i)

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["where do"] + tree[np].leaves() + [base]

		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["where did"] + tree[np].leaves() + [base]

		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["where does"] + tree[np].leaves() + [base]

	
	return result

################WHEN QUESTION#####################
def ask_when(tree, index, ner_tags):
	tokens = tree.leaves()
	vp = tree[1]
	pos_tag = vp[0].label()

	if vp[0].leaves() in be_signal:
		return generate_be_where(tree, 0, 1, 2)
	else:

		return generate_do_where(tree, 0, 1, 2)

	
def generate_be_when(tree, np, vp, pp_pos):
	result = []

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "PP":
			tree[vp].pop(i)

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["when "+verb] + tree[np].leaves() + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["when "+verb] + tree[np].leaves() + [base] + tree[vp].leaves()
			break;
		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["when "+verb] + tree[np].leaves() + [base] + tree[vp].leaves()
			break
	return result


def generate_do_when(tree, np, vp, pp_pos):
	result = []

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "PP":
			tree[vp].pop(i)

	for i in range(len(tree[vp])):
		if tree[vp][i].label() == "VB":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["when do"] + tree[np].leaves() + [base]

		elif tree[vp][i].label() == "VBD":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["when did"] + tree[np].leaves() + [base]

		elif tree[vp][i].label() == "VBZ":
			[verb] = tree[vp].pop(i).leaves()
			base = wordnet_lemmatizer.lemmatize(verb, "v")
			result = ["when does"] + tree[np].leaves() + [base]

	
	return result+tree[vp].leaves()

################HOW QUESTION#####################

def ask_how(tree):
	tokens = tree.leaves()
	np = tree[0]
	vp = tree[2]
	adv = tree[1]

	pos_tag = vp.label()

	if adv in decoration_adv:
		return

	result += generate_do_how(tokens, len(np)+len(adv), pos_tag)


def generate_do_how(tokens, index, pos_tag):
	verb = tokens[index] 
	base = wordnet_lemmatizer.lemmatize(verb, "v")
	if pos_tag == "VB":
		return "how do " + " ".join(tokens[:index]) + " " + base
	elif pos_tag == "VBD":
		return "how did " + " ".join(tokens[:index]) + " " + base
	elif pos_tag == "VBP":
		return "how does " + " ".join(tokens[:index]) + " "+ base


################WHY QUESTION#####################
raw1 = "Ants are social insects of the family Formicidae, and along with the related wasps and bees, they belong to the order Hymenoptera. Ants evolved from wasp-like ancestors in the mid-Cretaceous period between 110 and 130 million years ago and diversified after the rise of flowering plants. Today, more than 12,500 species are classified with upper estimates of about 22,000 species. They are easily identified by their elbowed antennae and a distinctive node-like structure that forms a slender waist."



