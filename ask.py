import sys
import tag1
import preprocess

def main(argv):


	file_path = argv[1]
	num_questions = argv[2]

	extract_sentences = preprocess.parse_txt(file_path)


	questions = tag1.main(extract_sentences, num_questions)
 


if __name__ == '__main__':
	main(sys.argv)