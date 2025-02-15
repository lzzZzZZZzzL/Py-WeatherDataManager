import pandas as pd
import users

########################################
#内部函数
########################################
def query_data(
    data_file: str= "weather_data.csv",
    location: str = None,
    date_range: str = None,
    temperature_range: tuple = None,
    pressure_range: tuple = None,
    humidity_range: tuple = None,
    wind_direction: str = None,
    wind_speed_range: tuple = None,
    output_file: str = "filtered_data.csv",
):#查找函数
    try:
        data = pd.read_csv(data_file, encoding="utf-8")
    except Exception as e:
        print(f"加载数据失败：{e}")
        return

    filtered_data = data.copy()

    # 1. 地点筛选
    if location:
        filtered_data = filtered_data[filtered_data["地点"].str.contains(location, na=False)]

    # 2. 时间范围筛选
    if date_range:
        try:
            start_time, end_time = date_range.split("~")
            start_time = pd.to_datetime(start_time.strip(), errors="coerce")
            end_time = pd.to_datetime(end_time.strip(), errors="coerce")

            if pd.isnull(start_time) or pd.isnull(end_time):
                raise ValueError("日期范围格式错误。")

            filtered_data["当地时间"] = pd.to_datetime(filtered_data["当地时间"], errors="coerce")
            filtered_data = filtered_data[
                (filtered_data["当地时间"] >= start_time) & (filtered_data["当地时间"] <= end_time)
            ]
        except Exception as e:
            print(f"时间范围解析失败：{e}")
            return

    # 3. 温度范围筛选
    if temperature_range:
        min_temp, max_temp = temperature_range
        filtered_data = filtered_data[
            (filtered_data["温度"] >= min_temp) & (filtered_data["温度"] <= max_temp)
        ]

    # 4. 气压范围筛选
    if pressure_range:
        min_pressure, max_pressure = pressure_range
        filtered_data = filtered_data[
            (filtered_data["气压"] >= min_pressure) & (filtered_data["气压"] <= max_pressure)
        ]

    # 5. 湿度范围筛选
    if humidity_range:
        min_humidity, max_humidity = humidity_range
        filtered_data = filtered_data[
            (filtered_data["湿度"] >= min_humidity) & (filtered_data["湿度"] <= max_humidity)
        ]

    # 6. 风向筛选
    if wind_direction:
        filtered_data = filtered_data[filtered_data["风向"].str.contains(wind_direction, na=False)]

    # 7. 风速范围筛选
    if wind_speed_range:
        min_speed, max_speed = wind_speed_range
        filtered_data = filtered_data[
            (filtered_data["风速"] >= min_speed) & (filtered_data["风速"] <= max_speed)
        ]

    # 输出结果到文件并保存
    if not filtered_data.empty:
        filtered_data.to_csv(output_file, index=False, encoding="utf-8")
        print(f"查询结果已保存到 {output_file}，共 {len(filtered_data)} 条记录。")
    else:
        print("没有符合条件的记录。")

    return filtered_data


########################################
#API函数
########################################
def query_data_api():
    """
    查找数据
    """
    data_file = "weather_data.csv"
    output_file ="query_data.csv"

    # 地点筛选
    location = input("请输入地点关键词（按回车完成，可跳过）：") or None

    # 具有权限二的用户才可以查询2024年之前的数据
    date_range = None
    while True:
        if users.has_permission_two():
            # 有权限二的用户
            date_range_input = input(
                "请输入时间范围（格式: 年-月-日~年-月-日，按回车完成，可跳过）：") or None
            date_range = date_range_input
            break
        else:
            # 没有权限二的用户
            date_range_input = input(
                f"请输入2024年时间范围（格式: 2024-月-日~2024-月-日，按回车完成，可跳过）：") or None

            # 检查输入的时间是否包含2024年以前的日期
            if date_range_input:
                try:
                    start_date, end_date = date_range_input.split('~')
                    start_year = int(start_date.split('-')[0])
                    end_year = int(end_date.split('-')[0])
                    if start_year < 2024 or end_year < 2024:
                        print("您没有权限查询2024年之前的数据，请重新输入2024年内的时间范围。")
                        continue
                except ValueError:
                    print("输入的时间格式不正确，请重新输入。")
                    continue
            date_range = date_range_input
            break


    # 具有权限一的用户才可以通过温度范围、气压范围、湿度范围、风向、风速范围查询
    temperature_range=None
    pressure_range=None
    humidity_range=None
    wind_direction=None
    wind_speed_range=None


    if users.has_permission_one():
        # 温度范围筛选
        temperature_range = input("请输入温度范围（格式: 最小值,最大值，按回车完成，可跳过）：")
        temperature_range = tuple(map(float, temperature_range.split(","))) if temperature_range else None

        # 气压范围筛选
        pressure_range = input("请输入气压范围（格式: 最小值,最大值，按回车完成，可跳过）：")
        pressure_range = tuple(map(float, pressure_range.split(","))) if pressure_range else None

        # 湿度范围筛选
        humidity_range = input("请输入湿度范围（格式: 最小值,最大值，按回车完成，可跳过）：")
        humidity_range = tuple(map(float, humidity_range.split(","))) if humidity_range else None

        # 风向筛选
        wind_direction = input("请输入风向关键词（按回车完成，可跳过）：") or None

        # 风速范围筛选
        wind_speed_range = input("请输入风速范围（格式: 最小值,最大值，按回车完成，可跳过）：")
        wind_speed_range = tuple(map(float, wind_speed_range.split(","))) if wind_speed_range else None


    # 调用查询函数
    try:
        result = query_data(
            data_file=data_file,
            location=location,
            date_range=date_range,
            temperature_range=temperature_range,
            pressure_range=pressure_range,
            humidity_range=humidity_range,
            wind_direction=wind_direction,
            wind_speed_range=wind_speed_range,
            output_file=output_file,
        )
        if result is not None:
            print("查询完成。")
    except Exception as e:
        print(f"查询过程中发生错误：{e}")


if __name__ == "__main__":
    """
    result = query_data(
        data_file,
        location="京",
        date_range="2024-10-09~2024-12-10",
        temperature_range=(-5, 10),
        pressure_range=(770, 775),
        humidity_range=(20, 60),
        wind_direction="北",
        wind_speed_range=(0, 5),
        output_file="query_weather_data.csv",
    )"""
    query_data_api()
