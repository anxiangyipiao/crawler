import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

provinces_hrss = {
    "北京": "http://rsj.beijing.gov.cn/",
    "天津": "http://hrss.tj.gov.cn/",
    "河北": "http://rst.hebei.gov.cn/",
    "山西": "http://rst.shanxi.gov.cn/",
    "内蒙古": "http://hrss.nmg.gov.cn/",
    "辽宁": "http://rst.ln.gov.cn/",
    "吉林": "http://rst.jl.gov.cn/",
    "黑龙江": "http://hlj12333.gov.cn/",
    "上海": "http://rsj.sh.gov.cn/",
    "江苏": "http://jshrss.jiangsu.gov.cn/",
    "浙江": "http://www.zjhrss.gov.cn/",
    "安徽": "http://hrss.ah.gov.cn/",
    "福建": "http://hrss.fujian.gov.cn/",
    "江西": "http://rst.jiangxi.gov.cn/",
    "山东": "http://hrss.shandong.gov.cn/",
    "河南": "http://hrss.henan.gov.cn/",
    "湖北": "http://rst.hubei.gov.cn/",
    "湖南": "http://rst.hunan.gov.cn/",
    "广东": "http://hrss.gd.gov.cn/",
    "广西": "http://rst.gxzf.gov.cn/",
    "海南": "http://hrss.hainan.gov.cn/",
    "重庆": "http://rlsbj.cq.gov.cn/",
    "四川": "http://rst.sc.gov.cn/",
    "贵州": "http://rst.guizhou.gov.cn/",
    "云南": "http://hrss.yn.gov.cn/",
    "西藏": "http://xz.hrss.gov.cn/",
    "陕西": "http://rst.shaanxi.gov.cn/",
    "甘肃": "http://rst.gansu.gov.cn/",
    "青海": "http://www.qhhrss.gov.cn/",
    "宁夏": "http://hrss.nx.gov.cn/",
    "新疆": "http://www.xjrs.gov.cn/"
}

def get_province_sections(provinces):
    """检查站点是否可访问，提取招标和招聘栏目链接"""
    sections = {}
    for province, base_url in provinces.items():
        print(f"正在检查: {province} - {base_url}")
        tender_link = None
        recruit_link = None
        try:
            # 部分网站需要模拟浏览器访问
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            resp = requests.get(base_url, headers=headers, timeout=15, verify=False) # 增加超时时间并忽略SSL验证错误
            resp.raise_for_status() # 检查请求是否成功
            resp.encoding = resp.apparent_encoding # 自动检测编码
            soup = BeautifulSoup(resp.text, 'html.parser')

            # 尝试多种关键词查找链接
            tender_keywords = ['招标', '采购', '交易']
            recruit_keywords = ['招聘', '录用', '人才', '就业']

            for a in soup.find_all('a', href=True):
                text = a.get_text(strip=True)
                href = a['href']

                # 查找招标链接
                if tender_link is None:
                    for keyword in tender_keywords:
                        if keyword in text:
                            tender_link = urljoin(base_url, href)
                            break # 找到一个即停止

                # 查找招聘链接
                if recruit_link is None:
                    for keyword in recruit_keywords:
                        if keyword in text:
                            recruit_link = urljoin(base_url, href)
                            break # 找到一个即停止

                # 如果两个都找到了，提前结束当前页面的查找
                if tender_link and recruit_link:
                    break

            sections[province] = {'招标': tender_link, '招聘': recruit_link}
            print(f"  找到招标: {tender_link}")
            print(f"  找到招聘: {recruit_link}")

        except requests.exceptions.RequestException as e:
            print(f"  访问失败: {e}")
            sections[province] = {'招标': None, '招聘': None, '错误': str(e)}
        except Exception as e:
            print(f"  处理时发生错误: {e}")
            sections[province] = {'招标': tender_link, '招聘': recruit_link, '错误': str(e)} # 保留已找到的链接

    return sections

# 如果直接运行此文件，则执行检查
if __name__ == "__main__":
    # 禁用requests库的SSL警告
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    print("开始检查各省人社厅网站...")
    provinces_sections = get_province_sections(provinces_hrss)
    print("\n检查完成，结果如下:")
    import json
    print(json.dumps(provinces_sections, indent=4, ensure_ascii=False))




json_str= {
    "北京": {
        "招标": "http://rsj.beijing.gov.cn/xxgk/zfxxgk/zfcg/",
        "招聘": "http://rsj.beijing.gov.cn/xxgk/gkzp/"
    },
    "天津": {
        "招标": null,
        "招聘": "http://hrss.tj.gov.cn/xinwenzixun/xinwendongtai/202504/t20250407_6902089.html"
    },
    "河北": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='rst.hebei.gov.cn', port=80): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x000001711EA149A0>, 'Connection to rst.hebei.gov.cn timed out. (connect timeout=15)'))"        
    },
    "山西": {
        "招标": null,
        "招聘": "http://rst.shanxi.gov.cn/ztzl/jyfwj/"
    },
    "内蒙古": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='hrss.nmg.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711EAEA110>: Failed to resolve 'hrss.nmg.gov.cn' ([Errno 11001] getaddrinfo failed)\"))"
    },
    "辽宁": {
        "招标": "http://rst.ln.gov.cn/rst/zfxx/fdzdgknr/zfcg/index.shtml",
        "招聘": "http://rst.ln.gov.cn/rst/zxzx/jycy/index.shtml"
    },
    "吉林": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='rst.jl.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711E81CFA0>: Failed to resolve 'rst.jl.gov.cn' ([Errno 11001] getaddrinfo failed)\"))"   
    },
    "黑龙江": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='hlj12333.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711E81D8D0>: Failed to resolve 'hlj12333.gov.cn' ([Errno 11001] getaddrinfo failed)\"))"
    },
    "上海": {
        "招标": null,
        "招聘": "http://rsj.sh.gov.cn/tgsgg_17341/20250424/t0035_1432075.html"
    },
    "江苏": {
        "招标": null,
        "招聘": "http://jshrss.jiangsu.gov.cn/col/col77276/index.html"
    },
    "浙江": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='www.zjhrss.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711ED44E80>: Failed to resolve 'www.zjhrss.gov.cn' ([Errno 11001] getaddrinfo failed)\"))"
    },
    "安徽": {
        "招标": null,
        "招聘": "https://hrss.ah.gov.cn/zxzx/gzdt/80764828.html"
    },
    "福建": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='hrss.fujian.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711EE3D420>: Failed to resolve 'hrss.fujian.gov.cn' ([Errno 11001] getaddrinfo failed)\"))"
    },
    "江西": {
        "招标": null,
        "招聘": null
    },
    "山东": {
        "招标": null,
        "招聘": "http://hrss.shandong.gov.cn/articles/ch00005/202504/904ed611-eb4e-426f-a3c6-825a748ca40a.shtml"
    },
    "河南": {
        "招标": "http://hrss.henan.gov.cn/zwgk/xxgk/bmcg/",
        "招聘": "http://hrss.henan.gov.cn/2025/04-25/3151860.html"
    },
    "湖北": {
        "招标": null,
        "招聘": "http://rst.hubei.gov.cn/bmdt/rsyw/202504/t20250425_5629284.shtml"
    },
    "湖南": {
        "招标": null,
        "招聘": "http://rst.hunan.gov.cn/rst/xxgk/zpzl/index.html"
    },
    "广东": {
        "招标": null,
        "招聘": "https://hrss.gd.gov.cn/zwgk/xxgkml/lbtp/content/post_4665488.html"
    },
    "广西": {
        "招标": null,
        "招聘": "http://rst.gxzf.gov.cn/xwdt/xwdtzyxw/t20061590.shtml"
    },
    "海南": {
        "招标": "http://hrss.hainan.gov.cn/hrss/0400/202504/f3f427138d884ff6b7f1290083dbe6a0.shtml?ddtab=true",
        "招聘": "http://hrss.hainan.gov.cn/hrss/zwdt/202502/c167c581d05b4e13ade817529ca11402.shtml?ddtab=true"
    },
    "重庆": {
        "招标": "https://ggzyjyjgj.cq.gov.cn/",
        "招聘": "http://dzcs.newjobs.com.cn"
    },
    "四川": {
        "招标": "http://rst.sc.gov.cn/rst/gsgg/2025/4/27/c9cf737a38a7426d8470aa783db66a67.shtml",
        "招聘": "http://rst.sc.gov.cn/rst/zwyw/2025/4/22/aa3f07e3fdd04e0a8501fdcec00f4100.shtml"
    },
    "贵州": {
        "招标": "https://rst.guizhou.gov.cn/xwzx/xwdt/202504/t20250419_87548804.html",
        "招聘": "https://rst.guizhou.gov.cn/xwzx/gggs/202504/t20250409_87494311.html"
    },
    "云南": {
        "招标": null,
        "招聘": "http://hrss.yn.gov.cn/NewsLsit.aspx?ClassID=458"
    },
    "西藏": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='xz.hrss.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711E9DDFC0>: Failed to resolve 'xz.hrss.gov.cn' ([Errno 11001] getaddrinfo failed)\"))" 
    },
    "陕西": {
        "招标": "http://ggzy.shaanxi.gov.cn/",
        "招聘": "http://rst.shaanxi.gov.cn/sy/jdtp/202502/t20250208_3429049.html"
    },
    "甘肃": {
        "招标": null,
        "招聘": null,
        "错误": "412 Client Error: Precondition Failed for url: https://rst.gansu.gov.cn/"
    },
    "青海": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='www.qhhrss.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711E9DE7A0>: Failed to resolve 'www.qhhrss.gov.cn' ([Errno 11001] getaddrinfo failed)\"))"
    },
    "宁夏": {
        "招标": "https://hrss.nx.gov.cn/xxgk/gkmu/zfcg/",
        "招聘": "http://hrss.nx.gov.cn/gzdt/tpxx/202501/t20250117_4793382.html"
    },
    "新疆": {
        "招标": null,
        "招聘": null,
        "错误": "HTTPConnectionPool(host='www.xjrs.gov.cn', port=80): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0x000001711ED2F610>: Failed to resolve 'www.xjrs.gov.cn' ([Errno 11001] getaddrinfo failed)\"))"
    }
}