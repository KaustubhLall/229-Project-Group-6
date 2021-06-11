from utils import *


def test_remove_nan():
    df = pd.read_csv('preprocess_data.csv')
    df = remove_nan(df)
    assert isinstance(df, pd.DataFrame)
    assert not df.isnull().values.any()


def test_predict_sales():
    predict_sales('PC', 'Action', 'Nintendo', 'JP', "RF", "models_and_encoder")


def test_remove_outliers():
    import pandas as pd
    df = pd.read_csv('preprocess_data.csv')
    prices = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']

    for col in prices:
        df = remove_outliers(col, df)

    assert len(df.shape) == 2
    assert not df.isnull().values.any()
    # check if function works as expected
    for col in prices:
        assert not (all([not isclose(list(df[col])[x], 0) for x in range(len(df[col]))]))


def test_encode_df():
    df = pd.read_csv('preprocess_data.csv')
    df = encode_df(df)
    assert not df.isnull().values.any()
    assert any(['encoding' in c for c in list(df.columns)])


def test_sale_visualization():
    df = pd.read_csv("preprocess_data.csv")
    df.head()
    dff = sale_visualization('Publisher', 'Global_Sales')


def test_gen_sales_vs_year():
    gen_sales_vs_year('Genre')


def test_get_hv_line():
    get_hv_line('Action', 'Global')


def test_get_hv_bar_pie():
    get_hv_bar_pie('Global_Sales')


def test_get_feature_importance():
    get_feature_importance('Global_Sales')
