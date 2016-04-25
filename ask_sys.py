import nltk


questions = []

#TAG
nn_tag = ["NN", "NNS", "NNP", "NNPS"]
vb_tag = ["VB", "VBD", "VBP", "VBZ"]
in_tag = ["IN"]

#SIGNAL
be_signal = ["is", "am", "are", "was", "were"]


def process(sentence):
	tokens = nltk.word_tokenize(sentence)
	pos_tags = nltk.pos_tag(tokens)

	verb_index = -1
	verb_tag = ""

	for i, (word, tag) in enumerate(pos_tags):
		if tag in vb_tag:
			verb_index = i
			if tag in be_signal:
				be_transform(tokens, i)
			else:
				verb_transform(tokens, i, tag)
		elif tag in in_tag and verb_index != -1:
			continue
			#in_transform(tokens, i, verb_index, verb_tag)


def be_transform(tokens, index):
	question_tokens1 = tokens[index] + tokens[:index] + tokens[index+1:] 
	question1 = " ".join(question_tokens1)
	question1 += " ?"
	quesionts.append(question1)

	question_tokens2 = tokens[index] + tokens[:index]
	question2 = " ".join(question_tokens2)
	question2 = "What " + question2
	quesionts.append(question2)


def stem(word_token):

	return word_token

def verb_transform(tokens, index, tag):

	question_tokens = tokens[:index] + [stem(tokens[index])] + tokens[index+1:]
	question = " ".join(question_tokens)
	question += " ?"

	if tag == "VB":
		question = "Do " + question
	elif tag == "VBD":
		question = "Did " + question
	elif tag == "VBZ":
		question = "Does " + question
	else:
		print(question)

	questions.append(question)

#def in_transform(tokens, in_index, verb_index, verb_tag):

	#if verb_tag in vb_tag:
		#question_tokens += tokens[verb_index]


def init(sentences):
	global questions

	for sentence in sentences:
		process(sentence)

	return questions