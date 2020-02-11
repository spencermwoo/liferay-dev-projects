def diff(filename1, content1, filename2, content2):
	diff = difflib.unified_diff(content1, content2, fromfile=filename1, tofile=filename2)
	lines = list(diff)[2:]
	
	added = [line[1:] for line in lines if line[0] == '+']
	removed = [line[1:] for line in lines if line[0] == '-']

	unique_added_count = 0
	unique_removed_count = 0

	file = open(filename1.split('.')[0] + "_" + filename2, 'w', encoding='UTF-8')

	# Position agnostic
	file.write("Additions : \n")
	for line in added:
	    if line not in removed:
	    	unique_added_count += 1
	    	file.write(line)

	file.write('\nRemovals : \n')
	for line in removed:
	    if line not in added:
	    	unique_removed_count += 1
	    	file.write(line)

	file.write("\n" + str(unique_added_count) + " - " + str(unique_removed_count) + " = " + str(unique_added_count - unique_removed_count))

def getLatest():
	#os.path.getmtime()
	directory_contents = os.listdir()
	
	latest = 0

	for files in directory_contents:
		if files != 'util.py':
			modTime = os.path.getmtime(files)
			if modTime > latest:
				latest = os.path.getmtime(files)
				latestFile = files
	print(latest)
	print(latestFile)

def parseNames(path, input_file):
	chars_to_remove = ['|', '\\','/','-']

	output = ""
	ret = []

	with open(input_file, 'r') as file:
		for line in file:
			temp = (''.join(x for x in line if x not in chars_to_remove)).strip() + '\n'
			ret.append(temp)
			output += temp

	writeOutput(path, input_file, output)

	return ret