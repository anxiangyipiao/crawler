import json
import requests
import random
import os





X_YP_Access_Token = "a36a90f6-d119-4b50-970f-30894a2f39fa"



contents = {
        "text": "中国21世纪议程管理中心2025年度公开招聘应届毕业生公告\n     发布日期：2025-04-25 来源：事业单位人事管理司 打印本页 \n    \n      中国21世纪议程管理中心（以下简称“21世纪中心”），是国家自然科学基金委员会直属的公益一类事业单位。主要职责是承担中央财政科技计划（专项、基金等）中资源、环境、海洋、公共安全、城镇化、应对气候变化等领域项目管理工作，履行项目管理专业机构职责，开展生态环境、气候变化等可持续发展领域的国际合作与交流，研究可持续发展相关领域的发展状况、趋势和重大问题等相关工作。根据工作需要，现公开招聘2025年应届毕业生3名。现将有关要求公告如下：\n一、招聘范围\n在校期间为非在职的2025年国内高校应届毕业生（不含各类定向生、委培生，含两年择业期内未落实工作单位的毕业生），能如期毕业并取得与最高学历对应的学历证书、学位证书。\n二、应聘条件\n1. 具有中华人民共和国国籍；\n2. 政治立场坚定，拥护中华人民共和国宪法，拥护中国共产党领导和社会主义制度，增强“四个意识”、坚定“四个自信”、做到“两个维护”，在思想上、政治上、行动上同以习近平同志为核心的党中央保持高度一致，有志投身国家科技计划项目事业；\n3. 应届毕业生年龄不超过35周岁〔1990年1月1日（含）以后出生〕。京外生源应符合北京市有关就业落户政策规定。京内生源指已具有北京市常住户口的人员，不含北京高校集体户口；\n4. 遵守宪法和法律，作风正派，办事公正，具有良好的服务意识、团队协作精神和道德品行；\n5. 具有扎实的理论功底、较强的专业素养、较好的英文及计算机水平，学习成绩优良；\n6. 具有较强的组织协调能力和语言文字表达能力；\n7. 具有较强的科研工作能力。具有较好的学术教育背景、扎实的专业基础知识、良好的科研工作经历，参与过相关科研项目，在本领域重要学术期刊公开发表过学术论文；\n8. 具有正常履行职责的身体条件和心理素质；\n9. 符合《事业单位人事管理回避规定》有关回避要求；\n10. 有下列情形之一者不得应聘：\n（1）与国家自然科学基金委员会机关和直属单位工作人员及离退休人员有夫妻关系、直系血亲关系、三代以内旁系血亲或近姻亲关系；\n（2）受过刑事处罚或被开除党籍、公职的；\n（3）受过党内严重警告或行政记大过以上处分的；\n（4）曾被开除学籍的；\n（5）在校期间受过院系级以上单位处分的；\n（6）被依法列入失信联合惩戒对象名单的；\n（7）曾有学术不端等不良行为的；\n（8）正在接受立案审查，或受党纪政务处分未撤销或处分影响期未满的；\n（9）在此前的各级公职人员招考中被认定有舞弊等严重违反录用纪律行为还在禁考期的；\n（10）法律法规规定不得招聘到事业单位工作的其他情形。\n三、招聘岗位及资格条件\n本次招聘涉及2个岗位、计划招聘3人，具体岗位及资格条件详见《中国21世纪议程管理中心2025年度公开招聘应届毕业生岗位信息表》。其中，有关岗位学历学位要求为应届毕业生即将获得的最高学历学位，当年如期取得毕业证、学位证。岗位专业要求为应届毕业生即将获得的最高学历学位对应专业。岗位专业条件参考教育部公布的《学位授予和人才培养学科目录（2018年4月版）》。对于所学专业接近，但不在上述学科专业参考目录中的，应聘人员可与21世纪中心联系，确认报名资格。\n四、招聘流程\n（一）报名\n应聘人员请下载《中国21世纪议程管理中心工作人员应聘申请表》，填写完成签字后扫描成PDF文件作为附件1，按照“岗位序号+姓名+附件1”的方式命名；同时还需将身份证、学生证、就业推荐表、在校期间成绩单等相关证明文件扫描成一个PDF文件作为附件2，按照“岗位序号+姓名+附件2”的方式命名；将附件1和附件2一并发送到renshi@acca21.org.cn，未按上述要求提交应聘材料者视为无效申请。每人限报考1个岗位。\n（二）笔试\n报名截止后，对应聘人员的应聘资格和岗位匹配度进行资格审查。资格审查工作贯穿公开招聘全过程，按照客观、公正、及时的要求，对所有应聘人员一视同仁。笔试人选名单将在21世纪中心网站上进行公布，并以短信、电话或电子邮件方式通知本人。\n若通过资格审查进入笔试人选不足5人，经招聘领导小组集体研究决定是否按照实际通过资格审查的人数组织考试。笔试为综合能力测试，笔试成绩100分。笔试成绩低于70分者，不列为综合能力评估人选。笔试不指定辅导用书，不举办不委托任何机构举办辅导培训班。\n（三）综合能力评估\n根据应聘人员的笔试成绩由高到低，按照1:20比例确定综合能力评估人选。综合能力评估人选名单将在21世纪中心网站上进行公布。\n综合能力评估专家组对应聘人员的学术水平、专业背景、综合能力、岗位匹配度等方面进行综合能力评估。综合能力评估总分100分，评估成绩低于70分者，不列为面试人选。\n（四）面试\n根据应聘人员的综合能力评估成绩由高到低，按照1:5比例确定面试人选。当综合能力评估合格人数不足1:5比例时，综合能力评估成绩达到70分的考生均可进入面试环节。面试人选名单将在21世纪中心网站进行公布，并以短信、电话或电子邮件方式通知本人。\n面试前，全部面试人员需参加心理素质测评。参加面试时，应试人须携带本人居民身份证、《中国21世纪议程管理中心工作人员应聘申请表》、就业推荐表、学生证、在校学习成绩单、奖励证书等相关证明材料原件。\n（五）考察和体检\n根据面试结果由高到低顺序，按照1:1等额比例确定考察和体检人选。所有面试人员均不符合岗位需求的，经招聘领导小组集体研究，取消该岗位招聘计划。岗位考察人选名单将在21世纪中心网站公布，21世纪中心综合与监督处会同用人部门按照有关规定到考察人选所在单位（院校），对其思想政治表现、道德品质、业务能力、工作实绩、遵纪守法及廉洁自律等情况进行考察，并查阅考察人选干部人事档案。对政治上不合格的，坚决“一票否决”。\n通知考察对象体检，体检费用由21世纪中心承担。参照《公务员录用体检通用标准》，统一组织到定点医院进行体检，体检合格方可聘用。对在体检过程中弄虚作假或者隐瞒真实情况致使体检结果失真的，一经查实，取消聘用资格。\n因应聘人员自愿放弃、考察或体检不合格等原因产生岗位候选人空缺，经招聘领导小组研究，可根据面试成绩进行递补，也可不再递补。\n（六）公示和聘用\n拟聘用人员将在21世纪中心网站、中央国家机关所属事业单位公开招聘服务平台公示5个工作日。公示期满后无异议的按照有关程序办理聘用手续。\n五、相关说明\n（一）笔试和面试的具体时间、方式等另行通知。\n（二）以上岗位一经聘用即为21世纪中心事业编制内正式工作人员，行政关系、人事档案等需转入我中心。如想了解21世纪中心应聘部门的基本情况，请登录21世纪中心主页https://www. acca21.org.cn。\n（三）以上岗位不接收博士后。\n（四）应聘人员对应聘过程所有环节提供的材料真实性负责，若弄虚作假，一经查实，取消应聘资格或聘用资格，并按照《事业单位公开招聘违纪违规行为处理规定》严肃处理。\n报名截止日期为2025年5月12日17:00。\n咨询方式：010-58884821 58884817（工作日8:30-17:00）。\n \n中国21世纪议程管理中心\n2025年4月25日\n \n\n      \n\t  \n        附件下载:\n        \n\n\t\t\n\t\t附件1-中国21世纪议程管理中心2025年度公开招聘应届毕业生岗位信息表.pdf\n\t\t\n\t\t附件2-中国21世纪议程管理中心工作人员应聘申请表.docx",
        "attachments": [
            "https://www.mohrss.gov.cn/SYrlzyhshbzb/fwyd/SYkaoshizhaopin/zyhgjjgsydwgkzp/zpgg/202504/P020250425563747683413.pdf",
            "https://www.mohrss.gov.cn/SYrlzyhshbzb/fwyd/SYkaoshizhaopin/zyhgjjgsydwgkzp/zpgg/202504/P020250425563747770415.docx"
        ]
    }



class WoCloudAI:
    def __init__(self):
        self.url = "https://panservice.mail.wo.cn/wohome/ai/assistant/query"
        self.x_yp_client_id = [
            "1001000035",
            "1001000036",
            "1001000037",
            "1001000021",
            "1001000022",
            "1001000023",
            "1001000024",
            "1001000025",
            "1001000026",
            "1001000027",
            "1001000028",
            "1001000029",
            "1001000030",
            "1001000031",
            "1001000032",
            "1001000033",
            "1001000034",
        ]
        self.user_agent = [
            "Mozilla/5.0 (Linux; Android 14; MEIZU 21 Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36/woapp LianTongYunPan/3.0.14 (Android 14)",
            "Mozilla/5.0 (Linux; Android 13; Google Pixel 6 Build/TQ3A.230805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Samsung Galaxy S21 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.92 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; OnePlus 9 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.49 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; Huawei P40 Build/HUAWEIANA-LX4; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.77 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 9; Oppo Reno 3 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.124 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 8; Vivo X21 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.91 Mobile Safari/537.36",
        ]
        self.headers = {
            "Host": "panservice.mail.wo.cn",
            "Connection": "close",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Android WebView";v="127", "Chromium";v="127"',
            "X-YP-Access-Token": X_YP_Access_Token,
            "X-YP-App-Version": "3.0.14",
            "sec-ch-ua-mobile": "?1",
            "User-Agent": random.choice(self.user_agent),
            "Content-Type": "application/json",
            "accept": "text/event-stream",
            "X-YP-Client-Id": random.choice(self.x_yp_client_id),
            "sec-ch-ua-platform": '"Android"',
            "Origin": "https://panservice.mail.wo.cn",
            "X-Requested-With": "com.chinaunicom.bol.cloudapp",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://panservice.mail.wo.cn/h5/wocloud_ai/",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def query(self, input_text="aaa",  model_id=0, tag=0, history=None):

        # model_id: 0 是默认模型，1 是 deepseek
        # input_text： 输入文本

        if history is None:
            history = []

        data = {"input": input_text, "modelId": model_id, "tag": tag, "history": history}

        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            print(response.status_code)

            for line in response.iter_lines():
                print(line.decode("utf-8"))

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


    def get_prompt(self, contents):

        prompt = """
        从以下文本中提取招聘单位和招聘岗位。如果招聘岗位在附件中，请说明。
        文本： {text}
        """
        return prompt.format(text=contents['text'])
        
    



if __name__ == "__main__":

    ai = WoCloudAI()

    prompt = ai.get_prompt(contents)

    ai.query(input_text=prompt)  # Example usage