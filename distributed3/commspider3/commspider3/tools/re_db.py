# -*- coding: utf-8 -*-
import re,sys

# reload(sys)
# sys.setdefaultencoding('UTF-8')

def dealstr(table1):
    table = table1.lower()
    table = re.sub(r"<table\s?[^>]*>", '<table>', table)

    table = re.sub(r"<tbody\s?[^>]*>", '', table)
    table = re.sub(r"</tbody\s?[^>]*>", '', table)


    table = re.sub(r"<h3\s?[^>]*>", '<h3>', table)

    table = re.sub(r"<tr\s?[^>]*>", '<tr>', table)
    table = re.sub(r"<td\s?[^>]*>", '<td>', table)

    table = re.sub(r"<th\s?[^>]*>", '<td>', table)
    table = re.sub(r"</th\s?[^>]*>", '</td>', table)

    table = re.sub(r"<!--[\s\S]*?-->", '', table)#去除html注释部分
    table = re.sub(r"<(?!t|/t)[^>]*>", '', table)
    table = re.sub(r"&nbsp;", '', table)

    # pattern = re.compile(r'<tr><td>.+?</td></tr>')
    # td_match = pattern.finditer(table)
    # # td_match = re.findall(pattern, table)
    # a =''
    # for item in td_match:
    #     item = item.group(0)
    #     pattern = re.compile(r'\s+')
    #     replace = pattern.search(item)
    #     table = replace.group(1) + replace.group(2)
    #     a += table

    table = re.sub(r"[\r\n]", '', table)
    table = re.sub(r">\s*<", '><', table)

    table = re.sub(r"\s*", '', table)
    # table = table.replace('\t', '').replace('\n', '').replace(' ', '')

    # return a
    return table

if __name__ == '__main__':

    b = dealstr('''<table border="0" cellspacing="0" cellpadding="0" width="280" align="center" style="margin-top:4px; margin-bottom:14px;">
		<tbody><tr>
			<td colspan="2"><h3 class="tac mb5 a-blue">山东明水大化集团</h3></td>
		</tr>
			</tbody></table>''')

    print(b)
    # print(type(b))