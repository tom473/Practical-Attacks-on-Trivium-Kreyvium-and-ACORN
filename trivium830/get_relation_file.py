# -*- coding: utf-8 -*-


import glob
import os

all_candidates = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,30,32,33,34,35,37,39,41,43,44,47,49,51,53,55,57,59,61,64,66,68,70,72,74,76,77,78]

all_files = glob.glob("./polys_used_to_attack/*")


for file in all_files:

    f = open(file, "r+")
    all_lines = f.readlines()
    f.close()
 
    all_terms = {}
    for line in all_lines:
        term = line.strip()
        line = line.strip().split(" ")

        if line[0] == "":
            continue
        
        if term not in all_terms.keys():
            all_terms[term] = 0
        all_terms[term] += 1
    
    independent = set()
    related = set()
    linear = set()

    for term in all_terms.keys():
        if all_terms[term] % 2 == 0:
            continue

        line = term.split(" ")

        if len(line) == 1:
            linear.add(int(line[0]))

        if len(line) == 1 and int(line[0]) not in related:
            independent.add(int(line[0]))
            continue

        for item in line:
            var = int(item)
            related.add(var)

            if var in independent:
                independent.remove(var)
    
    if len(independent) == 0:
        continue
        
    print(file)
    cube_str = file.split("/")[-1].split(".")[0].replace("v", "").split("_")[2:-1]
    cube = [int(v) for v in cube_str]
    for v in all_candidates:
        if v in cube:
            continue
        print(f"v{v}")
        break
    
    print(f"linear: {linear}")
    print(f"independent: {independent}")
    print(f"related: {related}\n")






