import os
import pickle
from math import isclose

import numpy as np
import pandas as pd
import holoviews as hv
from scipy.stats import stats

hv.extension('plotly')
df = pd.read_csv("preprocess_data.csv")
genres = df.Genre.unique().tolist()
platforms = df.Platform.unique().tolist()
publishers = df.Publisher.unique().tolist()
regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
regions_name = ['North America', 'Europe', 'Japan', 'Other Regions', 'Global']
sales2region = dict(zip(regions, regions_name))


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


def sale_visualization(category, sale_region):
    """
    This function takes the category and sale_region as inputs and returns a pandas DataFrame as output,
    the total amount
    of the category items from a specific sales_region will be stored and returned
    inputs:
    params: category, sale_region
    types: string, string
    output:
    returns: dff
    types: Pandas.DataFrame
    """
    assert category in ['Publisher', 'Genre', 'Platform']
    assert sale_region in ['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    assert isinstance(category, str)
    assert isinstance(sale_region, str)

    df = pd.read_csv("preprocess_data.csv")
    pub_values_list = df[category].value_counts().keys().tolist()
    publisher_avg_global_sales = []
    for i in pub_values_list:
        entries = df.loc[df[category] == i]
        publisher_avg_global_sales.append(entries[sale_region].sum() / len(entries))

    zipped = zip(pub_values_list, publisher_avg_global_sales)
    sorted_zipped = list(sorted(zipped, key=lambda x: x[1]))
    publisher_list = []
    pub_global_list = []
    for s in sorted_zipped:
        publisher_list.append(s[0])
        pub_global_list.append(s[1])
    dic = {}
    for s in sorted_zipped:
        dic[s[0]] = s[1]
    dff = pd.DataFrame(list(dic.items()), columns=[category, sale_region])

    return dff


def gen_sales_vs_year(groupby):
    """
      Aggregate sales for the given year and 'groupby', unpivot the columns 'NA_sales', 'EU_sales' and etc. to
      the column 'Region' with values 'North America' and 'Europe' and etc.

      :param groupby: the categorical variable to group
      :type groupby: str

      :return: the processed dataframe
      :rtype: pandas.DataFrame

    """

    assert groupby in ['Genre', 'Publisher', 'Platform']
    method = 'sum'
    aggdict = dict(zip(regions, [method] * len(regions)))
    data = df.groupby([groupby, 'Year']).agg(aggdict)
    data = data.reset_index()
    data = data.melt(id_vars=[groupby, 'Year'], value_vars=regions, var_name='Region', value_name='Sales')

    # map EU_Sales to Europe
    data.Region = data.Region.map(sales2region).fillna(data.Region)
    return data


def get_hv_line(genre, region):
    assert isinstance(genre, str)
    assert isinstance(region, str)
    assert region in regions_name
    assert genre in genres

    line_data = gen_sales_vs_year('Genre').groupby(['Genre', 'Region'])
    data = line_data.get_group((genre, region))
    hv_line = hv.Dataset(data=data, vdims=['Sales']).to(hv.Curve, 'Year', 'Sales').relabel('Sales(millions)')
    return hv_line


def get_hv_bar_pie(region):
    assert isinstance(region, str)
    assert region in regions

    df_filtered = df.groupby(['Year', 'Genre'])[region].sum().unstack()
    value_max = int(df_filtered.sum(1).max() * 1.1)
    hv_bar = df_filtered.hvplot.bar(stacked=True, rot=45) \
        .redim(value=hv.Dimension('value', label='Sales', range=(0, value_max))) \
        .relabel('Sales(millions)')


def get_feature_importance(region):
    assert isinstance(region, str)
    assert region in regions
    fets = ['Genre', 'Platform', 'Publisher']

    colors = ['blue', 'blueviolet', 'brown']
    result = {}
    for fet in fets:
        sales_grouped = df.groupby(by=fet)[region].agg(list).values.tolist()
        # result = {fet:(importance, p-value)}
        result[fet] = tuple(stats.f_oneway(*sales_grouped))
    return result
