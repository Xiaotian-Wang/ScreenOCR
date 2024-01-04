# src/ocr.py
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

def preprocess_image(image):
    image = image.convert('L')  # 转换为灰度图像
    # image = image.filter(ImageFilter.MedianFilter())  # 应用中值滤波去噪
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(3.0)  # 适度增加对比度
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)

    return image

def recognize_text(image_path):
    # 指定Tesseract-OCR的安装路径
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # 加载图像
    image = Image.open(image_path)
    image = preprocess_image(image)
    image.save('../screenshots/preprocessed.png')
    # 识别中文文字
    text = pytesseract.image_to_string(image, lang='chi_sim')

    return text


def recognize_text_and_draw_boxes(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    image = Image.open(image_path)
    # image.save('../screenshots/preprocessed.png')
    draw = ImageDraw.Draw(image)
    image_preprocessed = preprocess_image(image)
    # 使用image_to_data获取文字和位置信息
    data = pytesseract.image_to_data(image_preprocessed, lang='chi_sim', output_type=pytesseract.Output.DICT, config='--oem 3 --psm 6')
    text_boxes = []

    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text = data['text'][i]
            draw.rectangle([x, y, x + w, y + h], outline='red')
            text_boxes.append((text, x, y, w, h))

    return image, text_boxes