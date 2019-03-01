from lxml import etree

import requests

url = 'https://tieba.baidu.com/p/6051491278'
headers = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}

res = requests.get(url,
                   headers=headers)
res.encoding = 'utf-8'
html = res.text

parsehtml = etree.HTML(html)
rlist = parsehtml.xpath('//div[@class="video_src_wrapper"]/embed/@data-video')
print(rlist)
filename = url[-10:]
with open('/home/tarena/django_project/'
          'crawl/百度贴吧＿图片xpath爬取/贴吧视频/%s' % filename, 'wb') as f:
    f.write(html)