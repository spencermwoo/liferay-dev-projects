import json, os, re, time
from time import strftime
from Employee import Employee
from robobrowser import RoboBrowser

LIFERAY_URL = "https://web.liferay.com/sign-in"
LOOP_URL = "https://loop.liferay.com"
GUEST_PATH = "/web/guest/home/-/loop/"

COMPANY = "company"
DEPARTMENT = "departments"
LOCATIONS = "locations"
PEOPLE = "people"
TEAMS = "teams"
TOPIC = "topics"

#COMPANY_URL = "https://loop.liferay.com/web/guest/home/-/loop/company/_Liferay"
DEPARTMENT_URL = "https://loop.liferay.com/web/guest/home/-/loop/departments"
PEOPLE_URL = "https://loop.liferay.com/home/-/loop/people"

USERNAME = os.environ['LOOP_USERNAME']
PASSWORD = os.environ['LOOP_PASSWORD']

EMPLOYEES = {}
STACK = []
#QUEUE = deque()

OUTPUT = ""
PATH = "C:\\Users\\liferay\\Desktop\\me\\looper\\log"

# =============
#     MAIN
# =============
def looper():
	global EMPLOYEES, STACK, OUTPUT, PATH

	browser = login()

	# employeeName = input("Enter Employee Name : \n")
	# employeeId = getEmployeeId(browser, employeeName)

	# if employeeId < 0 :
	# 	print("FAILURE : Invalid Employee Name")
	# 	return

	#employeeId = 3407654 # Spencer Woo
	employeeId = 29156 # ROOT
	#employeeId = 29849 # Angelo
	# print("\n\n")

	option = "tree"
	employee = addEmployee(browser, employeeId)
	EMPLOYEES[employeeId] = employee
	STACK.append(employeeId)

	# option = input("Upper or Lower or Tree : \n")
	# option = option.lower()
	# print("\n\n\n")

	# Upper recursive managers
	# Lower recursive subordinates
	# Tree full organization chart

	# if option == "upper" or option == "lower" or option == "tree":
	# 	print(employeeName)
	# else:
	# 	print("FAILURE : Invalid Option")
	# 	return
	
	while STACK:
		if option == "upper":
			generateChain(browser, STACK.pop(), True)
		elif option == "lower":
			generateChain(browser, STACK.pop(), False)
		elif option == "tree":
			generateChart(browser, STACK.pop())
		
	if option == "tree":
		OUTPUT = ""
		root = 29156
		SEEN = []
		printTreeFromRoot(EMPLOYEES[root], "", False, SEEN)

	writeOutput(PATH, OUTPUT)

# =============
#    API GET
# =============
def viewEndpoint(browser, employeeStrId, viewType):
	global PEOPLE_URL

	viewEndpoints = {
		0 : '/view.json?id=', 
		1 : '/viewManagers.json?start=-1&end=-1&id=',
		2 : '/viewSubordinates.json?start=-1&end=-1&id='
	}

	viewURL = PEOPLE_URL + viewEndpoints.get(viewType, '') + employeeStrId
	browser.open(viewURL)
	json_data = str(browser.parsed)
	# print(viewURL, flush=True)
	json_data = fixInvalidJSON(str(browser.parsed))

	return json.loads(json_data)

# =============
#     ADD
# =============
def addEmployee(browser, employeeId):
	global EMPLOYEES

	if employeeId in EMPLOYEES:
		print("FAILURE : OCCURING LOOP", flush=True)
		sys.exit()

	responseJSON = viewEndpoint(browser, str(employeeId), 0)
	return createEmployee(responseJSON)

def addHierachy(browser, employee, isManager):
	global EMPLOYEES, STACK

	employeeId = employee.getId()
	if isManager:
		responseJSON = viewEndpoint(browser, str(employeeId), 1)
	else:
		responseJSON = viewEndpoint(browser, str(employeeId), 2)

	results = responseJSON['data']['results']
	if not results:
		return

	for current in results:
		curId = current['entityClassPK']
		if curId not in EMPLOYEES:
			curEmployee = addEmployee(browser, curId)
			EMPLOYEES[curId] = curEmployee
			STACK.append(curId)
		curEmployee = EMPLOYEES[curId]

		if isManager:
			if not employee.hasManager(curEmployee):
				employee.addManager(curEmployee)
		else:
			if not employee.hasSubordinate(curEmployee):
				employee.addSubordinate(curEmployee)
	return

# =============
#    CREATE
# =============
def createEmployee(responseJSON):
	status = responseJSON['status']
	if status != 200:
		print('FAILURE : JSON RESPONSE', flush=True)
		sys.exit()

	data = responseJSON['data']

	employeeId = data['entityClassPK']
	firstName = data['firstName']
	lastName = data['lastName']
	emailAddress = data['emailAddress']
	# jobTitle = data['jobTitle']
	# hireDate = data['hireDate']
	# locationName = data['locationName']

	# try:
	# 	print(firstName + " " + lastName, flush=True)
	# except:
	# 	print(emailAddress.split("@")[0], flush=True)

	return Employee(employeeId, firstName, lastName, emailAddress)

# =============
#     GEN
# =============
def generateChart(browser, employeeId):
	global EMPLOYEES, STACK

	if employeeId in EMPLOYEES:
		addHierachy(browser, EMPLOYEES[employeeId], True)
		addHierachy(browser, EMPLOYEES[employeeId], False)
	else:
		employee = addEmployee(browser, employeeId)
		EMPLOYEES[employeeId] = employee
		STACK.append(employeeId)
	return

def generateChain(browser, employeeId, isUpperChain):
	addHierachy(browser, EMPLOYEES[employeeId], isUpperChain)

# =============
#     UTIL
# =============
def login():
	browser = RoboBrowser(user_agent='testing', history=True, parser="html.parser")
	browser.open(LIFERAY_URL)

	form = browser.get_form(id='_58_fm')
	form

	if form is None:
		print("Could not find login form.", flush=True)
	else:
		form['_58_login'].value = USERNAME
		form['_58_password'].value = PASSWORD

		browser.submit_form(form)
		time.sleep(2)
		browser.open(LOOP_URL)

		form = browser.get_form(action="https://web.liferay.com/c/portal/saml/sso")
		browser.submit_form(form)
		
		form = browser.get_form(action="https://loop.liferay.com/c/portal/saml/acs")
		browser.submit_form(form)

		browser.open(LOOP_URL)

	# print((browser.parsed).encode('UTF-8'), flush=True)
	return browser

def fixInvalidJSON(JSON):
	flag = True
	new = ""

	split1 = JSON.split('\"descriptionMarkdownHTML\":\"');
	for x in split1:
		if flag:
			new += split1[0]
			flag = False
		else:
			split2 = x.split(',\"firstName\":\"')
			new += "\"descriptionMarkdownHTML\":\"\",\"firstName\":\""
			new += split2[1]

	while (not new.endswith('}')):
		new = new[:-1]

	return new

#https://loop.liferay.com/web/guest/home/-/loop/departments/_TS+-+US
# TS - US
def getDepartmentId(browser, departmentName):
	departmentName = departmentName.strip()
	departmentName = departmentName.replace(" ", "+")

	try:
		groupURL = URL + DEPARTMENT + JOIN_URL + departmentName
		browser.open(gropuURL)

		print(browser.parsed)

		return 0
	except:
		return -1
		
# fix / improve this
def getEmployeeId(browser, employeeName):
	global PEOPLE_URL

	employeeName = employeeName.strip()
	splitName = employeeName.split(" ")

	try:
		firstName = splitName[0]
		lastName = splitName[1]

		parsedName = firstName.lower() + "." + lastName.lower()
		employeeURL = PEOPLE_URL + "/_" + parsedName

		browser.open(employeeURL)

		#(entityClassPK:[0-9]*)
		split = str(browser.parsed).split("entityClassPK")
		split2 = split[len(split) - 1].split(",")

		employeeId = split2[0][1:]
		return int(employeeId)

	except:
		return -1

def getHexConversion(character):
	return character.encode("hex")

def getURL(append):
	return LOOP_URL + GUEST_PATH + append

def isInteger(x):
	try:
		int(x)
		return True
	except ValueError:
		return False

def printTreeFromRoot(employee, prefix, isLeaf, SEEN):
	global OUTPUT

	try:
		print(prefix + ("\--  " if isLeaf else "|-- ") + employee.getName())
		OUTPUT += prefix + ("\--  " if isLeaf else "|-- ") + employee.getName() + "\n"
		# OUTPUT += employee.getEmail() + "\n"
	except:
		OUTPUT += prefix + ("\--  " if isLeaf else "|-- ") + employee.getEmail().split("@")[0] + "\n"
		# OUTPUT += employee.getEmail() + "\n"
	
	s = employee.getSubordinates()
	if s:
		for i in range(0, len(s)):
			if s[i] not in SEEN:
				SEEN.append(s[i])
				if i == len(s) - 1:
					printTreeFromRoot(s[i], prefix + ("   " if isLeaf else "|  "), True, SEEN)
				else:
					printTreeFromRoot(s[i], prefix + ("   " if isLeaf else "|  "), False, SEEN)

def splitJSON(line):
	if(line.index(',') < line.index('{')):
		return line.split(',')
	return line.split("{")

def writeOutput(path, output):
	filename = "looper"
	# filename = "emails"
	filename += strftime("%y%m%d")

	try:
		file = open(path + "\\" + filename + ".txt","w", encoding="UTF-8")
		file.write(output)
		file.close()
		
		return True
	except IOError:
		return False

looper()

locations = {}
titles = {}
positions = {}

def appendStats(output):
	global locations, positions, titles
	
	output += "\n LOCATIONS : \n"
	for w in sorted(locations, key=locations.get, reverse=True):
		output += str(w) + "," + str(locations[w]) + "\n"

	output += "\n POSITIONS : \n"

	for w in sorted(positions, key=positions.get, reverse=True):
		output += str(w) + "," + str(positions[w]) + "\n"


	output += "\n TITLES : \n"

	for w in sorted(titles, key=titles.get, reverse=True):
		output += str(w) + "," + str(titles[w]) + "\n"


	locations.clear()
	positions.clear()
	titles.clear()

	return output

def loopUser():
	global PATH, locations, positions, titles
	browser = login()

	output = ""
	seen = False

	with open("difference.txt", "r", encoding="UTF-8") as f:
		for line in f:
			if line.strip() == '':
				output += "\n"
				continue
			elif ":" in line:
				if seen:
					output = appendStats(output)
				else:
					seen = True
				# output += line
				continue
			# elif "-" in line:
			# 	output += line
			# 	continue
			else:
				if "." in line:
					splits = line.split(".")
				else:
					splits = line.split(" ")
				firstName = splits[0]
				lastName = splits[1]

				name = name = "_" + firstName + "." + lastName
				name = name.lower().strip()

				responseJSON = getUserId(browser, name)
				output = parseResponse(responseJSON, output)

	output += "\n\n==========="
	output += "\nREMOVALS : \n"
	output = appendStats(output)
	writeOutput(PATH, output)

def getUserId(browser, name):
	viewURL = PEOPLE_URL + name + "/view.json"
	browser.open(viewURL)

	json_data = fixInvalidJSON(str(browser.parsed))
	return json.loads(json_data)

# Refactor
def parseResponse(responseJSON, output):
	global locations, positions, titles

	status = responseJSON['status']
	if status != 200:
		print('FAILURE : JSON RESPONSE', flush=True)
		sys.exit()

	data = responseJSON['data']

	# employeeId = data['entityClassPK']
	firstName = data['firstName']
	lastName = data['lastName']

	emailAddress = data['emailAddress']
	jobTitle = data['jobTitle']
	hireDate = data['hireDate']
	locationName = data['locationName']

	if locationName in locations:
		locations[locationName] = locations[locationName] + 1
	else:
		locations[locationName] = 1

	if jobTitle in positions:
		positions[jobTitle] = positions[jobTitle] + 1
	else:
		positions[jobTitle] = 1

	firstTitle = jobTitle.split(" ")
	if firstTitle[0] in titles:
		titles[firstTitle[0]] = titles[firstTitle[0]] + 1
	else:
		titles[firstTitle[0]] = 1

	name = firstName + " " + lastName
	return output

# loopUser()