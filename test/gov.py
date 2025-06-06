# -*- coding: utf-8 -*-
from requests_html import HTMLSession
import lxml



session = HTMLSession()


url = 'https://www.mca.gov.cn/mzsj/xzqh/2025/202401xzqh.html'



headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "https_waf_cookie=c4f37d08-ff21-4e1857af76162e23418208eedff7e6133432",
    "Host": "www.mca.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://www.mca.gov.cn/n156/n2679/index.html", 
    "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}


response = session.get(url, headers=headers)
response.encoding = 'utf-8'



if response.status_code == 200:


    # save the HTML content
    # with open('gov.html', 'w', encoding='utf-8') as f:
    #     f.write(response.text)

    html = response.text
    tree = lxml.html.fromstring(html)
    
    # <table border=0 cellpadding=0 cellspacing=0 width=945 style='border-collapse:
#  collapse;table-layout:fixed;width:709pt'>
    # Extract the table rows
    rows = tree.xpath('//tr[@height="19"]')
    # Extract data from each row
    data = []

    province = ''

    city = ''

    for row in rows:

        cells = row.xpath('.//td')

        print(cells[2].xpath('.//span/text()'))

        # 如果不存在span标签，是省级行政区
        if not cells[2].xpath('.//span'):

            province = cells[2].text_content().strip()

            city = ''

            full_name = province
            
        # 如果存在span标签，但span里只有一个&nbsp; 是市级行政区
        elif cells[2].xpath('.//span') and cells[2].xpath('.//span/text()') ==['\xa0']:

            city = cells[2].text_content().strip()

            full_name = f"{province}{city}".strip()

        # 如果存在span标签，但span里有2个&nbsp;，是县级行政区

        elif cells[2].xpath('.//span') and cells[2].xpath('.//span/text()') == ['\xa0\xa0 ']:
            name = cells[2].text_content().strip()

            full_name = f"{province}{city}{name}".strip()
        

        item = {
                'code': cells[1].text_content().strip(),
                'name': full_name,
                
            }
        
        data.append(item)
       
    
    # save csv

    import csv
    with open('govs.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['code', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    