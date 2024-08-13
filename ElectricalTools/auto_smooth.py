import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os


def smooth_data_by_depth(data):
    # 按深度对数据进行分组并平滑处理
    grouped = data.groupby('depth')
    smoothed_data = []

    for depth, group in grouped:
        x_values = group['x'].values
        resistivity_values = group['resistivity'].values

        # 使用Savitzky-Golay滤波器进行平滑
        smoothed_resistivity = savgol_filter(resistivity_values, window_length=5, polyorder=2)

        smoothed_group = pd.DataFrame({
            'x': x_values,
            'depth': [depth] * len(x_values),
            'resistivity': smoothed_resistivity
        })
        smoothed_data.append(smoothed_group)

    return pd.concat(smoothed_data)


def main():
    Tk().withdraw()
    file_path = askopenfilename(filetypes=[("DAT files", "*.dat")])
    if not file_path:
        print("没有选择文件。")
        return

    # 读取文件的前6行数据
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        header = [next(file) for _ in range(6)]

    # 读取数据文件，从第7行开始，每行有三个数据
    data = pd.read_csv(file_path, skiprows=6, delim_whitespace=True, header=None, names=['x', 'depth', 'resistivity'],
                       encoding='ISO-8859-1')

    smoothed_data = smooth_data_by_depth(data)

    new_file_path = os.path.splitext(file_path)[0] + "_autosmooth.dat"
    with open(new_file_path, 'w', encoding='ISO-8859-1') as file:
        # 写入前6行的header
        file.writelines(header)
        # 写入平滑后的数据
        for _, row in smoothed_data.iterrows():
            line = f"{row['x']} {row['depth']} {row['resistivity']}\n"
            file.write(line)

    print(f"平滑处理后的数据已保存到: {new_file_path}")


if __name__ == "__main__":
    main()
