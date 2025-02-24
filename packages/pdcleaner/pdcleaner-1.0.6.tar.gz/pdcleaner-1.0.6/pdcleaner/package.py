import pandas as pd
import numpy as np
from datetime import datetime
import re
from decimal import Decimal

class DataSet:

    def __init__(self):
        pass

    @classmethod
    def _remove_permil(cls,number_str:str):
        """
        删除数字中的千分号（可识别中文和英文逗号）
        并保留小数点，确保只移除正确的千分位分隔符
        """
        pattern = r'(\d+)[，,](?=\d{1,3}(?:\.\d+)?)'
        # 使用re.sub()进行替换，循环替换所有匹配项
        cleaned_number_str = re.sub(pattern, r'\1', number_str)
        return cleaned_number_str
    
    @classmethod
    def clean_data(cls, df, drop_cols=None, rename_cols=None, add_time=False,del_cols=True):
        """
        清洗数据的函数。

        参数:
        df (pd.DataFrame): 输入的数据框。
        drop_cols (list, optional): 需要删除的列名列表。默认为 None。
        rename_cols (dict, optional): 需要重命名的列名字典，键为旧列名，值为新列名。默认为 None。
        add_time (bool, optional): 是否添加数据写入时间列。默认为 False。
        del_cols (dict, optional): 是否删除完全为空的列。默认为 True。

        返回:
        pd.DataFrame: 清洗后的数据框。
        """
        # 检查 DataFrame 是否为空
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        # 删除空白行
        df = df.dropna(how='all')
        
        # 删除完全重复的行
        df = df.drop_duplicates()

        # 根据参数删除完全为空的列
        if del_cols:
            # # 方法1
            # non_nan_counts = df.notna().sum() # 找出所有列中非NaN值的数量
            # empty_cols = non_nan_counts[non_nan_counts == 0].index # 找出完全为空的列（即非NaN值数量为0的列）
            # df = df.drop(columns=empty_cols)

            # 方法2
            df = df.dropna(axis=1, how='all')
        
        # 新增功能：去掉列名中的首尾空格和首尾换行符
        # df.columns = df.columns.str.replace(r'^[\s\n\r]+|[\s\n\r]+$', '', regex=True)
        df.columns = [re.sub(r'^[\s\n\r]+|[\s\n\r]+$', '', col) for col in df.columns]
        
        # 移除字符串两端的多余空格、换行符、回车符和单引号
        # df = df.apply(lambda x: x.str.replace(r"^[\'\s\n\r]+|[\'\s\n\r]+$", "", regex=True) if x.dtype == "object" else x)
        df = df.apply(lambda x: x.astype(str).str.replace(r"^[\'\s\n\r]+|[\'\s\n\r]+$", "", regex=True) if x.dtype == "object" else x)
        
        # 移除字符串中的千分号及其后的数字
        # df = df.apply(lambda x: x.apply(lambda y: cls._remove_permil(y) if isinstance(y, str) else y) if x.dtype == "object" else x)
        df = df.apply(lambda x: x.apply(lambda y: cls._remove_permil(y) if isinstance(y, str) else y).where(pd.notna(x), x) if x.dtype == "object" else x)
        
        # 将百分比字符串转换为浮点数
        df = df.apply(lambda x: x.apply(
            lambda x: (
                float(Decimal(re.match(r'^\s*(-?\d+(\.\d+)?)\s*%\s*$', x.strip()).group(1)) / Decimal('100'))
                if isinstance(x, str) and re.match(r'^\s*(-?\d+(\.\d+)?)\s*%\s*$', x.strip())
                else x
            ) if isinstance(x, str) else x
        # ) if x.dtype == "object" else x)
        ).where(pd.notna(x), x) if x.dtype == "object" else x)
        
        # 将 '-' 和 NaN 替换成 None
        # df = df.apply(lambda x: [None if pd.isna(i) or i == '-' else i for i in x]) 
        # df = df.replace({np.nan: '', None: '', 'nan': '', 'NaN': '','-':''})
        df = df.replace({np.nan: None, 'nan': None, 'NaN': None,'-':None,'':None})
        
        # 根据参数删除存在的列
        if drop_cols is not None:
            # df = df.drop(columns=[col for col in drop_cols if col in df.columns])
            df = df.drop(columns=df.columns.intersection(drop_cols), axis=1) # 检查并删除存在的列

        # 根据参数修改存在的列的列名
        if rename_cols is not None:
            df = df.rename(columns=rename_cols)

        # 新增功能：如果不存在 '数据写入时间' 列且 add_timestamp 为 True，则增加一个列记录当前时间
        if add_time and '数据写入时间' not in df.columns:
            df['数据写入时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return df
