# # import tkinter as tk
#
# # find_sender.py
# # From foo@bar.baz Thu Dec 20 01:22:50 2008
# # Return-Path: <foo@bar.baz>
# # Received: from xyzzy42.bar.com (xyzzy.bar.baz [123.456.789.42])
# # by frozz.bozz.floop (8.9.3/8.9.3) with ESMTP id BAA25436
# # for <magnus@bozz.floop>; Thu, 20 Dec 2004 01:22:50 +0100 (MET)
# # Received: from [43.253.124.23] by bar.baz
# # (InterMail vM.4.01.03.27 201-229-121-127-20010626) with ESMTP
# # id <20041220002242.ADASD123.bar.baz@[43.253.124.23]>; Thu, 20 Dec 2004 00:22:42 +0000
# # User-Agent: Microsoft-Outlook-Express-Macintosh-Edition/5.02.2022
# # Date: Wed, 19 Dec 2008 17:22:42 -0700
# # Subject: Re: Spam
# # From: Foo Fie <foo@bar.baz>
# # To: Magnus Lie Hetland <magnus@bozz.floop>
# # CC: <Mr.Gumby@bar.baz>
# # Message-ID: <B8467D62.84F%foo@baz.com>
# # In-Reply-To: <20041219013308.A2655@bozz.floop> Mime- version: 1.0
# # Content-type: text/plain; charset="US-ASCII" Content-transfer-encoding: 7bit
# # Status: RO
# # Content-Length: 55
# # Lines: 6
# # So long, and thanks for all the spam!
# #
# # Yours,
# # Foo Fie
# '''
# 对于这个程序，应注意如下几点。
#  为提高处理效率，我编译了正则表达式。
#  将用于匹配要提取文本的子模式放在圆括号内，使其变成了一个编组。
#  使用了一个非贪婪模式，使其只匹配最后一对尖括号（以防姓名也包含尖括号）。
#  使用了美元符号指出要使用这个模式来匹配整行（直到行尾）。
#  使用了if语句来确保匹配后才提取与特定编组匹配的内容。
# 要列出邮件头中提及的所有邮件地址，需要创建一个只与邮件地址匹配的正则表达式，然后
# 使用方法findall找出所有与之匹配的内容。为避免重复，可将邮件地址存储在本章前面介绍的集合中。最后，提取键，将它们排序并打印出来。
#  每个可选的子模式都放在圆括号内。
#  每个可选的子模式都可以出现，也可以不出现。
# 问号表示可选的子模式可出现一次，也可不出现。还有其他几个运算符用于表示子模式可重
# 复多次。
#  (pattern)*：pattern可重复0、1或多次。
#  (pattern)+：pattern可重复1或多次。
#  (pattern){m,n}：模式可从父m~n次
# '''
# import re
# import fileinput
#
# #输入文件路径
# input_file = "D:\message.eml.txt"
#
# pat = re.compile('From: (.*) <.*?>$')
#
# pat1 = re.compile(r'[a-z\-\.]+@[a-z\-\.]+', re.IGNORECASE)
# addresses = set()
#
# for line in fileinput.input(input_file):
#     m = pat.match(line)
#     if m: print(m.group(1))
#
#     for address in pat1.findall(line):
#         addresses.add(address)
# for address in sorted(addresses):
#     print (address)
#
# # pat1 = re.compile(r'[a-z\-\.]+@[a-z\-\.]+', re.IGNORECASE)
# # addresses = set()
# # for line in fileinput.input():
# #     for address in pat.findall(line):
# #         addresses.add(address)
# # for address in sorted(addresses):
# #     print (address)
#
# # templates.py
# # files = ('D:\\magnus.txt', 'D:\\Template.txt')
# input_file1 = "D:\Calculate.txt"
# input_file2 = "D:\magnus.txt"
# input_file3 = "D:\Template.txt"
# # 与使用方括号括起的字段匹配
# field_pat = re.compile(r'\[(.+?)\]')
# # 我们将把变量收集到这里：
# scope = {}
# # 用于调用re.sub：
# def replacement(match):
#     code = match.group(1)
#     try:
#         # 如果字段为表达式，就返回其结果：
#         return str(eval(code,scope))
#
#     except SyntaxError:
#         # 否则在当前作用域内执行该赋值语句
#
#         # 并返回一个空字符串
#         return ''
# # 获取所有文本并合并成一个字符串：
# #（还可采用其他办法来完成这项任务，详情请参见第11章）
# lines = []
# # for line in fileinput.input(input_file1):
# #     lines.append(line)
# # text = ''.join(lines)
#
# text = ''
# for line in fileinput.input(input_file1):
#     text += line
# # 替换所有与字段模式匹配的内容：
# print(text)
# print(field_pat.sub(replacement, text))
#
# # b'<a href="([^"]+)" .*?>about</a>',





import re
line ='192.168.0.1 25/Oct/2012:14:46:34 "GET /api HTTP/1.1" 200 44 "http://abc.com/search" "Mozilla/5.0"'
reg = re.compile('^(?P<remote_ip>[^ ]*) (?P<date>[^ ]*) "(?P<request>[^"]*)" (?P<status>[^ ]*) (?P<size>[^ ]*) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"')
regMatch = reg.match(line)
linebits = regMatch.groupdict()
print(linebits)
for k, v in linebits.items() :
    print(k+": "+v)

str = "a123b456b"
print(re.findall(r"a(.+?)b", str))

print(re.findall(r"a(.+)b", str))

# 如果你要多行匹配，那么需要加上re.S和re.M标志. 加上re.S后, .将会匹配换行符，默认.不会匹配换行符
str = "a23b\na34b"

print(re.findall(r"a(\d+)b.+a(\d+)b", str))
# 输出[]
# 因为不能处理str中间有\n换行的情况
print(re.findall(r"a(\d+)b.+a(\d+)b", str, re.S))
# 加上re.M后,^$标志将会匹配每一行，默认^和$只会匹配第一行.
print(re.findall(r"^a(\d+)b", str))
# 输出['23']
print(re.findall(r"^a(\d+)b", str, re.M))
