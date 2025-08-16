import json
import sys
import re
from pathlib import Path

# --- 配置 ---
# SOURCE_DIR = Path(".") 
SOURCE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
# 为这种格式使用一个专门的输出文件夹
OUTPUT_DIR = Path("chatgpt_markdown_output")

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

def convert_tree_based_chat_to_markdown(conversation_data: dict, output_md_path: Path) -> bool:
    """
    【您的原始核心逻辑】解析基于'mapping'的单个对话树状结构。
    """
    mapping = conversation_data.get('mapping')
    if not mapping:
        return False

    # 查找根节点 (没有父节点的节点)
    root_node_id = next((key for key in mapping if mapping[key].get('parent') is None), None)
    if not root_node_id:
        return False
    
    root_node = mapping.get(root_node_id, {})

    # 寻找实际对话的起始节点ID
    current_node_id = None
    if 'client-created-root' in mapping and mapping['client-created-root'].get('children'):
         current_node_id = mapping['client-created-root']['children'][0]
    elif root_node.get('children'):
         current_node_id = root_node['children'][0]
    else:
         return False # 没有对话内容

    has_content = False
    with open(output_md_path, 'w', encoding='utf-8') as md_file:
        # 沿着对话树的子节点链条遍历
        while current_node_id:
            node = mapping.get(current_node_id)
            if not node or not node.get('message'):
                break

            message = node['message']
            role = message.get('author', {}).get('role')
            content_parts = message.get('content', {}).get('parts', [])
            full_content = "".join(part for part in content_parts if isinstance(part, str)).strip()

            if role == 'user' and full_content:
                md_file.write(f"# 用户: {full_content}\n\n---\n\n")
                has_content = True
            elif role == 'assistant' and full_content:
                md_file.write(f"## 回答\n\n{full_content}\n\n")
                has_content = True
            
            children = node.get('children', [])
            current_node_id = children[0] if children else None
            
    return has_content

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
            # 这种格式的JSON，顶层本身就是一个对话列表
            if isinstance(data, list):
                count = len(data)
                file_counts.append((filepath.name, count))
                total_conversations += count
            else:
                file_counts.append((filepath.name, 0, "结构不符 (顶层不是列表)"))
        except (json.JSONDecodeError, IOError):
            file_counts.append((filepath.name, 0, "无法解析"))
    
    print("分析结果:")
    for name, count, *error in file_counts:
        status = f"-> 包含 {count} 段对话" if not error else f"-> 错误: {error[0]}"
        print(f"  - 文件: {name.ljust(40)} {status}")
        
    print("-" * 30)
    print(f"分析完成！总共将在 {len(json_files)} 个文件中处理 {total_conversations} 段对话。")
    print("="*40)

def process_tree_based_file(input_path: Path):
    """读取指定的树状格式JSON文件，并为每个对话生成Markdown。"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            # 对于这种格式，整个文件就是一个对话列表
            conversations = json.load(f)
    except Exception:
        return 0, 0, 1

    if not isinstance(conversations, list):
        # 错误已在预计算阶段报告，这里仅作防御
        return 0, 0, 1

    success_count, skipped_count = 0, 0
    num_total = len(conversations)
    print(f"\n处理中: {input_path.name} (共 {num_total} 段对话)")

    for i, conv in enumerate(conversations):
        # 使用原始脚本中的标题生成逻辑
        title = conv.get('title', f"对话_{conv.get('conversation_id', i + 1)}")
        safe_filename = sanitize_filename(title)
        md_path = get_unique_filepath(OUTPUT_DIR, safe_filename)
        
        if convert_tree_based_chat_to_markdown(conv, md_path):
            print(f"  ({i+1}/{num_total}) -> 成功: {md_path.name}")
            success_count += 1
        else:
            print(f"  ({i+1}/{num_total}) -> 警告: 对话 '{title}' 为空或结构不完整，已跳过。")
            skipped_count += 1
    return success_count, skipped_count, 0

def main():
    """主执行函数，包含预计算和转换两个阶段。"""
    print(f"--- ChatGPT/树状格式对话记录转换器 (标准化版) ---")
    
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
    except PermissionError:
        print(f"严重错误: 无法创建文件夹 '{OUTPUT_DIR}'。请检查权限。")
        sys.exit(1)

    json_files = sorted(list(SOURCE_DIR.glob('*.json')))
    if not json_files:
        print("信息: 当前文件夹中没有找到任何 .json 文件。")
        sys.exit(0)

    pre_check_files(json_files)

    print("\n--- 阶段 2: 开始正式转换 ---")
    total_success, total_skipped, total_file_errors = 0, 0, 0
    for filepath in json_files:
        success, skipped, file_error = process_tree_based_file(filepath)
        total_success += success
        total_skipped += skipped
        total_file_errors += file_error
            
    print("\n" + "="*40)
    print("🎉 所有任务已完成！ 🎉")
    print(f"总计成功生成: {total_success} 个Markdown文档")
    if total_skipped > 0:
        print(f"总计跳过(空或损坏的对话): {total_skipped} 个")
    if total_file_errors > 0:
        print(f"处理失败的文件数: {total_file_errors} 个 (详细错误见上方分析)")
    print(f"所有文件已保存至 '{OUTPUT_DIR}' 文件夹。")

if __name__ == "__main__":
    main()