#include <iostream>
#include <cstdlib>
#include <string>

// 一个辅助函数，用于执行命令并检查结果
// 这样可以避免代码重复，让main函数更清晰
bool execute_command(const std::string& command) {
    std::cout << "\n----------------------------------------\n";
    std::cout << "即将执行命令: " << command << std::endl;
    std::cout << "----------------------------------------\n";

    // system() 函数执行命令。如果返回0，通常表示成功
    int return_code = system(command.c_str());

    if (return_code != 0) {
        // 如果返回值不为0，说明脚本执行可能出错了
        std::cerr << "\n错误：命令执行失败，返回码为: " << return_code << std::endl;
        std::cerr << "请检查Python脚本是否出错，或Python环境是否配置正确。" << std::endl;
        return false;
    }

    std::cout << "\n----------------------------------------\n";
    std::cout << "命令执行成功！" << std::endl;
    std::cout << "----------------------------------------\n";
    return true;
}

int main() {
    std::cout << "自动化脚本启动器已启动" << std::endl;

    // --- 第一个要执行的Python脚本 ---
    std::string script1 = "python add_extension.py";

    if (!execute_command(script1)) {
        // 如果第一个脚本失败了，就没必要继续执行第二个了
        std::cerr << "由于第一步失败，启动器已中止。" << std::endl;
        return 1;
    }

    // --- 第二个要执行的Python脚本 ---
    std::string script2 = "python batch_converter.py";

    if (!execute_command(script2)) {
        std::cerr << "第二步执行失败。" << std::endl;
        return 1;
    }

    std::cout << "\n 全部任务已成功执行完毕！" << std::endl;

    return 0;
}