import os, nltk
from nltk.corpus import stopwords

def list_folder(PATH,suffix=''):
	result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) \
		for f in filenames if os.path.splitext(f)[1] == suffix]
	return result

def tagging(document):
	if document.strip() is "":
		return []
	sentences = nltk.sent_tokenize(document) 
	sentences = [nltk.word_tokenize(sent) for sent in sentences] 
	sentences = [nltk.pos_tag(sent) for sent in sentences] 
	return sentences
	
def chunk_sentence(sentence):
	grammar = r"""
	  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
		  {<NNP>+}				  # chunk sequences of proper nouns
	"""
	cp = nltk.RegexpParser(grammar)
	chunked = cp.parse(sentence)
	return chunked

def extract_phrase(chunked):
	"""
	get the phrase list of a sentence
	"""
	phrases = []
	for subtree in chunked.subtrees(filter = lambda t:t.label() == "NP"):
		phrase = []
		for node in subtree:
			phrase.append(node[0].lower())
		if phrase:
			phrases.append(" ".join(phrase))
	return phrases

if __name__ == "__main__":

	# param-1
	INPUT_FOLDER = "goals"

	STOP = stopwords.words("english")

	files = list_folder(INPUT_FOLDER,".txt")
	for fp in files:
		with open(fp,"r") as f:
			text_body = f.read()

		all_phrases = []
		# chunk text body
		sentences = tagging(text_body)
		for sentence in sentences:
			chunked = chunk_sentence(sentence)
			# draw the figure
			phrases = extract_phrase(chunked)
			all_phrases += phrases
		effect_phrase = []
		for phrase in list(set(all_phrases)):
			print(phrase)
			if len(phrase) > 1:
				if phrase not in STOP:
					effect_phrase.append(phrase)
		with open(fp + "keyword.txt", "w") as fw:
			fw.write("\n".join(effect_phrase))
