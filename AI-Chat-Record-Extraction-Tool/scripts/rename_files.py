import sys
from pathlib import Path

# 从命令行参数读取源目录，如果未提供，则默认为当前目录
SOURCE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

def main():
    """主执行函数：在指定的源目录中查找并重命名文件。"""
    print(f"--- 正在运行前置处理脚本：智能重命名文件 ---")
    print(f"目标目录: '{SOURCE_DIR.resolve()}'")
    
    if not SOURCE_DIR.exists():
        print(f"错误: 目标目录 '{SOURCE_DIR}' 不存在。")
        sys.exit(1)
        
    files_to_rename = []
    print("\n正在检查目录下的所有文件...")
    for item in SOURCE_DIR.iterdir():
        if not item.is_file() or item.name.startswith('.'):
            continue
        if not item.suffix or ' ' in item.suffix:
            print(f"  -> '{item.name}' -> ✅ 判定为有效目标")
            files_to_rename.append(item)
        else:
            print(f"  -> '{item.name}' -> 跳过 (拥有正常的后缀 '{item.suffix}')")

    if not files_to_rename:
        print("\n分析完成：未发现需要重命名的文件。")
        return

    print(f"\n分析完成，找到 {len(files_to_rename)} 个文件需要处理。正在开始重命名...")
    renamed_count, skipped_count = 0, 0
    for old_path in files_to_rename:
        new_path = old_path.with_suffix('.json')
        if new_path.exists():
            print(f"  - 跳过: '{old_path.name}' (因为 '{new_path.name}' 已存在)")
            skipped_count += 1
            continue
        try:
            old_path.rename(new_path)
            print(f"  - 成功: '{old_path.name}' -> '{new_path.name}'")
            renamed_count += 1
        except Exception as e:
            print(f"  - 错误: 重命名 '{old_path.name}' 时失败。原因: {e}")

    print("\n" + "="*40)
    print("🎉 前置处理完成！ 🎉")
    if renamed_count > 0: print(f"总计成功重命名: {renamed_count} 个文件")
    if skipped_count > 0: print(f"总计跳过(因目标已存在): {skipped_count} 个文件")

if __name__ == "__main__":
    main()