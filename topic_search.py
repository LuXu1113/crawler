# coding: utf-8
# python-version: 3.6

import re
import os
import crawler_agent
import crawler_for_baidu_se
from bs4 import BeautifulSoup


if __name__ == "__main__" :
    dev_proxy    = 'http://dev-proxy.oa.com:8080'
    office_proxy = 'http://web-proxy.oa.com:8080'

    agent   = crawler_agent.CrawlerAgent(proxy = dev_proxy)
    crawler = crawler_for_baidu_se.Crawler(agent)
    
    crawler.set_keywords('FPGA')
    result_list = crawler.get_next_n_results(10)

    for result in result_list :
        if None == result.link :
            print('[ERROR][%s:%d]: result.link is None' % (__file__, sys.getframe().f_lineno))
            break

        result_html = agent.get_data(result.link)
        if None == result_html :
            print('[ERROR][%s:%d]: result html is None' % (__file__, sys.getframe().f_lineno))
            break
            
        result_soup = BeautifulSoup(result_html, 'html.parser')
        if None == result_soup :
            print('[ERROR][%s:%d]: result soup is None' % (__file__, sys.getframe().f_lineno))
            break

        [script.extract() for script in result_soup.find_all('script')]
        [style.extract()  for style  in result_soup.find_all('style')]

        texts = result_soup.find_all(text = True)
        for text in texts :
            text = text.strip()
            if len(text) > 0 :
                print(text)

        print('===============================================================')
        break;
