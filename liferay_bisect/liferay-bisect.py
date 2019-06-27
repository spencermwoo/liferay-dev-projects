#!/usr/bin/env python

# This is a work in progress.  I'll polish near the end.

# Make functional -- todo
# Make clean
# Make efficient
# Additional function

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
LOG_FILENAME = "bisect_log" + FILE_EXT


LPS_DICT = {}

dir_path = os.getcwd()


def print_flush(*objects, sep='', end='\n', flush=False):
    """ Override print() function """
    return builtins.print(objects, sep, end, flush=True)

builtins.__print__ = print_flush

# Help
def print_help():
    print("USAGE : lb <bad_commit> <good_commit>")
    
    print("")

    print("CMDs : bad, good, reset, log")
    # print("\nhttps://git-scm.com/docs/git-bisect")

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
              ' '.join(str(p) for p in params[0]))

    args = [program] + [cmd] + params[0]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=dir_path)

    if output:
        return process.communicate()[0].decode("UTF-8", "replace")

# Utility

# Write or Append
def file_write(filename, content, write=True):
    with open(os.path.join(dir_path, filename),"w" if write else "a", encoding="UTF-8") as file:
        file.write(content)

def time():
    time.sleep(5)

# Fix decorator
def outer():
    def reader(func):
        def wrapper():
            LPS_DICT = list_read()

            if len(LPS_DICT) < 2:
                l = LPS_DICT.popitem()
                sys.exit("Found Ticket : " + l[0] + " at " + l[1])

            length = len(LPS_DICT) - 1
            num = int(length / 2)
            
            try:
                with open(BISECT_FILENAME, encoding="UTF-8") as file:
                    output = func(file, num, length)
            except FileNotFoundError:
                sys.exit("You need to start bisect.")
                
            except:
                if length == 1:
                    bisect()
                else:
                    sys.exit("[!] XD")

            return output

        return wrapper
    return reader

# Functional
@outer()
def bisect(file, num, length):
    """ Liferay Bisect """
    commit = file.readlines()[num]
    steps = (int) (math.log(length, 2)) + 1

    print("\nSteps remaining : " + str(steps))
    return commit.split()[0]

@outer()
def bisect_bad(file, num, length):
    """ Liferay Bisect """
    output = file.readlines()[:num+1]

    output = ''.join(output)

    file_write(BISECT_FILENAME, output)

    return bisect()

@outer()
def bisect_good(file, num, length):
    """ Liferay Bisect """
    output = file.readlines()[num-1:]

    output = ''.join(output)

    file_write(BISECT_FILENAME, output)

    return bisect()

def list_generate():
    """ Transform TMP_FILENAME into BISECT_FILENAME """
    with open(TMP_FILENAME, encoding="UTF-8") as f:
        for line in f:
            split_line = line.split()

            commit_hash = split_line[0]
            LPS = split_line[1]

            if LPS != LPS.upper():
                continue
            elif LPS in LPS_DICT:
                continue
            else:
                LPS_DICT[LPS] = commit_hash

    output = ""
    for lp in LPS_DICT:
        output += LPS_DICT[lp] + " : " + lp + "\n"

    file_write(BISECT_FILENAME, output)
    file_write(LOG_FILENAME, output)

def list_read():
    """ Populate LPS_DICT from BISECT_FILENAME """
    LPS_DICT = {}
    try:
        with open(BISECT_FILENAME, encoding="UTF-8") as f:
            for line in f:
                split_line = line.split()
                
                commit_hash = split_line[0]
                LPS = split_line[2]

                if LPS in LPS_DICT:
                    continue
                else:
                    LPS_DICT[LPS] = commit_hash

    except FileNotFoundError:
        sys.exit("You need to start bisect.")
        
    except:
        sys.exit("[!] XD2")

    return LPS_DICT

def list_log(commit_hash, cmd=""):
    """ Appends to LOG_FILENAME """
    if cmd:
        cmd = " - " + cmd

    content = cmd + "\n\n" + commit_hash
    file_write(LOG_FILENAME, content, False)

def main():
    #lb bad good -- implicit bisect start

    #Expecting : bisect.py command
    num_args = len(sys.argv)

    if "-help" in sys.argv or "-h" in sys.argv:
        print_help()

    elif num_args == 2:
        cmd = sys.argv[1]

        commands = ["bad", "good", "reset", "log"]

        if cmd in commands:
            commit = None

            if cmd == commands[0]:
                commit = bisect_bad()

            elif cmd == commands[1]:
                commit = bisect_good()

            elif cmd == commands[2]:
                commit = bisect()

            else:
                sys.exit(LOG_FILENAME)

            commit_hash = commit.split()[0]
            git_checkout(commit_hash)

            list_log(commit_hash, cmd)

    elif num_args == 3:
        bad = sys.argv[1]
        good = sys.argv[2]

        git_log_pretty(bad, good)

        list_generate()

        commit_hash = bisect()
        git_checkout(commit_hash)

        list_log(commit_hash)

        # commit_hash = commit.split()[0]
        # git_checkout(commit)\

        # else:
        #   print_help()

        # yield
    else:
        sys.exit("Improper argument.  '-help' for guide.")

# git_checkout("6f0df7c1b8f733294df4c878393664156b884716")
if __name__ == "__main__":
    main()