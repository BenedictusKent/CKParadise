from requests import get
from bs4 import BeautifulSoup as soup
import re

# grab the whole page
search_url = "https://hululu.tw/tainanbar/"
req = get(search_url)
wholepage = soup(req.text, "html.parser")

# data in tag is inconsistent, just grab all text
text = wholepage.get_text()
text = text[33448:46065]

# remove whitespaces
text = re.sub('\n+', '\n', text).strip()
text = re.sub(r'\n\s*\n', '\n\n', text)

# remove unnecessary sentences/words
bar = []
count = 0
temp = ""
for i in text:
    if i == '\n':
        count += 1
    else:
        count = 0
    if count < 2:
        temp += i
    elif count == 2:
        bar.append(temp)
        temp = ""
    elif count > 2:
        temp = ""
bar.append(text[-148:])
for i in range(len(bar)):
    if "中西區\n" in bar[i]:
        bar[i] = bar[i].replace("中西區\n", "")
    elif "東區\n" in bar[i]:
        bar[i] = bar[i].replace("東區\n", "")
    elif "北區\n" in bar[i]:
        bar[i] = bar[i].replace("北區\n", "")
    elif "南區\n" in bar[i]:
        bar[i] = bar[i].replace("南區\n", "")
    elif "永康區\n" in bar[i]:
        bar[i] = bar[i].replace("永康區\n", "")
    elif "新營區\n" in bar[i]:
        bar[i] = bar[i].replace("新營區\n", "")
    elif "安平區\n" in bar[i]:
        bar[i] = bar[i].replace("安平區\n", "")
bar = list(filter(None, bar))
sent = wholepage.findAll("a", {"data-wpel-link": "internal", "target": "_blank"})
temp = [i.text for i in sent]
temp = list(filter(None, temp))
temp.append('滿滿花藝空間結合創意酒品好吸晴。「Ai-Wei Bistro愛薇餐酒館」|晚餐|酒吧|聚餐|寵物友善|')
for i in range(len(bar)):
    for j in temp:
        if j in bar[i]:
            bar[i] = bar[i].replace(j+"\n", "")
for i in bar:
    print(i)