def calculate_frequency(input_file, patterns, encoding_type=None, output_file=None):
	"""calculate_frequency(input_file, patterns, encoding_type, output_file):

	   Return dictionary that contains tokens frequency distribution in given file
	   matching given pattern(s).

	   input_file    ... plain text file encoded according to 'encoding_type' parameter	   
	   patterns      ... list of string patterns to look for
	   encoding_type ... character encoding	('utf-8' if not specified)   
	   output_file   ... name of a file to write the output to ('output.txt' by default)

	"""
	if encoding_type == None: # default encoding
		encoding_type = "utf-8"
	
	if output_file == None: # default output file name
		output_file = "output.txt"

	try:#better safe than sorry
		with open(input_file, encoding=encoding_type) as file:
			lines = file.readlines() # read lines from file to list
	except FileNotFoundError:
		print("File not accessible")

	result = {} # initialize dictionary to store frequency counts

	for line in lines: # process input line by line
		token = '' # initialize token object
		for char in line: # iterate over all characters in line
			if char != ' ' and char != '\n': # tokens are set of characters separated by white-spaces or newlines
				token += char # add character to the token
			else:
				if len(token) != 0: # if token,
					for string in patterns: # check string patterns
						if string in token: # if match,
							if not token in result:
								result[token] = 1 # if new match, count equals one
							else:
								result[token] += 1 # else, increment match count
							break # no need to continue; avoid duplicity
					token = '' # empty token object
	
	if result: # if not empty
		with open(output_file, "a") as file:
			for key in sorted(result):
				file.write(f"{key} {result[key]}\n")
			file.write(f"{'-'*10}\n")

	return result

def test_function():
	print("Testing ... ", calculate_frequency.__doc__)
	# Tesctcase #1 (regular case)
	test_dictionary = {
	"awe":    1,
	"pa,":     1,
	"pat":    2,
	"pawes.": 1,
	"we" :    2
	}

	output_dictionary = calculate_frequency('test.txt', ['pa', 'we'])
	
	print("\nTestcase #1 (regular case)", end=' ')
	for key in test_dictionary:
		if not key in output_dictionary or \
		test_dictionary[key] != output_dictionary[key]:
			print("Fail")
			return
	print("OK")

	print("\nTokens frequency distribution: ")
	for key in sorted(output_dictionary): # print results
		print(f"{key:>10}: {output_dictionary[key]}")

	# Tesctcase #2 (empty input_file)
	output_dictionary = calculate_frequency('test2.txt', ['pa', 'we'])
	
	print("\nTestcase #2 (empty input_file)", end=' ')
	if len(output_dictionary) == 0:
		print("OK")
	else:
		print("Fail")

	# Tesctcase #3 (nonexisting string pattern)
	output_dictionary = calculate_frequency('test.txt', ['nesmysl'])
	
	print("\nTestcase #3 (nonexisting string pattern)", end=' ')
	if len(output_dictionary) == 0:
		print("OK")
	else:
		print("Fail")

if __name__ == '__main__':
	test_function()

# Bonus: linux shell solution
# cat test.txt | tr ' ' '\n' | awk '/pa|we/' | sort | uniq -c > output.txt