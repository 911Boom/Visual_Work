import requests
import re
import pandas as pd
from multiprocessing import Pool
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

df = pd.DataFrame(columns=[
    '省', '市', '日期', '星期', '最高温度', '最低温度', '天气', '风向风力'
])


def query(province, city, year, urls):
    global df
    for url in urls:
        print(url)
        html = requests.get(url, headers=headers)
        html.encoding = html.apparent_encoding
        bs = BeautifulSoup(html.text, 'html.parser')
        data = bs.find_all(class_='thrui')
        date = re.compile('class="th200">(.*?)</')
        tem = re.compile('class="th140">(.*?)</')
        time = re.findall(date, str(data))
        temp = re.findall(tem, str(data))
        print(time)
        # print(temp)
        data = []
        for i in range(len(time)):
            l1 = [province, city, time[i][:10], time[i][10:], temp[i * 4 + 0], temp[i * 4 + 1], temp[i * 4 + 2], temp[i*4+3]]
            data.append(l1)
        df1 = pd.DataFrame(
            data, columns=['省', '市', '日期', '星期', '最高温度', '最低温度', '天气', '风向风力'], index=None)
        df = pd.concat([df, df1])
        # print(df)


citys = pd.read_csv('../VisualWork/city.csv')
# print(citys)


# 生成所有的url
url_dict = {}
for i in range(2011, 2023):
    for row in citys.itertuples():
        province = row[2]
        if province != '北京':
            continue
        city = row[3]
        link = []
        for j in range(1, 13):
            if j < 10:
                url = 'https://lishi.tianqi.com{}{}0{}.html'.format(row[4], i, j)
            else:
                url = 'https://lishi.tianqi.com{}{}{}.html'.format(row[4], i, j)
            link.append(url)
        url_dict[(province, city, i)] = link


# query('四川', '绵阳', '2019', 'mianyang', url_dict[('四川', '绵阳', 2019)])
# df.to_csv('../VisualWork/Total_weather.csv', index=False)
# 使用多进程并发调用query函数
def run(args):
    province, city, year = args
    query(province, city, year, url_dict[(province, city, year)])

for key in url_dict.keys():
    run(key)

df.to_csv('../VisualWork/Total_weather.csv', index=False)
#
# if __name__ == '__main__':
#     pool = Pool()
#     pool.map(run, url_dict.keys())
#     pool.close()
#     pool.join()
