import csv

########################################
#内部函数
########################################
def add_rows_to_main_file(main_file, input_file, output_file):#增加函数
    try:
        # 读取主文件和输入文件内容
        with open(main_file, mode="r", encoding="utf-8") as main_f, \
                open(input_file, mode="r", encoding="utf-8") as input_f:

            main_reader = list(csv.reader(main_f))
            input_reader = list(csv.reader(input_f))

            # 提取表头和数据
            main_header, main_data = main_reader[0], main_reader[1:]
            input_header, input_data = input_reader[0], input_reader[1:]

            # 检查表头是否一致
            if main_header != input_header:
                raise ValueError("主文件与输入文件的表头不一致，无法进行操作。")

            # 将输入文件中与主文件不同的行添加到主文件后
            main_set = set(map(tuple, main_data))
            new_rows = [row for row in input_data if tuple(row) not in main_set]

            # 写入结果到输出文件
            with open(output_file, mode="w", encoding="utf-8", newline="") as out_f:
                writer = csv.writer(out_f)
                writer.writerow(main_header)  # 写入表头
                writer.writerows(main_data + new_rows)  # 写入主文件数据和新增行

        print(f"增加操作完成，输出文件已保存到：{output_file}")
    except Exception as e:
        print(f"发生错误：{e}")


def delete_rows_from_main_file(main_file, input_file, output_file):#删除函数
    try:
        # 读取主文件和输入文件内容
        with open(main_file, mode="r", encoding="utf-8") as main_f, \
                open(input_file, mode="r", encoding="utf-8") as input_f:

            main_reader = list(csv.reader(main_f))
            input_reader = list(csv.reader(input_f))

            # 提取表头和数据
            main_header, main_data = main_reader[0], main_reader[1:]
            input_header, input_data = input_reader[0], input_reader[1:]

            # 检查表头是否一致
            if main_header != input_header:
                raise ValueError("主文件与输入文件的表头不一致，无法进行操作。")

            # 将输入文件中与主文件相同的行从主文件中删除
            input_set = set(map(tuple, input_data))
            remaining_rows = [row for row in main_data if tuple(row) not in input_set]

            # 写入结果到输出文件
            with open(output_file, mode="w", encoding="utf-8", newline="") as out_f:
                writer = csv.writer(out_f)
                writer.writerow(main_header)  # 写入表头
                writer.writerows(remaining_rows)  # 写入剩余行

        print(f"删除操作完成，输出文件已保存到：{output_file}")
    except Exception as e:
        print(f"发生错误：{e}")


########################################
#API函数
########################################
def add_data_api():
    """
    增加数据
    """
    add_main_file=input("请输入主数据文件名：")
    add_input_file = input("请输入新增数据文件名：")
    add_output_file = input("请输入增加后数据文件名：")
    add_rows_to_main_file(add_main_file,add_input_file,add_output_file)

def delete_data_api():
    """
    删除数据
    """
    delete_main_file=input("请输入主数据文件名：")
    delete_input_file = input("请输入删除数据文件名：")
    delete_output_file = input("请输入删除后数据文件名：")
    delete_rows_from_main_file(delete_main_file,delete_input_file,delete_output_file)

if __name__=="__main__":
    add_rows_to_main_file(r"file1.csv",r"file2.csv",r"weather_data.csv")
    add_rows_to_main_file(r"weather_data.csv",r"file3.csv",r"weather_data.csv")
