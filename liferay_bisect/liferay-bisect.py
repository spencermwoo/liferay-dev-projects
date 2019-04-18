#!/usr/bin/env python
# from __future__ import print_function

import os
import re
import subprocess
import sys
import time
import builtins
import math

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


def print_flush(*objects, sep='', end='\n', flush=False):
	""" Override print() function """
	return builtins.print(objects, sep, end, flush=True)

builtins.__print__ = print_flush

def print_help():
	print("USAGE : lb <bad_commit> <good_commit>")

def print_exit(msg):
	print(msg)
	exit()


# Processes

def git_checkout(commit):
	print("Checking out " + commit)
	args = [commit]

	return run_process(True, "git", "checkout", args)
	
def git_log(commit):
    args = ["-1", commit]

    return run_process(True, "git", "log", args)

# git log --pretty=oneline fix-pack-de-28-7010..fix-pack-de-27-7010 > tmp_bisect.txt
def git_log_pretty(bad, good):
	args = ["--pretty=oneline", bad + "..." + good]

	output = run_process(True, "git", "log", args)
	file_write(TMP_FILENAME, output)

def run_process(output, program, cmd, *params):
    if not quiet:
        print("\t" + program + " " + cmd + " " +
              ' '.join(str(x) for x in params[0]))

    args = [program] + [cmd] + params[0]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=dir_path)

    if output:
        return process.communicate()[0].decode("UTF-8", "replace")

# Utility

def file_write(filename, content):
	with open(os.path.join(dir_path, filename),"w", encoding="UTF-8") as file:
		file.write(content)

def time():
	time.sleep(5)

def outer():
	def reader(func):
		def wrapper():
			LPS_LIST = list_read()

			if len(LPS_LIST) < 2:
				print_exit("Found Ticket : " + LPS_LIST[0])

			length = len(LPS_LIST) - 1
			num = int(length / 2)
			
			try:
				with open(BISECT_FILENAME, encoding="UTF-8") as f:
					output = func(f, num, length)
			except FileNotFoundError:
				print_exit("You need to start bisect.")
				
			except:
				print_exit("[!] XD")

			return output

		return wrapper
	return reader

# Functional

# decorate better? -- @outer(False, False) -- file_write and bisect?
@outer()
def bisect(f, num, length):
	""" Liferay Bisect """
	commit = f.readlines()[num]
	steps = (int) (math.sqrt(length)) + 1

	# if steps:

	print("\nSteps remaining : " + str(steps))
	# print("\n" + str(num) + " : " + str(commit))
	return commit.split()[0]

@outer()
def bisect_bad(f, num, length):
	""" Liferay Bisect """
	output = f.readlines()[:num+1]

	output = ''.join(output)

	file_write(BISECT_FILENAME, output)

	return bisect()

@outer()
def bisect_good(f, num, length):
	""" Liferay Bisect """
	output = f.readlines()[num:]

	output = ''.join(output)

	file_write(BISECT_FILENAME, output)

	return bisect()

def list_generate():
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

def list_read():
	""" Creates LPS_LIST from BISECT_FILENAME """
	LPS_LIST = {}
	try:
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

	except FileNotFoundError:
		print_exit("You need to start bisect.")
		
	except:
		print_exit("[!] XD")

	return LPS_LIST

def history_write():
	print("init history")

def history_append():
	print("append")

def history_read():
	print("read)")

# @contextmanager
# def checkout(commit):

	# commit

def main():
	#0-, 4+
	if len(sys.argv) < 2 or len(sys.argv) > 3:
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
			list_generate()

			commit = bisect()
			commit_hash = commit.split()[0]
			git_checkout(commit_hash)
		elif (v1 == "log" or v1 == "l"):
			print("bisect log")

		else:
			# print("try")
			try:
				bad = sys.argv[1]
				good = sys.argv[2]
			except:
				print_exit("Improper argument.  '-help' for guide.")

			git_log_pretty(bad, good)

			list_generate()

			# bisect()
			git_checkout(bisect())
			# commit_hash = commit.split()[0]
			# git_checkout(commit)\

		# else:
		# 	print_help()

		# yield


# git_checkout("6f0df7c1b8f733294df4c878393664156b884716")
if __name__ == "__main__":
    main()