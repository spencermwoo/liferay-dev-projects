from robobrowser import RoboBrowser
from time import strftime
import os
import time
import tldextract

# Configure to avoid testing certain prefixes or subdomains.
filter_out_prefix = ["camera", "cdn", "cloud", "dmz", "haproxy", "lrdcom", "mfs", "mysql", "maxscale", "virt", "wifi"]
filter_out_subdomain = ["lax"]  # Not quite

# TODO : Configure to only test certain tlds
filter_only = [".com"]

public_domains = []
private_domains = []
failure_domains = []
skipped_domains = []

# The first run tests all domains whether they are public, private, or unresolvable (failure).
# The subsequent runs use history (existing file) and only test the public domains.

write_output = True
use_history = False

# Input Output
file_path = os.path.join(os.getcwd())
down_url = "http://downforeveryoneorjustme.com/"

domains_file = "liferay-domains/liferay-domains.txt"
output_file = "liferay-domains/liferay-domains-check.txt"


def check_public_domain(url):
	browser = RoboBrowser(user_agent='testing', history=True, parser="html.parser")
	browser.open(down_url + url + "/c")

	result = browser.parsed.get_text()

	return is_valid(url, result)

def check_public_domains():
	if use_history:
		get_history()

	for line in open(domains_file, 'r'):
		line = line.strip()
		if line not in private_domains and \
			line not in failure_domains and \
			line not in skipped_domains:

			if get_subdomain_match(line) in filter_out_subdomain or \
				get_prefix(line) in filter_out_prefix:

				print("Skipping " + line, flush=True)
				skipped_domains.append(line)
			else:
				print("Checking " + line, flush=True)
				if check_public_domain(line):
					public_domains.append(line)
				else:
					if line not in failure_domains:
						private_domains.append(line)

				time.sleep(.5)
		else:
			print(line + " has a history.", flush=True)

	if write_output:
		output_str = "Public : \n"
		output_str = domain_append(output_str, public_domains)

		output_str += "Private : \n"
		output_str = domain_append(output_str, private_domains)

		output_str += "Failure : \n"
		output_str = domain_append(output_str, failure_domains)

		output_str += "Skipped : \n"
		output_str = domain_append(output_str, skipped_domains)

		print("=====")
		print(output_str)

		write_file(file_path, output_file, output_str)
		# write_file(file_path, output_file[:-4] + strftime("%y%m%d") + ".txt", output_str)


def domain_append(string, domain_list):
	for domain in domain_list:
		string += domain + "\n"
	return string + "\n"


def domain_print(domain_list):
	for domain in domain_list:
		print(domain)


def get_history():
	is_private = False
	is_failure = False
	is_skipped = False
	try:
		for line in open(output_file, 'r'):
			line = line.strip()
			if is_skipped:
				if line not in skipped_domains:
					skipped_domains.append(line)
			elif is_failure:
				if line not in failure_domains:
					failure_domains.append(line)
			elif is_private:
				if line not in private_domains:
					private_domains.append(line)

			if "Private :" in line:
				is_private = True

			if "Failure :" in line:
				is_failure = True

			if "Skipped :" in line:
				is_skipped = True

		return True
	except FileNotFoundError:
		return False


# Add Error Handling
def get_prefix(string):
	return string.split("-")[0]


def get_subdomain(url):
	if not url:
		return ""

	extracted = tldextract.extract(url)
	if not extracted.domain:
		return ""

	return extracted.subdomain


def get_subdomain_match(url):
	return get_subdomain(url).split(".")[-1]


def is_valid(url, result):
	splits = result.split(url)
	try:
		first_split = splits[3]
		second_split = splits[4]

		if validate_first(first_split):
			return validate_second(second_split)
	except IndexError:
		print("Failure determining " + url)
		failure_domains.append(url)
		return False


def validate_first(string):
	# It's not just you!
	# It's just you.
	if "It's just you." in string.splitlines()[-1]:
		return True
	else:
		return False


def validate_second(string):
	# looks down from here
	# is up.
	if "is up." in string.splitlines()[0]:
		return True
	else:
		return False


def write_file(path, name, output):
	try:
		with open(os.path.join(path, name),"w", encoding="UTF-8") as file:
			file.write(output)

		return True
	except IOError:
		return False


check_public_domains()
