import os
import pickle
from math import isclose

from pandas import np
import pandas as pd


def encode_df(df):
    # Encode Genre
    genre_values = df['Genre'].value_counts().keys().tolist()
    genre_list = []
    for each in df.Genre:
        genre_list.append(genre_values.index(each))
    df["Genre_encoding"] = genre_list
    # Encode Publisher
    publisher_values = df['Publisher'].value_counts().keys().tolist()
    publisher_list = []
    for each in df.Publisher:
        publisher_list.append(publisher_values.index(each))
    df["Publisher Encoding"] = publisher_list
    # Encode Platform
    platform_values = df['Platform'].value_counts().keys().tolist()
    platform_list = []
    for each in df.Platform:
        platform_list.append(platform_values.index(each))
    df["Platform Encoding"] = platform_list
    publisher_values = df['Publisher'].value_counts().keys().tolist()
    return df


def remove_outliers(col_name, df):
    mean = df[col_name].mean()
    std = df[col_name].std()
    cut_off = std * 2
    lower, upper = mean - cut_off, mean + cut_off
    new_df = df[(df[col_name] < upper) & (df[col_name] > lower)]

    return new_df


def predict_sales(platform, genre, publisher, region, model_type, models_and_encoder_dir):
    """
    This function predicts the sales of a video game for the given platform,
    genre, publisher, and region. The type of model used in the prediction is also
    selected, and a directory containing these models and the label encoder must
    also be specified.

    Valid regions are 'na','eu','jp', and 'global' (not case-sensitive)
    Valid models are 'rf','knn','dt', and 'xg' (not case-sensitive)

    :param platform: Platform on which the game is published i.e. 'GBA','PS2',etc.
    :type platform: str
    :param genre: Genre of the game i.e. 'Sports','Action',etc.
    :type genre: str
    :param publisher: Company that publishes the game i.e. 'Nintendo','Sega',etc.
    :type publisher: str
    :param region: Region where sales will be predicted
    :type region: str
    :param models_and_encoder_dir: Directory containing the pickled files of the models and encoder
    :type models_and_encoder_dir: str

    :return sales: Predicted sales in millions of $
    :type sales: float
    """

    # Assert that all inputs are strings
    assert all(isinstance(param, str) for param in locals().values())

    # Assert that a valid region and model type have been given
    region = region.lower()
    regions = ['na', 'eu', 'jp', 'global']
    model_type = model_type.lower()
    models_d = {
        'rf' : 'rf_model.pkl',
        'knn': 'knn_model.pkl',
        'dt' : 'dt_model.pkl',
        'xg' : 'xg_model_'
        }  # xg requires a different model for each region
    assert region in regions
    assert model_type in models_d.keys()

    # Assert that the pickle files for the encoder and the feature values exist
    encoder_file = os.path.join(models_and_encoder_dir, "encoder.pkl")
    feature_values_file = os.path.join(models_and_encoder_dir, "feature_values.pkl")
    assert os.path.exists(encoder_file)
    assert os.path.exists(feature_values_file)

    # Load the label encoder and the possible values for the features
    with open(encoder_file, "rb") as f:
        le = pickle.load(f)

    with open(feature_values_file, "rb") as f:
        feature_values = pickle.load(f)

    # Assert that the given parameters are viable inputs to the models
    assert platform in feature_values['Platform']
    assert genre in feature_values['Genre']
    assert publisher in feature_values['Publisher']

    # Encode the labels for the new input
    x1 = le['Platform'].transform([platform])[0]
    x2 = le['Genre'].transform([genre])[0]
    x3 = le['Publisher'].transform([publisher])[0]
    x_new = np.array([x1, x2, x3]).reshape(-1, 3)

    if model_type == 'xg':
        # Load specific regional model for xg
        model_file = os.path.join(models_and_encoder_dir, models_d[model_type] + region + ".pkl")
        with open(model_file, "rb") as f:
            model = pickle.load(f)

        # Make sales prediction (only outputs sales for given region)
        preds = model.predict(x_new)
        sales = preds[0]

    else:
        # Load the specified model
        model_file = os.path.join(models_and_encoder_dir, models_d[model_type])
        with open(model_file, "rb") as f:
            model = pickle.load(f)

        # Make sales prediction (outputs all sales for NA,EU,JP, and Global)
        preds = model.predict(x_new)

        # Extract specific regional sales
        sales = preds[0][regions.index(region)]

    return sales


def remove_nan(df):
    return df.dropna()


def test_remove_nan():

    df = pd.read_csv('preprocess_data.csv')
    df = remove_nan(df)
    assert isinstance(df, pd.DataFrame)
    assert not df.isnull().values.any()


def test_predict_sales():
    predict_sales('GC', 'Action', 'Nintendo', 'JP', "RF", "models_and_encoder")


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
        assert not (any([isclose(df[col][x], 0) for x in range(len(df[col]))]))


def test_encode_df():
    pass
