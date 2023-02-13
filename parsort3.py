from copy import copy
import time
import bisect
from collections import Counter
import threading



hash_table = {}
eq_dict = {}
quick_table = []
max_len = 0
    
ret = {i:[] for i in range(1000)}
#########################################################################################
def get_data():
    global hash_table, eq_dict, quick_table, max_len
    print(f"load data ..")  
    begin = time.time()
    with open('P.txt') as f:
        for line in f.readlines():
            if line[0] == '#': _id = int(line.strip()[1::])
            else:
                item_val = int(float(line.split()[0])*100000)
                if item_val in hash_table:
                    if _id in hash_table[item_val].id:
                        eq_dict[_id] = item_val
                    hash_table[item_val].id.append(_id)
                else:
                    hash_table[item_val] = Node(item_val, _id)
        hash_table = {k: hash_table[k] for k in sorted(hash_table)}
        quick_table = list(hash_table.keys())
        max_len = len(quick_table)

    end = time.time()
    print(f"load data takes: {end-begin}")
############################################################################################

class Node:
    def __init__(self, val, id) -> None:
        self.val = val
        self.id = [id]
        self.nxt = None

def mission(datas,idx):
    #print("cal sim")
    global hash_table, eq_dict, quick_table, max_len, ret
    _eq_dict = copy(eq_dict)
    visited = set()
    final_dct = Counter()
    for item in datas:
        item_val = int(float(item.split()[0])*100000)
        may_sim_dct = {}
        search_begin = item_val-1000
        search_begin_idx = bisect.bisect_right(quick_table, search_begin)
        search_val = hash_table[quick_table[search_begin_idx]].val
        end_val = item_val+1000
        while True:
            if search_val>=end_val: break
            node = hash_table[search_val]
            if len(node.id) == 1:
                _id = node.id[0]
                if _id not in may_sim_dct:
                    may_sim_dct[_id] = search_val
                elif abs(search_val-item_val) < abs(may_sim_dct[_id]-item_val):
                    may_sim_dct[_id] = search_val
            else:
                for _id in node.id:
                    if _id not in may_sim_dct:
                        may_sim_dct[_id] = search_val
                    elif abs(search_val-item_val) < abs(may_sim_dct[_id]-item_val):
                        may_sim_dct[_id] = search_val
            search_begin_idx += 1
            if search_begin_idx >= max_len:break
            search_val = hash_table[quick_table[search_begin_idx]].val
        for k, v in may_sim_dct.items():
            set_key = k*10000000000+v
            if set_key in visited:
                continue
            final_dct[k] += 1
            if k in _eq_dict:
                del _eq_dict[k]
                continue
            visited.add(set_key)
    # lock.acquire()
    ret[idx] = final_dct.most_common(1)[0]
    # lock.release()
    #print("cal sim over")

# @profile
def cal_similar(lock,queue):
    #print("cal sim")
    temp = []
    with open('S.txt') as s:
        with open('R.txt', 'w')  as r:
            proce = []
            for item in s.readlines():
                if item[0] == '#':
                    if len(temp) != 0:
                        # t = multiprocessing.Process(target=mission, args=(max_len, hash_table, eq_dict, quick_table,temp, _id,queue))
                        t = threading.Thread(target=mission, args=(temp,_id,queue))
                        proce.append(t)
                        t.start()
                        lock.acquire()
                        k,v = queue.get()
                        r.write(f"{k}\t{v}\n")
                        lock.release()
                        temp = []     
                    _id = int(item[1::])
                else:
                    temp.append(item)
            for p in proce: 
                p.close()
                p.join()
            k, v = mission(temp, _id)

            r.write(f"{k}\t{v}\n")
    #print("cal sim over")



def main():
    global hash_table, eq_dict, quick_table, max_len, ret
    lock = threading.Lock()
    begin = time.time()
    with open('S.txt') as s:
        datas, temp = [], []
        for item in s.readlines():
            if item[0] == '#': 
                if len(temp):
                    datas.append(temp)
                    temp =  []
            else: temp.append(item)
        datas.append(temp)
    proce = []
    for i, data in enumerate(datas):
        p = threading.Thread(target=mission, args=(data,i))
        p.start()
        proce.append(p)
    for p in proce: p.join()
    end = time.time()
    print(f"search time:{end - begin}")
    with open('R.txt', 'w') as r:
        # print(ret)
        for k,v in ret.values(): r.write(f"{k}\t{v}\n")

if __name__ == '__main__': 
    get_data()
    main()
    

    
