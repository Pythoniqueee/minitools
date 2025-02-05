import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox
from PyPDF2 import PdfMerger

# 创建PDFMergerApp类，继承 QWidget
class PDFMergerApp(QWidget):
    # 定义构造函数 初始化窗口
    def __init__(self):
        # 调用 QMainWindow 的 __init__ 方法
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("PDF 合并工具")
        # 设置窗口 (x, y, 宽, 高) 在荧幕上的位置 (200, 200) 大小 500 x 400 像素
        self.setGeometry(200, 200, 500, 400)

        # 创建布局 所有组件会从上到下排列
        layout = QVBoxLayout()

        # 创建按钮
        # 创建按钮 ”选择 PDF 文件“
        self.select_button = QPushButton("选择 PDF 文件")
        # 当用户点击按钮时，连接 select_pdfs() 方法，打开文件选择对话框
        self.select_button.clicked.connect(self.select_pdfs)
        # 将按钮 添加到布局
        layout.addWidget(self.select_button)

        # 显示选中的文件列表
        # 创建一个 列表框，用于 显示用户选择的 PDF 文件
        self.file_list = QListWidget()
        # 将列表框 添加到布局
        layout.addWidget(self.file_list)

        # 创建合并按钮
        # 创建按钮 "合并 PDF"
        self.merge_button = QPushButton("合并 PDF")
        # 当用户点击按钮时，连接 merge_pdfs() 方法
        self.merge_button.clicked.connect(self.merge_pdfs)
        # 将按钮 添加到布局
        layout.addWidget(self.merge_button)

        # 设置布局
        # 将窗口布局设为 layout，确保所有组件正确排列
        self.setLayout(layout)

        # 存储选中的文件路径
        # 定义一个 列表变量，用于 存储用户选择的 PDF 文件路径
        self.pdf_files = []

    # 定义 select_pdfs() 方法，让用户 选择多个 PDF 文件
    def select_pdfs(self):
        """ 选择多个 PDF 文件 """
        # 打开文件对话框，让用户选择多个 PDF 文件 | files: 返回选择的文件路径列表
        files, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        # 如果 files 不为空
        if files:
            # 存储文件路径
            self.pdf_files = files
            # 清空旧的文件列表
            self.file_list.clear()
            # 将新选择的文件添加到 QListWidget 中显示
            self.file_list.addItems(self.pdf_files)

    # 定义 merge_pdfs() 方法，处理 PDF 文件合并
    def merge_pdfs(self):
        """ 合并 PDF 文件 """
        # 如果没有选中文件
        if not self.pdf_files:
            # 如果没有选中文件 弹出警告框 QMessageBox.warning()
            QMessageBox.warning(self, "警告", "请先选择至少两个 PDF 文件！")
            # 并返回
            return

        # 选择保存路径
        # 弹出文件保存对话框，让用户选择合并后的 PDF 保存位置
        save_path, _ = QFileDialog.getSaveFileName(self, "保存合并后的 PDF", "", "PDF Files (*.pdf)")
        # 如果用户没有选择保存路径
        if not save_path:
            # 直接返回
            return

        # 使用异常处理
        try:
            # 创建 PDF 合并对象
            merger = PdfMerger()

            # 遍历用户选择的所有 PDF 文件
            for pdf in self.pdf_files:
                # 并使用 merger.append(pdf) 添加到合并对象中
                merger.append(pdf)
            # 写入合并后的 PDF 文件 到 save_path
            merger.write(save_path)
            # 然后 关闭 merger 释放资源
            merger.close()

            # 合并成功后弹出消息框，通知用户 文件已保存
            QMessageBox.information(self, "成功", f"PDF 已成功合并并保存到：\n{save_path}")
        # 如果发生错误（例如 PDF 文件损坏）
        except Exception as e:
            # 弹出错误对话框
            QMessageBox.critical(self, "错误", f"合并 PDF 失败：\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())
