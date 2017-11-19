# coding: utf-8
# python-version: 3.6

# ------------------------------------------------------------------------------
# Page structure of baidu search engine
# <html>
# <head>...</head>
# <body>
#     <div id = "wrapper">
#         <div id = "wrapper_wrapper">
#             <div id = "container">
#                 <div id = "content_left">
#                     <div class = "result(.*)" id = "[[rank]]" tpl="[[tpl]]">
#                         <h3><a href = "[[link of search result]]">
#                             [[title of search result]]
#                         </a></h3>
#                     </div>
#                     <div class = "result(.*)" id = "[[rank]]" tpl="[[tpl]]">
#                         <h3><a href = "[[link of search result]]">
#                             [[title of search result]]
#                         </a></h3>
#                     </div>
#                     ...
#                 </div>
#             </div>
#             <div id = "page">
#                 <a class = "n" href = "[[prev page]]">上一页</a>
#                 <a href = "...">第n页</a>
#                 ...
#                 <a class = "n" href = "[[next page]]">下一页</a>
#             </div>
#         </div>
#     </div>
# <body>
# </html>
# ------------------------------------------------------------------------------
import re
import urllib.request
import html.parser
import crawler_agent
from bs4 import BeautifulSoup

class Result :
    def __init__(self) :
        self.title   = None
        self.href    = None    # baidu link
        self.link    = None    # real link
        self.tpl     = None
        self.rank    = None

class Crawler :
    def __init__(self, agent, keywords = None) :
        self.agent     = agent
        self.keywords  = keywords  # string      of keywords
        self.curr_url  = None      # string      of url of current result page
        self.next_url  = None      # string      of url of the next result page
        self.html      = None      # string      of current html page
        self.soup      = None      # bs object   of self.html
        self.results   = []        # result list of baidu search engine

    def set_agent(self, agent) :
        self.agent     = agent

    def set_keywords(self, keywords) :
        self.keywords = keywords
        self.curr_url  = None
        self.next_url  = None
        self.html      = None
        self.soup      = None
        self.results   = []

    def get_top_n_results(self, keywords, n = 1) :
        self.set_keywords(keywords)
        return self.get_next_n_results(n)

    def get_next_n_results(self, n = 1) :
        begin = len(self.results)
        num   = 0;
        while num < n :
            # Generate URL
            if None == self.curr_url :
                if None == self.keywords :
                    print('[ERROR] No keywords.')
                    break;
                self.curr_url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote(self.keywords)
            else :
                if None == self.next_url :
                    print('[Warning] No more results.')
                    break;
                self.curr_url = self.next_url

            # Download html
            self.html = self.agent.get_data(self.curr_url)
            if None == self.html :
                print('[ERROR] Download html failed.')
                break;

            # Parse html to bs object
            self.soup = BeautifulSoup(self.html, 'html.parser')
            if None == self.soup :
                print('[ERROR] Parse html failed.')
                break;

            # Fetch wrapper
            wrapper   = self.soup.find_all(name = 'div', attrs = {'id' : 'wrapper_wrapper'})
            if len(wrapper) != 1 :
                print('[ERROR] Invalid, wrapper num = ', len(wrapper))
                break;

            # Fetch container
            container = wrapper[0].find_all(name = 'div', attrs = {'id' : 'container'})
            if len(container) != 1 :
                print('[ERROR] Invalid, contianer num = ', len(container))
                break;

            # Fetch the url of the next page from wrapper
            page_container = container[0].find_all(name = 'div', attrs = {'id' : 'page'})
            if len(page_container) != 1 :
                print('[ERROR] Invalid, page container num = ', len(page_container))
                break;

            next_link = page_container[0].find_all(name = 'a', attrs = {'class': 'n'})
            if len(next_link) != 1 and len(next_link) != 2 :
                print('[ERROR] Invalid, next link num = ', len(next_link))
                break;

            self.next_url = 'http://www.baidu.com' + next_link[len(next_link) - 1].get('href')

            # Fetch results from wrapper
            result_container = container[0].find_all(name = 'div', attrs = {'id' : 'content_left'})
            if len(result_container) != 1 :
                print('[ERROR] Invalid, result container num = ', len(result_container))
                break;
            
            results = result_container[0].find_all(name = 'div', attrs = {'class' : re.compile('^result')})

            if not results :
                break

            # Convert result from HTML to our structure
            for result in results :
                tmp = Result()
                tmp.title = result.h3.get_text()
                tmp.href  = result.h3.a.get('href')
                tmp.link  = self.agent.get_url(tmp.href)
                tmp.tpl   = result.get('tpl')
                tmp.rank  = result.get('id')
                self.results.append(tmp)

                num += 1
                if num == n :
                    break;

        return self.results[begin : begin + num]

if __name__ == "__main__" :
    proxy = None

    keywords = "五月天 突然好想你"

    my_agent   = crawler_agent.CrawlerAgent(proxy = proxy)
    my_crawler = Crawler(my_agent)
    results    = my_crawler.get_top_n_results(keywords, 13)

    for result in results :
        print('----------------------------------------')
        print('title:    ', result.title)
        print('link:     ', result.link)
        print('href:     ', result.href)
        print('tpl:      ', result.tpl)
        print('rank:     ', result.rank)

