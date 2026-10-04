# PDF 解析。安装命令 uv add pypdf
from pypdf import PdfReader
from io import BytesIO

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    # 从 PDF 字节流提取文本，BytesIO 把字节流包装成“类文件对象”，PdfReader 才能读取
    reader = PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text