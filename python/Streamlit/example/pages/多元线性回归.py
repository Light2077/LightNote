import math
import time
import joblib

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from plot_helper import selectable_scatter_plot
from feature_engineering import (
    transform_columns,
    generate_feature_combinations,
    generate_three_feature_combinations,
)

st.header("多元线性回归建模")
st.subheader("文件上传")
uploaded_file = st.file_uploader("上传数据文件")

if uploaded_file is not None:
    fname = uploaded_file.name
    if fname.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    elif fname.endswith("xls") or fname.endswith("xlsx"):
        try:
            df = pd.read_excel(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_excel(uploaded_file)
    else:
        st.write("??")
    st.table(df.head())

    # 上传后
    st.subheader("参数配置")
    # 特征列默认除了最后一列
    cols = df.columns
    features = st.multiselect("选择特征列", cols, cols[:-1].tolist())
    n_features = len(features)
    # 标签列默认是最后一列
    # target = st.multiselect("标签列选择", cols, cols[-1:].tolist())
    target = st.selectbox(
        label="选择标签列(默认最后一列)", options=cols.tolist(), index=len(cols) - 1
    )

    # 数据集划分
    test_size = st.slider(
        "选择测试集比例（测试集的大小）", min_value=0.1, max_value=0.9, value=0.2, step=0.1
    )

    # 特征组合
    st.subheader("特征组合")

    feature_combines = {
        "构建平方特征": {
            "func": lambda df: transform_columns(df, "square", features),
            "num_new_features": n_features,
        },
        "构建立方特征": {
            "func": lambda df: transform_columns(df, "cube", features),
            "num_new_features": n_features,
        },
        "两特征相乘组合": {
            "func": lambda df: generate_feature_combinations(df, "multiply", features),
            "num_new_features": math.comb(n_features, 2),
        },
        "两特征相除组合": {
            "func": lambda df: generate_feature_combinations(df, "divide", features),
            "num_new_features": math.comb(n_features, 2) * 2,
        },
        "三特征相乘组合": {
            "func": lambda df: generate_three_feature_combinations(df, features),
            "num_new_features": math.comb(n_features, 3),
        },
    }

    combine_names = st.multiselect("选择特征组合方案", list(feature_combines.keys()))

    new_features = 0
    comb_funcs = []
    for name in combine_names:
        comb = feature_combines[name]
        new_features += comb["num_new_features"]
        comb_funcs.append(comb["func"])

    if new_features > 0:
        st.write(f"🚩预计新增特征数量: {new_features}")

    model = None
    model_file = st.file_uploader("上传模型文件(可选)", type=["joblib"])
    if model_file is not None:
        model = joblib.load(model_file)
        st.session_state["model"] = model
        st.write("模型已成功加载")

    st.subheader("建模")
    if len(features) > 0 and target and st.button("开始建模"):
        # 特征组合
        new_df = [df]

        use_features = list(features)
        st.write("正在进行特征组合")
        my_bar = st.progress(0)

        for i, func in enumerate(comb_funcs):
            progress_text = f"当前阶段: {combine_names[i]}"
            my_bar.progress((i + 1) / len(comb_funcs), text=progress_text)
            tdf = func(df)
            new_df.append(tdf)
            time.sleep(0.5)
            use_features.extend(list(tdf.columns))

        new_df = pd.concat(new_df, axis=1)

        X = new_df[use_features]
        y = new_df[target]
        st.write("建模数据预览")
        st.write("特征列")
        st.dataframe(X.head())
        st.write("预测目标列")
        st.dataframe(y.head())
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        st.write(f"训练集: {len(X_train)}条数据")
        st.write(f"测试集: {len(X_test)}条数据")
        # 模型训练
        if model is None:
            model = LinearRegression()
            model.fit(X_train, y_train)
            st.write("模型训练已完成")
        else:
            st.write("使用加载的模型进行预测和评估")

        # st.session_state["model"] = model

        # 模型预测
        st.subheader("模型预测")

        y_pred = model.predict(X_test)

        # st.write(y_pred.shape)
        # st.write(st.session_state["y_test"].shape)
        result = pd.DataFrame({"实际值": y_test.values.ravel(), "预测值": y_pred.ravel()})
        result["误差"] = (result["实际值"] - result["预测值"]).abs()
        result["误差百分比(%)"] = result["误差"] / result["实际值"].mean() * 100

        st.dataframe(result)
        # left_column, right_column = st.columns([1, 3])
        # left_column.write(result)
        # with right_column:
        #     predict_compare_plot(y_test.values.ravel(), y_pred.ravel())

        # 模型评估
        st.subheader("模型评估")
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        st.write(f"均方误差 (MSE): {mse:.4f}")
        st.write(f"平均绝对误差 (MAE): {mae:.4f}")
        st.write(f"R^2: {r2:.4f}")

        selectable_scatter_plot(new_df.loc[X_test.index])
        # # 模型保存
        # if st.button("保存模型"):
        #     joblib.dump(model, "model.joblib")
        #     st.write("模型已成功保存为 model.joblib")
