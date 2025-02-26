import os
import sys
import subprocess
from pathlib import Path
import site
import platform

def install():
    """安装 git hooks"""
    try:
        # 检查 git 是否可用
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True, encoding='utf-8')
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 静默失败，因为用户可能在非 git 环境下安装
            return False
        
        # 检查是否在 git 仓库中
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True, encoding='utf-8')
        except subprocess.CalledProcessError:
            # 静默失败，用户可能不在 git 仓库中
            return False
            
        # 检查是否是开发模式安装
        def is_dev_install():
            try:
                import mkdocs_document_dates
                pkg_path = Path(mkdocs_document_dates.__file__).resolve().parent
                current_path = Path(__file__).resolve().parent
                # 检查是否在开发目录中
                if current_path == pkg_path:
                    return True
                # 检查是否是 egg-link 安装
                site_packages = [Path(p) for p in site.getsitepackages()]
                for p in site_packages:
                    if (p / 'mkdocs_document_dates.egg-link').exists():
                        return True
                return False
            except (ImportError, AttributeError) as e:
                print(f"开发模式检查失败: {e}")
                return False

        is_dev_mode = is_dev_install()
        hook_path = None
        
        if is_dev_mode:
            hooks_dir = Path(__file__).parent.resolve() / 'hooks'
            if hooks_dir.exists():
                hook_path = hooks_dir / 'pre-commit'
        else:
            for site_dir in site.getsitepackages():
                hooks_dir = Path(site_dir) / 'mkdocs_document_dates' / 'hooks'
                if hooks_dir.exists():
                    hook_path = hooks_dir / 'pre-commit'
                    break
        
                    
        if not hook_path or not hook_path.exists():
            print("错误: 未找到 hooks 目录或 hook 文件")
            return False

        # 设置文件权限（Unix-like 系统）
        if platform.system() != 'Windows':
            try:
                os.chmod(hook_path.parent, 0o755)
                os.chmod(hook_path, 0o755)
            except OSError as e:
                print(f"警告: 设置权限时出错: {e}")

        # 配置 git hooks 路径
        try:
            hooks_dir = hook_path.parent
            subprocess.run(['git', 'config', '--global', 'core.hooksPath', 
                          str(hooks_dir)], check=True, encoding='utf-8')
            print(f"Git hooks 已安装到: {hooks_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"错误: 设置 git hooks 路径失败: {e}")
            return False
            
    except Exception as e:
        print(f"安装 hooks 时出错: {e}")
        return False

if __name__ == '__main__':
    install()