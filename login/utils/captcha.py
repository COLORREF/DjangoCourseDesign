import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

# 字体文件路径
font_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../static/微软雅黑.ttf"))


def rndChar():
    """
    随机生成字母或数字
    """
    if random.random() < 0.5:
        return chr(random.randint(65, 90))  # 返回字母
    else:
        return str(random.randint(0, 9))  # 返回数字


def rndColor():
    """
    生成随机颜色
    """
    return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)


def create_captcha(width=120, height=30, char_length=5, font_file=font_path, font_size=20):
    """
    验证码图片生成
    :return image, str
    """
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    # 写文字
    font = ImageFont.truetype(font=font_file, size=font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text((i * width / char_length, h), char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


def base64_captcha():
    """
    base64编码验证码图片
    :return: base64 str,code str
    """
    image, code_str = create_captcha()
    stream = BytesIO()  # 二进制缓冲区
    image.save(stream, 'PNG')  # 保存进缓冲区
    base64_string = base64.b64encode(stream.getvalue()).decode('utf-8')  # 获取二进制图像进行Base64编码
    return base64_string, code_str
