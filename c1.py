from paddlex import create_pipeline
import pandas as pd
import os

# 初始化OCR（启用方向分类器）
pipeline = create_pipeline(pipeline="OCR")
    
# 遍历img目录下的图片
img_dir = os.path.join(os.getcwd(), "img")
invoice_data = []

for filename in os.listdir(img_dir):
    if filename.lower().endswith(('.jpg', '.png')):
        img_path = "img/"+ filename
        print(f"正在处理：{filename}")
        
        try:
            # OCR识别
            result = pipeline.predict(img_path)
            for res in result:
                res.save_to_json(save_path="./output/")
                res.save_to_img(save_path="./output/")
            
        except Exception as e:
            print(f"处理失败：{filename}，错误：{str(e)}")
            continue