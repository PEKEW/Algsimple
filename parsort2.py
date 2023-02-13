from copy import deepcopy
import time
import bisect
from collections import Counter
import multiprocessing

class Node:
    def __init__(self, val, id) -> None:
        self.val = val
        self.id = [id]
        self.nxt = None
        
# @profile
def get_big_dct():
    hash_table = {}
    eq_dict = {}
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
        return hash_table, eq_dict, quick_table


def mission(max_len, hash_table, eq_dict, quick_table, datas, t_id,queue):
    _eq_dict = deepcopy(eq_dict)
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
    # return final_dct.most_common(1)[0]
   # print(f"Id:{t_id} want to Put Data to Queue")
    queue.put(final_dct.most_common(1)[0])
    #print(f"Id:{t_id} Put Over")

# @profile
def cal_similar(max_len, hash_table, eq_dict, quick_table,lock,queue):
    temp = []
    with open('S.txt') as s:
        with open('R.txt', 'w')  as r:
            proce = []
            for item in s.readlines():
                if item[0] == '#':
                    if len(temp) != 0:
                        t = multiprocessing.Process(target=mission, args=(max_len, hash_table, eq_dict, quick_table,temp, _id,queue))
                        proce.append(t)
                        t.start()
                        # k, v = mission(temp, _id)
                        #lock.acquire()
                        #k,v = queue.get()
                        #r.write(f"{k}\t{v}\n")
                        #lock.release()
                        temp = []          
                    _id = int(item[1::])
                else:
                    temp.append(item)
            for p in proce: p.join()
            for i in range(queue.qsize()):
                k,v = queue.get()
                r.write(f"{k}\t{v}\n")
            mission(max_len, hash_table, eq_dict, quick_table,temp, _id,queue)
            k,v=queue.get()

            r.write(f"{k}\t{v}\n")
if __name__ == '__main__': 
    lock = multiprocessing.Lock()
    queue = multiprocessing.Queue()
    begin = time.time()
    hash_table, eq_dict, quick_table = get_big_dct()
    max_len = len(quick_table)
    # just_visited_once()
    end = time.time()
    print(f"{end-begin}")
    # exit()
    cal_similar(max_len,hash_table, eq_dict, quick_table,lock,queue)
    end2 = time.time()
    print(f"{end2-end}")