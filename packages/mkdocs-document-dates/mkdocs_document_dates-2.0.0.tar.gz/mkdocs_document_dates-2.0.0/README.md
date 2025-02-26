# mkdocs-document-dates

English | [简体中文](README_zh.md)



A MkDocs plugin for displaying **accurate** document creation and last modification dates.

## Features

- Automatically displays document creation and last modification times
- No Git dependency, uses filesystem timestamps directly
- Supports manual date specification in `Front Matter`
- Cross-platform support (Windows, macOS, Linux)
- Support for multiple time formats (date, datetime, timeago)
- Flexible display position (top or bottom)
- Support for document exclusion
- Material Design icons, Elegant styling
- Lightweight with no extra dependencies
- Multi-language support

## Installation

```bash
pip install mkdocs-document-dates
```

## Configuration

Just add the plugin to your mkdocs.yml:

```yaml
plugins:
  - document-dates
```

Or, customize the configuration:

```yaml
plugins:
  - document-dates:
      type: date               # Date type: date | datetime | timeago, default: date
      locale: en               # Localization: zh zh_tw en es fr de ar ja ko ru, default: en
      date_format: '%Y-%m-%d'  # Date format
      time_format: '%H:%M:%S'  # Time format (valid only if type=datetime)
      position: bottom         # Display position: top (after title) | bottom (end of document), default: bottom
      exclude:                 # List of file patterns to exclude
        - temp.md              # Exclude specific file
        - private/*            # Exclude all files in private directory, including subdirectories
        - drafts/*.md          # Exclude all markdown files in the current directory drafts, but not subdirectories
```

## Manual Date Specification

You can also manually specify the date of a Markdown document in its `Front Matter` :

```yaml
---
created: 2023-01-01
modified: 2023-12-31
---

# Document Title
```



## Configuration Options

- `type` : Date type (default: `date` )
  - `date` : Display date only
  - `datetime` : Display date and time
  - `timeago` : Display relative time (e.g., 2 minutes ago)
- `locale` : Localization (default: `en` )
  - Supports: `zh zh_tw en es fr de ar ja ko ru`
- `date_format` : Date format (default: `%Y-%m-%d`)
  - Supports all Python datetime format strings, e.g., %Y-%m-%d, %b %d, %Y, etc.
- `time_format` : Time format (default: `%H:%M:%S`)
- `position` : Display position (default: `bottom`)
  - `top` : Display after the first heading
  - `bottom` : Display at the end of the document
- `exclude` : File exclusion list (default: [] )
  - Supports glob patterns, e.g., ["private/\*", "temp.md", "drafts/\*.md"]

## Notes

- Creation time behavior varies across operating systems:
  - Windows: Uses file creation time
  - macOS: Uses file creation time (birthtime)
  - Linux: Uses modification time as creation time due to system limitations, if you need the exact creation time, you can manually specify it in Front Matter
- It still works when using CI/CD build systems (e.g. Github Actions)
  - Used a cache file `.dates_cache.json` to solve this problem
  - You can configure it like this: `pip install --upgrade mkdocs-document-dates`
    ```
    ...
    
      - run: pip install --upgrade mkdocs-document-dates
      - run: mkdocs gh-deploy --force
    ```  