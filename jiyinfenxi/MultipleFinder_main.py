import os

input_data_file = '/Users/luozhaoyang/Desktop/jiyinfenxi/data/SJTUF13468.fsa'

resfinder_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/resfinder-master/src/resfinder/run_resfinder.py'
plasmidfinder_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/plasmidfinder/plasmidfinder.py'
virulencefinder_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/virulencefinder/src/virulencefinder/__main__.py'
mlst_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/mlst/mlst.py'

resfinder_output_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/test_resfinder'
plasmidfinder_output_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/test_plasmid'
virulencefinder_output_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/test_virulence'
mlst_output_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/test_mlst'

plasmidfinder_db_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/plasmidfinder_db'
virulencefinder_db_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/virulencefinder_db'
mlst_db_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/mlst_db'

mlst_temp_path = '/Users/luozhaoyang/Desktop/jiyinfenxi/test_mlst'
mlst_species = 'senterica'

required_vars = [
    ('resfinder_path', resfinder_path),
    ('input_data_file', input_data_file),
    ('resfinder_output_path', resfinder_output_path),
    ('plasmidfinder_path', plasmidfinder_path),
    ('plasmidfinder_db_path', plasmidfinder_db_path),
    ('virulencefinder_path', virulencefinder_path),
    ('virulencefinder_db_path', virulencefinder_db_path),
    ('virulencefinder_output_path', virulencefinder_output_path),
    ('mlst_path', mlst_path),
    ('mlst_output_path', mlst_output_path),
    ('mlst_temp_path', mlst_temp_path),
    ('mlst_db_path', mlst_db_path),
    ('mlst_species', mlst_species),
]

#校验参数非空
for var_name, var_value in required_vars:
    if not isinstance(var_value, str) or not var_value.strip():
        raise ValueError(f"参数校验失败: '{var_name}' 必须为非空字符串")

# 校验工具可执行路径
for tool_name, tool_path in [
    ('ResFinder', resfinder_path),
    ('PlasmidFinder', plasmidfinder_path),
    ('VirulenceFinder', virulencefinder_path),
    ('MLST', mlst_path)
]:
    if not os.path.isfile(tool_path):
        raise FileNotFoundError(f"工具路径校验失败: {tool_name} 路径 '{tool_path}' 不存在")

# 校验输入文件
if not os.path.isfile(input_data_file):
    raise FileNotFoundError(f"输入文件校验失败: '{input_data_file}' 不存在")

# 校验数据库目录
for db_name, db_path in [
    ('PlasmidFinder', plasmidfinder_db_path),
    ('VirulenceFinder', virulencefinder_db_path),
    ('MLST', mlst_db_path)
]:
    if not os.path.isdir(db_path):
        raise NotADirectoryError(f"数据库校验失败: {db_name} 数据库目录 '{db_path}' 不存在")

# 校验输出目录
for dir_name, dir_path in [
    ('ResFinder输出', resfinder_output_path),
    ('VirulenceFinder输出', virulencefinder_output_path),
    ('MLST输出', mlst_output_path),
    ('MLST临时', mlst_temp_path)
]:
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"输出目录校验失败: {dir_name} 目录 '{dir_path}' 不存在")

os.system('python3.10 ' + resfinder_path + ' -ifa ' + input_data_file + ' -o ' + resfinder_output_path + ' -acq')
os.system('python3.10 ' + plasmidfinder_path + ' -i ' + input_data_file + ' -o ' + plasmidfinder_output_path + ' -p ' + plasmidfinder_db_path)
os.system('python3.10 ' + virulencefinder_path + ' -ifa ' + input_data_file + ' -o ' + virulencefinder_output_path + ' -p ' + virulencefinder_db_path + ' -q')
os.system('python3.10 ' + mlst_path + ' -i ' + input_data_file + ' -o ' + mlst_output_path + ' -t ' + mlst_temp_path + ' -p ' + mlst_db_path + ' -s ' + mlst_species)

import pandas as pd
import json

with open(virulencefinder_output_path + '/data.json', 'r') as json_file:
    result = json.loads(json_file.read())
print(result['__main__']['results']['Escherichia coli']['virulence_ecoli'].keys())
final_results = result['__main__']['results']['Escherichia coli']['virulence_ecoli']
final_results_df = pd.DataFrame(final_results).transpose()
final_results_df.to_csv(virulencefinder_output_path + "/data.csv")
print(final_results_df)

with open(mlst_output_path + "/data.json") as json_file:
    result = json.loads(json_file.read())
final_results = result['mlst']['results']['allele_profile']
final_results_df = pd.DataFrame(final_results)
final_results_df.to_csv(mlst_output_path + "/data.csv")
print(final_results_df)