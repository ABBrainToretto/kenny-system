#_*_ coding:utf-8 _*_
import requests
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from PIL import Image
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DouBanClint(object):
    def __init__(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer':'https://www.douban.com/'
        }
        self.session = requests.session()
        self.session.headers.update(headers)

    def login(self,username,password,
              source = 'index_nav',
              redir = 'https://www.douban.com/group/?start=',
              login = '登录'):
        url = 'https://accounts.douban.com/login'
        r = self.session.get(url)

        captcha_id,captcha_url = _get_captcha(r.content) #调用解析html函数，返回captcha_id,captcha_url
        if captcha_id:
            img_html = self.session.get(captcha_url)
            with open('captcha.jpg','wb') as f:
                f.write(img_html.content)
            try:
                im = Image.open('captcha.jpg')
                im.show()
                im.close()
            except:
                print 'error'
            captcha_solution = raw_input('please input solution: \n%s:\n'%captcha_url)
            print u'成功侵占豆瓣领地'
            time.sleep(1)


        for page in range(4):
            page = page * 50
            data = {
                'source':source,
                'redir':redir+str(page),
                'form_email':username,
                'form_password':password,
                'login':login
            }
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Referer':'https://www.douban.com/'
            }
            if captcha_id:
                data['captcha-id'] = captcha_id
                data['captcha-solution'] = captcha_solution

            r = self.session.post(url,data = data,headers = headers)
            text = r.text
            # print self.session.cookies.items()
            #print u'成功侵占豆瓣领地'
            soup = BeautifulSoup(text,'html.parser')
            result = soup.find_all("td",class_="td-subject")
            row = 0
            for i in result:
                href = i.find_all("a")
                print u'\n\n正在爬取第%s条优惠打折商品，快来看看哦：'%row
                print u'这是链接%s'%(href[0]['href'])
                print u'这是商品简介：%s'%(href[0]['title'])
                row += 1
                time.sleep(0.5)

def _attr(attrs,attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None

def _get_captcha(content):
    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_id = None
            self.captcha_url = None
        def handle_startendtag(self, tag, attrs):
            if tag == 'img' and _attr(attrs,'id') == 'captcha_image' and _attr(attrs,'class') == 'captcha_image':
                self.captcha_url = _attr(attrs,'src')

            if tag == 'input' and _attr(attrs,'type') == 'hidden' and _attr(attrs,'name') == 'captcha-id':
                self.captcha_id = _attr(attrs,'value')

    P = CaptchaParser()
    P.feed(content)
    return P.captcha_id,P.captcha_url


if __name__ == '__main__':
            c = DouBanClint()
            c.login('644853947@qq.com','12344321abc')
            # d = _getHtml().html_content()
