
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

# 使用POP3进行邮件接收
# python3内置了一个poplib模块，邮件接收的过程其实和发件是相反的，一个打包一个解析
# 主要步骤其实就两步：
# 1）使用poplib将邮件的原始件下载到本地
# 2）使用email解析原始文本，进行对象还原

# email = input('627277482@qq.com')
# password = input('dulq7551')
# pop3_server = input('627277482@qq.com')
# pop3_server =  'pop.163.com'  #'pop.sina.com'    #imap.163.com

email = input('Email:627277482@qq.com')
password = input('Password:dulq7551')
pop3_server = input('POP3 server:pop.163.com')
pop3_server = 'pop.163.com'

#这是检测编码部分，有点不懂
def guess_charset(msg):
	charset = msg.get_charset()
	if charset is None:
		content_type = msg.get('Content-type', '').lower()
		pos = content_type.find('charset=')
		if pos >= 0:
			charset = content_type[pos + 8:].strip()
	return charset


#这里只取出第一发件人
def decode_str(s):
	value, charset = decode_header(s)[0]
	if charset:
		value = value.decode(charset)
	return value

#递归打印信息
def print_info(msg, indent = 0):
	if indent == 0:
		for header in ['From', 'To', 'Subject']:
			value = msg.get(header, '')
			if value:
				if header == 'Subject':
					value = decode_str(value)
				else:
					hdr, addr = parseaddr(value)
					name = decode_str(hdr)
					value = u'%s <%s>' % (name, addr)
			print('%s%s: %s' % ('  ' * indent, header, value))
	if (msg.is_multipart()):
		parts = msg.get_payload()
		for n, part in enumerate(parts):
			print('%spart %s' % ('  '*indent, n))
			print('%s--------------------' % ('   '*indent))
			print_info(part, indent + 1)
	else:
		content_type = msg.get_content_type()
		if content_type == 'text/plain' or content_type == 'text/html':
			content = msg.get_payload(decode = True)
			charset = guess_charset(msg)
			if charset:
				content = content.decode(charset)
			print('%sText: %s' % ('  '*indent, content + '...'))
		else:
			print('%sAttachment: %s' % ('  '*indent, content_type))

#下载原始邮件
server = poplib.POP3(pop3_server)
server.set_debuglevel(0)
print(server.getwelcome().decode('utf-8'))
server.user(email)
server.pass_(password)

#打印邮件数量和占用空间
print('Message: %s, Size: %s' % server.stat())
resp, mails, octets = server.list()
print(mails)

#解析邮件
index = len(mails)
resp, lines, octets = server.retr(index)
msg_content = b'\r\n'.join(lines).decode('utf-8')
msg = Parser().parsestr(msg_content)
print_info(msg)