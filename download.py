import requests
import re
import gzip
import shutil
import io
import pandas as pd
import csv

myData1 = {                         #北京2024.01.01-2024.12.10
    "wmo_id": "54511",           # 气象站号码（例如：北京 54511，深圳 59493）
    "a_date1": "01.01.2024",     # 开始日期
    "a_date2": "10.12.2024",     # 结束日期
    "f_ed3": "1",                # 选择“仅一个月”时的月份
    "f_ed4": "1",                # 选择“仅某天”时的月份
    "f_ed5": "1",                # 选择“仅某天”时的日期
    "f_pe": "1",                 # 为给定范围选择：所有日期-1 仅一个月-2 仅某天-3
    "f_pe1": "2",                # 编码: ANSI-1 UTF-8-2 统一码-3
    "lng_id": "8",               # 语言：中文-8，英文-1，俄文-2
    'type': 'csv'                # 数据格式：当值为“xls”时，返回的是 Excel 文件，其余情况为 CSV 文件
}

myData2 = {                         #北京2023.01.01-2023.12.31
    "wmo_id": "54511",           # 气象站号码（例如：北京 54511，深圳 59493）
    "a_date1": "01.01.2023",     # 开始日期
    "a_date2": "31.12.2023",     # 结束日期
    "f_ed3": "1",                # 选择“仅一个月”时的月份
    "f_ed4": "1",                # 选择“仅某天”时的月份
    "f_ed5": "1",                # 选择“仅某天”时的日期
    "f_pe": "1",                 # 为给定范围选择：所有日期-1 仅一个月-2 仅某天-3
    "f_pe1": "2",                # 编码: ANSI-1 UTF-8-2 统一码-3
    "lng_id": "8",               # 语言：中文-8，英文-1，俄文-2
    'type': 'csv'                # 数据格式：当值为“xls”时，返回的是 Excel 文件，其余情况为 CSV 文件
}

myData3 = {                         #深圳2024.01.01-2024.12.10
    "wmo_id": "59493",           # 气象站号码（例如：北京 54511，深圳 59493）
    "a_date1": "01.01.2024",     # 开始日期
    "a_date2": "10.12.2024",     # 结束日期
    "f_ed3": "1",                # 选择“仅一个月”时的月份
    "f_ed4": "1",                # 选择“仅某天”时的月份
    "f_ed5": "1",                # 选择“仅某天”时的日期
    "f_pe": "1",                 # 为给定范围选择：所有日期-1 仅一个月-2 仅某天-3
    "f_pe1": "2",                # 编码: ANSI-1 UTF-8-2 统一码-3
    "lng_id": "8",               # 语言：中文-8，英文-1，俄文-2
    'type': 'csv'                # 数据格式：当值为“xls”时，返回的是 Excel 文件，其余情况为 CSV 文件
}

output1 = r"file1.csv"
output2 = r"file2.csv"
output3 = r"file3.csv"

# 要提取的列索引（从 0 开始）与新列名的映射
columns_to_extract = {
    29: "地点",      # 第三十列
    0: "当地时间",  # 第一列
    1: "温度",      # 第二列
    3: "气压",      # 第四列
    5: "湿度",      # 第六列
    6: "风向",      # 第七列
    7: "风速"       # 第八列
}

def download(myData,output_file):#下载气象文件函数
    """
        下载气象文件

    """
    session = requests.Session()

    # 模拟访问首页，获取初始 Cookie
    session.get("https://rp5.ru/")

    # 设置 Headers 和请求数据
    myUrl = "https://rp5.ru/responses/reFileSynop.php"
    myHeader = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "rp5.ru",
        "Origin": "https://rp5.ru",
        "Referer": "https://rp5.ru/",
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }


    # 发送请求
    response = session.post(myUrl, data=myData, headers=myHeader)
    print(response.text)

    # 提取下载链接
    download_url = re.search(r"href=(\S+)", response.text)
    if download_url is None:
        print("Failed to extract download URL.")
        exit()
    else:
        download_url = download_url.group(1).strip("'").strip('"')
    print(f"Download URL: {download_url}")

    # 下载并解压文件
    response_dl = requests.get(download_url, stream=True)

    decompressed_path = download_url.split('/')[-1][:-3]  # 解压后的文件名

    if response_dl.status_code == 200:
        with gzip.open(io.BytesIO(response_dl.content)) as gz_file:
            with open(decompressed_path, 'wb') as out_file:
                shutil.copyfileobj(gz_file, out_file)
        print(f"Downloaded and decompressed successfully: {decompressed_path}")    # 至此，包含天气数据的文件已下载并解压完成
    else:
        print(f"Failed to download file. Status code: {response_dl.status_code}")
        exit()

    # 打印解压后的文件内容（可选）
    # with open(decompressed_path, 'r', encoding='utf-8') as file:
    #     print(file.readline())  # 打印文件的第一行作为示例
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)
    # pd.describe_option()
    df_list = []

    data = pd.read_csv(decompressed_path, encoding='UTF-8', sep=';', header=6, usecols=range(29), index_col=0, parse_dates=True,
                       date_format='%d.%m.%Y %H:%M')
    index_name, city = data.index.name.split()
    data['city'] = city
    data.index.name = index_name
    data
    df_list.append(data)
    # 合并所有 DataFrame
    combined_data = pd.concat(df_list)

    # 保存结果到新的 CSV 文件
    combined_data.to_csv(decompressed_path)

    try:
        with open(decompressed_path, mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile)

            # 跳过第一行
            headers = next(reader)

            # 提取所需列的索引
            selected_indices = list(columns_to_extract.keys())
            new_headers = [columns_to_extract[i] for i in selected_indices]

            # 写入新文件
            with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(new_headers)  # 写入新列名

                for row in reader:
                    # 提取指定列的数据
                    extracted_row = [row[i] if i < len(row) else "" for i in selected_indices]
                    writer.writerow(extracted_row)

        print(f"提取完成，输出文件已保存到：{output_file}")

    except Exception as e:
        print(f"发生错误：{e}")


if __name__=="__main__":
    download(myData1,output1)
    download(myData2,output2)
    download(myData3,output3)
