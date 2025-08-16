import json
import sys
import re
from pathlib import Path

# --- 配置 ---
# SOURCE_DIR = Path(".") 
SOURCE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUTPUT_DIR = Path("qwen_markdown_output")

def sanitize_filename(filename: str) -> str:
    """增强版文件名清理函数。"""
    if not filename or not filename.strip():
        return "未命名对话"
    filename = filename.replace('\n', ' ').replace('\r', ' ')
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename[:100]
    filename = filename.strip('_')
    return filename or "特殊字符对话"

def get_unique_filepath(output_dir: Path, filename: str) -> Path:
    """确保生成的文件路径是唯一的，防止覆盖。"""
    base_path = output_dir / (filename + ".md")
    if not base_path.exists():
        return base_path
    counter = 1
    while True:
        new_path = output_dir / f"{filename}({counter}).md"
        if not new_path.exists():
            return new_path
        counter += 1

def convert_qwen_chat_to_markdown(conversation_data: dict, output_md_path: Path) -> bool:
    """【您的原始核心逻辑】提取qwen对话并写入文件。"""
    messages = conversation_data.get('chat', {}).get('messages', [])
    if not messages:
        return False
    with open(output_md_path, 'w', encoding='utf-8') as md_file:
        for message in messages:
            role = message.get('role')
            if role == 'user':
                content = message.get('content', '').strip()
                if content:
                    md_file.write(f"# 用户: {content}\n\n---\n\n")
            elif role == 'assistant':
                content_list = message.get('content_list', [])
                final_answer = ""
                for part in content_list:
                    if isinstance(part, dict) and part.get('phase') == 'answer':
                        final_answer = part.get('content', '').strip()
                        break
                if final_answer:
                    md_file.write(f"## 回答\n\n{final_answer}\n\n")
    return True

# --- 新增功能: 预计算与分析 ---
def pre_check_files(json_files: list):
    """
    第一阶段：快速分析所有JSON文件，报告每个文件的对话数和总数。
    """
    print("--- 阶段 1: 预计算分析 ---")
    file_counts = []
    total_conversations = 0
    
    for filepath in json_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 检查数据结构是否符合预期
            conversations = data.get('data')
            if isinstance(conversations, list):
                count = len(conversations)
                file_counts.append((filepath.name, count))
                total_conversations += count
            else:
                file_counts.append((filepath.name, 0, "结构不符"))
        except (json.JSONDecodeError, IOError):
            file_counts.append((filepath.name, 0, "无法解析"))
    
    print("分析结果:")
    for name, count, *error in file_counts:
        status = f"-> 包含 {count} 段对话" if not error else f"-> 错误: {error[0]}"
        print(f"  - 文件: {name.ljust(40)} {status}")
        
    print("-" * 30)
    print(f"分析完成！总共将在 {len(json_files)} 个文件中处理 {total_conversations} 段对话。")
    print("="*40)
    return total_conversations

def process_qwen_export_file(input_path: Path):
    """读取指定的qwen JSON文件，为每个对话生成Markdown，并返回详细计数。"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            export_data = json.load(f)
    except Exception:
        # 错误已在预计算阶段报告，这里直接返回
        return 0, 0, 1

    conversations = export_data.get('data', [])
    success_count, skipped_count = 0, 0
    num_total = len(conversations)
    print(f"\n处理中: {input_path.name} (共 {num_total} 段对话)")

    for i, conv in enumerate(conversations):
        title = conv.get('title', '').strip() or f"{input_path.stem}_对话_{i+1}"
        safe_filename = sanitize_filename(title)
        md_path = get_unique_filepath(OUTPUT_DIR, safe_filename)
        if convert_qwen_chat_to_markdown(conv, md_path):
            print(f"  ({i+1}/{num_total}) -> 成功: {md_path.name}")
            success_count += 1
        else:
            print(f"  ({i+1}/{num_total}) -> 警告: 对话 '{title}' 为空，已跳过。")
            skipped_count += 1
    return success_count, skipped_count, 0

def main():
    """主执行函数，包含预计算和转换两个阶段。"""
    print(f"--- Qwen 对话记录转换器 (最终版) ---")
    
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
    except PermissionError:
        print(f"严重错误: 无法创建文件夹 '{OUTPUT_DIR}'。请检查权限。")
        sys.exit(1)

    json_files = sorted(list(SOURCE_DIR.glob('*.json'))) # 排序使输出更整齐
    if not json_files:
        print("信息: 当前文件夹中没有找到任何 .json 文件。")
        sys.exit(0)

    # --- 阶段 1: 调用预计算函数 ---
    pre_check_files(json_files)

    # --- 阶段 2: 正式开始转换 ---
    print("\n--- 阶段 2: 开始正式转换 ---")
    total_success, total_skipped, total_file_errors = 0, 0, 0
    for filepath in json_files:
        success, skipped, file_error = process_qwen_export_file(filepath)
        total_success += success
        total_skipped += skipped
        total_file_errors += file_error
            
    # --- 最终的详细总结报告 ---
    print("\n" + "="*40)
    print("🎉 所有任务已完成！ 🎉")
    print(f"总计成功生成: {total_success} 个Markdown文档")
    if total_skipped > 0:
        print(f"总计跳过(空对话): {total_skipped} 个")
    if total_file_errors > 0:
        print(f"处理失败的文件数: {total_file_errors} 个 (详细错误见上方分析)")
    print(f"所有文件已保存至 '{OUTPUT_DIR}' 文件夹。")

if __name__ == "__main__":
    main()