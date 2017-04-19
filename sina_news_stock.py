# kenny-system
#_*_ coding:utf-8 _*_
import urllib,urllib2,re
from bs4 import BeautifulSoup
import time,socket
import sys
import xlwt
reload(sys)


sys.setdefaultencoding('utf-8')
theme_url = "http://guba.sina.com.cn/?s=bar&name=%CC%E2%B2%C4%CD%DA%BE%F2%BB%FA&type=0&page="
content_url = "http://guba.sina.com.cn"


class Theme():
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        self.theme_data = []
    def get_html_title(self,start_page,end_page):
        for i in range(start_page,end_page+1):
            get_html = urllib2.Request(theme_url+str(i))
            get_html.add_header('User-Agent',self.user_agent)
            try:
                my_data = urllib2.urlopen(get_html).read().decode('gbk').encode('utf-8')
                # print my_data
                self.theme_data.append(my_data)
                timesleep = 2
                socket.setdefaulttimeout(15)
            except urllib2.URLError,e:
                if hasattr(e,'reason'):
                    print u"连接失败",e.reason
        return str(self.theme_data)
        
               
class Getdatalist():
    def __init__(self):
        self.get_html = Theme().get_html_title(2,4)
        self.href = []
        self.items = []

    def getlist(self):
        result = re.compile(r'<td><span class="red">(.*?)</span></td>.*?<td><span class="red">(.*?)</span></td>.*?<a href="(.*?)" target="_blank" class=" linkblack f14">(.*?)</a>',re.S)
        totally_list = re.findall(result,self.get_html)
        #print totally_list
        for i in totally_list:
            article_url = content_url + i[2]
            self.href.append(article_url)
            plus_list = u'评论数：%s 文章标题：%s'%(i[0],i[3])
            self.items.append(plus_list)
        #print self.items[0]
        #print self.href
        return self.href


class Get_article():
    def __init__(self):
        self.hrefdetail = Getdatalist().getlist()
        self.article = []

    def show_article(self):
        file = xlwt.Workbook()
        sheet = file.add_sheet('invest_information')
        row = 0
        sheet.write(0,0,'title')
        sheet.write(0,1,'readcounts')
        for i in range(len(self.hrefdetail)):
            url = str(self.hrefdetail[i])
            get_request = urllib2.Request(url)
            try:
                req = urllib2.urlopen(get_request).read().decode('gbk').encode('utf-8')
                soup = BeautifulSoup(req,"html.parser")
                text = soup.find(id="thread_content")
                #print text
                del_tag = re.compile(r'<[^>]+>')
                article_detail = re.sub(del_tag,'',str(text))
                text_title_get = soup.find_all("h4",attrs={"class":"ilt_tit"})
                text_title = re.sub(del_tag,'',str(text_title_get[0]))
                print text_title
                #text_count = soup.find_all("div",attrs={"class":"fl_right iltp_span"})
                re_rule = re.compile(r'<span>阅读数(.*?)</span>')
                text_count = re.findall(re_rule,req)
                read_count = str(text_count).replace("['(",'').replace(")']",'')
                print read_count
                print article_detail
                try:
                    with open(text_title.decode('utf-8')+'.txt','wb') as f:
                        f.write('\t'*4+'标题：%s    \n阅读数：%s\r\n'%(text_title,read_count))
                        f.write('\t'+article_detail)
                        #break
                except IOError,e:
                    continue
                row += 1
                sheet.write(row,0,text_title.decode('utf-8'))
                sheet.write(row,1,read_count.decode('utf-8'))
                print u'已爬完%s条'%str(row)
            except urllib2.URLError,e:
                print '第%s条爬取出错'%row
                row += 1
                continue

        file.save('invest_information.xls')
        return
Get_article().show_article()





