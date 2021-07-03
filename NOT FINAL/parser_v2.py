'''
parser_v2.py is the 2nd version of parser.py.
both were meant to be able to parse code from 
a text file, but i scraped parser.py because 
it was starting to get clunky and there was no
structure.

the reason that parser_v2 is different is because
it is able to parse text that looks like regular
speech. look at code_v2.txt for an example.

the only possible code that the parser is able to 
parse are the following:

{'increase':'var change',
'decrease':'var change',
'contains':'list set',
'append': 'list append',
'remove': 'list remove',
'pop': 'list pop',
'delete': 'delete'}

the keys represent the keywords needed to call
the functions, which are the values.
however, there are sub-keywords that are needed
to work, so i would try to copy the sentence 
structure from the txt file for this parser 
to work.



'''

def read(filename):
	with open(filename + '.txt', 'r') as f:
		return f.read()

def checkForKeywords(line, keywords):
	for word in keywords:
		if word in line:
			return True

	return False

def puncutation(lines):

	if type(lines) == str:
		if lines.isalpha():
			puncutated_lines =  '"' + lines + '"'
		else:
			puncutated_lines = lines
	elif type(lines) == list:
		puncutated_lines = []
		for line in lines:
			if lines.isalpha():
				puncutated_lines.append('"' + lines + '"')
			else:
				puncutated_lines = lines
	return puncutated_lines

def replaceList(line, replacements):
	for mod in replacements:
		line = line.replace(mod[0],mod[1])

	return line
def parseLine(line, type_):
	if type_ == 'delete':

		# parse info out
		mod_list = [('delete ','')]
		mod_line = replaceList(line, mod_list)
		
		# format data structure name
		name = mod_line.replace(' ','_')

		# create mod line
		mod_line = 'del ' + name
	elif type_ == 'var change':
		if 'increase' in line:
			symbol = ' += '
		else:
			symbol = ' -= '

		# parse info out
		mod_list = [('increase ',''),('decrease ','')]
		mod_line = replaceList(line, mod_list)
		
		# split var name, mod_amt
		mod_line = tuple(mod_line.split(' by '))

		# replace (' ','_')
		var, mod_amt = mod_line
		var = var.replace(' ','_')

		# create mod_line
		mod_line = var + symbol + mod_amt

	elif type_ == 'list remove':

		# parse info out
		mod_list = [('remove ','')]
		mod_line = replaceList(line, mod_list)

		# split new_value, list_name
		mod_line = mod_line.split(' from ')
		new_value, list_name = tuple(mod_line)

		# format list_name
		list_name = list_name.replace(' ','_')

		# add puncutation around the string
		new_value = puncutation(new_value)

		# add the remove code to new value`
		new_value = f'.remove({new_value})'

		# create mod_line
		mod_line = list_name + new_value
	elif type_ == 'list pop':

		# parse info out
		mod_list = [('pop #','')]
		mod_line = replaceList(line, mod_list)

		# split pop index, list_name
		mod_line = mod_line.split(' from ')
		pop_i, list_name = tuple(mod_line)

		# format list_name
		list_name = list_name.replace(' ','_')

		# create mod_line
		mod_line = list_name + f'.pop({pop_i})'

	elif type_ == 'list append':

		# parse info out
		mod_list = [('append ','')]
		mod_line = replaceList(line, mod_list)

		# split new_value, list_name
		mod_line = mod_line.split(' to ')
		new_value, list_name = tuple(mod_line)

		# format list_name
		list_name = list_name.replace(' ','_')

		# add puncutation around the string
		new_value = puncutation(new_value)

		# add the append code to new value`
		new_value = f'.append({new_value})'

		# create mod_line
		mod_line = list_name + new_value

	elif type_ == 'list set':

		# parse info out
		mod_list = [('and ','')]
		mod_line = replaceList(line, mod_list)

		# split list_name, list_values
		mod_line = mod_line.split(' contains ')
		list_name, list_v = tuple(mod_line)

		# format list_name
		list_name = list_name.replace(' ','_')

		# split list values
		list_v = list_v.split(',')
		# put puncutation around 
		for i, v in enumerate(list_v):
			'''we need to enumerate the list
			because we need to reference the
			index if we are to add it back to
			the list'''

			'''take away the extra space that
			is there to look cool'''
			v = v.strip()

			'''use the puncutation function to
			return a form of the string with
			the '"' around it'''
			v = puncutation(v)

			'''add back the extra space that was
			taken away'''
			v = ' ' + v if i != 0 else v

			# add the value back to the list
			list_v[i] = v

		''' change list_v back to a string
		so that the concatenation that we'll 
		have to do next will work (can't
		concatenate str with list) '''
		list_v_copy, list_v = list_v, ''
		for i, v in enumerate(list_v_copy):
			if i != len(list_v_copy) - 1:
				list_v = list_v + v + ', '
			else:
				list_v = list_v + v

		# add the list brackets
		list_v = '[' + list_v + ']'

		# create mod_line
		mod_line = list_name + ' = ' + list_v

	elif type_ == 'var set':

		# split variable name and variable value
		line = line.split(' is ')

		# replace var name " " with "_"
		name = line[0].replace(' ','_')

		# format value (v)
		v = puncutation(line[1])
		# create parsed code
		mod_line = name + ' = ' + v

	elif type_ == 'print':

		# split keyword with variable
		line = line.replace("repeat to me ", "")

		# create parsed code
		mod_line = 'print("""' + line + '""")'

	elif type_ == 'print var':

		# split keyword with variable
		line = line.replace("what is ", "")

		# create parsed code
		mod_line = 'print(' + line.replace(' ', '_') + ')'

	elif type_ == 'input':

		# split keyword with variable
		line = line.replace("ask ", "")

		# create parsed code
		mod_line = 'input("""' + line + '""")'

	return mod_line

def findLineType(line, keyword_dict):
	for key, line_type in keyword_dict.items():
		if key in line:
			return line_type

	# if none of the keys were found, default to var set
	return 'var set'

def parse(text):
	# split into lines
	text = text.split('\n')

	# take out empty lines
	while '' in text:
		text.remove('')

	# setting variables before loop
	parsed_code = []
	key_dict = {'increase':'var change',
				'decrease':'var change',
				'contains':'list set',
				'append': 'list append',
				'remove': 'list remove',
				'pop': 'list pop',
				'delete': 'delete',
				'what is': 'print var',
				'repeat to me': 'print',
				'ask': 'input'}

	# main parsing loop 
	# (iterates through each line)
	for line in text:


		# check if line is changing a var
		mod_type = findLineType(line, key_dict)
		mod_line = parseLine(line, mod_type)
		
		# add line to parsed_code
		parsed_code.append(mod_line)

	return parsed_code

def printCode(parsed_code):
	for line in parsed_code:
		print(line)

def createPythonFile(parsed_code, filename = None):
	filename = 'unamed_code_file' if filename == None else filename
	with open(filename + '.py', 'w') as f:
		for line in parsed_code:
			f.write(line + '\n')

# main
code_file = read('code_v2')
parsed_code = parse(code_file)
printCode(parsed_code)
createPythonFile(parsed_code, 'My first python project')