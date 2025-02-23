import os
import platform
from datetime import datetime
from pathlib import Path
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from .lang import load_translations
from .styles import DOCUMENT_DATES_CSS

class DocumentDatesPlugin(BasePlugin):
    config_scheme = (
        ('type', config_options.Type(str, default='date')),
        ('locale', config_options.Type(str, default='en')),
        ('date_format', config_options.Type(str, default='%Y-%m-%d')),
        ('time_format', config_options.Type(str, default='%H:%M:%S')),
        ('position', config_options.Type(str, default='bottom')),
        ('exclude', config_options.Type(list, default=[])),
    )

    def __init__(self):
        super().__init__()
        self.translations = load_translations()

    def _get_css_content(self):
        """返回插件的 CSS 样式"""
        return DOCUMENT_DATES_CSS

    def on_config(self, config):
        """配置插件并添加必要的 CSS"""
        if 'extra_css' not in config:
            config['extra_css'] = []
        
        # 添加 Material Icons
        material_icons_url = 'https://fonts.googleapis.com/icon?family=Material+Icons'
        if material_icons_url not in config['extra_css']:
            config['extra_css'].append(material_icons_url)
        
        # 添加自定义 CSS
        css_file = Path(config['docs_dir']) / 'assets' / 'document_dates.css'
        css_file.parent.mkdir(parents=True, exist_ok=True)
        css_file.write_text(self._get_css_content())
        config['extra_css'].append('assets/document_dates.css')
        
        return config

    def _get_date_info(self, created, modified):
        """格式化日期信息的 HTML"""
        # 获取翻译字典
        locale = self.config['locale']
        if locale not in self.translations:
            locale = 'en'
        t = self.translations[locale]
        
        return (
            f"<div class='document-dates-plugin-wrapper'>"
            f"<div class='document-dates-plugin'>"
            f"<span title='{t['created_time']}'><span class='material-icons'>add_circle</span>"
            f"{self._get_formatted_date(created)}</span>"
            f"<span title='{t['modified_time']}'><span class='material-icons'>update</span>"
            f"{self._get_formatted_date(modified)}</span>"
            f"</div>"
            f"</div>"
        )

    def _insert_date_info(self, markdown, date_info):
        """根据配置将日期信息插入到合适的位置"""
        if not markdown.strip():
            return markdown
            
        if self.config['position'] == 'top':
            lines = markdown.splitlines()
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    lines.insert(i + 1, date_info)
                    return '\n'.join(lines)
            return f"{date_info}\n{markdown}"
        return f"{markdown}\n\n{date_info}"

    def on_page_markdown(self, markdown, page, config, files):
        """处理页面内容，添加日期信息"""
        file_path = Path(page.file.abs_src_path)
        
        if self._is_excluded(file_path, Path(config['docs_dir'])):
            return markdown
        
        created, modified = self._get_file_dates(file_path)
        created, modified = self._process_meta_dates(page.meta, created, modified)
        
        date_info = self._get_date_info(created, modified)
        return self._insert_date_info(markdown, date_info)

    def _is_excluded(self, file_path: Path, docs_dir: Path) -> bool:
        """检查文件是否在排除列表中"""
        for pattern in self.config['exclude']:
            if self._matches_exclude_pattern(file_path, docs_dir, pattern):
                return True
        return False

    def _matches_exclude_pattern(self, file_path: Path, docs_dir: Path, pattern: str) -> bool:
        """检查文件是否匹配排除模式
        支持三种匹配模式：
        1. 具体文件路径：支持多级目录，如 'private/temp.md'
        2. 目录下所有文件：使用 '*' 通配符，如 'private/*'，匹配包含子目录的所有文件
        3. 指定目录下特定类型文件：如 'private/*.md'，仅匹配当前目录下的特定类型文件
        """
        try:
            # 获取相对于 docs_dir 的路径
            rel_path = file_path.relative_to(docs_dir)
            pattern_path = Path(pattern)

            # 情况1：匹配具体文件路径
            if '*' not in pattern:
                return str(rel_path) == pattern

            # 情况2：匹配目录下所有文件（包含子目录）
            if pattern.endswith('/*'):
                base_dir = pattern[:-2]
                return str(rel_path).startswith(f"{base_dir}/")

            # 情况3：匹配指定目录下的特定类型文件（不包含子目录）
            if '*.' in pattern:
                pattern_dir = pattern_path.parent
                pattern_suffix = pattern_path.name[1:]  # 去掉 * 号
                return (rel_path.parent == Path(pattern_dir) and 
                       rel_path.name.endswith(pattern_suffix))

            return False
        except ValueError:
            return False

    def _process_meta_dates(self, meta: dict, created: datetime, modified: datetime) -> tuple[datetime, datetime]:
        """处理 frontmatter 中的日期"""
        result_created = self._parse_meta_date(meta.get('created_date'), created)
        result_modified = self._parse_meta_date(meta.get('modified_date'), modified)
        return result_created, result_modified

    def _parse_meta_date(self, date_str: str | None, default_date: datetime) -> datetime:
        """解析 meta 中的日期字符串"""
        if not date_str:
            return default_date

        try:
            return datetime.fromisoformat(str(date_str).strip("'\""))
        except (ValueError, TypeError):
            return default_date

    def _get_file_dates(self, file_path):
        """获取文件的创建时间和修改时间"""
        try:
            stat = os.stat(file_path)
            modified = datetime.fromtimestamp(stat.st_mtime)

            system = platform.system().lower()
            if system == 'darwin':  # macOS
                try:
                    created = datetime.fromtimestamp(stat.st_birthtime)
                except AttributeError:
                    created = datetime.fromtimestamp(stat.st_ctime)
            elif system == 'windows':  # Windows
                created = datetime.fromtimestamp(stat.st_ctime)
            else:  # Linux 和其他系统
                # Linux 没有可靠的创建时间，使用修改时间作为创建时间
                created = modified

            return created, modified
        except (OSError, ValueError) as e:
            # 添加错误处理，确保即使文件访问出错也能正常工作
            current_time = datetime.now()
            return current_time, current_time

    def _get_timeago(self, date):
        """将日期格式化为 timeago 格式"""
        now = datetime.now()
        diff = now - date
        seconds = diff.total_seconds()
        
        # 获取翻译字典
        locale = self.config['locale']
        if locale not in self.translations:
            locale = 'en'
        t = self.translations[locale]
        
        # 时间间隔判断
        if seconds < 10:
            return t['just_now']
        elif seconds < 60:
            return t['seconds_ago'].format(int(seconds))
        elif seconds < 120:
            return t['minute_ago']
        elif seconds < 3600:
            return t['minutes_ago'].format(int(seconds / 60))
        elif seconds < 7200:
            return t['hour_ago']
        elif seconds < 86400:
            return t['hours_ago'].format(int(seconds / 3600))
        elif seconds < 172800:
            return t['day_ago']
        elif seconds < 604800:
            return t['days_ago'].format(int(seconds / 86400))
        elif seconds < 1209600:
            return t['week_ago']
        elif seconds < 2592000:
            return t['weeks_ago'].format(int(seconds / 604800))
        elif seconds < 5184000:
            return t['month_ago']
        elif seconds < 31536000:
            return t['months_ago'].format(int(seconds / 2592000))
        elif seconds < 63072000:
            return t['year_ago']
        else:
            return t['years_ago'].format(int(seconds / 31536000))

    def _get_formatted_date(self, date):
        """格式化日期，支持 timeago、date 和 datetime 格式"""
        if self.config['type'] == 'timeago':
            return self._get_timeago(date)
        elif self.config['type'] == 'datetime':
            return date.strftime(f"{self.config['date_format']} {self.config['time_format']}")
        return date.strftime(self.config['date_format'])