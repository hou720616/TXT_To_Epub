import os
import re
from html import escape
from ebooklib import epub

ENCODINGS = ['utf-8', 'gb18030', 'gbk', 'big5', 'utf-16']
CHAPTER_PATTERN = re.compile(
    r'^\s*(第[零一二三四五六七八九十百千万0-9]+[章节卷回]|Chapter\s*\d+)',
    re.IGNORECASE
)


def detect_encoding(file_path):
    for enc in ENCODINGS:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(65536)
            return enc, 'strict'
        except UnicodeDecodeError:
            continue
    return 'utf-8', 'ignore'

def txt_to_epub(txt_path, epub_path, title="未知书籍", author="佚名"):
    book = epub.EpubBook()
    book.set_identifier(os.path.basename(epub_path))
    book.set_title(title)
    book.set_language('zh-CN')
    book.add_author(author)

    current_chapter_title = "正文"
    current_chapter_content = []
    current_chapter_from_heading = False
    epub_chapters = []
    chapter_index = 0

    def flush_current_chapter():
        nonlocal chapter_index, current_chapter_content, current_chapter_from_heading
        file_name = f'chap_{chapter_index:04d}.xhtml'
        c = epub.EpubHtml(title=current_chapter_title, file_name=file_name, lang='zh-CN')
        c.content = f'<h1>{escape(current_chapter_title)}</h1>\n' + ''.join(current_chapter_content)
        book.add_item(c)
        epub_chapters.append(c)
        chapter_index += 1
        current_chapter_content = []
        current_chapter_from_heading = False

    encoding, errors = detect_encoding(txt_path)
    with open(txt_path, 'r', encoding=encoding, errors=errors) as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                current_chapter_content.append('<br/>')
                continue

            if CHAPTER_PATTERN.match(line) and len(line) < 50:
                if current_chapter_content or current_chapter_from_heading:
                    flush_current_chapter()
                current_chapter_title = line
                current_chapter_from_heading = True
                continue

            current_chapter_content.append(f'<p>{escape(line)}</p>')

    if current_chapter_content or current_chapter_from_heading or not epub_chapters:
        flush_current_chapter()

    book.toc = tuple(epub_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    style = '''
    body { font-family: "Microsoft YaHei", sans-serif; padding: 20px; line-height: 1.6; }
    h1 { text-align: center; color: #333; margin-bottom: 30px; }
    p { text-indent: 2em; margin-bottom: 10px; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    book.spine = ['nav'] + epub_chapters
    epub.write_epub(epub_path, book, {})

if __name__ == '__main__':
    pass
