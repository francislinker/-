
#思路分析：

# 帖子链接列表=parseHtml.xpath('...')
# for 一个帖子链接 in 帖子链接列表:
#     图片链接列表 = 对一个帖子发请求后xpath出来的
#     for 一个图片链接 in 图片链接列表：
#         发请求，写入

#第一页：url = 'https://tieba.baidu.com/f?kw=??&pn=0'
#第n页：pn = (n-1)*50

#<a rel="noreferrer" href="/p/3868265577" title="英国麦田圈组织悬赏10万英镑！！！" target="_blank" class="j_th_tit ">英国麦田圈组织悬赏10万英镑！！！</a>
#xpath表达式：http://tieba.baidu.com/p/3868265577 ----//div[@class="t_con cleafix"]/div/div/div/a/@href
#提取帖子中图片的链接

import requests
from lxml import etree

class BaiduSpyder(object):
    def __init__(self):
        self.baseurl = 'https://tieba.baidu.com'
        self.headers = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
        self.url =  'https://tieba.baidu.com/f?'

    #获取帖子链接：
    def getPageUrl(self,params):
        res = requests.get(url=self.url,headers=self.headers,
                           params=params)
        res.encoding = 'utf-8'
        html = res.text
        #从html中提取帖子链接
        parsehtml = etree.HTML(html)
        tlist = parsehtml.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        #H获得列表tlist:['/p32123','/p4213'...],拼接帖子链接
        print(tlist)
        for t in tlist:
            tlink = self.baseurl + t
            self.getImgUrl(tlink)


    #获取一个帖子中图片的链接
    def getImgUrl(self,tlink):

        res = requests.get(url=tlink,headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text

        parsehtml = etree.HTML(html)
        imgurlList = parsehtml.xpath('//div[@class="d_post_content j_d_post_content "]'
                                     '/img[@class="BDE_Image"]/@src|//div[@class="video_src_wrapper"]/embed/@data-video')
        print(imgurlList)#获得列表：帖子的图片链接
        for imgurl in imgurlList:
            self.writeImg(imgurl)

    #保存图片
    def writeImg(self,imgurl):
        res = requests.get(imgurl,headers=self.headers)
        res.encoding = 'utf-8'
        html = res.content
        #利用字符串切片后十为作为文件名
        filename = imgurl[-10:]

        with open('/home/tarena/django_project/'
                  'crawl/百度贴吧＿图片xpath爬取/贴吧图片/%s'%filename,'wb') as f:
            f.write(html)
        print('%s抓取成功' % filename)
    # /django_project/crawl/百度贴吧＿图片xpath爬取/
    #主函数
    def workOn(self):
        name = input('请输入贴吧名:')
        start = input('起始页：')
        end = input('终止页：')
        for i in range(int(start),int(end)+1):
            pn = (i-1)*50
            #定义查询参数
            params = {
                'kw':name,
                'pn':str(pn)
            }
            self.getPageUrl(params)


if __name__ == '__main__':
    spyder = BaiduSpyder()
    spyder.workOn()
