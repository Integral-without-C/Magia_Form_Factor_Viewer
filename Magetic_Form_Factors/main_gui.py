import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit,
    QComboBox, QCheckBox, QHBoxLayout, QVBoxLayout, QMessageBox, QGroupBox, QFileDialog,
    QDialog, QTextEdit, QSpacerItem, QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_manager import MagneticFormFactorDB


ELEMENTS = [
    (1, 'H', '氢', (0, 0)), (2, 'He', '氦', (0, 17)),
    (3, 'Li', '锂', (1, 0)), (4, 'Be', '铍', (1, 1)), (5, 'B', '硼', (1, 12)), (6, 'C', '碳', (1, 13)),
    (7, 'N', '氮', (1, 14)), (8, 'O', '氧', (1, 15)), (9, 'F', '氟', (1, 16)), (10, 'Ne', '氖', (1, 17)),
    (11, 'Na', '钠', (2, 0)), (12, 'Mg', '镁', (2, 1)), (13, 'Al', '铝', (2, 12)), (14, 'Si', '硅', (2, 13)),
    (15, 'P', '磷', (2, 14)), (16, 'S', '硫', (2, 15)), (17, 'Cl', '氯', (2, 16)), (18, 'Ar', '氩', (2, 17)),
    (19, 'K', '钾', (3, 0)), (20, 'Ca', '钙', (3, 1)), (21, 'Sc', '钪', (3, 2)), (22, 'Ti', '钛', (3, 3)),
    (23, 'V', '钒', (3, 4)), (24, 'Cr', '铬', (3, 5)), (25, 'Mn', '锰', (3, 6)), (26, 'Fe', '铁', (3, 7)),
    (27, 'Co', '钴', (3, 8)), (28, 'Ni', '镍', (3, 9)), (29, 'Cu', '铜', (3, 10)), (30, 'Zn', '锌', (3, 11)),
    (31, 'Ga', '镓', (3, 12)), (32, 'Ge', '锗', (3, 13)), (33, 'As', '砷', (3, 14)), (34, 'Se', '硒', (3, 15)),
    (35, 'Br', '溴', (3, 16)), (36, 'Kr', '氪', (3, 17)),
    (37, 'Rb', '铷', (4, 0)), (38, 'Sr', '锶', (4, 1)), (39, 'Y', '钇', (4, 2)), (40, 'Zr', '锆', (4, 3)),
    (41, 'Nb', '铌', (4, 4)), (42, 'Mo', '钼', (4, 5)), (43, 'Tc', '锝', (4, 6)), (44, 'Ru', '钌', (4, 7)),
    (45, 'Rh', '铑', (4, 8)), (46, 'Pd', '钯', (4, 9)), (47, 'Ag', '银', (4, 10)), (48, 'Cd', '镉', (4, 11)),
    (49, 'In', '铟', (4, 12)), (50, 'Sn', '锡', (4, 13)), (51, 'Sb', '锑', (4, 14)), (52, 'Te', '碲', (4, 15)),
    (53, 'I', '碘', (4, 16)), (54, 'Xe', '氙', (4, 17)),
    (55, 'Cs', '铯', (5, 0)), (56, 'Ba', '钡', (5, 1)), (57, 'La', '镧', (5, 2)), (72, 'Hf', '铪', (5, 3)),
    (73, 'Ta', '钽', (5, 4)), (74, 'W', '钨', (5, 5)), (75, 'Re', '铼', (5, 6)), (76, 'Os', '锇', (5, 7)),
    (77, 'Ir', '铱', (5, 8)), (78, 'Pt', '铂', (5, 9)), (79, 'Au', '金', (5, 10)), (80, 'Hg', '汞', (5, 11)),
    (81, 'Tl', '铊', (5, 12)), (82, 'Pb', '铅', (5, 13)), (83, 'Bi', '铋', (5, 14)), (84, 'Po', '钋', (5, 15)),
    (85, 'At', '砹', (5, 16)), (86, 'Rn', '氡', (5, 17)),
    (87, 'Fr', '钫', (6, 0)), (88, 'Ra', '镭', (6, 1)), (89, 'Ac', '锕', (6, 2)), (104, 'Rf', '𬬻', (6, 3)),
    (105, 'Db', '𬭊', (6, 4)), (106, 'Sg', '𬭳', (6, 5)), (107, 'Bh', '𬭶', (6, 6)), (108, 'Hs', '𬭸', (6, 7)),
    (109, 'Mt', '鿔', (6, 8)), (110, 'Ds', '𫟼', (6, 9)), (111, 'Rg', '𬬭', (6, 10)), (112, 'Cn', '鿬', (6, 11)),
    (113, 'Nh', '鉨', (6, 12)), (114, 'Fl', '鈇', (6, 13)), (115, 'Mc', '镆', (6, 14)), (116, 'Lv', '鉝', (6, 15)),
    (117, 'Ts', '石田', (6, 16)), (118, 'Og', '气奥', (6, 17)),
    (58, 'Ce', '铈', (7, 3)), (59, 'Pr', '镨', (7, 4)), (60, 'Nd', '钕', (7, 5)), (61, 'Pm', '钷', (7, 6)),
    (62, 'Sm', '钐', (7, 7)), (63, 'Eu', '铕', (7, 8)), (64, 'Gd', '钆', (7, 9)), (65, 'Tb', '铽', (7, 10)),
    (66, 'Dy', '镝', (7, 11)), (67, 'Ho', '钬', (7, 12)), (68, 'Er', '铒', (7, 13)), (69, 'Tm', '铥', (7, 14)),
    (70, 'Yb', '镱', (7, 15)), (71, 'Lu', '镥', (7, 16)),
    (90, 'Th', '钍', (8, 3)), (91, 'Pa', '镤', (8, 4)), (92, 'U', '铀', (8, 5)), (93, 'Np', '镎', (8, 6)),
    (94, 'Pu', '钚', (8, 7)), (95, 'Am', '镅', (8, 8)), (96, 'Cm', '锔', (8, 9)), (97, 'Bk', '锫', (8, 10)),
    (98, 'Cf', '锎', (8, 11)), (99, 'Es', '锿', (8, 12)), (100, 'Fm', '镄', (8, 13)), (101, 'Md', '钔', (8, 14)),
    (102, 'No', '锘', (8, 15)), (103, 'Lr', '铹', (8, 16))
]

class PeriodicTableWidget(QWidget):
    def __init__(self, db, on_element_clicked):
        super().__init__()
        self.db = db
        self.on_element_clicked = on_element_clicked
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        elements_with_data = set(self.db.get_elements())
        for num, en, zh, (row, col) in ELEMENTS:
            btn = QPushButton(f"{zh}\n{en}\n{num}")
            btn.setFixedSize(60, 80)
            if en not in elements_with_data:
                btn.setStyleSheet("background-color: lightgray;")
            btn.clicked.connect(lambda _, e=en: self.on_element_clicked(e))
            grid.addWidget(btn, row, col)
        self.setLayout(grid)

INSTRUCTION_TEXT = """
【Magia_Form_Factor_Viewer: 磁性Form Factor可视化工具 使用说明】
***确保原始数据和程序位于同一目录下***
1. 在左侧周期表中点击元素，若有数据则可选择价态和j类型，若无数据则提示。
2. 输入波长（单位Å）、θ范围和步长。
3. 选择价态和j类型（可多选），点击“绘图”显示曲线。
4. 可勾选“对数坐标”切换横轴为对数。
5. 可导出当前曲线为PNG图片和数据文件（.dat）。

【数据表格式示例，可随时继续添加】
文件首行为j类型和元素类型说明，如：
<j0> Form factors for 3d transition elements and their ions
Ion	A	a	B	b	C	c	D
Sc0	0.2512	90.0296	0.329	39.4021	0.4235	14.3222	-0.0043
Sc1	0.4889	51.1603	0.5203	14.0764	-0.0286	0.1792	0.0185
...
（每行依次为元素符号、A、a、B、b、C、c、D参数，Tab分隔）
***数据文件需要保存至相同目录下，以Table*.txt命名。***

"""

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)  
        self.setWindowTitle("操作说明") 
        self.resize(1500, 800)  
        layout = QVBoxLayout(self) 
        text_edit = QTextEdit() 
        text_edit.setReadOnly(True) 
        text_edit.setPlainText(INSTRUCTION_TEXT)  
        text_edit.setFont(QFont("Consolas", 15)) 
        layout.addWidget(text_edit) 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MagneticFormFactorDB(r"d:\\study\\Magnetic_Form_Factors\\data")
        self.selected_element = None
        self.selected_valence = None
        self.selected_jtypes = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Magia_Form_Factor_Viewer")
        main_layout = QHBoxLayout()

        # 周期表
        self.pt_widget = PeriodicTableWidget(self.db, self.on_element_clicked)
        main_layout.addWidget(self.pt_widget, 2)

        # 右侧参数区
        param_layout = QVBoxLayout()

        # 使用说明按钮
        help_btn = QPushButton("使用说明")
        help_btn.clicked.connect(self.show_help)
        param_layout.addWidget(help_btn, alignment=Qt.AlignRight)

        # 波长
        w_box = QHBoxLayout()
        w_box.addWidget(QLabel("波长 λ (Å):"))
        self.w_input = QLineEdit()
        w_box.addWidget(self.w_input)
        param_layout.addLayout(w_box)

        # θ范围
        theta_box = QHBoxLayout()
        theta_box.addWidget(QLabel("θ范围 (度):"))
        self.theta_min = QLineEdit("0")
        self.theta_max = QLineEdit("80")
        self.theta_step = QLineEdit("0.05")
        theta_box.addWidget(self.theta_min)
        theta_box.addWidget(QLabel("~"))
        theta_box.addWidget(self.theta_max)
        theta_box.addWidget(QLabel("步长:"))
        theta_box.addWidget(self.theta_step)
        param_layout.addLayout(theta_box)

        # 价态下拉
        self.valence_combo = QComboBox()
        self.valence_combo.currentIndexChanged.connect(self.on_valence_changed)
        param_layout.addWidget(QLabel("选择价态:"))
        param_layout.addWidget(self.valence_combo)

        # j类型多选
        self.j0_cb = QCheckBox("j0")
        self.j2_cb = QCheckBox("j2")
        self.j4_cb = QCheckBox("j4")
        self.j6_cb = QCheckBox("j6")
        jtype_box = QHBoxLayout()
        for cb in [self.j0_cb, self.j2_cb, self.j4_cb, self.j6_cb]:
            jtype_box.addWidget(cb)
        param_layout.addWidget(QLabel("选择j类型:"))
        param_layout.addLayout(jtype_box)

        # 对数坐标
        self.log_cb = QCheckBox("对数坐标（横轴s）")
        param_layout.addWidget(self.log_cb)

        # 绘图与导出按钮
        btn_box = QHBoxLayout()
        self.plot_btn = QPushButton("绘图")
        self.export_btn = QPushButton("导出")
        btn_box.addWidget(self.plot_btn)
        btn_box.addWidget(self.export_btn)
        param_layout.addLayout(btn_box)

        # matplotlib画布
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        plot_group = QGroupBox("Form Factor 曲线")
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)
        plot_group.setLayout(plot_layout)
        param_layout.addWidget(plot_group, 2)

        # 右侧布局
        main_layout.addLayout(param_layout, 1)
        self.setLayout(main_layout)

        # 事件绑定
        self.plot_btn.clicked.connect(self.on_plot)
        self.export_btn.clicked.connect(self.on_export)

        # 数据缓存
        self.last_plot_data = None

    def on_element_clicked(self, elem):
        self.selected_element = elem
        valences = self.db.get_valences(elem)
        if not valences:
            QMessageBox.information(self, "提示", "暂无数据，亟需补充。")
            self.valence_combo.clear()
            return
        self.valence_combo.clear()
        self.valence_combo.addItems(valences)
        self.on_valence_changed(0)

    def on_valence_changed(self, idx):
        elem = self.selected_element
        if not elem:
            return
        valence = self.valence_combo.currentText()
        self.selected_valence = valence
        jtypes = self.db.get_j_types(elem, valence)
        # 自动勾选有数据的j类型
        self.j0_cb.setEnabled("j0" in jtypes)
        self.j2_cb.setEnabled("j2" in jtypes)
        self.j4_cb.setEnabled("j4" in jtypes)
        self.j6_cb.setEnabled("j6" in jtypes)
        for cb, jt in zip([self.j0_cb, self.j2_cb, self.j4_cb, self.j6_cb], ["j0", "j2", "j4", "j6"]):
            cb.setChecked(jt in jtypes)

    def on_plot(self):
        elem = self.selected_element
        valence = self.valence_combo.currentText()
        jtypes = []
        for cb, jt in zip([self.j0_cb, self.j2_cb, self.j4_cb, self.j6_cb], ["j0", "j2", "j4", "j6"]):
            if cb.isChecked() and cb.isEnabled():
                jtypes.append(jt)
        if not elem or not valence or not jtypes:
            QMessageBox.warning(self, "警告", "请先选择元素、价态和j类型。")
            return
        try:
            w = float(self.w_input.text())
            theta_min = float(self.theta_min.text())
            theta_max = float(self.theta_max.text())
            theta_step = float(self.theta_step.text())
            if w <= 0 or theta_min < 0 or theta_max > 180 or theta_min >= theta_max or theta_step <= 0:
                raise ValueError
        except Exception:
            QMessageBox.warning(self, "警告", "请输入有效的波长和θ范围参数。")
            return

        theta = np.arange(theta_min, theta_max + theta_step, theta_step)
        s = np.sin(np.deg2rad(theta)) / w

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        plot_data = []

        for jt in jtypes:
            params = self.db.get_params(elem, valence, jt)
            if not params:
                continue
            if jt == "j0":
                y = (
                    params["A"] * np.exp(-params["a"] * s ** 2)
                    + params["B"] * np.exp(-params["b"] * s ** 2)
                    + params["C"] * np.exp(-params["c"] * s ** 2)
                )
            else:
                y = (
                    params["A"] * np.exp(-params["a"] * s ** 2)
                    + params["B"] * np.exp(-params["b"] * s ** 2)
                    + params["C"] * np.exp(-params["c"] * s ** 2)
                    + params["D"]
                ) * s ** 2
            ax.plot(s, y, label=jt)
            plot_data.append((jt, s.copy(), y.copy()))

        ax.set_xlabel("s = sinθ / λ (Å⁻¹)")
        ax.set_ylabel("Form Factor")
        title = f"{elem} {valence}+  Form Factor"
        ax.set_title(title)
        ax.legend()
        if self.log_cb.isChecked():
            ax.set_xscale("log")
        ax.grid(True)
        self.canvas.draw()
        self.last_plot_data = plot_data

    def on_export(self):
        if not self.last_plot_data:
            QMessageBox.warning(self, "警告", "请先绘制曲线后再导出。")
            return
        # 导出图片
        img_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "PNG图片 (*.png)")
        if img_path:
            self.fig.savefig(img_path)
        # 导出数据
        dat_path, _ = QFileDialog.getSaveFileName(self, "保存数据", "", "数据文件 (*.dat)")
        if dat_path:
            with open(dat_path, "w", encoding="utf-8") as f:
                f.write("# s\t" + "\t".join(jt for jt, _, _ in self.last_plot_data) + "\n")
                s_arr = self.last_plot_data[0][1]
                y_arrs = [y for _, _, y in self.last_plot_data]
                for i in range(len(s_arr)):
                    row = [f"{s_arr[i]:.6f}"] + [f"{y[i]:.6f}" for y in y_arrs]
                    f.write("\t".join(row) + "\n")
        QMessageBox.information(self, "提示", "导出完成！")

    def show_help(self):
        dlg = HelpDialog(self)
        dlg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())