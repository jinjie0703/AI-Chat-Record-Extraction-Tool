# search_keyword.py - 强大的Markdown内容深度搜索脚本 (最终修复版)

import sys
from pathlib import Path

def main():
    """
    主执行函数：从命令行接收源目录和关键词，并进行深度搜索。
    """
    # --- 核心修正：确保我们正确地解析两个参数 ---
    if len(sys.argv) < 3:
        print("错误：脚本需要提供源目录和关键词。")
        print("用法: python search_keyword.py <source_directory> <your_keyword>")
        sys.exit(1)

    # 第一个参数是C++传来的数据目录 (我们在这里用不上，但为了统一接口而接收)
    source_dir_str = sys.argv[1] 
    # 第二个参数才是我们真正要搜索的关键词！
    keyword = sys.argv[2]      
    
    # 定义搜索的根目录。我们从当前项目的主目录开始搜索，
    # 这样可以一次性找到所有转换器生成的Markdown文件。
    search_root = Path(".") 
    
    print(f"正在 '{search_root.resolve()}' 及其所有子目录中深度搜索 *.md 文件...")
    # 打印正确的关键词
    print(f"搜索关键词: \"{keyword}\"")
    print("-" * 40)

    found_files = []
    # rglob 会递归地查找所有子目录
    for file_path in search_root.rglob('*.md'):
        if file_path.is_file():
            try:
                with file_path.open('r', encoding='utf-8') as f:
                    content = f.read()
                    # 使用正确的关键词进行搜索
                    if keyword in content:
                        found_files.append(file_path)
            except Exception:
                continue

    # --- 打印正确的结果 ---
    print("-" * 40)
    if found_files:
        print(f"✅ 找到 {len(found_files)} 个内容包含关键词 \"{keyword}\" 的文件:")
        for path in found_files:
            print(f"  -> {path}")
    else:
        # 报告正确的未找到的关键词
        print(f"❌ 未在任何 .md 文件内容中找到关键词 \"{keyword}\"。")

if __name__ == "__main__":
    main()