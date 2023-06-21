import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'}

# 该程序用于爬取所有的城市信息，用于下一步爬取每个城市天气使用

html = requests.get('https://www.tianqi.com/chinacity.html', headers=headers)
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.text, "html.parser")
# 找到所有的城市标签，它们都是h2元素
city_tags = soup.find_all("h2")
# 遍历每个城市标签
df = pd.DataFrame(columns=['城市', '区域', '链接'])

for city_tag in city_tags:
    # 获取城市的名字，它是a元素的文本内容
    city_name = city_tag.a.text
    # 获取城市对应的区域标签，它们都是span元素
    area_tags = city_tag.find_next_sibling("span")
    # 遍历每个区域标签
    for area_tag in area_tags:
        # 获取区域的名字，它是a元素的文本内容
        area_name = area_tag.text
        # 获取区域的链接，它是a元素的href属性
        area_url = ''
        if area_tag.name == 'a':
            area_url = area_tag['href']
        elif area_tag.name == 'h3' and area_tag.a is not None:
            area_url = area_tag.a['href']
        else:
            area_url = None
        # print(city_name, area_name, area_url)
        # 把区域的名字添加到列表中
        df = df.append({'城市': city_name, '区域': area_name,
                       '链接': area_url}, ignore_index=True)

print(df)
df.to_csv('city.csv', encoding='utf-8-sig')
