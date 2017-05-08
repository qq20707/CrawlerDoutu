#-*- coding:utf-8 -*-
import requests,threading
from lxml import etree
from bs4 import BeautifulSoup

def get_html(url):
	#url = 'https://www.doutula.com/article/list?page=1'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	request = requests.get(url = url,headers = headers)
	request.encoding = 'utf-8'
	response = request.content #获取的源码
	#print(response)
	return response

#获取图片的超链接，获取源代码
def get_img_html(html):
	soup = BeautifulSoup(html,'lxml')
	all_a = soup.find_all('a',class_='list-group-item')#找到a标签
	for i in all_a:
		#print(i)
		#获取超链接源码
		img_html = get_html(i['href'])
		print("--------")
		#print(img_html)
		get_img(img_html)
		#print(i['href'])

def get_img(html):
	soup = etree.HTML(html)
	items = soup.xpath('//div[@class="artile_des"]')#@是用来选取属性
	for item in items:
		imgurl_list = item.xpath('table/tbody/tr/td/a/img/@onerror')
		print(imgurl_list)
		start_save_img(imgurl_list)

x = 1 
def save_img(img_url):
	global x
	x +=1
	img_url = img_url.split('=')[-1][1:-2].replace('jp','jpg')
	print("正在下载"+"http:"+img_url)
	img_content = requests.get('http:'+img_url).content
	with open('doutu/%s.jpg' % x,'wb') as f:
		f.write(img_content)
#多线程下载
def start_save_img(imgurl_list):
	for i in imgurl_list:
		print(i)
		th = threading.Thread(target=save_img,args=(i,))
		th.start()
#多页
def main():
	start_url = 'https://www.doutula.com/article/list?page='
	for i in range(1,10):
		start_html = get_html(start_url.format(i))
		get_img_html(start_html)#获取图片链接源码
	imgurl="this.src='//img.doutula.com/production/uploads/image/2017/05/07/20170507114728_gLKtzv.jpg'"
	save_img(imgurl)


if __name__ == '__main__':
	main()
