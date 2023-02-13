
import time

# @profile
def get_big_dct():
    with open('pp.txt') as f:
        for line in f:
            if line[0] == '#': _id = int(line[1::])
            else:
                item = int(float(line.split()[0])*100000)
                if item in big_dict:
                    if _id in big_dict[item]:
                        eq_dict[_id] = item
                    big_dict[item].add(_id)
                else:
                    big_dict[item] = {_id}

@profile
def cal_similar():
    final_dct = None
    with open('ss.txt') as s:
        with open('R.txt','w') as r:
            for item in s.readlines():
                if item[0] == '#':
                    if final_dct:
                        # 如果进入这个分支 说明一个数组已经计算完了
                        k = max(final_dct,key=final_dct.get)
                        r.write(f"{k}\t{final_dct[k]}\n")
                    visited = set()
                    final_dct = {i:0 for i in range(1,10001)}
                else:
                    item_val = int(float(item.split()[0])*100000)
                    
                    window_left = []
                    for i in range(item_val-999,item_val+1):
                        if i in big_dict:
                            window_left.append(i)
                            
                    window_right = []
                    for i in range(item_val+1000,item_val,-1):
                        if i in big_dict:
                            window_right.append(i)
                    
                    # todo 早退 一个循环
                    window_left = [i for i in range(item_val-999,item_val+1) if i in big_dict]
                    window_right = [i for i in range(item_val+1000,item_val,-1) if i in big_dict]
                    
                    # # 可以相似 但是还要做最后的距离比较 先存在可能相似的字典里
                    may_sim_dct = {}
                    for val in window_left:
                        for _id in big_dict[val]: 
                            may_sim_dct[_id] = val
                    for val in window_right:
                        for _id in big_dict[val]:
                            if _id not in may_sim_dct:
                                may_sim_dct[_id] = val
                            elif abs(val-item_val) < abs(may_sim_dct[_id]-item_val):
                                may_sim_dct[_id] = val

                    # 计数
                    for k, v in may_sim_dct.items():
                        if f"{k}-{v}" in visited: 
                            # print(f"{k}-{v}")
                            continue
                        # print(v)
                        final_dct[k] += 1
                        if k in eq_dict:
                            del eq_dict[k]
                            continue
                        visited.add(f"{k}-{v}")
            # for item .. 结束 
            k =  max(final_dct,key=final_dct.get)
            r.write(f"{k}\t{final_dct[k]}")

            
if __name__ == '__main__': 
    begin = time.time()
    big_dict, eq_dict = {}, {}
    get_big_dct()
    end = time.time()
    print(f"{end-begin}")
    # exit()
    cal_similar()
    end2 = time.time()
    print(f"{end2-end}")
    
    