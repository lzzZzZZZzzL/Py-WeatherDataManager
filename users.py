import re
import csv
import json

users_file="users_data.csv"
now_user=None#当前登录用户，初始为None，执行登录函数后赋值为当前用户名


########################################
#内部函数
########################################
def is_valid_username(username):# 检查用户名是否合法
    return re.match(r'^(?!\d+$)[\w\u4e00-\u9fa5]+$', username) is not None#用户名仅包含中英文、数字和下划线


def is_username_exists(username):#检查用户名是否存在
    try:
        with open(users_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            for row in reader:
                if row[0] == username:
                    return True
    except FileNotFoundError:
        print(f"文件 {users_file} 不存在！")
    except Exception as e:
        print(f"读取文件时出错：{e}")

    return False


def password_strength(password):# 检查密码的强度
    types_count = sum(1 for c in [any(c.islower() for c in password),
                                  any(c.isupper() for c in password),
                                  any(c.isdigit() for c in password),
                                  any(c in '!@#￥%&*<>|(){}[]~+-=' for c in password)]
                      if c)#统计密码包含多少种类型的字符

    if len(password) > 10 and types_count >= 3:
        return "高"
    elif len(password) >= 8 and types_count >= 2:
        return "中"
    else:
        return "弱"



########################################
#API函数
########################################
def register_user_api():
    """
    用户注册

    """
    try:
        with open(users_file, "r", encoding="utf-8") as f:
            pass  # 文件已存在，跳过表头写入
    except FileNotFoundError:
        # 文件不存在，创建文件并写入表头
        with open(users_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["用户名", "密码", "权限"])

    while True:#主函数
        username = input("请输入用户名：")
    
        if re.match("^[0]+$",username):#全0字符串
            break
    
        if not is_valid_username(username):#不合法重新输入
            print("用户名不合法，请输入其他用户名")
            continue
    
        if is_username_exists(username):#重复重新输入
            print("用户名已存在，请输入其他用户名")
            continue
    
        print("用户名可用，请设置密码")
    
        while True:#设置密码
            password = input("请输入密码：")
            strength = password_strength(password)
            if strength == "弱":#密码太弱
                print("密码强度弱，请设置更高强度的密码")
            else:
                # 设置初始权限
                initial_permissions = {
                    "权限一": False,  # 权限一
                    "权限二": False  # 权限二
                }
                permissions_json = json.dumps(initial_permissions, ensure_ascii=False)

                # 将用户信息保存
                with open(users_file, "a", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([username, password, permissions_json])

                print(f"用户 {username} 注册成功")
                return


def login_api():
    """
    用户登录

    """
    global now_user

    while True:
        username = input("请输入用户名：")
        password = input("请输入密码：")

        try:
            with open(users_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # 跳过表头

                user_found = False
                for row in reader:
                    if len(row) < 3:
                        continue  # 如果行数据有缺失则跳过
                    csv_username, csv_password,csv_permissions = row[0], row[1],row[2]
                    if username == csv_username and password == csv_password:# 检查用户名和密码是否匹配
                        user_found = True # 成功登录
                        permissions = json.loads(csv_permissions)  # 导出用户权限
                        now_user = {'username': username, 'permissions': permissions}  # 保存现在登录用户
                        break

                if user_found:
                    print(f"{username} 登录成功")
                    return username
                else:
                    print("用户名或密码错误，请重新输入")

        except FileNotFoundError:
            print(f"数据有误！")
            return
        except Exception as e:
            print(f"数据有误！")
            return


def show_users_api():
    """
     显示所有用户及权限

     """
    try:
        with open(users_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)  # 读取表头

            print(f"当前所有用户及权限：")
            print(f"{'用户名':<15}{'权限一':<10}{'权限二':<10}")
            print("-" * 35)

            for row in reader:
                username = row[0]
                permission_json = row[2] if len(row) > 2 else "{}"

                try:
                    # 将权限转换为字典
                    permissions = json.loads(permission_json)
                    permission_1 = "是" if permissions.get("权限一", False) else "否"
                    permission_2 = "是" if permissions.get("权限二", False) else "否"
                except json.JSONDecodeError:
                    permission_1 = "错误"
                    permission_2 = "错误"

                print(f"{username:<15}{permission_1:<10}{permission_2:<10}")

    except FileNotFoundError:
        print(f"文件 {users_file} 不存在！请检查文件路径。")
    except Exception as e:
        print(f"读取用户信息时出错：{e}")


def is_admin():
    """
    判断当前登录用户是否是管理员

    """
    if now_user is None:
        print("请先登录！")
        return False

    username = now_user.get('username')

    if username == "admin": # 当前登录用户是管理员
        return True
    else:
        return False


def has_permission_one():
    """
    判断当前登录用户是否有 权限一

    """
    if now_user is None:
        print("请先登录！")
        return False

    permissions = now_user.get('permissions', {})
    return permissions.get("权限一", False) # 当前登录用户是否有权限一


def has_permission_two():
    """
    判断当前登录用户是否有 权限二

    """
    if now_user is None:
        print("请先登录！")
        return False

    permissions = now_user.get('permissions', {})
    return permissions.get("权限二", False) # 当前登录用户是否有权限二


def manage_user_permissions_api():
    """
    管理员管理其他用户的权限

    """
    if not is_admin():
        print("只有管理员才能执行此操作！")
        return

    # 需要管理的用户
    username_to_manage = input("请输入需要管理的用户名：")

    # 检查该用户是否存在
    try:
        with open(users_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)  # 读取所有行

            # 如果文件为空，直接写入表头
            if len(rows) <= 1:
                print("用户数据文件为空，无法读取。")
                return

            user_found = False
            user_permissions = None

            # 查找目标用户
            for row in rows[1:]:  # 跳过表头
                if len(row) < 3:
                    continue  # 跳过不完整的行

                csv_username = row[0]
                if csv_username == username_to_manage:
                    user_found = True
                    # 导出用户权限
                    user_permissions = json.loads(row[2])
                    break

            if not user_found:
                print(f"用户名 {username_to_manage} 不存在！")
                return

    except FileNotFoundError:
        print(f"文件 {users_file} 不存在！请检查文件路径。")
        return
    except Exception as e:
        print(f"读取用户信息时出错：{e}")
        return

    # 显示该用户权限
    print(f"当前用户 {username_to_manage} 拥有的权限：")
    print(f"权限一: {'是' if user_permissions.get('权限一', False) else '否'}")
    print(f"权限二: {'是' if user_permissions.get('权限二', False) else '否'}")

    # 管理权限
    while True:
        print("\n请选择操作：")
        print("0 - 返回上一级")
        print("1 - 管理权限一")
        print("2 - 管理权限二")

        choice = input("请输入选项：")

        #退出
        if choice == "0":
            break

        #设置权限一
        if choice == "1":
            new_permission_one = input("是否拥有权限一？(yes/no): ").lower() == 'yes'
            user_permissions["权限一"] = new_permission_one
            print(f"权限一已设置为: {'是' if new_permission_one else '否'}")

        #设置权限二
        elif choice == "2":
            new_permission_two = input("是否拥有权限二？(yes/no): ").lower() == 'yes'
            user_permissions["权限二"] = new_permission_two
            print(f"权限二已设置为: {'是' if new_permission_two else '否'}")

        else:
            print("无效选项，请重新输入！")
            continue

        # 更新该用户权限
        try:
            with open(users_file, mode="w", encoding="utf-8", newline='') as file:
                writer = csv.writer(file)

                for row in rows[:]:
                    if len(row) < 3:
                        continue  # 跳过不完整的行

                    if row[0] == username_to_manage:
                        # 更新权限，确保保存中文时不会转义成 Unicode 编码
                        row[2] = json.dumps(user_permissions, ensure_ascii=False)

                    # 写回每一行
                    writer.writerow(row)

                print(f"用户 {username_to_manage} 的权限已更新。")

        except Exception as e:
            print(f"写入文件时出错：{e}")
            break


if __name__=="__main__":
    login_api()
    manage_user_permissions_api()
