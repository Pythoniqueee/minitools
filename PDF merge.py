import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from PyPDF2 import PdfMerger

# 创建PDFMergerApp类，继承 QMainWindow
class PDFMergerApp(QMainWindow):
    # 定义构造函数 初始化窗口
    def __init__(self):
        # 调用 QMainWindow 的 __init__ 方法
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("PDFMerge")
        # 设置窗口 (x, y, 宽, 高) 在荧幕上的位置 (100, 100) 大小 600 x 400 像素
        self.setGeometry(100, 100, 600, 400)

        # 初始化UI
        self.init_ui()

    def init_ui(self):
        # 主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # 文件列表控件
        self.file_list = QListWidget()
        self.file_list.setDragDropMode(QListWidget.InternalMove)  # 允许拖拽调整顺序
        layout.addWidget(QLabel("已选文件（拖拽调整顺序）:"))
        layout.addWidget(self.file_list)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 添加文件按钮
        self.btn_add = QPushButton("Add PDFs")
        self.btn_add.clicked.connect(self.add_files)
        button_layout.addWidget(self.btn_add)

        # 移除文件按钮
        self.btn_remove = QPushButton("Remove selected")
        self.btn_remove.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.btn_remove)

        # 上移/下移按钮
        self.btn_up = QPushButton("Up")
        self.btn_up.clicked.connect(lambda: self.move_item(-1))
        button_layout.addWidget(self.btn_up)

        self.btn_down = QPushButton("Down")
        self.btn_down.clicked.connect(lambda: self.move_item(1))
        button_layout.addWidget(self.btn_down)

        layout.addLayout(button_layout)

        # 合并按钮
        self.btn_merge = QPushButton("Merge")
        self.btn_merge.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.btn_merge)

        # 状态标签
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def add_files(self):
        """添加PDF文件到列表"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择PDF文件", "", "PDF文件 (*.pdf)"
        )
        if files:
            self.file_list.addItems(files)
            self.status_label.setText(f"已添加 {len(files)} 个文件")

    def remove_selected(self):
        """移除选中的文件"""
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))
        self.status_label.setText("Selected File Removed")

    def move_item(self, direction):
        """调整文件顺序（direction=-1上移，1下移）"""
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            new_row = current_row + direction
            if 0 <= new_row < self.file_list.count():
                current_item = self.file_list.takeItem(current_row)
                self.file_list.insertItem(new_row, current_item)
                self.file_list.setCurrentRow(new_row)

    def merge_pdfs(self):
        """合并PDF文件"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "错误", "请先添加PDF文件！")
            return

        # 选择保存路径
        save_path, _ = QFileDialog.getSaveFileName(
            self, "保存合并后的PDF", "", "PDF文件 (*.pdf)"
        )
        if not save_path:
            return  # 用户取消保存

        # 确保文件扩展名正确
        if not save_path.lower().endswith('.pdf'):
            save_path += '.pdf'

        try:
            merger = PdfMerger()

            # 按顺序添加文件
            for i in range(self.file_list.count()):
                file_path = self.file_list.item(i).text()
                merger.append(file_path)

            # 写入合并后的PDF
            with open(save_path, 'wb') as f:
                merger.write(f)

            self.status_label.setText(f"合并成功！保存至: {save_path}")
            QMessageBox.information(self, "成功", "PDF合并完成！")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"合并失败: {str(e)}")
            self.status_label.setText("合并失败")

        finally:
            merger.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())