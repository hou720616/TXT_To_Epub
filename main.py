import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
                             QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from converter import txt_to_epub

class ConvertThread(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, txt_path, epub_path, title, author):
        super().__init__()
        self.txt_path = txt_path
        self.epub_path = epub_path
        self.title = title
        self.author = author

    def run(self):
        try:
            txt_to_epub(self.txt_path, self.epub_path, self.title, self.author)
            self.finished.emit(True, "转换成功！\n文件已保存至：\n" + self.epub_path)
        except Exception as e:
            self.finished.emit(False, str(e))


class TxtToEpubApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TXT 转 EPUB 工具')
        self.resize(860, 560)
        self.setMinimumSize(760, 520)
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f6fb;
                color: #1f2937;
                font-family: "Microsoft YaHei UI";
                font-size: 14px;
            }
            QGroupBox {
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                margin-top: 14px;
                padding: 14px 14px 12px 14px;
                background-color: #ffffff;
                font-weight: 600;
                color: #111827;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                top: 3px;
                padding: 0 6px;
                color: #4b5563;
                font-size: 13px;
                font-weight: 500;
            }
            QLabel {
                color: #374151;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px 10px;
                selection-background-color: #2563eb;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
            }
            QPushButton {
                background-color: #ffffff;
                color: #1f2937;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f9fafb;
                border: 1px solid #cbd5e1;
            }
            QPushButton:pressed {
                background-color: #f3f4f6;
            }
            QPushButton[primary="true"] {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 700;
                padding: 12px;
            }
            QPushButton[primary="true"]:hover {
                background-color: #1d4ed8;
            }
            QPushButton[primary="true"]:pressed {
                background-color: #1e40af;
            }
            QPushButton[primary="true"]:disabled {
                background-color: #93c5fd;
                color: #e5e7eb;
            }
        """)
        
        # 整体布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(26, 24, 26, 24)
        main_layout.setSpacing(14)

        # 标题标签
        title_label = QLabel("TXT 到 EPUB 转换器")
        title_font = QFont("Microsoft YaHei UI", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("简洁、快速地将 TXT 电子书转换为 EPUB")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #6b7280; font-size: 13px;")
        main_layout.addWidget(subtitle_label)
        
        # 文件选择区
        file_group = QGroupBox("文件设置")
        file_group_font = QFont("Microsoft YaHei", 10)
        file_group.setFont(file_group_font)
        file_layout = QFormLayout()
        file_layout.setSpacing(10)

        # 输入 TXT
        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("请选择要转换的 TXT 文本文件...")
        self.txt_input.setReadOnly(True)
        txt_btn = QPushButton("浏览...")
        txt_btn.setMinimumWidth(96)
        txt_btn.clicked.connect(self.select_txt)
        
        txt_box = QHBoxLayout()
        txt_box.addWidget(self.txt_input)
        txt_box.addWidget(txt_btn)
        file_layout.addRow("输入文件:", txt_box)

        # 输出 EPUB
        self.epub_input = QLineEdit()
        self.epub_input.setPlaceholderText("转换后的 EPUB 保存位置...")
        epub_btn = QPushButton("浏览...")
        epub_btn.setMinimumWidth(96)
        epub_btn.clicked.connect(self.select_epub)
        
        epub_box = QHBoxLayout()
        epub_box.addWidget(self.epub_input)
        epub_box.addWidget(epub_btn)
        file_layout.addRow("输出文件:", epub_box)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # 元数据区
        meta_group = QGroupBox("书籍信息 (可选)")
        meta_group.setFont(file_group_font)
        meta_layout = QFormLayout()
        meta_layout.setSpacing(10)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("未填写将默认使用文件名")
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("默认作者: 佚名")
        
        meta_layout.addRow("书  名:", self.title_input)
        meta_layout.addRow("作  者:", self.author_input)
        
        meta_group.setLayout(meta_layout)
        main_layout.addWidget(meta_group)

        # 转换按钮
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.setMinimumHeight(52)
        self.convert_btn.setProperty("primary", True)
        self.convert_btn.clicked.connect(self.start_conversion)
        main_layout.addWidget(self.convert_btn)

        self.setLayout(main_layout)

    def select_txt(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择 TXT 文件", "", "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if file_path:
            self.txt_input.setText(file_path)
            # 自动填充输出路径和书名
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            dir_name = os.path.dirname(file_path)
            self.epub_input.setText(os.path.join(dir_name, f"{base_name}.epub"))
            if not self.title_input.text():
                self.title_input.setText(base_name)

    def select_epub(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存 EPUB 文件", "", "EPUB 文件 (*.epub);;所有文件 (*.*)"
        )
        if file_path:
            self.epub_input.setText(file_path)

    def start_conversion(self):
        txt_path = self.txt_input.text()
        epub_path = self.epub_input.text()

        if not txt_path or not os.path.exists(txt_path):
            QMessageBox.warning(self, "提示", "请选择有效的 TXT 文件！")
            return
        if not epub_path:
            QMessageBox.warning(self, "提示", "请选择保存路径！")
            return

        # 获取元数据
        title = self.title_input.text().strip() or os.path.splitext(os.path.basename(txt_path))[0]
        author = self.author_input.text().strip() or "佚名"

        # 禁用按钮，显示进度
        self.convert_btn.setEnabled(False)
        self.convert_btn.setText("正在转换中，请稍候...")

        # 启动后台线程转换，避免界面卡死
        self.thread = ConvertThread(txt_path, epub_path, title, author)
        self.thread.finished.connect(self.conversion_done)
        self.thread.start()

    def conversion_done(self, success, message):
        self.convert_btn.setEnabled(True)
        self.convert_btn.setText("开始转换")
        
        if success:
            QMessageBox.information(self, "转换成功", message)
        else:
            QMessageBox.critical(self, "转换失败", f"发生错误：\n{message}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # 使用现代风格
    ex = TxtToEpubApp()
    ex.show()
    sys.exit(app.exec())
