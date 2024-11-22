from rapidocr_onnxruntime import RapidOCR
import re
from PIL import Image

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

img_path = './imgs/test2.jpg'
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

target_text = '号码'
for text in texts:
    if text.startswith(target_text):
        # print(text) # 号码：01819689
        numbers = ''.join(filter(str.isdigit, text))
        print(numbers)


# 检测texts中符合 x年x月x日格式、2022-12-12格式的文本
# date_pattern = re.compile(r'^\d{4}年\d{1,2}月\d{1,2}日$|^\d{4}-\d{1,2}-\d{1,2}$')
# for text in texts:
#     if date_pattern.match(text):
#         print(text)
