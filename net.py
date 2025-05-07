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


