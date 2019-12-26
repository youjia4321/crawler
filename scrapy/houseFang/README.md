# 抓取房天下的房源信息（新房、二手房）

1.获取所有城市的URL链接
##### https://www.fang.com/SoufunFamily.htm

2.获取所有城市的新房的URL链接
##### 安庆 https://anqing.fang.com/
##### 安庆新房 https://anqing.newhouse.fang.com/house/s/

3.获取所有城市的二手房的URL链接
##### 安庆 https://anqing.fang.com/
##### 安庆二手房 https://anqing.esf.fang.com/

北京是个例外：
##### 新房链接 https://newhouse.fang.com/house/s/
##### 二手房链接 https://esf.fang.com/


运行完爬虫

运行new2excel.py文件  将新房信息写入excel表

运行esf2excel.py文件  将二手房信息写入excel表
   