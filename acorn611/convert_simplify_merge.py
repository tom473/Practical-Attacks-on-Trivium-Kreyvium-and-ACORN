

import glob
import os
import numpy as np



######################################################

logs_dir = "all_superpolys"

tar_dir = "superpolys"

key_size = 128


#######################################################

if os.path.exists(tar_dir):
	os.system("rm -r " + tar_dir)
os.system("mkdir " + tar_dir)


print("step 1: load relation and remove duplicated ones")

all_files = glob.glob(logs_dir + "/*")

all_relations = {} # iterm format: "x x x x x", where the first one is deduced by the others.
count = 0
for filepath in all_files:

	if count > 0 and count % 100 == 0:
		print("%d / %d, # all_relations %d" % (count, len(all_files), len(all_relations)))
	count += 1

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
				var[int(lsp[r])] = 2 # higher

	for dk in range(key_size):
		if var[dk] != 1: # balanced
			continue

		# dk is balanced
		line = str(dk)
		for other in range(key_size):
			if other == dk or var[other] == 0:
				continue

			line += " " + str(other)

		all_relations[line] = 0

print("Got %d raw relations from %d files\n" % (len(all_relations), count))








print("step 2: remove cover ralations")

def is_redundant(tar_relation, unchecked, checked):

	workspace = np.zeros(key_size, int)
	lsp = tar_relation.split(" ")
	tar_var = int(lsp[0])

	for i in range(1, len(lsp)):
		workspace[int(lsp[i])] = 1
	assert(workspace[tar_var] == 0)

	updated = True
	while updated:
		updated = False

		for dt in checked:
			dtlsp = dt.split(" ")
			if workspace[int(dtlsp[0])] == 1:
				continue
			fit = True
			for i in range(1, len(dtlsp)):
				if workspace[int(dtlsp[i])] == 0:
					fit = False
					break
			if fit:
				if int(dtlsp[0]) == tar_var:
					return True
				workspace[int(dtlsp[0])] = 1
				updated = True

		for dt in unchecked:
			dtlsp = dt.split(" ")
			if workspace[int(dtlsp[0])] == 1:
				continue
			fit = True
			for i in range(1, len(dtlsp)):
				if workspace[int(dtlsp[i])] == 0:
					fit = False
					break
			if fit:
				if int(dtlsp[0]) == tar_var:
					return True
				workspace[int(dtlsp[0])] = 1
				updated = True

	return False


sim_relations = {}

old_num = len(all_relations)
count = 0
for _ in range(len(all_relations)):

	if count > 0 and count % 100 == 0:
		print("%d / %d, # sim_relations %d" % (count, old_num, len(sim_relations)))
	count += 1

	dt = all_relations.popitem()[0]

	if not is_redundant(dt, all_relations, sim_relations):
		sim_relations[dt] = 0

print("Got %d simplified relations from %d raw relations\n" % (len(sim_relations), count))






print("step 3: merge ralations")

new_relations = {}
count = 0
for dt in sim_relations:

	if count > 0 and count % 100 == 0:
		print("%d / %d, new_relations %d" % (count, len(sim_relations), len(new_relations)))
	count += 1

	lsp = dt.split(" ")
	dk = int(lsp[0])

	ss = []
	for it in lsp:
		ss += [int(it)]	
	ss.sort()

	term = "%03d" % (len(ss))
	for it in ss:
		term += " " + str(it)

	if term in new_relations:
		new_relations[term] += [dk]
	else:
		new_relations[term] = [dk]

new_relations = sorted(new_relations.items())


print("=" * 64)


count = 0
for st in new_relations:

	newname = tar_dir + "/%d" % count
	count += 1

	print(count, ":", st)

	n = 0
	line = ""
	deduce_keys = st[1]
	lsp = st[0].split(" ")
	other = ""
	n_other = 0

	for i in range(1, len(lsp)):

		key = int(lsp[i])

		if key in deduce_keys:
			n += 1
			line += " 1 %d" % (key)
		else:
			n_other += 1
			other += " %d" % (key)

	if n_other > 0:
		n += 1
		line += " %d%s" % (n_other, other)

	line = str(n) + line


	out = open(newname, "w")
	out.write(line + "\n")
	out.close()



