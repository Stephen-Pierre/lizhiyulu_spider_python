import urllib.request
import re
import os


def handle_request(url, page=None):
	
	'''创建请求对象并返回'''

	# 拼接url
	if page != None:
		url = url + str(page) + '.html'
	# 创建头部信息
	headers = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
	}
	# 创建请求对象并作为参数返回
	request = urllib.request.Request(url, headers=headers)
	return request

def get_text(url):
	# 调用函数获取请求对象
	request = handle_request(url)
	# 发送请求获取内容
	content = urllib.request.urlopen(request).read().decode()
	# 编写正则获取内容
	pattern_text = re.compile(r'<div class="neirong">(.*?)</div>', re.S)
	li_text = pattern_text.findall(content)
	# 去掉图片链接
	text = li_text[0]
	pat = re.compile(r'<img .*?>')
	text = pat.sub('', text)
	return text


def write(title, content):
	# 创建保存目标文件夹
	path = '励志签名'
	if not os.path.exists(path):
			os.mkdir(path)

	filename = path + '/' + title + '.html'
	string = '<h1>%s</h1>%s'%(title, content)
	with open(filename, 'w') as fp:
		fp.write(string)
		

def parse_content(content):
	
	# 正则匹配所有标题及内容链接
	pattern_texturl = re.compile(r'<h3><a href="(.*?)"><b>(.*?)</b></a></h3>')
	li = pattern_texturl.findall(content)
	for item in li:
		title = item[1]
		url_text = 'http://www.yikexun.cn' + item[0]
		text = get_text(url_text)
		write(title, text)



def main():
	url = 'http://www.yikexun.cn/lizhi/qianming/list_50_'
	# 获取起始和结束页码
	start_page = int(input('请输入起始页码：'))
	end_page = int(input('请输入结束页码：'))
	# 根据起始和结束页码遍历发起请求
	for page in range(start_page, end_page + 1):
		request = handle_request(url, page)
		# 发送请求
		content = urllib.request.urlopen(request).read().decode()
		# 解析内容
		parse_content(content)

if __name__ == '__main__':
	main()