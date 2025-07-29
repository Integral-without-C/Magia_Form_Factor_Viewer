import os
import re
import glob

class MagneticFormFactorDB:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data = {}  # {元素: {价态: {j类型: 参数dict}}}
        self.j_types = {}  # {j类型: 文件首行描述}
        self._parse_all_tables()

    def _parse_all_tables(self):
        table_files = glob.glob(os.path.join(self.data_dir, "Table*.txt"))
        for file in table_files:
            with open(file, encoding='utf-8') as f:
                lines = f.readlines()
            if not lines or len(lines) < 2:
                continue
            # 识别j类型
            header = lines[0].strip()
            j_match = re.search(r'<(j\d)>', header)
            if not j_match:
                continue
            j_type = j_match.group(1)
            # 识别参数列
            columns = [col.strip() for col in lines[1].split('\t') if col.strip()]
            # 逐行解析
            for line in lines[2:]:
                if not line.strip():
                    continue
                parts = [p.strip() for p in line.split('\t')]
                if len(parts) < 8:
                    continue
                ion = parts[0]
                m = re.match(r"([A-Za-z]+)(\d+)", ion)
                if not m:
                    continue
                elem, valence = m.group(1), m.group(2)
                params = dict(zip(columns[1:], map(float, parts[1:])))
                self.data.setdefault(elem, {}).setdefault(valence, {})[j_type] = params
                self.j_types[j_type] = header

    def get_elements(self):
        return sorted(self.data.keys())

    def get_valences(self, elem):
        return sorted(self.data.get(elem, {}).keys(), key=int)

    def get_j_types(self, elem, valence):
        return sorted(self.data.get(elem, {}).get(valence, {}).keys())

    def get_params(self, elem, valence, j_type):
        return self.data.get(elem, {}).get(valence, {}).get(j_type, None)

    def get_j_type_desc(self, j_type):
        return self.j_types.get(j_type, "")

# 新增 X 射线形状因子数据库
class XRayFormFactorDB:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data = {}  # {元素: {'method': str, 'points': [(x, y)]}}
        self._parse_all_tables()

    def _parse_all_tables(self):
        table_files = glob.glob(os.path.join(self.data_dir, "Table_*.txt"))
        for file in table_files:
            with open(file, encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            if len(lines) < 4:
                continue
            # 第一行：元素名（首列为"Element"，需跳过）
            header = lines[0].split('\t')
            elements = [e.strip() for e in header[1:] if e.strip()]
            # 第二行：原子序数（首列为"Z"，需跳过）
            # 第三行：method（首列为"Method"，需跳过）
            method_line = lines[2].split('\t')
            methods = [m.strip() for m in method_line[1:len(elements)+1]]
            # 数据区
            for idx, elem in enumerate(elements):
                points = []
                for line in lines[3:]:
                    parts = line.split('\t')
                    if len(parts) < idx + 2:
                        continue
                    x_str = parts[0].strip()
                    y_str = parts[idx + 1].strip()
                    if not x_str or not y_str:
                        continue
                    try:
                        x = float(x_str)
                        y = float(y_str)
                        points.append((x, y))
                    except ValueError:
                        continue
                if points:
                    self.data[elem] = {'method': methods[idx], 'points': points}

    def has_data(self, elem):
        return elem in self.data

    def get_method(self, elem):
        return self.data.get(elem, {}).get('method', '')

    def get_points(self, elem):
        return self.data.get(elem, {}).get('points', [])

    def get_all_elements(self):
        return set(self.data.keys())

#主程序不会运行下述代码，仅作为测试用
#注意，该路径不会加载入主程序中，请确保主程序中的路径也修改正确
if __name__ == "__main__":
    db = MagneticFormFactorDB(r"D:\\study\\Program\\XRD_Form_Factors\\Magnetic_Form_factor_data")
    print("所有有数据的元素：", db.get_elements())
    print("Fe的所有价态：", db.get_valences("Fe"))
    print("Fe2的所有j类型：", db.get_j_types("Fe", "2"))
    print("Fe2, j0的参数：", db.get_params("Fe", "2", "j0"))

    xdb = XRayFormFactorDB(r"D:\\study\\Program\\XRD_Form_Factors\\Xray_scatter_data")
    print("X射线有数据的元素：", xdb.get_all_elements())
    print("H的method：", xdb.get_method("H"))
    print("H的数据点：", xdb.get_points("H"))