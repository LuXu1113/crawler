# coding: utf-8
# python-version: 3.6

import re
import crawler_agent
import crawler_for_baidu_se

def result_is_music(result) :
    if result_list[i].tpl == 'musicsongs' :
        return True
    if result_list[i].tpl == 'musicsong' :
        return True

    return False;

if __name__ == "__main__" :
    proxy = None

    in_file_list = ['D:\\data\\song_title\\songs']
    agent   = crawler_agent.CrawlerAgent(proxy = dev_proxy)
    crawler = crawler_for_baidu_se.Crawler(agent)

    for in_file in in_file_list :
        in_fh = open(in_file, mode = 'r', encoding = 'UTF-8')

        out_file_music    = in_file + '_is_music'
        out_file_nonmusic = in_file + '_is_not_music'
        out_file_fail     = in_file + '_fail_case'
        out_fh_music      = open(out_file_music, mode = 'w', encoding = 'UTF-8')
        out_fh_nonmusic   = open(out_file_nonmusic, mode = 'w', encoding = 'UTF-8')
        out_fh_fail       = open(out_file_fail, mode = 'w', encoding = 'UTF-8')

        while True :
            lines = in_fh.readlines(100)
            if not lines :
                break;
            
            for line in lines :
                is_music = False

                try :
                    crawler.set_keywords(line)
                    result_list = crawler.get_results(5)
                except :
                    out_fh_fail.write(line)
                    out_fh_fail.flush()
                    continue

                if len(result_list) == 0 :
                    out_fh_fail.write(line)
                    out_fh_fail.flush()
                    continue
                
                for i in range(len(result_list)) :
                    if result_is_music(result_list[i]) :
                        is_music = True
                        break;

                if is_music :
                    out_fh_music.write(line)
                    out_fh_music.flush()
                else :
                    print(line)
                    out_fh_nonmusic.write(line)
                    out_fh_nonmusic.flush()

        out_fh_fail.close()
        out_fh_nonmusic.close()
        out_fh_music.close()
        in_fh.close()
