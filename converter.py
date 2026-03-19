import os
import re
from ebooklib import epub

def detect_encoding_and_read(file_path):
    """尝试以不同编码读取文件内容，返回内容行列表"""
    encodings = ['utf-8', 'gb18030', 'gbk', 'big5', 'utf-16']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.readlines()
        except UnicodeDecodeError:
            continue
    
    # 如果全部失败，使用 utf-8 忽略错误读取
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.readlines()

def txt_to_epub(txt_path, epub_path, title="未知书籍", author="佚名"):
    """将 TXT 转换为 EPUB"""
    book = epub.EpubBook()
    
    # 设置元数据
    book.set_identifier(os.path.basename(epub_path))
    book.set_title(title)
    book.set_language('zh-CN')
    book.add_author(author)
    
    lines = detect_encoding_and_read(txt_path)
    
    chapters = []
    current_chapter_title = "正文"
    current_chapter_content = []
    
    # 简单的章节匹配正则：匹配“第一章”、“第1章”、“Chapter 1”等常见格式
    chapter_pattern = re.compile(r'^\s*(第[零一二三四五六七八九十百千万0-9]+[章节卷回]|Chapter\s*\d+)', re.IGNORECASE)
    
    for line in lines:
        line = line.strip()
        if not line:
            current_chapter_content.append('<br/>')
            continue
        
        # 判断是否为章节标题
        if chapter_pattern.match(line) and len(line) < 50: # 限制长度防止误判
            if current_chapter_content or len(chapters) == 0:
                chapters.append((current_chapter_title, current_chapter_content))
            current_chapter_title = line
            current_chapter_content = []
        else:
            # 普通段落
            current_chapter_content.append(f'<p>{line}</p>')
            
    # 添加最后一章
    if current_chapter_content:
        chapters.append((current_chapter_title, current_chapter_content))
        
    epub_chapters = []
    for i, (chap_title, content) in enumerate(chapters):
        # 创建章节
        file_name = f'chap_{i:04d}.xhtml'
        c = epub.EpubHtml(title=chap_title, file_name=file_name, lang='zh-CN')
        
        # 拼接HTML内容
        html_content = f'<h1>{chap_title}</h1>\n' + '\n'.join(content)
        c.content = html_content
        
        book.add_item(c)
        epub_chapters.append(c)
        
    # 定义目录 (TOC)
    book.toc = tuple(epub_chapters)
    
    # 添加必须的内置文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # 基础 CSS 样式
    style = '''
    body { font-family: "Microsoft YaHei", sans-serif; padding: 20px; line-height: 1.6; }
    h1 { text-align: center; color: #333; margin-bottom: 30px; }
    p { text-indent: 2em; margin-bottom: 10px; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # 设置书脊 (Spine) - 定义阅读顺序
    book.spine = ['nav'] + epub_chapters
    
    # 生成 epub 文件
    epub.write_epub(epub_path, book, {})

if __name__ == '__main__':
    # 简单测试代码
    pass
