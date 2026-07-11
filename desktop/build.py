# -*- coding: utf-8 -*-
"""
打包脚本（跨平台 Python 版）
用法：python build.py
功能：自动安装依赖 + 调用 PyInstaller 按 build.spec 打包为 exe。
"""
import sys, os, subprocess, shutil


def check_python_version():
    """检查 Python 版本兼容性。"""
    v = sys.version_info
    print(f"[检测] Python {v.major}.{v.minor}.{v.micro}")
    # PySide6 支持 3.8-3.12，3.13+ 可能无预编译 wheel
    if v.minor >= 13:
        print("[警告] PySide6 可能不支持 Python 3.13+，建议使用 3.10~3.12")
        ans = input("是否继续？(y/N): ").strip().lower()
        if ans != 'y':
            sys.exit(1)
    return True


def install_deps():
    """安装运行时依赖和 PyInstaller。"""
    desktop = os.path.dirname(os.path.abspath(__file__))
    req = os.path.join(desktop, "requirements.txt")
    print("[1/3] 正在安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", req], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("[OK] 依赖安装完成")


def build():
    """使用 build.spec 打包。"""
    desktop = os.path.dirname(os.path.abspath(__file__))
    spec = os.path.join(desktop, "build.spec")
    dist = os.path.join(desktop, "dist")

    # 清理旧产物
    for d in [dist, os.path.join(desktop, "build")]:
        if os.path.exists(d):
            shutil.rmtree(d)

    print(f"[2/3] 正在打包（spec: {spec}）...")
    print("     首次打包需 5-10 分钟，请耐心等待")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", spec, "--noconfirm"],
        cwd=desktop,
    )
    if result.returncode != 0:
        print("[错误] 打包失败")
        return False

    exe_path = os.path.join(dist, "学生会人事管理系统.exe")
    print(f"[3/3] 打包成功！")
    print(f"     输出: {exe_path}")
    print(f"     双击即可运行，无需 Python 或浏览器")
    return True


def main():
    check_python_version()
    try:
        install_deps()
        build()
    except subprocess.CalledProcessError as e:
        print(f"[错误] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
