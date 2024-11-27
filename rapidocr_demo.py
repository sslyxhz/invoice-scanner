import os
import re
from rapidocr_onnxruntime import RapidOCR
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

# 按照位置排序
def get_text_position(item, image_height):
    box = item[0]  # 获取文本框坐标
    y = box[0][1]  # 左上角y坐标
    x = box[0][0]  # 左上角x坐标
    
    # y坐标在图片上1/3的分到第一组(group=0)，其余分到第二组(group=1)
    group = 0 if y <= image_height/3 else 1
    
    # 返回 (组号, x坐标) 作为排序依据
    return (group, x)



engine = RapidOCR()

img_path = './imgs/test3.heic'
# img_path = './imgs/WechatIMG29815.jpg'

# 使用前先获取图片高度
img = Image.open(img_path)
img_height = img.height

# result, elapse = engine(img_path)
# result, elapse = engine(img_path, use_det=False, use_cls=False, use_rec=True) # 只有识别
result, elapse = engine(img_path, use_det=True, use_cls=False, use_rec=True) # 检测+识别

# print(result)
# print(elapse)

sorted_result = sorted(result, key=lambda item: get_text_position(item, img_height))

texts = [item[1] for item in sorted_result]
# print(texts)

for text in texts:
    pattern = r'号码：\d{8}'
    match = re.search(pattern, text)
    if match:
        number = match.group(0)
        print('1>>>', number)
    elif text.startswith('号码') or text.startswith('母码') or text.startswith('务码') or text.startswith('粤码'):
        # print(text) # 号码：01819689
        print('text[2]', text[2])
        numbers = ''.join(filter(str.isdigit, text))
        print(numbers)
    elif text.__contains__('号码'):
        # 代码：135022422881代码：135022322881号码：00213347 提取出号码  
        start_index = text.find('号码：')
        if start_index != -1:
            number = text[start_index + 3:]
            print('>>>', number)
        


# 检测texts中符合 x年x月x日格式、2022-12-12格式的文本
# date_pattern = re.compile(r'^\d{4}年\d{1,2}月\d{1,2}日$|^\d{4}-\d{1,2}-\d{1,2}$')
# for text in texts:
#     if date_pattern.match(text):
#         print(text)
