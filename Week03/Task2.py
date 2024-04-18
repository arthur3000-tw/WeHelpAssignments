# 樂透板連結：https://www.ptt.cc/bbs/Lottery/index.html
# 取得樂透板文章所有的 link
# 連結中可以取得『文章標題』、『推/噓』數、『發佈時間』
# 『文章標題』：<span class="article-meta-value">[報牌] 享受輸的感覺539</span>
# 『推』：<span class="hl push-tag">推 </span>
# 『噓』：<span class="f1 hl push-tag">噓 </span>
# 『發佈時間』：<span class="article-meta-value">Mon Apr 15 16:57:49 2024</span>

# 抓取 PTT 樂透板的網頁原始碼(HTML)
import urllib.request as req
import bs4 # 載入 BeautifulSoup library
import csv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 建立函式：輸入網頁連結，回傳原始數據
def getRawData(url):
    # 建立一個 Request 物件，附加 Request Headers 的資訊
    request=req.Request(url, headers={
        "cookie":"over18=1", # 需要確認超過 18 歲，將 cookie 中 over18 設定為 1
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })
    # 取得原始碼
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    return data # 回傳原始數據

# 建立函式：輸入文章的網頁連結，回傳『文章標題』、『推/噓』數、『發佈時間』資訊
def getArticleData(url):
    data = getRawData(url)
    root=bs4.BeautifulSoup(data, "html.parser")
    # 取得標題
    articleTitles=root.find_all("span", class_="article-meta-value") # 取得 span 中 class 為 article-meta-value 的標籤
    articleTexts=[]
    for articleTitle in articleTitles: # 將標籤中的文字取出，其中包含『文章標題』、『發佈時間』
        articleTexts.append(articleTitle.string)
    # 取得『推』數量
    likeCount=0
    likeTags=root.find_all("span", class_="hl push-tag")
    for likeTag in likeTags:
        if(likeTag.string=="推 "):
            likeCount+=1
    # 取得『噓』數量
    dislikeCount=0
    dislikeTags=root.find_all("span", class_="f1 hl push-tag")
    for dislikeTag in dislikeTags:
        if(dislikeTag.string=="噓 "):
            dislikeCount+=1
    # 排除沒抓到數據的資料（文章沒有篩選的狀況下，會抓到特殊頁面，可以忽略沒抓到的資料）
    # if(len(articleTexts)==0):
    #     return
    return [articleTexts[2],str(likeCount)+"/"+str(dislikeCount),articleTexts[3]] # 輸出按照需求格式的資料

# 建立函式：輸入某某板網址（url）及要爬的頁數(pages)，輸出資料
def getData(url,pages):    
    url_head=url[:18] # 取出 https://www.ptt.cc
    outputData=[]
    # 多頁爬文
    for page in range(pages):
        data = getRawData(url)
        # 解析原始碼，取得每篇文章的標題
        root=bs4.BeautifulSoup(data, "html.parser") # 讓 BeautifulSoup 解析 HTML 格式文件
        # 搜尋文章連結並取得文章內資料（沒有做篩選）
        # a_tags=root.select(".title a") # 尋找所有 class="title" 的 div 標籤子層中的 a 標籤
        # for a_tag in a_tags: # 取得 a 標籤中的 link
        #     url=url_head+(a_tag.get('href'))
        #     print(url)
        #     outputData.append(getArticleData(url))
        # 搜尋文章連結並取得文章內資料（排除 M 文）
        a_tags=root.select(".r-ent")
        for a_tag in a_tags:
            if(a_tag.find("div",class_="mark").string == None): # 標記 M 文的文字為 None，表示非 M 文
                if(a_tag.find("div",class_="title").a != None): # 排除被刪除的文章
                    url=url_head+a_tag.find("div",class_="title").a.get("href")
                    outputData.append(getArticleData(url))
        # 點選上一頁連結
        url=url_head+root.find("a",string="‹ 上頁")["href"]
    return outputData

# 輸入網址及爬取頁面數量，取得數據
article_info=getData("https://www.ptt.cc/bbs/Lottery/index.html",3)

# 將數據寫入檔案
with open("article.csv", mode="w", newline="") as file: # 建立 article.csv 檔案
    writer=csv.writer(file)
    for info in article_info:
        writer.writerow(info)
