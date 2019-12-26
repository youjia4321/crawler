import json
import pandas as pd

with open("esf_house.json", "rb") as fp:
    all_data = []
    for data in fp.readlines():
        all_data.append(json.loads(data))


df = pd.DataFrame(all_data)  # 设置索引值
df.columns = ['省份', '城市', '房源信息', '小区名字', '拥有者', '地址', '价格', '详情页面']  # 设置列名
df.to_csv("esf_house.csv", index=0, encoding="ansi")
