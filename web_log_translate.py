#!/bin/python

import sys

try:
	with open(sys.argv[1], 'r') as file:
		file_output = file.read()
except:
	print "Usage: ./tidy_up <file>"
	exit()

try:
	file_output = file_output\
	.replace('%255Cr', '\n')\
	.replace('%255Cn', '')\
	.replace('%2520', ' ')\
	.replace('%250A', '\n')\
	.replace('%20', ' ')\
	.replace('%0A', '\n')\
	.replace("details: \nb'", "details: \n")
	print file_output
except:
	print "An error occurred."
