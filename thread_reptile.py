import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os
import threading

def SurfInternet(url_in):                      #创建下载网页函数
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    start_html = requests.get(url_in, headers=headers)  # 打开网址，搜索所有分类
    Soup = BeautifulSoup(start_html.text, 'lxml')  # 将网址下载，并生成Soup对象
    return Soup

class MyThread(threading.Thread):

    def __init__(self,savepath,theme,imagehref,pages,headers,databig):
        threading.Thread.__init__(self)
        self.theme = theme              #主题名，由主题查找得到
        self.savepath = savepath        #保存文件夹的地址，一开始 由用户输入
        self.imagehref = imagehref      #主题网址，由主题查找得到
        self.pages = pages              #所要下载的页数，一开始 由用户输入
        self.headers = headers          #浏览器访问头，主函数定义
        self.databig = databig          #图片分辨率，一开始 由用户输入



    def run(self):
        """
        运行线程
        """
        SaveImagePath = self.MkDir(self.theme,self.savepath)
        ThemeHref = 'http://wallpaperswide.com/'+self.imagehref

        j = 1
        while j<= int(self.pages):
            href_page = ThemeHref.replace('.html','/page/'+str(j))
            img_Soup = self.SurfInternet(href_page)
            for img in img_Soup.find_all('img', class_='thumb_img'):
                img_dizhi = img.attrs['src']
                img_name = img_dizhi[37:]
                img_HDdizhi = img_name.replace("t1", "wallpaper-" + self.databig)
                img_HDdizhi = "http://wallpaperswide.com/download/" + img_HDdizhi  # 获取图片地址
                img_content = requests.get(img_HDdizhi, headers=self.headers)
                f = open(SaveImagePath + '\\' + img_name, 'ab')
                f.write(img_content.content)
            j += 1

        print(self.theme,"下载完毕")

    def MkDir(self,theme,savepath):
        theme = theme.strip()
        isExists = os.path.exists(os.path.join(savepath, theme))
        if not isExists:
            os.makedirs(os.path.join(savepath, theme))
        print("创建",theme,"文件夹")
        return savepath + '\\' + theme

    def SurfInternet(self,url_in):
        start_html = requests.get(url_in, headers=self.headers)  # 打开网址，搜索所有分类
        Soup = BeautifulSoup(start_html.text, 'lxml')  # 将网址下载，并生成Soup对象
        return Soup




if __name__ == '__main__':
    all_url = 'http://wallpaperswide.com/'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    SoupTheme = SurfInternet(all_url)
    all_a = SoupTheme.find('ul', class_='side-panel categories').find_all('a')  # 调用对象函数，查找网页中特定信息
    print('可选的主题有：')
    i = 1
    for a in all_a:
        title = a.get_text()
        print(i, '.', title)
        i = i + 1

    theme = input("输入您希望下载主题的序号(空格分离，输入all即全部选择):")
    databig = input("输入您需要的分辨率(960x540,1024x576,1920x1080,2048x1152,3554x1999等):")
    pages = input("输入您需要的图片数(num=input*10):")
    savepath = input("输入您保存的目录(比如 D:\桌面):")
    if (theme == 'all'):
        themelist = [i for i in range(1, len(all_a) + 1)]
    else:
        themelist = theme.split(' ')
    i = 0
    threadlist = []
    for a in all_a:
        i += 1
        if(str(i) in themelist):
            theme = a.get_text()
            theme = str(theme).replace("?","_")
            imagehref = a['href']
            thread = MyThread(savepath,theme,imagehref,pages,headers,databig)
            thread.setName(theme)
            threadlist.append(thread)
            thread.start()
    for i in range(len(threadlist)):
        threadlist[i].join()

