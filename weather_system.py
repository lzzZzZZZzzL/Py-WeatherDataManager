import download
import add_and_delete
import query
import data_statistics
import  users


def menu(): #菜单
    while True:
        print("\n1. 登录")
        print("2. 注册")
        print("0. 退出")
        choice = input("请选择操作：")

        if choice == "1":
            users.login_api()#登录
            break
        elif choice == "2":
            users.register_user_api()#注册
        elif choice == "0":
            print("退出系统！")
            exit()#退出
        else:
            print("无效选项，请重新选择！")

    if users.is_admin():#管理员用户
        while True:
            print("\n1. 查询天气数据")
            print("2. 统计天气数据并统计数值")
            print("3. 统计天气数据并显示图表")
            print("4. 显示所有用户及权限")
            print("5. 设置用户权限")
            print("6. 增加数据")
            print("7. 删除数据")
            print("0. 退出")
            choice = input("请选择操作：")

            if choice == "1":
                query.query_data_api()
            elif choice == "2":
                data_statistics.calculate_statistics_api()
            elif choice == "3":
                data_statistics.visualize_parameter_with_stats_api()
            elif choice == "4":
                users.show_users_api()
            elif choice == "5":
                users.manage_user_permissions_api()
            elif choice == "6":
                add_and_delete.add_data_api()
            elif choice == "7":
                add_and_delete.delete_data_api()
            elif choice == "0":
                print("退出系统！")
                exit()
            else:
                print("无效选项，请重新选择！")

    else:#普通用户
        while True:
            print("\n1. 查询天气数据")
            print("2. 统计天气数据并统计数值")
            print("3. 统计天气数据并显示图表")
            print("0. 退出")
            choice = input("请选择操作：")

            if choice == "1":
                query.query_data_api()
            elif choice == "2":
                data_statistics.calculate_statistics_api()
            elif choice == "3":
                data_statistics.visualize_parameter_with_stats_api()
            elif choice == "0":
                print("退出系统！")
                exit()
            else:
                print("无效选项，请重新选择！")


if __name__=="__main__":
    menu()
