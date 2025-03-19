import os
import re
from paddlex import create_pipeline
import pandas as pd
import json
import traceback
from pathlib import Path
import cv2
import numpy as np


def extract_invoice_info(texts):
    results = []
    
    guige_pattern = re.compile(r'OSG\d{2}')  # 匹配规格型号的规则
    pattern =re.compile(r'^([1-9][0-9]?|99)$') 
    ba_indices = [index for index, item in enumerate(texts) if re.search("S", item)]
    if len(ba_indices) > 1:
        current_item = {}
        for idx, item in enumerate(texts):
            index = 0
            # 提取公共字段
            if item.startswith("发票号码："):
                current_item["入院发票号码"] = item.split("：")[1]
            elif item.startswith("开票日期："):
                current_item["销售日期"] = item.split("：")[1]
            elif "医院" in item and "：" in item:
                item_list = item.split("：")
                if len(item_list) >1:
                    current_item["目标医院"] = item_list[1]
                else:
                    current_item["目标医院"] = item_list[0]
            
            # 当遇到"把"时创建新条目
            if re.search("S", item):
                # 提取销售数量（向后查找数字）
                for offset in range(0, ba_indices[index+1]-ba_indices[index]-1):
                    prev_item = texts[idx - offset]
                    if re.match(r'^([1-9][0-9]?|99)$', prev_item):
                        current_item["销售数量"] = prev_item
                        break
                
                # 提取规格型号（向前查找OSG格式）
                for offset in range(0, ba_indices[index+1]-ba_indices[index]-1):
                    next_item = texts[idx + offset]
                    if re.search("S", item):
                        current_item["规格型号"] = next_item
                        break
                
                # 添加到结果列表并重置临时存储
                results.append(current_item)
                current_item = current_item.copy()  # 保留公共字段
                index = index+1
    else:
     index_item = {}
     for idx, item in enumerate(texts):
        # 提取发票号码
        if item.startswith("发票号码："):
            index_item["入院发票号码"] = item.split("：")[1]
        
        # 提取开票日期
        elif item.startswith("开票日期："):
            index_item["销售日期"] = item.split("：")[1]
        
        # 提取目标医院（购方名称）
        elif "医院" in item:
            item_list = item.split("：")
            if len(item_list) >1:
                index_item["目标医院"] = item_list[1]
            else:
                index_item["目标医院"] = item_list[0]
        
        # 提取销售数量（需定位"数"和"量"后的数值）
        elif re.search(pattern, item):
            index_item["销售数量"] = item
        
        # 提取规格型号（组合相关字段）
        elif re.search("SG", item):
            index_item["规格型号"] = item

     results.append(index_item)
    return results

def safe_cv_read(path):
    """兼容中文路径的OpenCV读取方法"""
    path = Path(path)
    with open(path, 'rb') as f:  # 二进制模式读取
        img_data = np.frombuffer(f.read(), dtype=np.uint8)
    return cv2.imdecode(img_data, cv2.IMREAD_COLOR)

def main():
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
                result = pipeline.predict(safe_cv_read(img_path))
                for res in result:
                    res.save_to_json(save_path="./output/" + filename.split(".")[0] +"_res.json")
                    res.save_to_img(save_path="./output/")
                json_path = "output/"+ filename.split(".")[0] +"_res.json"
                save_json_path = "json/" + filename.split(".")[0] +"_res.txt"
                with open(json_path, 'r', encoding='utf-8') as f:
                    texts = json.load(f)
                    # 解析关键信息
                    info = extract_invoice_info(texts["rec_texts"])
                    for item in info:
                        item["图片文件名"] = filename
                    invoice_data.append(info)
                with open(save_json_path, 'w', encoding='utf-8') as f:
                     for text in texts["rec_texts"]:
                        f.write(f"{text}\n")
            except Exception as e:
                print(f"处理失败：{filename}，错误：{e}")
                traceback.print_exc()  
                continue
    
    # 生成Excel表格
    if invoice_data:
        flat = [item for sublist in invoice_data for item in sublist]
        df = pd.DataFrame(flat)
        excel_path = os.path.join(os.getcwd(), title + ".xlsx")
        df.to_excel(excel_path, index=False)
        os.rename("json",title)
        os.mkdir("json")
        print(f"处理完成！结果已保存至：{excel_path}")
    else:
        print("未找到可处理的发票图片")

title = "张悦597把"
if __name__ == "__main__":
    main()