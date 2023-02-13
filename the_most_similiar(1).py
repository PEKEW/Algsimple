
import time

# ! important 尽可能少地创建对象
# ! important 最相似的查找逻辑有问题
    

class HashNode:
    # @profile
    def __init__(self, list_value:str, id) -> None:
        # id 和 sed value 是要保证有序相对的 不能用集合
        # 需要索引sed value值 所以sed value应该作为key
        # self.extra_info = queue.Queue()
        # self.extra_info.put((int(list_value[2:5]), id))
        self.unique_id = 1
        self.extra_info = {}
        self.extra_info[0] = (int(list_value[2:5]), id)
        
    def merge(self, list_value, id) -> None:
        # self.extra_info.put((int(list_value[2:5]), id))
        self.extra_info[self.unique_id] = (int(list_value[2:5]), id)
        self.unique_id += 1
        
        

class HashList:
    def __init__(self, fst_value, node) -> None:
        # self.items.keys 就是first value
        self.items = {fst_value: node}
        self.quick_table = {fst_value, fst_value+1, fst_value-1}
    
    # @profile
    def append(self, list_value, id) -> None:
        fst_value = int(list_value[0:2])
        if fst_value in self.items:
            self.items[fst_value].merge(list_value, id)
        else:
            self.items[fst_value] = HashNode(list_value, id)
        self.quick_table |= {fst_value, fst_value+1, fst_value-1}

class MultiHash:
    def __init__(self) -> None:
        self.head:dict = {}
    
    # @profile
    def append(self, id: int, item: str) -> None:
        head_value, list_value = item.split('.')
        head_value = int(head_value)
        if head_value not in self.head:
            node = HashNode(list_value, id)
            fst_value = int(list_value[0:2])
            self.head[head_value] = HashList(fst_value, node)
        else:
            self.head[head_value].append(list_value, id)

# @profile
def file2multihash(filename: str) -> MultiHash:
    multihash = MultiHash()
    append = multihash.append
    with open(filename, 'r') as f:    
        for line in f.readlines():
            if line[0] == '#': 
                id = int(line.strip('#'))
            else:
                item = line.strip()
                append(id, item)
    return multihash

# @profile
def cal_similar(s_values:set, record):
    # {id: [set_key:int,similar_value:int]}
    similar_dct = {0:[0,0]}
    # 访问集合
    visited = set()
    visited_add = visited.add
    for each in s_values:
        distance_dct = {0:999}
        A, B_C = each.split('.')
        A = int(A)
        fst_value, sed_value = int(B_C[0:2]), int(B_C[2:5])
        # 如果head都不匹配 那就不用后续计算了
        if A not in record.head: continue
        # fst value 是小数点后两位*100 如果本位和上进位下进位不在快表 那说明A作为head, 没有相差在0.02的记录
        elif (fst_value not in record.head[A].quick_table) and \
            (fst_value+1 not in record.head[A].quick_table) and \
            (fst_value-1 not in record.head[A].quick_table): continue
        else:
            # cur_id 当前记录之前匹配的ID 如果之前和这一次匹配的ID一致 那就不重复计数
            cur_id = set()
            cur_id_add = cur_id.add

            if fst_value in record.head[A].items:
                iter_item_extra_info = record.head[A].items[fst_value].extra_info
                for _, (node_sed_value, node_id) in iter_item_extra_info.items():
                    set_key = node_id*10000000000000+A*1000000000+fst_value*10000+node_sed_value
                    if (set_key not in visited) and (node_id not in cur_id):
                        # 先放到字典里 随后再一起统计
                        cur_distance = abs(node_sed_value-sed_value)
                        if node_id not in distance_dct:
                            distance_dct[node_id] = cur_distance
                            if node_id not in similar_dct:
                                similar_dct[node_id] = [set_key,1]
                            else:
                                similar_dct[node_id] = [set_key,similar_dct[node_id][1]+1]
                        elif cur_distance <= distance_dct[node_id]:
                            distance_dct[node_id] = cur_distance
                            similar_dct[node_id] = [set_key,similar_dct[node_id][1]+1]

            if fst_value-1 in record.head[A].items:
                cur_fst_value = fst_value-1
                iter_item_extra_info = record.head[A].items[cur_fst_value].extra_info
                for _, (node_sed_value, node_id) in iter_item_extra_info.items():
                    set_key = node_id*10000000000000+A*1000000000+cur_fst_value*10000+node_sed_value
                    if (node_sed_value > sed_value) and \
                        (set_key not in visited) and \
                            (node_id not in cur_id):
                        # cur_distance = abs(node_sed_value-sed_value)
                        cur_distance = abs(node_sed_value-sed_value)
                        if node_id not in distance_dct:
                            distance_dct[node_id] = cur_distance
                            if node_id not in similar_dct:
                                similar_dct[node_id] = [set_key,1]
                            else:
                                similar_dct[node_id] = [set_key,similar_dct[node_id][1]+1]
                        elif cur_distance <= distance_dct[node_id]:
                            distance_dct[node_id] = cur_distance
                            similar_dct[node_id] = [set_key,similar_dct[node_id][1]+1]
            if fst_value+1 in record.head[A].items:
                cur_fst_value = fst_value+1
                iter_item_extra_info = record.head[A].items[cur_fst_value].extra_info
                for _, (node_sed_value, node_id) in iter_item_extra_info.items():
                    # 高进位和低进位逻辑类似
                    set_key = node_id*10000000000000+A*1000000000+cur_fst_value*10000+node_sed_value
                    if (node_sed_value < sed_value) and\
                        (set_key not in visited) and\
                            (node_id not in cur_id):
                        cur_distance = abs(node_sed_value-sed_value)
                        if node_id not in distance_dct:
                            distance_dct[node_id] = cur_distance
                            if node_id not in similar_dct:
                                similar_dct[node_id] = [set_key,1]
                            else:
                                similar_dct[node_id] = [set_key,similar_dct[node_id][1]+1]
                        elif cur_distance <= distance_dct[node_id]:
                            distance_dct[node_id] = cur_distance
                            similar_dct[node_id] = [set_key,similar_dct[node_id][1]+1]

            for node_id, val in similar_dct.items():
                visited_add(val[0])
                cur_id_add(val[1])
    # best_key = max(similar_dct, key=similar_dct.get)
    best_key = None
    best_value = 0
    for k, val in similar_dct.items():
        if val[1]>best_value:
            best_value = val[1]
            best_key = k
    return best_key, best_value

# @profile             
def get_max_similar(record):
    temp = set()
    with open('ss.txt', 'r') as f:
        with open('R.txt', 'w') as o:
            for line in f.readlines(): 
                if line[0] == '#' and len(temp) != 0:
                    key, bst  = cal_similar(temp, record)
                    o.write(f"{key}\t{bst}\n")
                    temp = set()
                elif line[0] != '#': temp.add(line.strip())
            key, bst = cal_similar(temp, record)
            o.write(f"{key}\t{bst}\n")
            
if __name__ == '__main__':
    begin = time.time()
    regular_p = file2multihash('pp.txt')
    end = time.time() 
    print(f"load time takes:{end-begin}")
    # exit()
    res = get_max_similar(regular_p)
    finished = time.time()
    print(f"algorithm takes:{finished-end}")