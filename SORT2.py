import time
import bisect
# todo Counter

class Node:
    def __init__(self, val, id) -> None:
        self.val = val
        self.multId = False
        self.idSig = id
        self.id = {id}
        self.nxt = None

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
                        hash_table[item_val].multId = True
                    hash_table[item_val].id.add(_id)
                else:
                    hash_table[item_val] = Node(item_val, _id)

        hash_table = dict(sorted(hash_table.items(), key=lambda x: x[1].val))
        pre_Node = None
        for key in hash_table.keys():
            if pre_Node == None:
                pre_Node = hash_table[key];
            else:
                pre_Node.nxt = hash_table[key]
                pre_Node = pre_Node.nxt
        return hash_table, eq_dict, list(hash_table.keys())
# @profile
def cal_similar():
    final_dct = None
    with open('S.txt') as s:
        with open('R.txt', 'w')  as r:
            for item in s.readlines():
                if item[0] == '#':
                    if final_dct:
                        k = max(final_dct, key=(final_dct.get))
                        r.write(f"{k}\t{final_dct[k]}\n")
                    visited = set()
                    final_dct = {i:0 for i in range(1,10001)}
                else:
                    item_val = int(float(item.split()[0])*100000)
                    may_sim_dct = {}
                    search_begin = item_val-1000
                    search_begin_idx = bisect.bisect_right(quick_table, search_begin)
                    node = hash_table[quick_table[search_begin_idx]]
                    search_val = node.val
                    while True:
                        if search_val>item_val+1000: break
                        if node.multId:
                            for _id in node.id:
                                if _id not in may_sim_dct:
                                    may_sim_dct[_id] = search_val
                                elif abs(search_val-item_val) < abs(may_sim_dct[_id]-item_val):
                                    may_sim_dct[_id] = search_val
                        else:
                            _id = node.idSig
                            if _id not in may_sim_dct:
                                may_sim_dct[_id] = search_val
                            elif abs(search_val-item_val) < abs(may_sim_dct[_id]-item_val):
                                may_sim_dct[_id] = search_val
                        if node.nxt == None:break
                        node = node.nxt
                        search_val = node.val
                    for k, v in may_sim_dct.items():
                        if f"{k}-{v}" in visited:
                            continue
                        final_dct[k] += 1
                        if k in eq_dict:
                            del eq_dict[k]
                            continue
                        visited.add(f"{k}-{v}")
            # for item .. 结束 
            k = max(final_dct,key=final_dct.get)
            r.write(f"{k}\t{final_dct[k]}")                 
if __name__ == '__main__': 
    
    
    begin = time.time()
    hash_table, eq_dict, quick_table = get_big_dct()
    end = time.time()
    print(f"{end-begin}")
    # exit()
    cal_similar()
    end2 = time.time()
    print(f"{end2-end}")