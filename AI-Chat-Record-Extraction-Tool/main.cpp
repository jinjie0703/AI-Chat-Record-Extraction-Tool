#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <filesystem> // 需要 C++17 标准
#include <limits>
#include <algorithm>

// --- 全局配置 ---
const std::string CONVERSATION_DIR = "conversation"; // 定义专用数据文件夹

// 定义脚本文件名
const std::string RENAME_SCRIPT = "rename_files.py";
const std::string SEARCH_SCRIPT = "keyword_search.py";
const std::string QWEN_SCRIPT = "qwen_converter.py";
const std::string CHATGPT_SCRIPT = "chatgpt_converter.py";
const std::string DEEPSEEK_SCRIPT = "deepseek_converter.py";
const std::string GOOGLE_AI_SCRIPT = "google_converter.py";

// 辅助函数：检查文件是否存在
bool file_exists(const std::string& filename) {
    return std::filesystem::exists(filename);
}

// 辅助函数：执行命令，现在总是将数据文件夹作为第一个参数传递
bool execute_command(const std::string& script_name, const std::string& args = "") {
    // 命令格式: python <script.py> <data_directory> <other_args>
    std::string command = "python " + script_name + " \"" + CONVERSATION_DIR + "\"";
    if (!args.empty()) {
        command += " \"" + args + "\"";
    }

    std::cout << "\n==================================================" << std::endl;
    std::cout << "即将执行: " << command << std::endl;
    std::cout << "==================================================" << std::endl;

    int return_code = system(command.c_str());

    if (return_code != 0) {
        std::cerr << "\n[错误] 命令执行失败，返回码: " << return_code << std::endl;
        std::cerr << "请检查Python脚本 '" << script_name << "' 是否有错误，或Python环境是否配置正确。" << std::endl;
        return false;
    }

    std::cout << "\n[成功] 脚本 '" << script_name << "' 执行完毕！" << std::endl;
    return true;
}

void display_menu() {
    std::cout << "\n+------------------------------------------+" << std::endl;
    std::cout << "|      AI 对话记录管理工具 - 主菜单        |" << std::endl;
    std::cout << "+------------------------------------------+" << std::endl;
    std::cout << "| 数据目录: ./" << CONVERSATION_DIR << "/" << std::endl;
    std::cout << "+------------------------------------------+" << std::endl;
    std::cout << "| --- 转换工具 ---                         |" << std::endl;
    std::cout << "| 1. 通义千问 (Qwen)                       |" << std::endl;
    std::cout << "| 2. ChatGPT                   |" << std::endl;
    std::cout << "| 3. DeepSeek                              |" << std::endl;
    std::cout << "| 4. Google AI Studio              |" << std::endl;
    std::cout << "|                                          |" << std::endl;
    std::cout << "| --- 检索工具 ---                         |" << std::endl;
    std::cout << "| 5. 关键词搜索 (文档内容搜索)                     |" << std::endl;
    std::cout << "|                                          |" << std::endl;
    std::cout << "| 6. 退出程序                              |" << std::endl;
    std::cout << "+------------------------------------------+" << std::endl;
    std::cout << "\n请输入您的选择 (1-6): ";
}

// 处理关键词搜索逻辑
void handle_search() {
    if (!file_exists(SEARCH_SCRIPT)) {
        std::cerr << "\n[错误] 找不到搜索脚本文件: '" << SEARCH_SCRIPT << "'" << std::endl;
        return;
    }

    std::string keyword;
    std::cout << "\n请输入您想在所有 .md 文件内容中搜索的关键词: ";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::getline(std::cin, keyword);

    if (keyword.empty()) {
        std::cout << "\n[信息] 搜索关键词不能为空。" << std::endl;
        return;
    }

    if (keyword.find('"') != std::string::npos || keyword.find('\\') != std::string::npos) {
        std::cerr << "\n[错误] 关键词中不能包含 '\"' 或 '\\' 字符。" << std::endl;
        return;
    }

    // 第二个参数是关键词
    execute_command(SEARCH_SCRIPT, keyword);
}

int main() {
    std::cout << "自动化控制器已启动..." << std::endl;

    if (!std::filesystem::exists(CONVERSATION_DIR)) {
        std::cout << "[信息] 未找到数据文件夹 '" << CONVERSATION_DIR << "'，正在为您创建..." << std::endl;
        std::filesystem::create_directory(CONVERSATION_DIR);
        std::cout << "[成功] 已创建！请将所有聊天记录文件放入 ./" << CONVERSATION_DIR << "/ 文件夹中。" << std::endl;
    }

    if (file_exists(RENAME_SCRIPT)) {
        execute_command(RENAME_SCRIPT);
    }
    else {
        std::cout << "\n[信息] 未找到前置重命名脚本 '" << RENAME_SCRIPT << "'，跳过此步骤。" << std::endl;
    }

    int choice = 0;
    while (true) {
        display_menu();
        std::cin >> choice;

        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "\n[错误] 无效输入，请输入一个数字。" << std::endl;
            continue;
        }

        std::string script_to_run;
        bool should_exit = false;

        switch (choice) {
        case 1: script_to_run = QWEN_SCRIPT; break;
        case 2: script_to_run = CHATGPT_SCRIPT; break;
        case 3: script_to_run = DEEPSEEK_SCRIPT; break;
        case 4: script_to_run = GOOGLE_AI_SCRIPT; break;
        case 5: handle_search(); continue;
        case 6: should_exit = true; break;
        default:
            std::cout << "\n[错误] 无效选择，请输入1到6之间的数字。" << std::endl;
            continue;
        }

        if (should_exit) {
            break;
        }

        if (file_exists(script_to_run)) {
            execute_command(script_to_run);
        }
        else {
            std::cerr << "\n[错误] 找不到指定的脚本文件: '" << script_to_run << "'" << std::endl;
        }

        std::cout << "\n按任意键返回主菜单...";
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cin.get();
    }

    std::cout << "\n程序已退出。感谢使用！" << std::endl;
    return 0;
}