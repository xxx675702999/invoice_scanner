import pandas as pd
import re
import os
ocr_list =[
 "电子发票（普通发票)",
        "发票号码：25212000000009561249",
        "北站",
        "开票日期：2025年02月10日",
        "辽宁省税务局",
        "共1页第1页",
        "购买方信息",
        "名称：中国医科大学附属第一医院",
        "销售方信息",
        "名称：沈阳美肯玛尼商贸有限公司",
        "统一社会信用代码/纳税人识别号：12210000410581610Y",
        "统一社会信用代码/纳税人识别号：91210111594113968E",
        "项目名称",
        "规格型号",
        "单位",
        "数量",
        "单价",
        "金额",
        "税率/征收率",
        "税额",
        "*医疗仪器器械*超声高频",
        "",
        "OSG22",
        "把",
        "30",
        "1194. 69026548673",
        "35840. 71",
        "%8 1",
        "4659.29",
        "外科集成手术设备超声刀",
        "头",
        "*医疗仪器器械*超声高频",
        "",
        "OSG35",
        "把",
        "80 1194. 69026548673",
        "95575. 22",
        "% I",
        "12424. 78",
        "外科集成手术设备超声刀",
        "头",
        "合",
        "计",
        "￥131415.93",
        "￥17084.07",
        "价税合计 (大写)",
        "壹拾肆万捌仟伍佰圆整",
        "（小写）￥148500.00",
        "购方开户银行：建行沈阳铁路支行：",
        "银行账号：21001460008052503344；",
        "销方开户银行：中国光大银行沈阳和平支行；",
        "备",
        "银行账号：75660188000108134;",
        "开票人：于千惠",
        

    ]
def extract_fields(data):
    results = []
    current_item = {}
    guige_pattern = re.compile(r'OSG\d{2}')  # 匹配规格型号的规则
    pattern =re.compile(r'^([1-9][0-9]?|99)$') 
    ba_indices = [index for index, item in enumerate(ocr_list) if re.search("S", item)]
    for idx, item in enumerate(data):
        index = 0
        # 提取公共字段
        if item.startswith("发票号码："):
            current_item["入院发票号码"] = item.split("：")[1]
        elif item.startswith("开票日期："):
            current_item["销售日期"] = item.split("：")[1]
        elif "医院" in item and "：" in item:
            current_item["目标医院"] = item.split("：")[1]
        
        # 当遇到"把"时创建新条目
        if re.search("S", item):
            # 提取销售数量（向后查找数字）
            for offset in range(0, ba_indices[index+1]-ba_indices[index]-1):
                prev_item = data[idx - offset]
                if re.match(r'^([1-9][0-9]?|99)$', prev_item):
                    current_item["销售数量"] = prev_item
                    break
            
            # 提取规格型号（向前查找OSG格式）
            for offset in range(0, ba_indices[index+1]-ba_indices[index]-1):
                next_item = data[idx + offset]
                if re.search("S", item):
                    current_item["规格型号"] = next_item
                    break
            
            # 添加到结果列表并重置临时存储
            results.append(current_item)
            current_item = current_item.copy()  # 保留公共字段
            index = index+1
    return results

# 执行提取
invoice_data = extract_fields(ocr_list)
    # 生成Excel表格
if invoice_data:
    df = pd.DataFrame(invoice_data)
    excel_path = os.path.join(os.getcwd(), "发票信息表.xlsx")
    df.to_excel(excel_path, index=False)
    print(f"处理完成！结果已保存至：{excel_path}")
else:
    print("未找到可处理的发票图片")