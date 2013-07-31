#!/usr/bin/env python
import os
import subprocess
import time

# Time limit for execution in milliseconds
LIMIT = .5

def run(code):
	p = subprocess.Popen(['lua', '-e', code], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	start = time.time()
	output = ''
	while p.returncode == None:
		p.poll()
		time.sleep(.1)
		if time.time() > start + LIMIT:
			p.kill()
			p.wait()
			output = 'Process killed'
			break

	if p.returncode == 0:
		output = p.stdout.read()
	elif p.returncode > 0:
		output = p.stderr.read()

	return output
