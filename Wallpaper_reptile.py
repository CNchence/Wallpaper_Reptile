import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os

def mkdir(path,savepath):
    path = path.strip()
    isExists = os.path.exists(os.path.join(savepath,path))
    if not isExists:
        os.makedirs(os.path.join(savepath,path))
    return savepath+'\\'+path

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
all_url = 'http://wallpaperswide.com/'  ##开始的URL地址
start_html = requests.get(all_url,  headers=headers)                     #打开网址，搜索所有分类
Soup = BeautifulSoup(start_html.text,'lxml')                             #将网址下载，并生成Soup对象
all_a = Soup.find('ul',class_='side-panel categories').find_all('a')     #调用对象函数，查找网页中特定信息

print('可选的主题有：')
i = 1
for a in all_a:
    title = a.get_text()
    print(i,'.',title)
    i = i+1

theme = input("输入您希望下载主题的序号(空格分离，输入all即全部选择):")
databig = input("输入您需要的分辨率(960x540,1024x576,1920x1080,2048x1152,3554x1999等):")
pages = input("输入您需要的图片数(num=input*10):")
savepath = input("输入您保存的目录(比如 D:\桌面):")
if(theme == 'all'):
    themelist = [i for i in range(1,len(all_a)+1)]
else:
    themelist = theme.split(' ')
i = 0
for a in all_a:
    i += 1
    if (str(i) in themelist):
        title = a.get_text()
        path = str(title).replace("?", '_')
        imgpath = mkdir(path,savepath)
        print(u'开始保存：', title)

        href = a['href']
        href = 'http://wallpaperswide.com/'+href
        j = 1
        while j <= int(pages) :
            j += 1
            href_page = href.replace('.html','/page/'+str(j))
            img_html = requests.get(href_page, headers=headers)                          #打开分类，搜索所有图片
            img_Soup = BeautifulSoup(img_html.text, 'lxml')
            for img in img_Soup.find_all('img',class_ = 'thumb_img'):
                img_dizhi = img.attrs['src']
                img_name = img_dizhi[37:]
                img_HDdizhi = img_name.replace("t1","wallpaper-"+databig)
                img_HDdizhi = "http://wallpaperswide.com/download/"+img_HDdizhi          #获取图片地址
                print(img_HDdizhi)
                img_content = requests.get(img_HDdizhi, headers=headers)
                f = open(imgpath + '\\' + img_name, 'ab')
                print(f)
                f.write(img_content.content)                                        #保存本地
