import pandas as pd
from pdcleaner import DataSet

def test_clean_data():
    # 生成测试数据
    test_data = {
        'Column 1': [' 1,234 ', '-1,253.8', "增长369,666.0", "1,2,3", None, '-'],
        'Column 2': ['20%', '98.88%', "1，235.69%", "增长10%", '-10%', '50%'],
        'Column 3': ['  extra space  ', 'no change', "'single'", "multi\nline\rtext", '1,234.56', '25%'],
        '数据写入时间2': ['2023-10-01 12:34:56', '2023-10-02 13:45:56', '2023-10-03 14:56:57', '2023-10-04 15:07:58', '2023-10-05 16:18:59', '2023-10-06 17:29:60']
    }
    df = pd.DataFrame(test_data)

    # 调用 clean_data 函数
    cleaned_df = DataSet.clean_data(df, drop_cols=['数据写入时间2'], rename_cols={'Column 1': 'New Column 1'}, add_time=True)
    print(cleaned_df)

if __name__ == '__main__':
    test_clean_data()