import ssl
import urllib.request as req
from urllib.parse import urljoin
import json
import csv


# Disable SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# !task1 

# Load JSON file 1
json1_src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
with req.urlopen(json1_src, context=ssl_context) as response:
    json1_data = json.load(response)
slist_json1 = json1_data["data"]["results"]

# Load JSON file 2
json2_src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with req.urlopen(json2_src, context=ssl_context) as response:
    json2_data = json.load(response)
mrt_list_json2 = json2_data["data"]

# Create a dictionary to store SERIAL_NO and MRT values from JSON file 2
# Use serial_no to compare the MRT
# Use the MRT["address"] to find the district
serial_no_mrt_map = {} # serial_no : MRT
serial_no_district_map = {} # serial_no : district
districts = ["中正區", "萬華區", "中山區", "大同區", "大安區", "松山區", "信義區", "士林區", "文山區", "北投區", "內湖區", "南港區"]

for item in mrt_list_json2: 
    serial_no_mrt_map[item["SERIAL_NO"]] = item.get("MRT", "N/A") # link serial number to MRT 

    # Assign the district to the item in JSON2
    for district in districts:
      if district in item["address"]:
        item["district"] = district
        serial_no_district_map[item["SERIAL_NO"]] = item["district"] # link serial number to district(every mrt station has a district)
        break  # Exit the loop of districts once the district is found and assigned


spot_list = [] # data to be written to CSV file
classified_by_mrt = {} #key: MRT, value: list of spot titles

for spot_json1 in slist_json1:
    serial_no = spot_json1["SERIAL_NO"]
    spot_json1["SERIAL_NO"]
    img_urls = spot_json1["filelist"].split("https://")[1:]  # Split on "https://" and skip the first element
    spot_json1["img"] = "https://" + img_urls[0] if img_urls else ""  # Add "https://" prefix to the first URL if it exists
    
    # if the serial_no of current item of json1 exist,use it as the key to find the value of MRT and district
    if serial_no in serial_no_mrt_map:
        spot_json1["mrt"] = serial_no_mrt_map[serial_no]  #give the item in json1 the key mrt and its value
        spot_json1["district"] = serial_no_district_map[serial_no]
        current_mrt = spot_json1["mrt"]
        stitle = spot_json1["stitle"]

        classified_by_mrt.setdefault(current_mrt, []).append(stitle)
    else:
        mrt = "N/A"
    print(spot_json1["mrt"], spot_json1["district"], spot_json1["stitle"], spot_json1["longitude"], spot_json1["latitude"])
    spot_data = [spot_json1["stitle"], spot_json1["district"], spot_json1["longitude"], spot_json1["latitude"], spot_json1["img"]]
    spot_list.append(spot_data)
with open("spot.csv", "w", encoding="utf-8") as file: 
    writer = csv.writer(file)
    writer.writerows(spot_list)

#sorted_dict = dict(sorted(classified_by_mrt.items()))
mrt = []

with open("mrt.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    for key, values in classified_by_mrt.items():
        data = []
        data.append(key)
        data.extend(values)  # Extend the data list with all values
        mrt.append(data)
        writer.writerow(data)  # Write the data to the CSV file


# !task2
def getData(url):
  # Disable SSL certificate verification
  ssl_context = ssl.create_default_context()
  ssl_context.check_hostname = False
  ssl_context.verify_mode = ssl.CERT_NONE
  # 建立一個 Request 物件，附加 Request Headers 的資訊
  # 讓程式看起來像是正常的使用者在瀏覽網頁
  request = req.Request(url, headers={
    "cookie": "over18=1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    })

  # get the PTT lottery board
  with req.urlopen(request, context=ssl_context) as response:
    data = response.read().decode("utf-8")
    #解析原始碼，取得每篇文章標題
    import bs4
    root = bs4.BeautifulSoup(data, "html.parser") # 讓 BeautifulSoup 協助解析 HTML 格式文件
    
    time_list = []
    tlist = []
    clist = []
    
    
          
    like_dislike_count = root.find_all("div", class_="nrec") # 尋找所有 class="nrec" 的 div 標籤
    for count in like_dislike_count:
      if count.span != None:
        clist.append(count.span.string)
      else:
        clist.append(0)

    next_link=root.find("a", string="‹ 上頁") #找到內文是‹ 上頁 的 a 標籤
    next_page_url=urljoin("https://www.ptt.cc", next_link["href"]) #if next_link else None
    #next_page_url = "https://www.ptt.cc" + next_link["href"] if next_link else None
    titles = root.find_all("div", class_="title") # 尋找所有 class="title" 的 div 標籤
    for title in titles:
      if title.a != None: #如果標題包含 a 標籤 (沒有被刪除)，印出來
        tlist.append(title.a.string)
      title_url = "https://www.ptt.cc" + title.a["href"]
      request = req.Request(title_url, headers={
        "cookie": "over18=1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        })
      with req.urlopen(request, context=ssl_context) as response:
        data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")
        content = root.find('span', string="時間")
        if content:
          content = content.find_next('span')
          time_list.append(content.string)
    return tlist, clist, time_list, next_page_url

def writtenDataTOCSV(file_name, tlist, clist, time_list):
  if count > 0:
    mode = "a"  
  else: 
    mode = "w"
  
  with open(file_name+".csv", mode, newline="", encoding="utf-8") as csvfile:
    for t, c, d in zip(tlist, clist, time_list):
        writer = csv.writer(csvfile)
        writer.writerow([t, c, d])
                      
count=0
pageURL = "https://www.ptt.cc/bbs/Lottery/index.html"
while count<3:
  result=getData(pageURL)
  if result:
    tlist, clist, time_list, next_page_url=result
    if next_page_url:
      pageURL = next_page_url
      file_name="article"
      writtenDataTOCSV(file_name, tlist, clist, time_list)
      count+=1


