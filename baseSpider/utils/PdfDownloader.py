import requests
import io
from PyPDF2 import PdfReader
from urllib.parse import urlparse, parse_qs, unquote
from playwright.sync_api import sync_playwright

class PDFDownloader:
    
    def __init__(self, viewer_url):
        self.viewer_url = viewer_url
        self.real_pdf_url = self._extract_pdf_url()
    
    def _extract_pdf_url(self) -> str:
        """
        通用解析 URL，如果 URL 包含 file 参数，则返回解码后的 file 参数值，
        否则直接返回传入的 URL。
        """
        parsed = urlparse(self.viewer_url)
        query_params = parse_qs(parsed.query)
        if "file" in query_params and query_params["file"]:
            return unquote(query_params["file"][0])
        return self.viewer_url
    
    def download_pdf(self):
        """
        下载 PDF 文件，返回 BytesIO 对象
        """
        headers = {
            "referer": self.viewer_url,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/134.0.0.0 Safari/537.36"
        }
        response = requests.get(self.real_pdf_url, headers=headers)
        response.raise_for_status()

        return io.BytesIO(response.content)
    
    # def download_pdf_with_Playwright(self):
    #     """
    #     使用 Playwright 下载 PDF 文件，返回 BytesIO 对象
    #     """
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(headless=True)  # 无头模式
    #         context = browser.new_context(accept_downloads=True)  # 启用下载功能
    #         page = context.new_page()

    #         # 打开 PDF 文件的 URL
    #         page.goto(self.real_pdf_url)

    #         # 等待下载完成
    #         download = page.wait_for_download()
    #         pdf_bytes = download.save_as_bytes()  # 获取下载的文件内容为字节流

    #         # 关闭浏览器
    #         browser.close()

    #         # 返回 BytesIO 对象
    #         return io.BytesIO(pdf_bytes)


    def extract_text(self):
        """
        解析 PDF 的文本内容，并返回字符串
        """
        pdf_file = self.download_pdf()
        reader = PdfReader(pdf_file)
        pdf_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"
        return pdf_text
    
    @staticmethod
    def download_pdf_text(viewer_url: str) -> str:
        """
        对外公开接口，根据 viewer_url 下载 PDF 并返回解析后的文本内容，
        无需外部实例化
        """
        downloader = PDFDownloader(viewer_url)
        return downloader.extract_text()







# # 示例调用
if __name__ == "__main__":
    
#     viewer_url = ("http://www.tdztb.com//resource/css/pdfjs/web/viewer.html?"
#                   "file=http://www.tdztb.com/bidprocurement/datacenter-cebpubserver/cebpubserver/"
#                   "dataCeboubServerCommonController/openFileById?fileType%3D2%26id%3D0c95e5e111da4885b49d0c6da76eb953&page=1")
    
#     viewer_url = "https://scm.esinochem.com/bidprocurement/common-tools/tools/commonUpload/readImageRoot?imagePath=2025-03/bulletin_template_pdf_base/3b915cb86a2645638417339d8dd6c094/20250331153955asY496TT.pdf"

    # viewer_url = 'https://scm.esinochem.com/sinochem-scm/gateway/obs/dowload/file/viewV2/fae61db1-fa93-4c27-b6a1-744a585e9a74.pdf?u=CFrW6a47eSV6IrPB4XAIiOSmxnfo8xbMC3VfzlqxX4nIg17a4NkHSkRooL74CwX4bD4I8kEdWLHCsTRMJXoRoOvxosQ'

    viewer_url='https://www.mohrss.gov.cn/SYrlzyhshbzb/fwyd/SYkaoshizhaopin/zyhgjjgsydwgkzp/zpgg/202504/P020250425563747683413.pdf'
    
    pdf_text = PDFDownloader.download_pdf_text(viewer_url)
    
    print(pdf_text)