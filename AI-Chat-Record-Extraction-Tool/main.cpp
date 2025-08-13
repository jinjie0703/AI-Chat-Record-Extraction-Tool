#include <iostream>
#include <cstdlib>
#include <string>

// һ����������������ִ����������
// �������Ա�������ظ�����main����������
bool execute_command(const std::string& command) {
    std::cout << "\n----------------------------------------\n";
    std::cout << "����ִ������: " << command << std::endl;
    std::cout << "----------------------------------------\n";

    // system() ����ִ������������0��ͨ����ʾ�ɹ�
    int return_code = system(command.c_str());

    if (return_code != 0) {
        // �������ֵ��Ϊ0��˵���ű�ִ�п��ܳ�����
        std::cerr << "\n��������ִ��ʧ�ܣ�������Ϊ: " << return_code << std::endl;
        std::cerr << "����Python�ű��Ƿ������Python�����Ƿ�������ȷ��" << std::endl;
        return false;
    }

    std::cout << "\n----------------------------------------\n";
    std::cout << "����ִ�гɹ���" << std::endl;
    std::cout << "----------------------------------------\n";
    return true;
}

int main() {
    std::cout << "�Զ����ű�������������" << std::endl;

    // --- ��һ��Ҫִ�е�Python�ű� ---
    std::string script1 = "python add_extension.py";

    if (!execute_command(script1)) {
        // �����һ���ű�ʧ���ˣ���û��Ҫ����ִ�еڶ�����
        std::cerr << "���ڵ�һ��ʧ�ܣ�����������ֹ��" << std::endl;
        return 1;
    }

    // --- �ڶ���Ҫִ�е�Python�ű� ---
    std::string script2 = "python batch_converter.py";

    if (!execute_command(script2)) {
        std::cerr << "�ڶ���ִ��ʧ�ܡ�" << std::endl;
        return 1;
    }

    std::cout << "\n ȫ�������ѳɹ�ִ����ϣ�" << std::endl;

    return 0;
}