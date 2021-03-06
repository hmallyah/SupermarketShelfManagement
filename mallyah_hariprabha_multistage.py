import sys
import os
import string
import itertools
import copy

basket_list = []
support = 0
hash_table_size = 0
max_basket_size = 0
candidate_itemsets = {}
frequent_itemsets = {}
candidate_count = {}
item_list = []
item_count = {}
item_hash_value = {}
itemsets_list = []
temp = []
itemsets_dict = {}


with open(sys.argv[1]) as inputfile:
    for line in inputfile:
        line = line.strip('\n')
        line = line.split(',')
        basket_list.append(line)
support = int(sys.argv[2])
hash_table_size = int(sys.argv[3])

for basket in basket_list:
    if len(basket) > max_basket_size:
        max_basket_size = len(basket)

for i in range(1, max_basket_size + 1):
    candidate_itemsets[i] = []
    frequent_itemsets[i] = []
    candidate_count[i] = []

for basket in basket_list:
    for item in basket:
        item_list.append(item)
        item_count[item] = 0
item_list = list(set(item_list))
item_list = sorted(item_list)

for basket in basket_list:
    for item in basket:
        item_count[item] += 1

for item in item_count:
    if item_count[item] >= support:
        frequent_itemsets[1].append(item)
candidate_itemsets[1] = item_list

for i in range(0,len(item_list)):
    item_hash_value[item_list[i]] = i

from itertools import combinations
for basket in basket_list:
    for i in range(2,len(basket)+1):
        itemsets_list.append([",".join(map(str,comb)) for comb in combinations(sorted(basket), i)])

for each_list in itemsets_list:
    for each_comb in each_list:
        temp.append(each_comb.split(','))

for i in range(2,max_basket_size+1):
    itemsets_dict[i] = []

for each_list in temp:
    itemsets_dict[len(each_list)].append(each_list)

def multistage(p, support, itemsets = [], frequents_prev = []):
    hash_table_1 = {}
    bucket_table_1 = {}
    bitmap1  = []
    temp1 = []
    hash_table_2 = {}
    bucket_table_2 = {}
    bitmap2  = []
    temp2 = []
    candidates = []
    candidatecount = []
    frequents = []

    for x in range(0, hash_table_size):
        hash_table_1[x] = 0
        bucket_table_1[x] = []
        bitmap1.append(0)
        hash_table_2[x] = 0
        bucket_table_2[x] = []
        bitmap2.append(0)

    if p == 2:
        for itemset in itemsets:
            itemset_hashvalue = 0
            bucket = 0
            for items in itemset:
                itemset_hashvalue += item_hash_value[items]
            bucket = itemset_hashvalue % hash_table_size
            hash_table_1[bucket] += 1
            bucket_table_1[bucket].append(itemset)

        for key in hash_table_1:
            if hash_table_1[key] >= support:
                bitmap1[key] = 1


        for n in range(0,hash_table_size):
            if bitmap1[n] == 1:
                for itemset in bucket_table_1[n]:
                    temp1.append(itemset)

        for itemset in temp1:
            itemset_hashvalue = 1
            bucket = 0
            for items in itemset:
                itemset_hashvalue *= item_hash_value[items]
            bucket = itemset_hashvalue % hash_table_size
            hash_table_2[bucket] += 1
            bucket_table_2[bucket].append(itemset)

        for key in hash_table_2:
            if hash_table_2[key] >= support:
                bitmap2[key] = 1

        for n in range(0,hash_table_size):
            if bitmap2[n] == 1:
                for itemset in bucket_table_2[n]:
                    temp2.append(itemset)

        for itemset in temp2:
            count = 0
            for item in itemset:
                if item in frequents_prev:
                    count += 1
            if count == 2:
                candidates.append(itemset)
        candidates.sort()
        candidates = list(candidates for candidates,_ in itertools.groupby(candidates))

    else:
        for itemset in itemsets:
            immediate_subset = []
            immediate_subset_temp = []
            check_candidacy = []
            immediate_subset_temp.append([",".join(map(str,comb)) for comb in combinations(itemset, i-1)])

            for each_list in immediate_subset_temp:
                for each_comb in each_list:
                    immediate_subset.append(each_comb.split(','))

            for each_list in immediate_subset:
                for freq_itemset in frequents:
                    if each_list == freq_itemset:
                        check_candidacy.append(each_list)
            if len(immediate_subset) == len(check_candidacy):
                temp1.append(itemset)

        temp1.sort()
        temp1 = list(temp1 for temp1,_ in itertools.groupby(temp1))

        for itemset in temp1:
            itemset_hashvalue = 0
            bucket = 0
            for items in itemset:
                itemset_hashvalue += item_hash_value[items]
            bucket = itemset_hashvalue % hash_table_size
            hash_table_1[bucket] += 1
            bucket_table_1[bucket].append(itemset)

        for key in hash_table_1:
            if hash_table_1[key] >= support:
                bitmap1[key] = 1

        for n in range(0,hash_table_size):
            if bitmap1[n] == 1:
                for itemset in bucket_table_1[n]:
                    temp2.append(itemset)

        for itemset in temp2:
            itemset_hashvalue = 1
            bucket = 0
            for items in itemset:
                itemset_hashvalue *= item_hash_value[items]
            bucket = itemset_hashvalue % hash_table_size
            hash_table_2[bucket] += 1
            bucket_table_2[bucket].append(itemset)

        for key in hash_table_2:
            if hash_table_2[key] >= support:
                bitmap2[key] = 1

        for n in range(0,hash_table_size):
            if bitmap2[n] == 1:
                for itemset in bucket_table_2[n]:
                    candidates.append(itemset)

    candidate_itemsets[p] = copy.deepcopy(candidates)

    candidatecount = copy.deepcopy(candidates)
    for candidate in candidatecount:
        candidate.append(0)

    for m in range(0, len(candidates)):
        for n in range(0, len(itemsets)):
            if candidates[m] == itemsets[n]:
                candidatecount[m][p] += 1

    for c in range(0, len(candidatecount)):
        if candidatecount[c][p] >= support:
            frequents.append(candidates[c])

    if p == 2:
        if len(frequents) != 0:
            print("memory for hash table 1 counts for size "+str(p)+" itemsets: "+str(hash_table_size*4))
            print(str(hash_table_1))
            print("frequent itemsets of size "+str(p-1)+" : "+str(sorted(frequents_prev))+'\n')
            print("memory for frequent itemsets of size "+str(p-1)+" : "+str(len(frequents_prev)*8))
            print("bitmap 1 size: "+str(len(bitmap1)))
            print("memory for hash table 2 counts for size "+str(p)+" itemsets: "+str(hash_table_size*4))
            print(str(hash_table_2)+'\n')
            print("memory for frequent itemsets of size "+str(p-1)+" : "+str(len(frequents_prev)*8))
            print("bitmap 1 size: "+str(len(bitmap1)))
            print("bitmap 2 size: "+str(len(bitmap2)))
            print("memory for candidates counts of size "+str(p)+" : "+str(len(candidatecount)*(i+1)*4))
            print("frequent itemsets of size "+str(p)+" : "+str(sorted(frequents))+'\n')

    else:
        if len(frequents) != 0:
            print("memory for frequent itemsets of size "+str(p-1)+" : "+str(len(frequents_prev)*8))
            print("memory for hash table 1 counts for size "+str(p)+" itemsets: "+str(hash_table_size*4))
            print(str(hash_table_1)+'\n')
            print("bitmap 1 size: "+str(hash_table_size))
            print("memory for hash table 2 counts for size "+str(p)+" itemsets: "+str(hash_table_size*4))
            print(str(hash_table_2)+'\n')
            print("bitmap 1 size: "+str(len(bitmap1)))
            print("bitmap 2 size: "+str(len(bitmap2)))
            print("memory for candidates counts of size "+str(p)+" : "+str(len(candidatecount)*(i+1)*4))
            print("frequent itemsets of size "+str(p)+" : "+str(sorted(frequents))+'\n')

    return frequents
'''
    if len(frequents) != 0:
        print "memory for hash table 1 counts for size " + str(p) + " itemsets: " + str(hash_table_size*4)
        print hash_table_1
        print "frequent itemsets of size " + str(p-1) + ":"
        print sorted(frequents)
        print "memory frequent itemsets of size " + str(p-1) + ": " + str(len(frequents)*8)
        print "bitmap size: " + str(len(bitmap1))
        print "memory for hash table 2 counts for size " + str(p) + " itemsets: " + str(hash_table_size*4)
        print hash_table_1
        print "memory frequent itemsets of size " + str(p-1) + ": " + str(len(frequents)*8)
        print "bitmap 1 size: " + str(len(bitmap1))
        print "bitmap 2 size: " + str(len(bitmap2))
        print "memory for candidates counts of size " + str(p) + ": " + str(len(candidatecount)*(i+1)*4)
        print "frequent itemsets of size " + str(p) + ":"
        print frequents
'''


print "memory for item counts:" + str(len(item_count)*8)
for p in range(2,max_basket_size+1):
    frequent_itemsets[p] = multistage(p, support, itemsets_dict[p], frequent_itemsets[p-1])
    #print len(candidate_itemsets[p]),len(frequent_itemsets[p])

