# Crawer

## Introduction

这是一个 Python 实现的网络爬虫，各个文件实现的功能如下：

## Modules
crawler_agent: 提供给它一个 URL，它可以把 URL 指向的网页内容抓取到本地；

crawler_for_baidu: 提供给它一个或几个搜索关键词，它可以把这些关键词在百度的搜索结果抓取下来，抓取的每条结果都包含以下的信息：

    title: 搜索结果的标题，也就是百度搜索引擎返回一条结果里最上面字体比较大的那一行；

    href: 搜索结果的直接链接，访问这个链接，百度会把它转成结果的真实 URL，再返回给我们；

    link: 搜索结果的真实链接；

    tpl: 百度标注的这条搜索结果的类型；

    rank: 搜索结果被百度排的序号。

    一个实例如下：
    title: 突然好想你在线试听_高音质歌曲_虾米音乐
    link: http://www.xiami.com/search?key=%E7%AA%81%E7%84%B6%E5%A5%BD%E6%83%B3%E4%BD%A0
    href: http://www.baidu.com/link?url=uP1pKlrf_bdgyNyYe3t7iZNsZOeg4-7UA6AO4DzCMyYYlpg8c_d_wbvd5tT7qt8F8-VAezuE21i6bAbQ08u-kzfAeOI3pufUIJirGzef-baB3yMq9RPuvDD63rTGV4e_
    tpl: musicsongs
    rank: 1

music_filter: 这是一个小工具，用来过滤关键字是不是一首歌曲的名字，判断的方法是把关键字提交给百度，如果返回的前五个结果有 tpl 是音乐的，就认为这个关键字是歌名。

topic_search: 还未完成

