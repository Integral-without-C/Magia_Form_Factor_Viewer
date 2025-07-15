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

if __name__ == "__main__":
    db = MagneticFormFactorDB(r"d:\\study\\Magnetic_Form_Factors\\data")
    print("所有有数据的元素：", db.get_elements())
    print("Fe的所有价态：", db.get_valences("Fe"))
    print("Fe2的所有j类型：", db.get_j_types("Fe", "2"))
    print("Fe2, j0的参数：", db.get_params("Fe", "2", "j0"))