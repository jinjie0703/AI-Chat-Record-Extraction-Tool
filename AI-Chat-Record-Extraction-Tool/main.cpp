#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <filesystem> // ��Ҫ C++17 ��׼
#include <limits>
#include <algorithm>

// --- ȫ������ ---
const std::string CONVERSATION_DIR = "conversation"; // ����ר�������ļ���

// ����ű��ļ���
const std::string RENAME_SCRIPT = "rename_files.py";
const std::string SEARCH_SCRIPT = "keyword_search.py";
const std::string QWEN_SCRIPT = "qwen_converter.py";
const std::string CHATGPT_SCRIPT = "chatgpt_converter.py";
const std::string DEEPSEEK_SCRIPT = "deepseek_converter.py";
const std::string GOOGLE_AI_SCRIPT = "google_converter.py";

// ��������������ļ��Ƿ����
bool file_exists(const std::string& filename) {
    return std::filesystem::exists(filename);
}

// ����������ִ������������ǽ������ļ�����Ϊ��һ����������
bool execute_command(const std::string& script_name, const std::string& args = "") {
    // �����ʽ: python <script.py> <data_directory> <other_args>
    std::string command = "python " + script_name + " \"" + CONVERSATION_DIR + "\"";
    if (!args.empty()) {
        command += " \"" + args + "\"";
    }

    std::cout << "\n==================================================" << std::endl;
    std::cout << "����ִ��: " << command << std::endl;
    std::cout << "==================================================" << std::endl;

    int return_code = system(command.c_str());

    if (return_code != 0) {
        std::cerr << "\n[����] ����ִ��ʧ�ܣ�������: " << return_code << std::endl;
        std::cerr << "����Python�ű� '" << script_name << "' �Ƿ��д��󣬻�Python�����Ƿ�������ȷ��" << std::endl;
        return false;
    }

    std::cout << "\n[�ɹ�] �ű� '" << script_name << "' ִ����ϣ�" << std::endl;
    return true;
}

void display_menu() {
    std::cout << "\n+------------------------------------------+" << std::endl;
    std::cout << "|      AI �Ի���¼������ - ���˵�        |" << std::endl;
    std::cout << "+------------------------------------------+" << std::endl;
    std::cout << "| ����Ŀ¼: ./" << CONVERSATION_DIR << "/" << std::endl;
    std::cout << "+------------------------------------------+" << std::endl;
    std::cout << "| --- ת������ ---                         |" << std::endl;
    std::cout << "| 1. ͨ��ǧ�� (Qwen)                       |" << std::endl;
    std::cout << "| 2. ChatGPT                   |" << std::endl;
    std::cout << "| 3. DeepSeek                              |" << std::endl;
    std::cout << "| 4. Google AI Studio              |" << std::endl;
    std::cout << "|                                          |" << std::endl;
    std::cout << "| --- �������� ---                         |" << std::endl;
    std::cout << "| 5. �ؼ������� (�ĵ���������)                     |" << std::endl;
    std::cout << "|                                          |" << std::endl;
    std::cout << "| 6. �˳�����                              |" << std::endl;
    std::cout << "+------------------------------------------+" << std::endl;
    std::cout << "\n����������ѡ�� (1-6): ";
}

// ����ؼ��������߼�
void handle_search() {
    if (!file_exists(SEARCH_SCRIPT)) {
        std::cerr << "\n[����] �Ҳ��������ű��ļ�: '" << SEARCH_SCRIPT << "'" << std::endl;
        return;
    }

    std::string keyword;
    std::cout << "\n���������������� .md �ļ������������Ĺؼ���: ";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::getline(std::cin, keyword);

    if (keyword.empty()) {
        std::cout << "\n[��Ϣ] �����ؼ��ʲ���Ϊ�ա�" << std::endl;
        return;
    }

    if (keyword.find('"') != std::string::npos || keyword.find('\\') != std::string::npos) {
        std::cerr << "\n[����] �ؼ����в��ܰ��� '\"' �� '\\' �ַ���" << std::endl;
        return;
    }

    // �ڶ��������ǹؼ���
    execute_command(SEARCH_SCRIPT, keyword);
}

int main() {
    std::cout << "�Զ���������������..." << std::endl;

    if (!std::filesystem::exists(CONVERSATION_DIR)) {
        std::cout << "[��Ϣ] δ�ҵ������ļ��� '" << CONVERSATION_DIR << "'������Ϊ������..." << std::endl;
        std::filesystem::create_directory(CONVERSATION_DIR);
        std::cout << "[�ɹ�] �Ѵ������뽫���������¼�ļ����� ./" << CONVERSATION_DIR << "/ �ļ����С�" << std::endl;
    }

    if (file_exists(RENAME_SCRIPT)) {
        execute_command(RENAME_SCRIPT);
    }
    else {
        std::cout << "\n[��Ϣ] δ�ҵ�ǰ���������ű� '" << RENAME_SCRIPT << "'�������˲��衣" << std::endl;
    }

    int choice = 0;
    while (true) {
        display_menu();
        std::cin >> choice;

        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "\n[����] ��Ч���룬������һ�����֡�" << std::endl;
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
            std::cout << "\n[����] ��Чѡ��������1��6֮������֡�" << std::endl;
            continue;
        }

        if (should_exit) {
            break;
        }

        if (file_exists(script_to_run)) {
            execute_command(script_to_run);
        }
        else {
            std::cerr << "\n[����] �Ҳ���ָ���Ľű��ļ�: '" << script_to_run << "'" << std::endl;
        }

        std::cout << "\n��������������˵�...";
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cin.get();
    }

    std::cout << "\n�������˳�����лʹ�ã�" << std::endl;
    return 0;
}