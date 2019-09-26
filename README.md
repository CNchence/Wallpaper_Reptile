## Wallpaper_Reptile
Python壁纸爬虫

## 依赖
* python 3
* requests
* BeautifulSoup4 
* lxml

运行时若提示缺少库，按照提示安装即可。


## 如何运行
使用 python3运行： `python thread_reptile.py`。
然后等待即可。

运行时会提示输入：
1. 希望下载的主题
1. 张数 
1. 分辨率
1. 存放目录
1. 每个主题放在各自单独的目录，或统一合并放到上一步指定的“存放目录”

 
 
## 已知BUG
1. 可能少数下载的图片无法打开，因为网站上缺少对应分辨率的图片
