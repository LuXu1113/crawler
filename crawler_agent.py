# coding: utf-8
# python-version: 3.6

import sys
import ssl
import urllib.request

C_CHROME_UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'

class CrawlerAgent :
    def __init__(self, user_agent = None, proxy = None) :
        self.opener = urllib.request.build_opener()

        if (proxy) :
            proxy_params = {'http' : proxy, 'https' : proxy}
            self.opener.add_handler(urllib.request.ProxyHandler(proxy_params))

        context = ssl._create_unverified_context()
        self.opener.add_handler(urllib.request.HTTPSHandler(context = context))

        if None == user_agent :
            self.headers = {'User-agent' : C_CHROME_UA}
        else :
            self.headers = {'User-agent' : user_agent}
        
            
    def get_data(self, url) :
        print('[INFO] Downloading: ', url)

        request = urllib.request.Request(url, headers = self.headers)
        
        try :
            html = self.opener.open(request).read()
        except Exception as err :
            print ('[ERROR][%s:%d]: %s.' % (__file__, sys._getframe().f_lineno, err))
            html = None

        return html

    def get_url(self, url):
        request = urllib.request.Request(url, headers = self.headers)

        try:
            url = self.opener.open(request).geturl()
        except Exception as err :
           print ('[ERROR][%s:%d]: %s.' % (__file__, sys._getframe().f_lineno, err))
           url = None

        return url

    def get_info(self, url) :
        request = urllib.request.Request(url, headers = self.headers)

        try :
            info = self.opener.open(request).info()
        except Exception as err :
            print ('[ERROR][%s:%d]: %s.' % (__file__, sys._getframe().f_lineno, err))
            info = None

        return info

    def get_code(self, url) :
        request = urllib.request.Request(url, headers = self.headers)

        try:
            code = self.opener.open(request).getcode()
        except Exception as err :
            print ('[ERROR][%s:%d]: %s.' % (__file__, sys._getframe().f_lineno, err))
            code = None

        return code
        

if __name__ == "__main__":
    proxy = None
    agent = CrawlerAgent(proxy = proxy)

    url  = "http://www.baidu.com/"

    html = agent.get_data(url)
    url  = agent.get_url(url)
    info = agent.get_info(url)
    code = agent.get_code(url)

    ofile = open('crawler_agent.html', 'wb')
    ofile.write(html)
    ofile.close()

    print('url:  ', url)
    print('info: ', info)
    print('code: ', code)

    print('[INFO] Finished!')
