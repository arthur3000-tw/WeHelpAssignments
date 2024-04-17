# 有兩筆數據在連結網址中
# 取得兩筆資料數據，進行整理，輸出兩個 csv 檔案
# 處理兩筆資料，得到適當的 csv 檔案格式
# 

import urllib.request as req
import ssl
import json
import csv
ssl._create_default_https_context = ssl._create_unverified_context

# 取得資料二資訊
url="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
request=req.Request(url)
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
result=json.loads(data)

# 處理資料二內容
address_info=[] # 建立 address information list 存放各地點資訊，每個地點都是一個 dictionary
for index in result["data"]:
    # 修改 address 成為某某區
    address=index["address"][5:8] # 偷懶做法，剛好每一區都是三個字且位置在相同位置
    address_info.append({"MRT":index["MRT"], "Serial_No":index["SERIAL_NO"], "Address":address})

# 取得資料一資訊
url="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
request=req.Request(url)
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
result=json.loads(data)

# 處理資料一內容（將資料二內容合併）
spot_info=[] # 建立 spot information list 存放各地點資訊，每個地點都是一個 dictionary
for index in result["data"]["results"]: # 從資料中取得數據，資料位於 {..., data:{..., result:{[資料]}, ...}, ...}
    # 處理圖片連結
    url_link=index["filelist"].split("https://") # 取圖片連結，用 "https://" 分隔
    url_link_first="https://"+url_link[1] # 取出第一個圖片連結及前面加上 "https://"
    # 將資料二中的 MRT 、 Address 加入
    add_dict={}
    for index_2 in address_info: # 走訪資料二的內容
        if(index_2["Serial_No"]==index["SERIAL_NO"]):
            add_dict=index_2 # 取得資料二對應的內容
    # 放入 spot_info 中，使用聯集將兩個字典融合
    spot_info.append({"SpotTitle":index["stitle"],"Longitude":index["longitude"],"Latitude":index["latitude"], "ImageURL":url_link_first, "Serial_No":index["SERIAL_NO"]} | add_dict)
    



# 準備 mrt.csv 內容

# 取出捷運站資訊
mrt_stations=[]
for index in spot_info:
    if(index["MRT"]) not in mrt_stations:
        mrt_stations.append(index["MRT"])
mrt_info=[]
# 依據每個捷運站走訪每個資料
i=0
for mrt_station in mrt_stations: # 依照每個捷運站走訪
    mrt_info.append({"MRT":mrt_station,"SpotTitle":[]}) # 將捷運站 key value 寫入、景點 key value 寫入（因為為多個景點因此用 list ）
    for index in spot_info: # 走訪每個資料
        if(mrt_station==index["MRT"]): # 若資料中的捷運站符合捷運站名稱
            mrt_info[i]["SpotTitle"].append(index["SpotTitle"]) # 將景點 value append
    i+=1

# print(mrt_info)
with open("mrt.csv", mode="w", newline="") as file:
    writer=csv.writer(file)
    for info in mrt_info:
        write_list=[] # 準備 list
        write_list.append(info["MRT"]) # 將訊息寫進 list
        writer.writerow(write_list+list(info["SpotTitle"]))


# 準備 spot.csv 內容





# 寫入檔案
with open("spot.csv", mode="w", newline="") as file: # 建立 spot.csv 檔案
    writer=csv.writer(file)
    index=0
    for info in spot_info: # 將每個字典中的 value 寫入
        writer.writerow(list(spot_info[index].values())[0:1]+list(spot_info[index].values())[6:7]+list(spot_info[index].values())[1:4])
        index+=1






# print(spot_info)

# print(result["data"]["results"][0]["info"])

# i=0
# for index in result["data"]["results"]:
#     print(i,index["info"])
#     i+=1

# print(result["data"]["results"][46])

# print(result["data"]["results"][0])