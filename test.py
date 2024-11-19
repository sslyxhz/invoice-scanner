from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_path = 'test2.jpg'
# result, elapse = engine(img_path)
# result, elapse = engine(img_path, use_det=False, use_cls=False, use_rec=True) # 只有识别
result, elapse = engine(img_path, use_det=True, use_cls=False, use_rec=True) # 检测+识别

# print(result)
# print(elapse)

texts = [item[1] for item in result]
# print(texts)

# target_text = '发票号码'
# index = texts.index(target_text)
# if index < len(texts) - 1:
#     next_text = texts[index + 1]
#     print(f"{target_text}: {next_text}")
# else:
#     print("找不到发票号码")

target_text = '号码'
for text in texts:
    if text.startswith(target_text):
        # print(text) # 号码：01819689
        numbers = ''.join(filter(str.isdigit, text))
        print(numbers)