#!/usr/bin/env python
import os
import subprocess
import time

# Time limit for execution in seconds
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

def run_safely(code):
	# escape slashes
	code = code.replace('\\', '\\\\')

    # escape double quotes
	code = code.replace('"', '\\"')

	# wrap with boilerplate
	code = """
	local env = {
		print = print,
        ipairs = ipairs,
        next = next,
        pairs = pairs,
        pcall = pcall,
        select = select,
        tonumber = tonumber,
        tostring = tostring,
        type = type,
        unpack = unpack,
        coroutine = { create = coroutine.create, resume = coroutine.resume,
           running = coroutine.running, status = coroutine.status, 
           wrap = coroutine.wrap },
        string = { byte = string.byte, char = string.char, find = string.find,
           format = string.format, gmatch = string.gmatch, gsub = string.gsub,
           len = string.len, lower = string.lower, match = string.match,
           rep = string.rep, reverse = string.reverse, sub = string.sub,
           upper = string.upper },
        table = { insert = table.insert, maxn = table.maxn, remove = table.remove,
           sort = table.sort },
        math = { abs = math.abs, acos = math.acos, asin = math.asin,
           atan = math.atan, atan2 = math.atan2, ceil = math.ceil, cos = math.cos,
           cosh = math.cosh, deg = math.deg, exp = math.exp, floor = math.floor,
           fmod = math.fmod, frexp = math.frexp, huge = math.huge,
           ldexp = math.ldexp, log = math.log, log10 = math.log10, max = math.max,
           min = math.min, modf = math.modf, pi = math.pi, pow = math.pow,
           rad = math.rad, sin = math.sin, sinh = math.sinh, sqrt = math.sqrt,
           tan = math.tan, tanh = math.tanh,
           random = math.random,
        },
        os = { clock = os.clock, difftime = os.difftime, time = os.time },
    }

	local _func = assert(loadstring("%s"))
	setfenv(1, env)
	print(_func())
	""" % code

	return run(code)
