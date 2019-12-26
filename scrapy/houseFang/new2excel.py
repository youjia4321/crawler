import json
import pandas as pd

with open("new_house.json", "rb") as fp:
    all_data = []
    for data in fp.readlines():
        all_data.append(json.loads(data))


df = pd.DataFrame(all_data)  # 设置索引值
df.columns = ['小区名字', '城市', '省份', '地址', '面积', '行政区', '价格', '状态', '几居', '详情页面']  # 设置列名
df.to_csv("new_house.csv", index=0, encoding="ansi")
