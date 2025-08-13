import os
import sys

def bulk_add_json_extension():
    print("正在运行文件后缀添加程序")
    
    try:
        current_directory_files = os.listdir('.')
    except Exception as e:
        print(f"错误：无法读取当前文件夹的文件列表。 {e}")
        sys.exit(1)

    files_to_rename = []
    print("\n--- 正在应用新的智能规则进行检查 ---")
    for item_name in current_directory_files:
        # 只处理文件，跳过文件夹
        if not os.path.isfile(item_name):
            continue

        # ======================================================
        # ===                【最终核心修正】                ===
        # ======================================================
        # 1. 像以前一样，分割主名和后缀
        basename, extension = os.path.splitext(item_name)
        
        # 2. 应用新的智能规则：
        #    如果后缀是空的(没有点)，或者后缀里面包含了空格，
        #    我们就认为它是一个需要处理的目标文件！
        if not extension or ' ' in extension:
            print(f" -> '{item_name}' -> ✅ 判定为有效目标 (原因: 后缀为空或包含空格)。")
            files_to_rename.append(item_name)
        else:
            print(f" -> '{item_name}' -> 跳过 (原因: 拥有一个不含空格的有效后缀 '{extension}')。")
    # ======================================================

    if not files_to_rename:
        print("\n检查完成：当前文件夹中没有找到任何需要添加后缀的文件。")
        sys.exit(0)

    print("\n已找到以下无后缀文件，准备为它们添加 '.json' 后缀：")
    for filename in files_to_rename:
        print(f"  - {filename}")
    
    try:
        confirm = input("\n您确定要继续吗？ (输入 y 继续, 输入 n 取消): ").lower().strip()
    except KeyboardInterrupt:
        print("\n操作已取消。")
        sys.exit(0)

    if confirm != 'y':
        print("操作已取消。")
        sys.exit(0)

    print("\n正在执行重命名...")
    renamed_count = 0
    for filename in files_to_rename:
        old_path = filename
        new_path = filename + '.json'
        try:
            os.rename(old_path, new_path)
            print(f"  {old_path}  ->  {new_path}")
            renamed_count += 1
        except Exception as e:
            print(f"错误：重命名文件 '{filename}' 失败。 {e}")
    
    print(f"\n🎉 操作完成！成功重命名了 {renamed_count} 个文件。")


if __name__ == "__main__":
    bulk_add_json_extension()