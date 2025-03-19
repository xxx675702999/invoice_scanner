from pathlib import Path
import cv2
import numpy as np
import os
from paddlex import create_pipeline

# 使用pathlib构建路径对象（自动处理编码）
img_path = Path("img/临沂弘屹医疗器械有限公司-郯城县第一人民医院-43把 (2).jpg")
# 初始化OCR（启用方向分类器）
pipeline = create_pipeline(pipeline="OCR")
# 转换为绝对路径并验证
abs_path = img_path.absolute()
print(f"绝对路径：{abs_path}")
print(f"文件存在：{abs_path.exists()}")
print(f"可读权限：{os.access(abs_path, os.R_OK)}")


def safe_cv_read(path):
    """兼容中文路径的OpenCV读取方法"""
    path = Path(path)
    with open(path, 'rb') as f:  # 二进制模式读取
        img_data = np.frombuffer(f.read(), dtype=np.uint8)
    return cv2.imdecode(img_data, cv2.IMREAD_COLOR)

# 使用示例
try:
    img = safe_cv_read(img_path)
    result = pipeline.predict(img)
    for res in result:
                res.save_to_json(save_path="./output/rrreww.json")
                
    print("图像尺寸：", img.shape)
except Exception as e:
    print(f"读取失败：{str(e)}")