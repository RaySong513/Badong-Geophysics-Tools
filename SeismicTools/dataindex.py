import os
import pandas as pd

data_folder = 'data'
output_file = 'dataoutput.txt'

all_data = pd.DataFrame()

file_index = 11.5
header_saved = False

for filename in sorted(os.listdir(data_folder)):
    if filename.endswith('.txt'):
        file_path = os.path.join(data_folder, filename)

        if header_saved:
            data = pd.read_csv(file_path, delim_whitespace=True, header=None, skiprows=1,
                               names=['Depth(ft)', 'S-velocity(ft/s)', 'P-velocity(ft/s)', 'Density(g/cc)', 'N'])
        else:
            data = pd.read_csv(file_path, delim_whitespace=True, header=0,
                               names=['Depth(ft)', 'S-velocity(ft/s)', 'P-velocity(ft/s)', 'Density(g/cc)', 'N'])
            header_saved = True

        data['index'] = file_index
        all_data = pd.concat([all_data, data], ignore_index=True)
        file_index += 4

# 将 index 列移到第一列
all_data = all_data[['index', 'Depth(ft)', 'S-velocity(ft/s)', 'P-velocity(ft/s)', 'Density(g/cc)', 'N']]

all_data.to_csv(output_file, sep='\t', index=False, header=True)
print(f"数据已成功拼接并保存到 {output_file}")
