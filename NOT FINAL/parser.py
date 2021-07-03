def read(filename):
	with open(filename + '.txt', 'r') as f:
		return f.read()

def parse(text):
	# split into lines
	text = text.split('\n')

	# take out empty lines
	while '' in text:
		text.remove('')

	# set vars before parse loop
	code = {}
	current_class = ''
	current_section = ''

	# parse loop
	for line in text:

		# title
		if '>' in line:

			# we found a new class, so we we should create a blank slate
			current_class_code = {}

			# parse
			title_line = line.replace('>','').replace(' (inherited ',' ').replace(')','').replace(',','').split()
			
			# split class name from parent classes
			class_name = title_line[0]
			title_line.pop(0)

			# format parent classes
			parent_classes = ''
			for parent in title_line:
				if title_line.index(parent) == 0:
					parent_classes = '(' + parent_classes + parent + ', '
				if title_line.index(parent) not in [0, len(title_line) - 1]:
					parent_classes = parent_classes + parent + ', '
				if title_line.index(parent) == len(title_line) - 1:
					parent_classes = parent_classes + parent + ')'

			# create object title line
			title_line = f'class {class_name}{parent_classes}:'
			current_class = class_name
			code[current_class]['title_line'] = title_line

			# since we just parsed the title, we expect the init def
			current_section = 'init'

		# init line
		if 'Unique Stats: ' in line and current_section == 'init':
			init_parameters = line.replace('Unique Stats: ','').split(',')

			if init_parameters == ['None']:
				init_line = '\tdef __init__(self):'
			else:
				init_line = '\tdef __init__(self'
				for parameter in init_parameters:
					init_line = init_line + ', ' + parameter
				init_line = init_line + '):'

			code[current_class]['init']['def'] = init_line

		# methods
		if '=' in line:
			line = line.replace('= ','')

			current_section = line
			code[current_class][current_section] = []

		# bulleted lines
		if '-' in line:
			line = line.replace('- ','')

			# find the type of the line i.e. "function" or "variable set"
			line_type = 'variable'
			for keyword in ['say ']:
				if keyword in line_data:
					line_type = 'function'

			if line_type == 'function':
				function = line_data

				# print
				if 'say ' in function:
					function = function.replace('say ','')
					function = f'\t\tprint("""{function}""")'

				code[current_class][current_section].append(function)

			if line_type == 'variable':
				variable = line_data
				if '=' not in variable:
					variable = '\t\tself.' + variable + ' = ' + variable
				else:
					variable = '\t\tself.' + variable
				
				code[current_class][current_section].append(variable)

		# methods
	
	# clean up loose ends

	# current class code
	if current_class_code != []:
		if method_code != []:
			current_class_code.append(method_code)
			
		code.append('')
		code.append(current_class_code)

	return code

code = read('code')
code = parse(code)
print(code)