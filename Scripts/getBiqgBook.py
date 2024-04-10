# -*- coding: utf-8 -*-
#爬取笔趣阁内小说
url= 'https://www.biqg.cc/book/117433/1.html'
import requests,json
from bs4 import BeautifulSoup
with open('result.txt', 'a', encoding='utf-8') as file:
    for i in range(1,2000):
        url= 'https://www.biqg.cc/book/117433/'+str(i)+'.html'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.get_text()
        chapter_content = soup.find('div', {'id': 'chaptercontent'}).get_text(separator="\n")
        file.write(title + "\n")
        file.write(chapter_content + "\n\n")