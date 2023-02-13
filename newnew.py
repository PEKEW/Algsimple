import time

def file2multihash(filename):
    with open(filename, 'r') as f:    
        for line in f.readlines():
            if line[0] == '#': 
                _id = int(line.strip('#'))
            else:
                int_value, dim_value = line.strip().split('.')
                int_value, dim_value = int(int_value), int(dim_value)
                if int_value not in multihash:
                    multihash[int_value] = {dim_value:{_id}}
                elif dim_value not in multihash[int_value]:
                    multihash[int_value][dim_value] = {_id}
                elif _id not in multihash[int_value][dim_value]:
                    multihash[int_value][dim_value].add(_id)
                else:
                    eq_dict[_id] = [int_value, dim_value]


def cal_similar(s_values):
    similar_dct = {}
    visited = set()
    final_dct = {i:0 for i in range(1,10001)}
    for each in s_values:
        may_sim_dict = {}
        A, B = each.split('.')
        A = int(A)
        B = int(B)
        if A not in multihash: continue
        dim_part = multihash[A]
        if B in dim_part:
            id_set = dim_part[B]
            window_left = [i for i in range(B-999,B+1) if i in dim_part]
            window_right = [i for i in range(B+1000,B,-1) if i in dim_part]
            for val in window_left:
                for _id in id_set: 
                    may_sim_dict[_id] = val
            for val in window_right:
                for _id in id_set:
                    if _id not in may_sim_dict:
                        may_sim_dict[_id] = val
                    elif abs(val-B) < abs(may_sim_dict[_id]-B):
                        may_sim_dict[_id] = val
            # for distance in range(1000):
            #     item = B + distance
            #     if item in dim_part:
            #         for _id in id_set:
            #             may_sim_dict[_id] = [A,item]
            #     item = B - distance
            #     if item in dim_part:
            #         for _id in id_set:
            #             if _id not in may_sim_dict:
            #                 may_sim_dict[_id] = [A,item]
            #             else:
            #                 if distance < may_sim_dict[_id][1] - B:
            #                     may_sim_dict[_id] = [A,item]
        for k, v in may_sim_dict.items():
            if f"{k}-{v}" in visited: 
                print(f"{k}-{v}")
                continue
            # print(v)
            final_dct[k] += 1
            if k in eq_dict:
                del eq_dict[k]
                continue
            visited.add(f"{k}-{v}")
    k =  max(final_dct,key=final_dct.get)
    return k, final_dct[k]         
def get_max_similar():
    temp = set()
    with open('ss.txt', 'r') as f:
        with open('R.txt', 'w') as o:
            for line in f.readlines(): 
                if line[0] == '#' and len(temp) != 0:
                    key, bst  = cal_similar(temp)
                    o.write(f"{key}\t{bst}\n")
                    temp = set()
                elif line[0] != '#': temp.add(line.strip())
            key, bst = cal_similar(temp)
            o.write(f"{key}\t{bst}\n")

if __name__ == '__main__':
    begin = time.time()
    multihash = {}
    eq_dict = {}
    file2multihash('pp.txt')
    end = time.time() 
    # print(f"load time takes:{end-begin}")
    # exit()
    res = get_max_similar()
    finished = time.time()
    # print(f"algorithm takes:{finished-end}")