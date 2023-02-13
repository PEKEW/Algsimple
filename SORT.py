import time
import bisect
from collections import Counter

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
        for line in f:
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
        pre_key = None
        for key in hash_table.keys():
            if pre_key == None:
                pre_key = key
            else:
                hash_table[pre_key].nxt = key
                pre_key = key
        return hash_table, eq_dict, list(hash_table.keys())
#@profile
def cal_similar():
    final_dct = None
    with open('S.txt') as s:
        with open('R.txt', 'w')  as r:
            for item in s.readlines():
                if item[0] == '#':
                    if final_dct:
                        k, v = final_dct.most_common(1)[0]
                        r.write(f"{k}\t{v}\n")
                    visited = set()
                    final_dct = Counter()
                else:
                    item_val = int(float(item.split()[0])*100000)
                    may_sim_dct = {}
                    search_begin = item_val-1000
                    search_begin_idx = bisect.bisect_right(quick_table, search_begin)
                    search_val = hash_table[quick_table[search_begin_idx]].val
                    end_val = item_val+1000
                    while True:
                        if search_val>end_val: break
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
                        if not node.nxt:break
                        search_val = hash_table[node.nxt].val
                    for k, v in may_sim_dct.items():
                        set_key = k*10000000000+v
                        if set_key in visited:
                            continue
                        final_dct[k] += 1
                        if k in eq_dict:
                            del eq_dict[k]
                            continue
                        visited.add(set_key)
            # for item .. 结束 
            k, v = final_dct.most_common(1)[0]
            r.write(f"{k}\t{v}")                 
if __name__ == '__main__': 
    begin = time.time()
    hash_table, eq_dict, quick_table = get_big_dct()
    end = time.time()
    print(f"{end-begin}")
    # exit()
    cal_similar()
    end2 = time.time()
    print(f"{end2-end}")