import requests
from lxml import html
import time
import json


class HospitalCrawler:
    """医院信息爬虫类"""
    
    def __init__(self):
        self.base_url = 'https://y.dxy.cn/hospital/'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 地区映射
        self.locations = {
            '110000': "北京市",
            '310000': "上海市", 
            '440000': "广东省",
            '330000': "浙江省",
            '120000': "天津市",
            '410000': "河南省",
            '500000': "重庆市",
            '320000': "江苏省",
            '370000': "山东省",
            '420000': "湖北省",
            '430000': "湖南省",
            '610000': "陕西省",
            '210000': "辽宁省",
            '340000': "安徽省",
            '220000': "吉林省",
            '360000': "江西省",
            '150000': "内蒙古自治区",
            '620000': "甘肃省",
            '650000': "新疆维吾尔自治区",
            '540000': "西藏自治区",
            '640000': "宁夏回族自治区",
            '460000': "海南省",
            '450000': "广西壮族自治区",
            '520000': "贵州省",
            '230000': "黑龙江省",
            '350000': "福建省",
            '140000': "山西省",
            '130000': "河北省",
            '630000': "青海省",
            '530000': "云南省",
            '510000': "四川省",
        }
        
        # 医院类型映射
        self.trades = {
            "1": "公立医院",
            "4": "私立医院",
        }
        
        # 医院属性映射
        self.attributions = {
            "1": "综合医院",
            "2": "专科医院",
        }
        
        # 医院等级映射
        self.grades = {
            "2": "三甲",
            "3": "三乙", 
            "4": "三丙",
            "5": "二甲",
            "6": "二乙",
            "7": "二丙",
            "8": "一甲",
            "9": "一乙",
            "10": "一丙",
            '14': '一级',
            '15': '未定级',
        }
    
    def get_hospitals_by_params(self, location_code=None, trade_code=None, 
                               grade_code=None, attribution_code=None, page=1):
        """
        根据参数获取医院列表
        
        Args:
            location_code: 地区代码
            trade_code: 医院类型代码
            grade_code: 医院等级代码  
            attribution_code: 医院属性代码
            page: 页码
            
        Returns:
            list: 医院信息列表
        """
        params = {"page": str(page)}
        
        if location_code:
            params["location"] = location_code
        if trade_code:
            params["trade"] = trade_code
        if grade_code:
            params["grade"] = grade_code
        if attribution_code:
            params["attribution"] = attribution_code
            
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()

            # 使用lxml解析HTML
            tree = html.fromstring(response.text)

            hospital_rows = tree.xpath('//div[@id="hospitallist"]//div[@class="tr"]')
 
            # 使用XPath查找医院列表
            hospitals = []
            
            if hospital_rows:
                # 提取医院信息
                for item in hospital_rows:
                    hospital_info = {}
                    
                    # 提取医院名称
                    title_elem = item.xpath('.//a/text()') or item.xpath('.//div[@class="hospital-title"]/text()')
                    if title_elem:
                        hospital_info['name'] = title_elem[0].strip()
                        hospitals.append(hospital_info)

        
            return hospitals
            
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return []
    
    def get_all_hospitals(self, delay=1, save_to_file=True):
        """
        优化版本：只获取有数据的组合和页面
        
        Args:
            delay: 请求间隔时间(秒)
            save_to_file: 是否保存到文件
            
        Returns:
            list: 所有医院信息列表
        """
        all_hospitals = []
        total_combinations = len(self.locations) * len(self.trades) * len(self.grades) * len(self.attributions)
        current_count = 0
        
        print(f"开始智能爬取，预计需要处理 {total_combinations} 种组合...")
        
        for location_code, location_name in self.locations.items():
            for trade_code, trade_name in self.trades.items():
                for grade_code, grade_name in self.grades.items():
                    for attr_code, attr_name in self.attributions.items():
                        current_count += 1
                        
                        print(f"[{current_count}/{total_combinations}] 正在爬取: {location_name} - {trade_name} - {grade_name} - {attr_name}")
                        
                        # 智能分页处理
                        combination_hospitals = []
                        page = 1
                        consecutive_empty_pages = 0
                        max_empty_pages = 1  # 连续空页面超过2页就停止
                        
                        while page <= 20:  # 最大10页保护
                            hospitals = self.get_hospitals_by_params(
                                location_code=location_code,
                                trade_code=trade_code, 
                                grade_code=grade_code,
                                attribution_code=attr_code,
                                page=page
                            )
                            
                            if not hospitals:
                                consecutive_empty_pages += 1
                                if consecutive_empty_pages >= max_empty_pages:
                                    print(f"  连续 {max_empty_pages} 页无数据，停止翻页")
                                    break
                            else:
                                consecutive_empty_pages = 0  # 重置空页面计数
                                
                                # 添加额外信息
                                for hospital in hospitals:
                                    hospital['location'] = location_name
                                    hospital['trade'] = trade_name
                                    hospital['grade_type'] = grade_name
                                    hospital['attribution'] = attr_name
                             
                                
                                combination_hospitals.extend(hospitals)
                                print(f"  第 {page} 页获取到 {len(hospitals)} 家医院")
                            
                            page += 1
                            time.sleep(delay)
                        
                        all_hospitals.extend(combination_hospitals)
                        if combination_hospitals:
                            print(f"本组合共获取到 {len(combination_hospitals)} 家医院")
                        else:
                            print(f"本组合无医院数据")
        
        # 去重处理
        unique_hospitals = []
        seen = set()
        for hospital in all_hospitals:
            identifier = (hospital.get('name', ''), hospital.get('address', ''))
            if identifier not in seen:
                seen.add(identifier)
                unique_hospitals.append(hospital)
        
        print(f"智能爬取完成！总共获取到 {len(all_hospitals)} 家医院（去重后 {len(unique_hospitals)} 家）")
        
        if save_to_file:
            self.save_to_file(unique_hospitals, f'hospitals_optimized_{len(unique_hospitals)}.json')
        
        return unique_hospitals
    
    def save_to_file(self, hospitals, filename='hospitals.json'):
        """保存医院信息到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(hospitals, f, ensure_ascii=False, indent=2)
            print(f"医院信息已保存到 {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")
    
    def get_hospital_titles(self, **kwargs):
        """获取医院标题列表"""
        hospitals = self.get_hospitals_by_params(**kwargs)
        return [hospital.get('name', '') for hospital in hospitals if hospital.get('name')]
    
    def search_hospitals(self, keyword, **kwargs):
        """搜索包含关键词的医院"""
        hospitals = self.get_hospitals_by_params(**kwargs)
        return [h for h in hospitals if keyword.lower() in h.get('name', '').lower()]


def main():
    """主函数示例"""
    crawler = HospitalCrawler()
    
    # 示例1: 获取北京三甲综合公立医院
    print("=== 获取北京三甲综合公立医院 ===")
    beijing_hospitals = crawler.get_hospitals_by_params(
        location_code="130000",
        trade_code="1", 
        grade_code="5",  # 三甲
        attribution_code="1",  # 综合医院
        page=11
    )
    
    for hospital in beijing_hospitals:
        print(f"- {hospital.get('name', 'N/A')}")
    
   
    # 如果需要获取所有医院（注意：这会花费很长时间）
    # all_hospitals = crawler.get_all_hospitals(delay=2)


if __name__ == "__main__":
    main()