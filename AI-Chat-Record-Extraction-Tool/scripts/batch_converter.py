import json
import os
import sys

def convert_chat_to_markdown(input_json_path, output_md_path):
    """
    读取指定的JSON聊天记录文件，并将其转换为Markdown格式。
    (这个核心函数与之前完全相同，无需改动)
    """
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  -> 错误：处理文件 '{input_json_path}' 失败。 {e}")
        return False

    if 'chunkedPrompt' not in data or 'chunks' not in data['chunkedPrompt']:
        print(f"  -> 错误：文件 '{input_json_path}' 结构不符，已跳过。")
        return False
        
    all_chunks = data['chunkedPrompt']['chunks']
    conversation_chunks = [chunk for chunk in all_chunks if not chunk.get('isThought', False)]

    with open(output_md_path, 'w', encoding='utf-8') as md_file:
        for chunk in conversation_chunks:
            role = chunk.get('role')
            text = chunk.get('text', '').strip()
            if role == 'user':
                if text:
                    md_file.write(f"# 用户: {text}\n\n")
                    md_file.write('---\n\n')
                elif 'driveImage' in chunk:
                     md_file.write(f"# 用户: (上传了一张图片)\n\n")
                     md_file.write('---\n\n')
            elif role == 'model':
                md_file.write("## 回答\n\n")
                md_file.write(text + "\n\n")
    return True


def main():
    """
    主执行函数，批量转换所有JSON文件，并存入指定文件夹。
    """
    print("开始批量转换任务 (升级版：自动存入文件夹)...")
    
    # ======================================================
    # ===                【核心改进】                    ===
    # ======================================================
    # 1. 定义输出文件夹的名称
    output_folder_name = "markdown_files"

    # 2. 检查输出文件夹是否存在，如果不存在则创建它
    try:
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"信息：已成功创建输出文件夹 -> '{output_folder_name}'")
    except Exception as e:
        print(f"严重错误：无法创建文件夹 '{output_folder_name}'。请检查权限。 {e}")
        sys.exit(1)
    # ======================================================

    # 查找所有.json文件 (这部分逻辑不变)
    try:
        current_directory_files = os.listdir('.')
        json_files = [f for f in current_directory_files if f.endswith('.json')]
    except Exception as e:
        print(f"错误：无法读取当前文件夹的文件列表。 {e}")
        sys.exit(1)

    if not json_files:
        print("信息：当前文件夹中没有找到任何 .json 文件可供转换。")
        sys.exit(0)

    print(f"已找到 {len(json_files)} 个 .json 文件，准备开始转换：")
    
    success_count = 0
    failure_count = 0
    
    for input_filename in json_files:
        print(f"\n处理中: {input_filename}")
        
        # ======================================================
        # ===                【核心改进】                    ===
        # ======================================================
        # 3. 构造指向新文件夹的输出路径
        base_filename, _ = os.path.splitext(input_filename)
        # 使用 os.path.join 来智能地拼接路径，它能适应所有操作系统
        output_filepath = os.path.join(output_folder_name, base_filename + '.md')
        # ======================================================

        if convert_chat_to_markdown(input_filename, output_filepath):
            print(f"  -> 成功生成: {output_filepath}")
            success_count += 1
        else:
            failure_count += 1
            
    print("\n--------------------")
    print("🎉 所有任务已完成！")
    print(f"结果：成功 {success_count} 个, 失败 {failure_count} 个。")
    print(f"所有Markdown文件已保存至 '{output_folder_name}' 文件夹。")


if __name__ == "__main__":
    main()