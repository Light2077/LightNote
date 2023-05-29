import numpy as np
import pandas as pd


# 单列数据转换
def transform_columns(df, transformation, columns=None):
    transformations = {
        "square": np.square,
        "cube": lambda x: np.power(x, 3),
        "log2": np.log2,
        "ln": np.log,
        "sqrt": np.sqrt,
        "reciprocal": lambda x: 1 / x,
        "exp": np.exp,
        # "boxcox": lambda x: np.power(x, 3),
    }
    if columns is None:
        columns = df.column

    if transformation not in transformations:
        return

    f = transformations[transformation]
    transformed_df = pd.DataFrame()

    for col in columns:
        original_col = df[col]
        transformed_col = f(original_col)
        # 新列
        new_col_name = col + "_" + transformation
        transformed_df[new_col_name] = transformed_col

    return transformed_df


def generate_feature_combinations(df, transformation, columns=None):
    combined_data = pd.DataFrame()
    if columns is None:
        columns = df.column

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            feature1 = columns[i]
            feature2 = columns[j]

            if transformation == "multiply":
                # 相乘
                multiply_col = df[feature1] * df[feature2]
                multiply_col_name = feature1 + "_" + feature2 + "_multiply"
                combined_data[multiply_col_name] = multiply_col
            elif transformation == "divide":
                # 相除（按不同顺序生成两个新特征）
                divide_col1 = df[feature1] / df[feature2]
                divide_col2 = df[feature2] / df[feature1]
                divide_col_name1 = feature1 + "_" + feature2 + "_divide"
                divide_col_name2 = feature2 + "_" + feature1 + "_divide"
                combined_data[divide_col_name1] = divide_col1
                combined_data[divide_col_name2] = divide_col2

    return combined_data


def generate_three_feature_combinations(df, columns):
    combined_data = pd.DataFrame()

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            for k in range(j + 1, len(columns)):
                col1 = columns[i]
                col2 = columns[j]
                col3 = columns[k]

                # 三个特征相乘
                multiply_col = df[col1] * df[col2] * df[col3]
                multiply_col_name = col1 + "_" + col2 + "_" + col3 + "_multiply"
                combined_data[multiply_col_name] = multiply_col

    return combined_data
