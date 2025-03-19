import pandas as pd
import re
ocr_list =[
 "开票人",
        "(小写)¥73913.00",
        "柒万叁仟玖佰壹拾叁圆整",
        "价税合计 (大写)",
        "￥8503.2",
        "￥65409.73",
        "计",
        "合",
        "血手术设备超声刀头",
        "2082.9",
        "13%",
        "16023. 01",
        "11 1456.63716814159",
        "把",
        "*医药*超声软组织切割止SG13",
        "血手术设备超声刀头",
        "3029.8",
        "13%",
        "23306.19",
        "16 1456.63716814159",
        "把",
        "*医药*超声软组织切割止SG35",
        "三",
        "三",
        "2103",
        "购灿生田",
        "云共",
        "税额",
        "税率/征收率",
        "金额",
        "单价",
        "数量",
        "单位",
        "规格型号",
        "项目名称",
        "销售方信息",
        "购买方信息",
        "统一社会信用代码/纳税人识别号：91370126MA3LY20N06",
        "统一社会信用代码/纳税人识别号：12371328495296332P",
        "名称：山东瑞青医疗器械有限公司",
        "名称：蒙阴县人民医院",
        "开票日期：2025年03月03日",
        "四著限幸团",
        "电子发票普通发票)",
        "发票号码：25372000000054451959"
    ]
def extract_fields(data):
    result = {}
    pattern = r'^([1-9][0-9]?|99)$'
    for idx, item in enumerate(data):
        # 提取发票号码
        if item.startswith("发票号码："):
            result["入院发票号码"] = item.split("：")[1]
        
        # 提取开票日期
        elif item.startswith("开票日期："):
            result["销售日期"] = item.split("：")[1]
        
        # 提取目标医院（购方名称）
        elif "医院" in item:
            result["目标医院"] = item.split("：")[1]
        
        # 提取销售数量（需定位"数"和"量"后的数值）
        elif re.search(pattern, item):
            result["销售数量"] = item
        
        # 提取规格型号（组合相关字段）
        elif re.search("SG", item):
            result["规格型号"] = item
    
    return result

# 执行提取
invoice_data = extract_fields(ocr_list)
df = pd.DataFrame([invoice_data])