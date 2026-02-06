import os
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


def generate_order(text):
    prompt = f"""
    Bạn là hệ thống POS.
    Trích xuất danh sách sản phẩm và số lượng từ câu:
    "{text}"

    Trả về JSON dạng:
    [
      {{"name":"product","qty":2}}
    ]
    """

    response = model.generate_content(prompt)

    return response.text
