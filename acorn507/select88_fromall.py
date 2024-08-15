

import glob
import os
import numpy as np



######################################################

logs_dir = "all_superpolys"

key_size = 128

src_file = "autosearch_guess40_fromall.log"

tar_dir = "selected_logs"

prefix = "ACORN_round507" 

#######################################################


if os.path.exists(tar_dir):
	os.system("rm -r " + tar_dir)
os.system("mkdir " + tar_dir)


f = open(src_file, "r")
all_lines = f.readlines()
f.close()



order = []

for line in all_lines:

	if "Deduced level:  " not in line:
		continue

	lsp = line.replace("Deduced level:  ", "").replace("\n", "").split(" ")

	for term in lsp:
		dkey = term.split("[")[0].replace("k", "")
		d_level = term.split("[")[-1].split("]")[0]
		order += ["%03d_%03d" % (int(d_level), int(dkey))]

order.sort()


dic = {}

for line in all_lines:

	if "Main deduced [eq index]: " not in line:
		continue

	lsp = line.replace("Main deduced [eq index]: ", "").replace("\n", "").split(" ")

	for term in lsp:
		# term "0[k16]"
		f = open("superpolys/" + term.split("[")[0], "r")
		data = f.readlines()[0].replace("\n", "").split(" ")
		f.close()
		
		var = np.zeros(key_size, int)
		
		# mark var
		pt = 1
		for mi in range(int(data[0])):
			degree = int(data[pt])
			pt += 1

			if degree == 1:
				k = int(data[pt])
				pt += 1
				if var[k] == 0:
					var[k] = 1 # balanced
			else:
				for d in range(degree):
					k = int(data[pt])
					pt += 1
					var[k] = 2
		assert(pt == len(data))

		s = ""
		for k in range(key_size):
			if var[k] != 0:
				if s != "":
					s += " "
				s += str(k)

		assert(s not in dic)
		dic[s] = int(term.split("[k")[-1].split("]")[0])



all_files = glob.glob(logs_dir + "/*")
for filepath in all_files:

	var = np.zeros(key_size, int)

	f = open(filepath, "r")
	all_lines = f.readlines()
	f.close()

	# mark var
	for line in all_lines:
		lsp = line.split("  ")[0].split(" ")
		if len(lsp) == 1: # constants
			continue

		if len(lsp) == 2: # linear
			if var[int(lsp[1])] == 0:
				var[int(lsp[1])] = 1 # balanced
		else:
			for r in range(1, len(lsp)):
				cc[int(lsp[r])] += 1
				var[int(lsp[r])] = 2 # higher

	s = ""
	for k in range(key_size):
		if var[k] != 0:
			if s != "":
				s += " "
			s += str(k)

	if s in dic:
		if dic[s] >= 0 and var[dic[s]] == 1:
			os.system("cp %s %s" % (filepath, tar_dir))
			dic[s] = -1

