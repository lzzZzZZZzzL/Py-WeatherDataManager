import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import query
import seaborn as sns
from math import pi

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

########################################
#内部函数
########################################
def calculate_statistics(data_file, parameter):#统计函数
    try:
        # 读取需统计文件内容
        data = pd.read_csv(data_file, encoding="utf-8")
    except Exception as e:
        print(f"加载数据失败：{e}")
        return

    if data is not None:
        if parameter not in data.columns:
            # 检查需统计气象参数是否存在
            print(f"指定的气象参数 '{parameter}' 不存在！")
            return None
        # 检查数据是否有效
        if data[parameter].isnull().all():
            print(f"参数 '{parameter}' 的数据全部为空，无法展示！")
            return None

        try:
            # 计算各种统计数据
            stats = {
                f"平均{parameter}": round(data[parameter].mean(), 2),
                f"最高{parameter}": data[parameter].max(),
                f"最低{parameter}": data[parameter].min(),
                f"{parameter}的极差": round(data[parameter].max()-data[parameter].min(),2),
                f"{parameter}的中位数": data[parameter].median(),
                f"{parameter}的方差": round(data[parameter].var(), 2),
            }

            # 确保数值转换为原生 Python 类型
            stats = {
                key: (float(value) if isinstance(value, (np.float64, np.float32))
                      else int(value) if isinstance(value, (np.int64, np.int32))
                      else value)
                for key, value in stats.items()
            }
            return stats
        except Exception as e:
            print(f"计算统计信息时出错：{e}")
            return None
    else:
        print("没有数据进行统计！")
        return None


def visualize_parameter_with_stats(data_file, parameter, chart_type):#画图函数
    try:
        # 读取需统计文件内容
        data = pd.read_csv(data_file, encoding="utf-8")
        if parameter not in data.columns:
            # 检查需统计气象参数是否存在
            print(f"指定的气象参数 '{parameter}' 不存在！")
            return
        # 检查数据是否有效
        if data[parameter].isnull().all():
            print(f"参数 '{parameter}' 的数据全部为空，无法展示！")
            return

        # 让数据按时间排序
        data['当地时间'] = pd.to_datetime(data['当地时间'], errors='coerce')
        data = data.sort_values(by='当地时间')
        x = data['当地时间']
        y = data[parameter]

        # 调用统计函数计算各种统计数据
        stats = calculate_statistics(data_file, parameter)

        # 画图
        plt.figure(figsize=(10, 6))

        if chart_type == "折线图":
            plt.plot(x, y, marker='o', linestyle='-', label=parameter)
            plt.xlabel('时间')
            plt.ylabel(parameter)
            plt.title(f'{parameter} 的变化趋势')
            plt.xticks(rotation=45)
            plt.legend()

            # 在图表中显示统计数据
            stats_text = '\n'.join([f"{key}: {value}" for key, value in stats.items()])
            plt.text(0.01, 0.95, stats_text, transform=plt.gca().transAxes,
                     fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

        elif chart_type == "柱状图":
            plt.bar(x, y, label=parameter, color='skyblue')
            plt.xlabel('时间')
            plt.ylabel(parameter)
            plt.title(f'{parameter} 的分布情况')
            plt.xticks(rotation=45)
            plt.legend()

            # 在图表中显示统计数据
            stats_text = '\n'.join([f"{key}: {value}" for key, value in stats.items()])
            plt.text(0.01, 0.95, stats_text, transform=plt.gca().transAxes,
                     fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

        elif chart_type == "饼状图":
            if y.isnull().all():
                print("饼状图需要非空的数值数据！")
                return
            y_counts = data[parameter].value_counts()
            labels = y_counts.index
            sizes = y_counts.values
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title(f'{parameter} 的分布情况（饼状图）')

             #在图表中显示统计数据
            stats_text = '\n'.join([f"{key}: {value}" for key, value in stats.items()])
            plt.text(0.01, 0.95, stats_text, transform=plt.gca().transAxes,
                     fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))


        elif chart_type == "热图":

            # 热图

            # 热图: 时间与地点的参数变化

            pivot_data = data.pivot_table(index='地点', columns='当地时间', values=parameter, aggfunc='mean')

            plt.figure(figsize=(12, 6))

            sns.heatmap(pivot_data, cmap='coolwarm', annot=True, fmt='.1f', linewidths=.5)

            plt.title(f'{parameter} 在各地点和时间的变化热图')

            plt.xlabel('时间')

            plt.ylabel('地点')


        elif chart_type == "雷达图":

            # 雷达图: 显示同一时间不同气象参数的变化

            categories = ['温度', '湿度', '气压', '风速']  # 雷达图可以包含多个参数

            values = [data[cat].mean() for cat in categories if cat in data.columns]

            if len(values) == 0:
                print("雷达图需要多个有效的气象参数！")

                return

            # 雷达图的准备

            N = len(categories)

            values += values[:1]

            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

            angles += angles[:1]

            # 绘制雷达图

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

            ax.fill(angles, values, color='green', alpha=0.25)

            ax.plot(angles, values, color='green', linewidth=2)  # 边界线

            ax.set_yticklabels([])  # 去掉圆圈标签

            ax.set_xticks(angles[:-1])  # 设置分类标签

            ax.set_xticklabels(categories, fontweight='bold')

            ax.set_title(f'{parameter} 各气象参数雷达图', size=16, color='black', verticalalignment='bottom')


        else:
            print(f"不支持的图表类型 '{chart_type}'，请选择 '折线图'、'柱状图' 或 '饼状图'或 '热图'或 '雷达图'！")
            return

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"绘制图表时出错：{e}")


########################################
#API函数
########################################
def calculate_statistics_api():
    """
    查找、统计数据
    """
    query.query_data_api()
    data_file =  "query_data.csv"

    # 要统计的气象参数
    parameter = input("请输入要统计的气象参数（支持: 温度, 气压, 湿度, 风速）：")

    try:
        # 调用统计函数
        stats = calculate_statistics(data_file, parameter)
        if stats:
            print(f"统计结果如下：")
            for key, value in stats.items():
                print(f"{key}: {value}")
        else:
            print("发生错误。")
    except Exception as e:
        print(f"统计过程中发生错误：{e}")


def visualize_parameter_with_stats_api():
    """
    查找、统计数据和画图
    """
    query.query_data_api()
    data_file = "query_data.csv"

    # 要统计的气象参数
    parameter = input("请输入要统计的气象参数（支持: 温度, 气压, 湿度, 风速）：")

    # 图表类型
    chart_type = input("请选择图表类型（支持: 折线图, 柱状图, 饼状图，热图，雷达图）：")

    try:
        # 调用画图函数
        visualize_parameter_with_stats(data_file, parameter, chart_type)
    except Exception as e:
        print(f"查询或可视化过程中发生错误：{e}")



# 测试用例
if __name__ == "__main__":
    visualize_parameter_with_stats("query_data.csv","温度","雷达图")
