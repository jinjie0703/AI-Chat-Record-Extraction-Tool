# AI-Chat-Record-Extraction-Tool

<p align="center">  <!-- ��������Է�һЩ���£����繹��״̬�����֤�� -->  <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">  <img src="https://img.shields.io/badge/platform-Windows-informational" alt="Platform"></p>

<details><summary>English Version (Click to expand)</summary>

### Introduction

This is a utility tool for extracting and converting chat records from mainstream AI applications (like ChatGPT, Claude, etc.). It's designed to help users parse exported chat data and convert it into a universal Markdown (`.md`) format for easier analysis, archiving, or sharing.

I created this tool with the personal goal of converting my AI conversations into `.md` format to better organize knowledge and build knowledge graphs. Realizing it could be useful in other scenarios, I decided to make it open-source. Currently, the script only supports converting chat records from **Google AI Studio**. Support for other mainstream platforms will be added in the future, along with general user experience improvements. Contributions to enhance the project by submitting PRs are highly welcome.

### Features

* **Multi-Platform Support**: Capable of extracting records exported from various AI chat platforms and converting them into `.md` documents.
* **Multiple Output Formats**: Supports Markdown (`.md`) and JSON (`.json`).
* **Batch Processing**: Provides a script to process all chat record files within a folder at once.
* **Easy to Extend**: Features a modular design, making it convenient for users to add support for new platforms or output formats.

### Installation & Setup

1. **Clone the Repository**:
  
      git clone https://github.com/jinjie0703/AI-Chat-Record-Extraction-Tool.git
  
2. **Compile the Project**:
  
  * Open the solution file (`.sln`) with **Visual Studio 2022**.
  * Select the `Release` and `x64` configuration.
  * Click on "Build" -> "Build Solution" in the menu bar (Shortcut: `F7` or `Ctrl+Shift+B`).
3. **Find the Executable**:
  
  * After a successful build, you can find `AI-Chat-Record-Extraction-Tool.exe` in the `x64/Release/` directory of the project.

### Usage

The core of this tool is a command-line program. Place the `AI-Chat-Record-Extraction-Tool.exe`, the Python script, and the data file(s) exported from the official source into the same folder, and then run the executable.

**Parameter Description**:

* `--source, -s`: Specify the source platform of the chat record (e.g., `chatgpt`, `claude`).
* `--input, -i`: The path to a single input chat record file.
* `--output, -o`: The path to the directory where the converted file will be saved.
* `--format, -f`: The desired output format (`txt`, `md`, `json`).

* * *

### How to Contribute

Contributions of any kind are welcome! If you have a suggestion or find a bug, please feel free to submit a Pull Request or create an Issue.

1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### License

This project is licensed under the [MIT](LICENSE.txt) License.

</details>

<details open><summary>���İ� (���չ��)</summary>

### ����

����һ��������ȡ��ת������AI����Ӧ�ã��� ChatGPT, Claude �ȣ���¼��ʵ�ù��ߡ���ּ�ڰ����û������������������ݣ�������ת��Ϊͨ�õ�Markdown (`.md`)��ʽ���Ա��ں����ķ������浵����������������С�����������ai�Ի�����������ת����.md��ʽ����֪ʶ���ܺ�����֪ʶͼ�ף����ǵ���һ����Ӧ�ó������Կ�Դ������Ŀǰ�ű�ֻ֧��Google AI Studio����������ת���������Ჹȫ����ƽ̨��ת���ű����Ż����飻��ӭ������Ŀ���ύPR��

### ��������

* **��ƽ̨֧��**: �ܹ���ȡ�Ӷ���AI����ƽ̨�����ļ�¼��ת����md�ĵ���
* **���������ʽ**: Markdown (`.md`) �� JSON (`.json`)��
* **��������**: �ṩ�ű�������һ����ת���ļ����ڵ����������¼�ļ���
* **������չ**: ģ�黯��ƣ������û���Ӷ���ƽ̨���������ʽ��֧�֡�

### ��װ������

1. **��¡�ֿ�**:
  
      git cone https://github.com/jinjie0703/AI-Chat-Record-Extraction-Tool.git
  
2. **������Ŀ**:
  
  * ʹ�� **Visual Studio 2022** �򿪽�������ļ� (`.sln`)��
  * ��������ѡ�� `Release` �� `x64`��
  * ����˵����ġ����ɡ� -> �����ɽ�������� (��ݼ� `F7` �� `Ctrl+Shift+B`)��
3. **�ҵ���ִ���ļ�**:
  
  * ����ɹ�������������ĿĿ¼�� `x64/Release/` �ļ������ҵ� `AI-Chat-Record-Extraction-Tool.exe`��

### ʹ�÷���

�����ߵĺ�����һ�������г��򣬽�`AI-Chat-Record-Extraction-Tool.exe`��`python`�ű���`�ٷ����ݿ⵼���������ļ�`����ͬһ���ļ��������exe����

**����˵��**:

* `--source, -s`: ָ�������¼����Դƽ̨ (���� `chatgpt`, `claude`)��
* `--input, -i`: �������������¼�ļ���·����
* `--output, -o`: ���ڴ��ת�����ļ���Ŀ¼·����
* `--format, -f`: ��ϣ��ת����Ŀ���ʽ (`txt`, `md`, `json`)��

</details>

* * *

### ��ι���

��ӭ�κ���ʽ�Ĺ��ף�������кõĽ��������Bug������ʱ�ύ Pull Request �򴴽� Issue��

1. Fork ���ֿ�
2. �������ķ�֧
3. �ύ���ĸ���
4. ���͵���֧
5. ��һ�� Pull Request

### ���֤

����Ŀ���� [MIT](LICENSE.txt) ���֤��