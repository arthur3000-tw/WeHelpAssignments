#
##########
# Task 1 #
##########
#
# 從 messages 中找出大家的位置，依據目前位置輸出距離最近的人
# 大家位於台北捷運綠線上，距離遠近定義為相隔車站數量
#
# 建立台北捷運綠線 dictionary，依序賦予每一站一個值，為了解決小碧潭支線，分為上下行，往新店方向與往松山方向進行賦值
# 
# 從 message 中提取出名字與站名關係
#   走訪每個 message 內容，與車站名稱比對
#   輸出人名(key)對車站名稱(value)的 dictionary
#
# 計算距離關係
#   走訪每個人的位置資訊，計算出相對距離
#   輸出人名(key)對距離資訊(value)的 dictionary
#
# 找出最近距離的人
#
# 建立台北捷運綠線資訊與座標
taipei_mrt_greenline = {
    "Songshan":[0,18],
    "Nanjing Sanmin":[1,17],
    "Taipei Arena":[2,16],
    "Nanjing Fuxing":[3,15],
    "Songjiang Nanjing":[4,14],
    "Zhongshan":[5,13],
    "Beimen":[6,12],
    "Ximen":[7,11],
    "Xiaonanmen":[8,10],
    "Chiang Kai-Shek Memorial Hall":[9,9],
    "Guting":[10,8],
    "Taipower Building":[11,7],
    "Gongguan":[12,6],
    "Wanlong":[13,5],
    "Jingmei":[14,4],
    "Dapinglin":[15,3],
    "Qizhang":[16,2],
    "Xiaobitan":[17,3],
    "Xindian City Hall":[17,1],
    "Xindian":[18,0]
}
def find_and_print(messages, current_station):
    # 準備人名、訊息及車站資訊
    message_name=list(messages.keys()) # 取得 message 中的名字(key)，放入 message_name list
    message_content=list(messages.values()) # 取得 message 中的內容(value)，放入 message_content list
    station_name=list(taipei_mrt_greenline.keys()) # 取得 taipei_mrt_greenlint 中的站名(key)，放入 station_name list
    name_position={} # 建立人名(key)對位置(value)的 dictionary
    # 從 message 中提取出名字與站名關係
    for content in message_content: # 走訪每個 message 中的 content
        for name in station_name: # 走訪每個 station 中的 name
            if(content.find(name)==-1): # 若找不到 name
                continue # 跳下一個 name
            else: # 若找到 name
                name_position.setdefault(message_name[message_content.index(content)],taipei_mrt_greenline[name]) # 將人名(key)及對應位置(value)寫入 name_postion
                break # 跳下一個 content
    # 計算距離關係
    current_position=taipei_mrt_greenline[current_station] # 取得目標位置數值
    relative_position={} # 建立人名(key)對相對距離(value) dictionary
    for person in name_position: # 走訪每個人的位置資訊
        relative=[] # 建立相對距離空 list
        for i in range(0,len(name_position[person])): # 走訪位置值，並且計算相對位置
            if(i==0): # 當第一個位置資訊時
                relative.append(abs(current_position[i]-name_position[person][i])) # 計算相對位置資訊（人名所在位置值扣掉目標位置值取絕對值），並放入相對距離 list
                relative_position.setdefault(person,relative[0]) # 放入人名對相對距離 dictionary
            else: # 當不是第一個位置資訊時
                if(abs(current_position[i]-name_position[person][i])>relative[0]): # 若計算出的相對位置資訊大於第一次計算之值
                    relative_position[person]=abs(current_position[i]-name_position[person][i]) # 將相對距離值取代
    # 找出距離最近的人名
    min_value=min(relative_position.values()) # 取出 relative_position dictionary 中 value 的最小值
    min_key=[k for k,v in relative_position.items() if v==min_value] # 取出 value 最小值的 key
    output="" # 準備空字串
    for person in min_key: # 走訪最小值 key
        if(output==""): # 若字串為空
            output=person # 把人名輸入
        else: # 若字串不為空
            output=output+", "+person # 把 output 後加上 ", " 再加上人名
    print(output)
messages={
    "Leslie":"I'm at home near Xiaobitan station.", 
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.", 
    "Copper":"I just saw a concert at Taipei Arena.", 
    "Vivian":"I'm at Xindian station waiting for you."
}
# 測試資料
find_and_print(messages, "Wanlong") # Mary 
find_and_print(messages, "Songshan") # Copper 
find_and_print(messages, "Qizhang") # Leslie 
find_and_print(messages, "Ximen") # Bob 
find_and_print(messages, "Xindian City Hall") # Vivian
#
##########
# Task 2 #
##########
#
# conslutants 有名稱、評價、價格，從使用者輸入的條件去預定時段
# 
# 確認條件，依據條件排序 conslutants，再確認 conslutants 時間表，若時間不許可，再找第二順位...，直到沒有符合的 conslutants，印出 no service
# 將 consultants 被預定的時段加入該名 consultants 的 dictionary 當中，例如：1:1，代表1點被預約
# 
# 依照條件找出對應的 consultants，price 由小到大，使用 sorted(range(list_name), key=list_name.__getitem__) 找出由小到大的 index 
# rate 由大到小， 使用 sorted(range(list_name), key=list_name.__getitem__, reverse=True) 找出由大到小的 index
# 
# 確認每位 consultant 是否可以 book 時間
#   以 index 走訪已排序的 consultants
#       確認 consultants 時間，若有時間重疊，記錄時段被佔用，並且找下一位
#   以 index 走訪確認可以佔用時段之 consultant
#       寫入 consultant 的 dictionary中，並且印出該名 consultant 的 name    
# 每位 cosultant 時段都被佔用，印出 no service
#
def book(consultants, hour, duration, criteria):
    consultants_criteria=[] # 建立 consultants_criteria 的空 list
    # 依據 criteria 取出數值，依序放入 consultants_criteria
    if(criteria=="price"):
        for person in consultants: # 每個 consultants 依序執行
            consultants_criteria.append(person[criteria]) # 依序放入 price 的 value
            criteria_index=sorted(range(len(consultants_criteria)), key=consultants_criteria.__getitem__) # 找出由小到大的 index 並放入 criteria_index
    elif(criteria=="rate"):
        for person in consultants:
            consultants_criteria.append(person[criteria]) # 依序放入 rate 的 value
            criteria_index=sorted(range(len(consultants_criteria)), key=consultants_criteria.__getitem__,reverse=True) # 找出由大到小的 index 並放入 criteria_index
    # 確認每個 consultants 是否可以 book 時間
    for person in criteria_index: # 依據 criteria 順序執行，走訪每個 consultant
        ocuppied_flag=0 # 歸零記錄時段被佔據
        # 根據 input 時段，確認其 consultant 時段沒有被佔用
        for time in range(0,duration): 
            if(hour+time in consultants[person]): # 如果此時段 hour+time 有在 consultant 的 dictionary 中
                if(consultants[person][hour+time]==1): # 若此時段對應之 value 為 1
                    ocuppied_flag=1 # 記錄時段被佔據
                    break
            # time+=1 # 下一個時段
        # 若時段被佔據，找下一順位的 consultant
        if(ocuppied_flag==1):
            continue
        # 時段沒有被佔用，將時段寫入 consultant 的 dictionary 中
        for time in range(0,duration):
            if(hour+time in consultants[person]): # 如果此時段 hour+time 有在 consultant 的 dictionary 中
                if(consultants[person][hour+time]==0): # 若此時段對應之 value 為 0
                    consultants[person][hour+time]=1 # 將此時段對應之 value 設為 1
            else:
                consultants[person].setdefault(hour+time,1) # 新增此時段，並將 value 設為 1
            # time+=1 # 下一個時段
        print(consultants[person]["name"]) # 印出對應之 consultant 的 name
        return
    # 每個 consultant 皆沒有時段
    print("No Service")

consultants=[
    {"name":"John", "rate":4.5, "price":1000}, 
    {"name":"Bob", "rate":3, "price":1200}, 
    {"name":"Jenny", "rate":3.8, "price":800}
]

# 測試資料
book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate") # Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John
#
##########
# Task 3 #
##########
#
# 找出最特別中間名字（姓名為兩個字取第二個字，姓名為四個字取第三個字）
#
# 取出中間名
#   使用 for 迴圈，把名字抓出來，再判斷名字長度，根據名字長度取出中間名
#
# 統計中間名  
#   準備一個 dictionary ，擺放取出的中間名，判斷中間名是否有出現過
#       沒有出現過就在 dictionary 中新增 key-value pair，並且set value = 1
#       有出現在 dictionary 中，將 key 所對應的 value +1
# 
# 找出最少的名
#   min(dict, key=dict.get) <-- 可以找出 value 最小的 key，若是有多個最小 value 的 key，僅回傳一個 key
#   min_value=min(dict.values())
#   min_key=[k for k,v in dict.items() if v==min_value] <-- 可以找出所有最小 value 的 key，並且存放在 min_key
#
# 輸出
#   若是 len(min_key)==1，表示有最少的名； len(min_key)!=1，表示沒有最少的名， print 沒有
#   有最少的名，用此 min_key 走訪 data 中所有的 name，有在 name 中則印出此 name <== 是否可以不用走訪的方式，在前面篩選的時候就可以記錄並直接印出
#
# 特殊狀況處理
#   data為空時，印出『沒資料』
#
def func(*data):
    # data 為 tuple
    # 特殊狀況處例
    if (data==()):
        print("沒資料")
        return
    middle_name_dict={} # 建立中間名字典
    midname="" # 中間名參數
    # 取出以及統計中間名
    for name in data:
        if(len(name)==2 or len(name)==3):
            midname=name[1]
            if midname in middle_name_dict:
                middle_name_dict[midname] += 1
            else:
                middle_name_dict.setdefault(midname,1)
        # elif(len(name)==3):
        #     midname=name[1]
        #     if midname in middle_name_dict:
        #         middle_name_dict[midname] += 1
        #     else:
        #         middle_name_dict.setdefault(midname,1)
        elif(len(name)==4 or len(name)==5):
            midname=name[2]
            if midname in middle_name_dict:
                middle_name_dict[midname] += 1
            else:
                middle_name_dict.setdefault(midname,1)
        # elif(len(name)==5):
        #     midname=name[2]
        #     if midname in middle_name_dict:
        #         middle_name_dict[midname] += 1
        #     else:
        #         middle_name_dict.setdefault(midname,1)
    # 找出最少的名
    min_value=min(middle_name_dict.values())
    min_key=[k for k,v in middle_name_dict.items() if v==min_value]
    # 確認是否有最少的名，並且印出對應結果
    if(len(min_key)==1):
        for name in data:
            if(min_key[0] in name):
                print(name)
    else:
        print("沒有")
# 測試資料
func("彭大牆", "陳王明雅", "吳明") # 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # 夏曼藍波安
#
##########
# Task 4 #
##########
#
# Number sequence: 0, 4, 8, 7, 11, 15, 14, 18, 22, 21, 25, ...
# 發現為 4 * index再扣除 （index / 3 的商數）* 5 
# Python 取商數為 //
# 
def get_number(index):
    q = index//3
    print(index*4-index//3*5)
# 測試資料
get_number(1)
get_number(5)
get_number(10)
get_number(30)
#
##########
# Task 5 #
##########
#
# 給定 spaces 為每個車廂有空位的數量
# 給定 stat 為各車廂是否可以使用
# 給定 n 為乘客數量
# 確認是否可以上車，依據車廂空位的數量最少開始乘坐（不分開坐）
#
# 將 spaces 與 stat 組合成 dictionary
# 走訪 dictionary 依據有開放的車廂搜尋最適合之車廂
# 
# 偷懶做法 
#   依據 index 順序將 space 與 stat 相乘再將每個 index 扣掉 n
#   找出大於等於 0 之 index
#
def find(spaces, stat, n):
    # 使用 spaces、stat 及 n 計算結果
    result=[a*b-n for a,b in zip(spaces,stat)]
    # 取出大於等於 0 之最小值
    min=[None]
    for value in result:
        if(value>=0):
            if(min[0]==None):
                min[0]=value
            elif(value<min[0]):
                min[0]=value
    # 若 min[0] 為 None，表示找不到符合車廂
    if(min[0]==None):
        print(-1)
        return
    # 找出最小值的 index
    min_index=[]
    i=0
    for min_value in result:
        if(min[0]==min_value):
            min_index.append(i)
        i+=1
    # 印出車廂 index
    output=""
    for value in min_index:
        if(output==""):
            output=str(value)
        else:
            output=output+", "+str(value)
    print(output)
# 測試資料
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # 5 
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # -1 
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # 2