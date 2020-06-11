import pandas as pd
import operator,re

if __name__ == "__main__":

	# param-1 dictionary file
	dictionary_file = "Goal 1--End poverty in all its forms everywhere.txtphrase.txt"
	# param-2 all the input data
	PATH = "goal1.csv"
	# param-3 output file
	OUTPUT = "goal1.keyword.txt"
	with open(dictionary_file,"r") as f:
		keywords = f.readlines()

	keywords = {k.strip():0 for k in keywords}

	df = pd.read_csv(PATH,usecols=[0,1,2,3,4])
	df.fillna("", inplace = True)

	goal1 = []
	for i in range(df.shape[0]):
		text_id = df.ix[i][0]
		text_url = df.ix[i][1]
		text_tag = df.ix[i][2]
		text_title = df.ix[i][3]
		text_body = df.ix[i][4]

		text = "%s \n %s" % (text_title.strip(), text_body.strip())

		for w in keywords.keys():
			freq = re.findall(r"(?i)\b%s\b" % w, text)
			if freq:
				keywords[w] += len(freq)

	sorted_x = sorted(keywords.items(), key = operator.itemgetter(1), reverse = True)
	print_list = ["%s\t%s" % (k,v)for k,v in sorted_x]

	with open(OUTPUT,"w") as f:
		f.write("\n".join(print_list))