def calculate_frequency(input_file, patterns, encoding_type=None, output_file=None):
	"""calculate_frequency(input_file, patterns, encoding_type, output_file):

	   Return dictionary that contains tokens frequency distribution in given file
	   matching given pattern(s) or -1 otherwise.

	   input_file    ... plain text file encoded according to 'encoding_type' attribute	   
	   patterns      ... list of string patterns to look for, e.g. [pattern1, pattern2, ...]
	   encoding_type ... character encoding	('utf-8' if not specified)   
	   output_file   ... name of a file to write the output to ('output.txt' by default)

	"""
	if encoding_type == None: # default encoding
		encoding_type = "utf-8"
	
	if output_file == None: # default output file name
		output_file = "output.txt"

	try: # better safe than sorry
		with open(input_file, encoding=encoding_type) as file:
			lines = file.readlines() # read all lines from file to list
	except FileNotFoundError:
		print("File not accessible")

	counters = {} # initialize dictionary to store frequency counters

	for line in lines: # go line by line
		token = '' # initialize token object
		for char in line: # go character by character in line
			if char != ' ' and char != '\n': # tokens are set of characters separated by white-spaces or newlines
				token += char # add character to token
			else: # end of token
				if len(token) != 0: # if token,
					for pattern in patterns: # go pattern by pattern in patterns
						if pattern in token: # if match,
							if not token in counters:
								counters[token] = 1 # if new match, counter equals one
							else:
								counters[token] += 1 # else, increment match counter
							break # no need to continue; avoid duplicity
					token = '' # empty token object for next entry
	
	if counters: # if not empty
		with open(output_file, "a") as file:
			for token in sorted(counters): # save token counters to file
				file.write(f"{token} {counters[token]}\n")
			file.write(f"{'-'*10}\n")

	return counters if counters else -1

def test_function():
	print("Testing ... ", calculate_frequency.__doc__)
	
	# Tesctcase #1 (regular case)
	test_token_counters = {
	"awe":    1,
	"pa,":    1,
	"pat":    2,
	"pawes.": 1,
	"we" :    2
	}

	token_counters = calculate_frequency('test.txt', ['pa', 'we'])
	
	print("\nTestcase #1 (regular case)", end=' ')
	for token in test_token_counters:
		if not token in token_counters or \
		test_token_counters[token] != token_counters[token]:
			print("Fail")
			return
	print("OK")

	print("\nTokens frequency distribution: ")
	for token in sorted(token_counters): # print results
		print(f"{token:>10}: {token_counters[token]}")

	# Tesctcase #2 (empty input_file)
	token_counters = calculate_frequency('test2.txt', ['pa', 'we'])
	
	print("\nTestcase #2 (empty input_file)", end=' ')
	print("OK") if token_counters == -1 else print("Fail")

	# Tesctcase #3 (nonexisting pattern)
	token_counters = calculate_frequency('test.txt', ['nesmysl'])
	
	print("\nTestcase #3 (nonexisting pattern)", end=' ')
	print("OK") if token_counters == -1 else print("Fail")

if __name__ == '__main__':
	test_function()

# Bonus: linux shell solution
# cat test.txt | tr ' ' '\n' | awk '/pa|we/' | sort | uniq -c > output.txt