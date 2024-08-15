# -*- coding: utf-8 -*-


import glob


all_files = glob.glob("./polys_used_to_attack/*.txt")

all_relations = []

for file in all_files:
    print(file)
    file_name = file.split("/")[-1].split(".")[0].split("_")
    k = int(file_name[1][1:])

    f = open(file, "r+")
    all_lines = f.readlines()
    f.close()

    relation = []
    for line in all_lines:
        line = line.strip().split(" ")
        for v in line:
            v = int(v)
            if v == k or v in relation:
                continue
            relation.append(v)
    
    relation = sorted(relation)
    all_relations.append((relation, k))

guess = [0,2,4,9,11,14,15,16,17,18,19,21,24,28,29,33,34,35,40,41,42,43,44,45,46,47,48,49,50,51,53,54,57,58,59,60,61,62,63,64,65,66,67,68,70,71,72,73,74,75,76,77,78,79]
print(len(guess))

cnt = 0
while cnt < 80:
    print(cnt)
    for relation in all_relations:
        if relation[1] in guess:
            continue

        flag = True
        for v in relation[0]:
            if v not in guess:
                flag = False
                break

        if flag:
            guess.append(relation[1])
            print(f"deduce {relation[1]}")
    
    cnt += 1
    
    if len(guess) == 80:
        print("success")
        break
    



