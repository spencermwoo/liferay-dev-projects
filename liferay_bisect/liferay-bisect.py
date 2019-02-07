#!/usr/bin/env python
# from __future__ import print_function

# This is a work in progress.  I'll polish near the end.

import os
import re
import subprocess
import sys
import time
import builtins

from time import strftime
from contextlib import contextmanager

# Configuration	

# Filenames will have timestamp appended.
timestamp = False

# Debug prints are disabled.
quiet = True




FILE_EXT = ".txt"

# fancy later
TMP_FILENAME = "tmp_bisect" + FILE_EXT
BISECT_FILENAME = "bisect" + FILE_EXT


LPS_LIST = {}

dir_path = os.getcwd()


def flush_print(*objects, sep='', end='\n', flush=False):
	""" Override print() function """
	return builtins.print(objects, sep, end, flush=True)

builtins.__print__ = flush_print

# Processes

def git_checkout(commit):
	args = [commit]

	return run_process(True, "git", "checkout", args)
	
def git_log(commit):
    args = ["-1", commit]

    return run_process(True, "git", "log", args)

# git log --pretty=oneline fix-pack-de-28-7010..fix-pack-de-27-7010 > tmp_bisect.txt
def git_log_pretty(bad, good):
	args = ["--pretty=oneline", bad + "..." + good]

	output = run_process(True, "git", "log", args)
	write_file(TMP_FILENAME, output)

def run_process(output, program, cmd, *params):
    if not quiet:
        print("\t" + program + " " + cmd + " " +
              ' '.join(str(x) for x in params[0]))

    args = [program] + [cmd] + params[0]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=dir_path)

    if output:
        return process.communicate()[0].decode("UTF-8", "replace")

# Utility

def write_file(filename, content):
	with open(os.path.join(dir_path, filename),"w", encoding="UTF-8") as file:
		file.write(content)

def time():
	time.sleep(5)

def outer():
	def reader(func):
		def wrapper():
			LPS_LIST = read_list()

			if len(LPS_LIST) < 2:
				print("Found Ticket.")

			num = int((len(LPS_LIST) - 1) / 2)
			
			with open(BISECT_FILENAME, encoding="UTF-8") as f:
				output = func(f, num)

			return output

		return wrapper
	return reader

# Functional

# decorate better? -- @outer(False, False) -- write_file and bisect?
@outer()
def bisect(f, num):
	""" Liferay Bisect """
	commit = f.readlines()[num]
	
	print("\n" + str(num) + " : " + str(commit))
	return commit

@outer()
def bisect_bad(f, num):
	""" Liferay Bisect """
	output = f.readlines()[:num+1]

	output = ''.join(output)

	write_file(BISECT_FILENAME, output)

	return bisect()

@outer()
def bisect_good(f, num):
	""" Liferay Bisect """
	output = f.readlines()[num:]

	output = ''.join(output)

	write_file(BISECT_FILENAME, output)

	return bisect()

def generate_list():
	""" Creates BISECT_FILENAME from TMP_FILENAME """
	with open(TMP_FILENAME, encoding="UTF-8") as f:
		for line in f:
			split_line = line.split()

			commit_hash = split_line[0]
			LPS = split_line[1]

			if LPS != LPS.upper():
				continue

			if LPS in LPS_LIST:
				continue
			else:
				LPS_LIST[LPS] = commit_hash

	output = ""
	for lp in LPS_LIST:
		output += LPS_LIST[lp] + " : " + lp + "\n"

	with open(os.path.join(dir_path, BISECT_FILENAME),"w", encoding="UTF-8") as file:
			file.write(output)

def read_list():
	""" Creates LPS_LIST from BISECT_FILENAME """
	LPS_LIST = {}

	with open(BISECT_FILENAME, encoding="UTF-8") as f:
		for line in f:
			split_line = line.split()
			
			commit_hash = split_line[0]
			LPS = split_line[2]

			if LPS in LPS_LIST:
				# print(LPS_LIST)
				continue
			else:
				LPS_LIST[LPS] = commit_hash

	return LPS_LIST

# @contextmanager
# def checkout(commit):

	# commit

def main():
	#0-, 4+
	if len(sys.argv) < 1 or len(sys.argv) > 3:
		print("'-help' for guide.")
	else:
		v1 = sys.argv[1]
		
		if "-help" in sys.argv or "--help" in sys.argv:
			print_help()

		# fix
		elif (v1 == "bad" or v1 == "b"):
			commit = bisect_bad()
			commit_hash = commit.split()[0]
			git_checkout(commit_hash)

		elif (v1 == "good" or v1 == "g"):
			commit = bisect_good()
			commit_hash = commit.split()[0]
			git_checkout(commit_hash)

		elif (v1 == "reset" or v1 == "r"):
			generate_list()

			commit = bisect()
			commit_hash = commit.split()[0]
			git_checkout(commit_hash)

		else:
			# print("try")
			try:
				bad = sys.argv[1]
				good = sys.argv[2]
			except:
				print("Improper argument.  '-help' for guide.")
				#exit				

			git_log_pretty(bad, good)

			generate_list()

			bisect()
			# commit_hash = commit.split()[0]
			# git_checkout(commit)

		# yield


# git_checkout("6f0df7c1b8f733294df4c878393664156b884716")
main()