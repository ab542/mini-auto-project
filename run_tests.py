"""便捷启动脚本：拉起开发者工具并运行测试"""
import subprocess
import sys
import os
import json


def main():
    # 确保工作目录在脚本所在目录，避免相对路径错误
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # 读取配置
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    project_path = config["project_path"]
    cli_path = config["dev_tool_path"]
    auto_port = config.get("auto_port", 9420)

    # 1. 启动开发者工具自动化端口
    print(f"[INFO] 启动开发者工具自动化端口: {auto_port}")
    subprocess.Popen(
        [cli_path, "auto", "--project", project_path, "--auto-port", str(auto_port)],
        shell=True,
    )

    # 2. 运行 pytest
    print("[INFO] 运行测试...")
    pytest_args = sys.argv[1:] if len(sys.argv) > 1 else []
    venv_python = os.path.join(script_dir, "venv", "Scripts", "python.exe")
    result = subprocess.run(
        [venv_python, "-m", "pytest"] + pytest_args
    )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
