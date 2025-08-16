import json
import sys
import re
from pathlib import Path

# --- 标准化配置 ---
# 脚本从C++控制器接收工作目录作为第一个参数
SOURCE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".") 
OUTPUT_DIR = Path("google_ai_studio_markdown_output")

# (sanitize_filename, get_unique_filepath, convert_google_ai_chat_to_markdown 函数不变)
def sanitize_filename(filename: str) -> str:
    """增强版文件名清理函数。"""
    if not filename or not filename.strip(): return "未命名对话"
    filename = filename.replace('\n', ' ').replace('\r', ' ')
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename[:100]; filename = filename.strip('_')
    return filename or "特殊字符对话"

def get_unique_filepath(output_dir: Path, filename: str) -> Path:
    """确保生成的文件路径是唯一的，防止覆盖。"""
    base_path = output_dir / (filename + ".md")
    if not base_path.exists(): return base_path
    counter = 1
    while True:
        new_path = output_dir / f"{filename}({counter}).md"
        if not new_path.exists(): return new_path
        counter += 1

def convert_google_ai_chat_to_markdown(conversation_data: dict, output_md_path: Path) -> bool:
    """【您的原始核心逻辑】从单个Google AI对话数据中提取对话。"""
    if 'chunkedPrompt' not in conversation_data or 'chunks' not in conversation_data['chunkedPrompt']: return False
    all_chunks = conversation_data['chunkedPrompt']['chunks']
    conversation_chunks = [c for c in all_chunks if not c.get('isThought', False)]
    if not conversation_chunks: return False
    has_content = False
    with open(output_md_path, 'w', encoding='utf-8') as md_file:
        for chunk in conversation_chunks:
            role, text = chunk.get('role'), chunk.get('text', '').strip()
            if role == 'user':
                if text: md_file.write(f"# 用户: {text}\n\n---\n\n"); has_content = True
                elif 'driveImage' in chunk: md_file.write(f"# 用户: (上传了一张图片)\n\n---\n\n"); has_content = True
            elif role == 'model' and text: md_file.write(f"## 回答\n\n{text}\n\n"); has_content = True
    return has_content

def process_single_file(input_path: Path):
    """
    处理单个文件并返回结果 (成功, 跳过, 文件错误)。
    这个函数保持“安静”，只返回状态码。
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f: conversation_data = json.load(f)
    except Exception:
        return 0, 0, 1
        
    if convert_google_ai_chat_to_markdown(conversation_data, input_path):
        # 成功，重命名文件到输出目录
        title = input_path.stem
        safe_filename = sanitize_filename(title)
        md_path = get_unique_filepath(OUTPUT_DIR, safe_filename)
        # 这是一个小技巧，因为convert函数已经写入了原路径，我们直接移动它
        try:
            # 确保输出目录存在
            OUTPUT_DIR.mkdir(exist_ok=True)
            input_path.rename(md_path)
            return 1, 0, 0
        except Exception:
            return 0, 0, 1
    else:
        # 对话为空或结构不符
        return 0, 1, 0

def main():
    """
    主执行函数，现在会自己计算总文件数并报告进度。
    """
    print(f"--- Google AI/Chunks 格式转换器 ---")
    print(f"数据源: '{SOURCE_DIR.resolve()}'")
    if not SOURCE_DIR.is_dir():
        print(f"错误: 源目录 '{SOURCE_DIR}' 不存在。")
        sys.exit(1)
        
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
    except PermissionError:
        print(f"严重错误: 无法创建文件夹 '{OUTPUT_DIR}'。请检查权限。")
        sys.exit(1)
    
    # --- 【核心修正】在开始前，先获取文件列表并计算总数 ---
    json_files_to_process = sorted(list(SOURCE_DIR.glob('*.json')))
    total_files = len(json_files_to_process)

    if total_files == 0:
        print("信息: 在 'conversation' 文件夹中没有找到任何 .json 文件。")
        sys.exit(0)
    
    print(f"分析完成！找到 {total_files} 个JSON文件，准备开始转换...")
    print("\n--- 阶段 2: 开始正式转换 ---")
    
    total_success, total_skipped, total_file_errors = 0, 0, 0
    
    # --- 在循环中报告正确的进度 ---
    for i, filepath in enumerate(json_files_to_process):
        # 在这里打印统一的、有意义的进度！
        print(f"\n--- [{i+1}/{total_files}] 处理文件: {filepath.name} ---")
        
        # 为了避免在原文件夹留下垃圾文件，我们先读取内容
        try:
            with filepath.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            print("  -> ❌ 错误: 读取文件失败，已跳过。")
            total_file_errors += 1
            continue

        title = filepath.stem
        safe_filename = sanitize_filename(title)
        md_path = get_unique_filepath(OUTPUT_DIR, safe_filename)

        if convert_google_ai_chat_to_markdown(data, md_path):
             print(f"  -> ✅ 成功生成: {md_path.name}")
             total_success += 1
        else:
             print(f"  -> 🟡 警告: 对话为空或结构不完整，已跳过。")
             total_skipped += 1

    # (最终报告部分不变)
    print("\n" + "="*40)
    print("🎉 所有任务已完成！ 🎉")
    print(f"总计成功生成: {total_success} 个Markdown文档")
    if total_skipped > 0:
        print(f"总计跳过(空或损坏的对话): {total_skipped} 个")
    if total_file_errors > 0:
        print(f"处理失败的文件数: {total_file_errors} 个")
    print(f"所有文件已保存至 '{OUTPUT_DIR}' 文件夹。")

if __name__ == "__main__":
    main()