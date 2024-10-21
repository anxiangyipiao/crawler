import requests
import ddddocr



# 使用 ddddocr 进行 OCR 识别
ocr = ddddocr.DdddOcr()

def recognize_captcha_from_url(image_url: str) -> str:
    """从网络上的图像 URL 识别验证码"""
    try:
        # 下载图像
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 逐块读取响应内容并拼接成完整的二进制字符串
        image_bytes = b''
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                image_bytes += chunk

        captcha_text = ocr.classification(image_bytes)
        
        # 返回识别结果
        return captcha_text.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"



