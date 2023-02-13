import time

class SimilarDct:
    def __init__(self) -> None:
        self.dct = {}
        self.bst_key = None
        self.bst_value = 0
    
    def record(self, k):
        if k in self.dct.keys():
            self.dct[k] += 1
        else:
            self.dct[k] = 1
        if self.bst_value < self.dct[k]:
            self.bst_value = self.dct[k]
            self.bst_key = k
    def ret(self):
        return self.bst_key, self.bst_value
    

class HashNode:
    def __init__(self, list_value, id) -> None:
        self.fst_value = list_value[0:2]
        self.sed_value = [list_value[2::]]
        self.id = [id]
        
    def merge(self, new_node) -> None:
        self.sed_value.append(new_node.sed_value[0])
        self.id.append(new_node.id[0])

class HashList:
    def __init__(self) -> None:
        self.items = [None] * 100
        self.quick_table = []
        
    def append(self, node: HashNode) -> None:
        if self.items[int(node.fst_value)]:
            self.items[int(node.fst_value)].merge(node)
        else:
            self.items[int(node.fst_value)] = node
        self.quick_table.append(int(node.fst_value))
        self.quick_table.append(int(node.fst_value)+1)
        self.quick_table.append(int(node.fst_value)-1)
        self.quick_table = list(set(self.quick_table))

class MultiHash:
    def __init__(self) -> None:
        self.head:dict = {}
        
    def append(self, id: int, item: str) -> None:
        head_value, list_value = item.split('.')
        head_value, list_value = head_value, list_value
        node = HashNode(list_value, id)
        if head_value not in self.head:
            self.head[head_value] = HashList()
        self.head[head_value].append(node)
    
def file2multihash(filename: str) -> MultiHash:
    with open(filename, 'r') as f:
        multihash = MultiHash()
        for line in f.readlines():
            if line[0] == '#': 
                id: int = int(line.strip('#'))
            else:
                item: str = line.strip()
                multihash.append(id, item)
    return multihash

def cal_similar(s_values, record):
    similar_dct = SimilarDct()
    # 访问集合
    visited = set()
    for each in s_values:
        A, B_C = each.split('.')
        fst_value, sed_value = B_C[0:2], B_C[2::]
        fst_value, sed_value = int(fst_value), int(sed_value)
        # 如果head都不匹配 那就不用后续计算了
        if A not in record.head: continue
        
        # fst value 是小数点后两位*100 如果本位和上进位下进位不在快表 那说明A作为head, 没有相差在0.02的记录
        elif (fst_value not in record.head[A].quick_table) and \
            (fst_value+1 not in record.head[A].quick_table) and \
            (fst_value-1 not in record.head[A].quick_table): continue
        else:
            # cur_id 当前记录之前匹配的ID 如果之前和这一次匹配的ID一致 那就不重复计数
            cur_id = set()
            if record.head[A].items[fst_value]:
                for idx, node_sed_value in enumerate(record.head[A].items[fst_value].sed_value):
                    cur_idx = record.head[A].items[fst_value].id[idx]
                    set_key = A +'.'+ str(fst_value) + node_sed_value + '#' + str(cur_idx)
                    # 如果本位匹配 那无论sed value为何值 差距都会小于0.01 直接找一个没有访问过的即可
                    
                    if (set_key not in visited) and (cur_idx not in cur_id):
                        # 标记访问 后续不再使用这个节点
                        visited.add(set_key)
                        similar_dct.record(cur_idx)
                        cur_id.add(cur_idx)
            # 边界处理
            if fst_value-1 > -1 and record.head[A].items[fst_value-1]:
                for idx, node_sed_value in enumerate(record.head[A].items[fst_value-1].sed_value):
                    cur_idx = record.head[A].items[fst_value-1].id[idx]
                    set_key = A +'.'+  str(fst_value-1) + node_sed_value + '#' + str(cur_idx)
                    # 没有在本位找到 那就在低进位查找 要求小数点后第三位-末尾(sed value) 大于当前查找项的小数点后第三位-末尾
                    # e.g. 100.6384 <-> 100.6371 => 0.013
                    #      100.6384 <-> 100.6375 => 0.009
                    if (int(node_sed_value) > sed_value) and \
                        (set_key not in visited) and \
                            (cur_idx not in cur_id):
                        # 找到这样的记录 且没有被访问过
                        visited.add(set_key)
                        similar_dct.record(cur_idx)
                        cur_id.add(cur_idx)
                        
            if fst_value+1 < 100 and record.head[A].items[fst_value+1]:
                for idx, node_sed_value in enumerate(record.head[A].items[fst_value+1].sed_value):
                    cur_idx = record.head[A].items[fst_value+1].id[idx]
                    # 高进位和低进位逻辑类似
                    set_key = A +'.'+  str(fst_value+1) + node_sed_value + '#' + str(cur_idx)
                    if (int(node_sed_value) < sed_value) and\
                        (set_key not in visited) and\
                            (cur_idx not in cur_id):
                        visited.add(set_key)
                        similar_dct.record(cur_idx)
                        cur_id.add(cur_idx)
    return similar_dct.ret()
                
def get_max_similar(record):
    temp = []
    with open('S.txt', 'r') as f:
        with open('R.txt', 'w') as o:
            for line in f.readlines(): 
                if line[0] == '#' and len(temp) != 0:
                    key, bst  = cal_similar(temp, record)
                    o.write(f"{key}\t{bst}\n")
                    temp = []
                elif line[0] != '#': temp.append(line.strip())
            key, bst = cal_similar(temp, record)
            o.write(f"{key}\t{bst}\n")
            
if __name__ == '__main__':
    begin = time.time()
    regular_p = file2multihash('P.txt')
    end = time.time() 
    print(f"load time takes:{end-begin}")
    res = get_max_similar(regular_p)
    finished = time.time()
    print(f"algorithm takes:{finished-end}")