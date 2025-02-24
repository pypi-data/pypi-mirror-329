import os
import sys
import subprocess
from pathlib import Path
import site

def install():
    """安装 git hooks 的入口点函数"""
    print("\n正在安装 git hooks...\n")
    try:
        # 先清除旧的配置
        subprocess.run(['git', 'config', '--global', '--unset', 'core.hooksPath'], 
                     check=False)
        
        # 优先使用开发目录
        dev_hooks_dir = Path(__file__).parent.resolve() / 'hooks'
        if dev_hooks_dir.exists():
            hook_path = dev_hooks_dir / 'pre-commit'
            if hook_path.exists():
                if os.name != 'nt':
                    os.chmod(dev_hooks_dir, 0o755)
                    os.chmod(hook_path, 0o755)
                subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(dev_hooks_dir)],
                            check=True)
                print(f"Hooks 已安装到 (开发模式): {dev_hooks_dir}")
                return True
        
        # 如果开发目录不存在，再尝试 site-packages
        for site_dir in site.getsitepackages():
            hooks_dir = Path(site_dir) / 'mkdocs_document_dates' / 'hooks'
            if hooks_dir.exists():
                hook_path = hooks_dir / 'pre-commit'
                if hook_path.exists():
                    if os.name != 'nt':
                        os.chmod(hooks_dir, 0o755)
                        os.chmod(hook_path, 0o755)
                    subprocess.run(['git', 'config', '--global', 'core.hooksPath', str(hooks_dir)],
                                check=True)
                    print(f"Hooks 已安装到: {hooks_dir}")
                    return True
        
        print("错误: 未找到 hooks 目录")
        return False
    except Exception as e:
        print(f"安装 hooks 时出错: {e}")
        return False

if __name__ == '__main__':
    install()