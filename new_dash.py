import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

from holoviews.plotting.plotly.dash import to_dash
import holoviews as hv

import pandas as pd
import numpy as np
import pickle
import os
from collections import defaultdict

from holoviews import opts
import hvplot.pandas

from scipy import stats

hv.extension('plotly')
df = pd.read_csv("preprocess_data.csv")
genres = df.Genre.unique().tolist()
platforms = df.Platform.unique().tolist()
publishers = df.Publisher.unique().tolist()
regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
regions_name = ['North America', 'Europe', 'Japan', 'Other Regions', 'Global']
sales2region = dict(zip(regions, regions_name))


def sale_visualization(category, sale_region):
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


def predict_sales(platform, genre, publisher, region, model_type="XG", models_and_encoder_dir="models_and_encoder"):
    # Assert that all inputs are strings
    assert all(isinstance(param, str) for param in locals().values())

    # Assert that a valid region and model type have been given
    regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    model_type = model_type.lower()
    models_d = {
        'rf': 'rf_model.pkl',
        'knn': 'knn_model.pkl',
        'dt': 'dt_model.pkl',
        'xg': 'xg_model_'
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
    # assert platform in feature_values['Platform']
    # assert genre in feature_values['Genre']
    # assert publisher in feature_values['Publisher']

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


# newly added starts here


def gen_sales_vs_year(groupby):
    method = 'sum'
    aggdict = dict(zip(regions, [method] * len(regions)))
    data = df.groupby([groupby, 'Year']).agg(aggdict)
    data = data.reset_index()
    data = data.melt(id_vars=[groupby, 'Year'], value_vars=regions, var_name='Region', value_name='Sales')

    data.Region = data.Region.map(sales2region).fillna(data.Region)
    return data


groupby = 'Genre'
line_data = gen_sales_vs_year(groupby).groupby(['Genre', 'Region'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container([
    # 1st row
    dbc.Row(
        dbc.Col(html.H1("Interactive Video Games Sales Dashboard", className='text-center text-info mb-4'), width=12)
        ),
    dbc.Row(dcc.Markdown("""
                   **This web-app provides interactive dashboards for users to 
                   explore, analyze and predict the sales of video games.**
                   
                   """)),
    # 2nd row
    dbc.Tabs([dbc.Tab([
        dbc.Row(dbc.Col(html.H3("Overall distribution of video game sales", \
                                className='text-center text-secondary '), width=12)),
        dbc.Row(dcc.Markdown("""
             The following charts show the distribution of cumulative sales of video games in the past 30 years,
             in both bar chart and pie chart view.
         
            
            """)),
        dbc.Row([

            # 1st col
            dbc.Col(dcc.Dropdown(
                id="dropdown",
                options=[{'label': 'Global', 'value': 'Global_Sales'},
                         {'label': 'North America', 'value': 'NA_Sales'},
                         {'label': 'Europe', 'value': 'EU_Sales'},
                         {'label': 'Japan', 'value': 'JP_Sales'},
                         {'label': 'Others', 'value': 'Other_Sales'},
                         ],
                value='Global_Sales',

                clearable=False,
                ), width=6),
            # 2nd col
            dbc.Col(dcc.Dropdown(
                id="dropdown_tab",
                options=[{'label': 'Publisher', 'value': 'Publisher'},
                         {'label': 'Genre', 'value': 'Genre'},
                         {'label': 'Platform', 'value': 'Platform'}
                         ],
                value='Publisher',
                clearable=False,
                ), width=6),
            ]),
        # 3rd row
        dbc.Row([
            # 1st col
            dbc.Col(
                dcc.Graph(id="bar-chart"), width=6
                ),
            # 2nd col
            dbc.Col(
                dcc.Graph(id="pie-chart"), width=6
                )]
            ),
        dbc.Row(dbc.Col(html.H3("Sales VS Years with different region and Genre", \
                                className='text-center text-success '
                                          'mb-4'), width=12)),
        dbc.Row(dcc.Markdown("""
                 This line chart shows the sales v.s. the year of games' release, for the given region and genre.
                """)),
        # 5th row (swapped)
        dbc.Row(
            [dbc.Col(dcc.Dropdown(
                id="dropdown_line_genre",

                options=list(map(lambda x: {'label': x, 'value': x}, genres)),
                value='Action',
                clearable=False,
                ), width=6),
                dbc.Col(dcc.Dropdown(
                    id="dropdown_line_region",
                    options=list(map(lambda x: {'label': x, 'value': x}, regions_name)),
                    value='Global',
                    clearable=False,
                    ), width=6)]  # newly added
            ),

        dbc.Row(
            dbc.Col(html.Div(id="line-chart"), width=12)  # newly added
            ),
        dbc.Row(dbc.Col(html.H3("Bar Plots of Sales VS Years with different region ", className='text-center text-info '
                                                                                                'mb-4'), width=12)),
        dbc.Row(dcc.Markdown("""
                 This bar chart shows the sales (for different genres) at the selected region  v.s. the year of 
                 games' release. 
                """)),
        # 4th row
        dbc.Row(
            dbc.Col(dcc.Dropdown(
                id="dropdown_bar",
                options=[{'label': 'Global', 'value': 'Global_Sales'},
                         {'label': 'North America', 'value': 'NA_Sales'},
                         {'label': 'Europe', 'value': 'EU_Sales'},
                         {'label': 'Japan', 'value': 'JP_Sales'},
                         {'label': 'Other Regions', 'value': 'Other_Sales'},
                         ],
                value='Global_Sales',
                clearable=False,
                ), width=12)  # newly added  # modified the width
            ),
        # 5th row
        dbc.Row(
            dbc.Col(html.Div(id="bar-pie-chart"), width=12)  # newly added
            ),
        dbc.Row(),
        dbc.Row(dbc.Col(html.H3("Feature Importance analysis", className='text-center text-warning '
                                                                         'mb-4'), width=12)),
        dbc.Row(dcc.Markdown("""
                 The following two charts shows the correlation between categorical features and sales data at the 
                 selected region.
                 The left bar chart shows feature importance (F-statistic) and the right bar chart shows the 
                 corresponding p-value, under the evaluation of one-way ANOVA. 
                """)),
        # 4th row
        dbc.Row(
            dbc.Col(dcc.Dropdown(
                id="dropdown_anova",
                options=[{'label': 'Global', 'value': 'Global_Sales'},
                         {'label': 'North America', 'value': 'NA_Sales'},
                         {'label': 'Europe', 'value': 'EU_Sales'},
                         {'label': 'Japan', 'value': 'JP_Sales'},
                         {'label': 'Other Regions', 'value': 'Other_Sales'},
                         ],
                value='Global_Sales',
                clearable=False,
                ), width=12)  # newly added  # modified the width
            ),

        dbc.Row([
            # 1st col
            dbc.Col(
                dcc.Graph(id="bar-fet-importance"), width=6
                ),
            # 2nd col
            dbc.Col(
                dcc.Graph(id="bar-p-value"), width=6
                )]
            )
        ], label='Data Exploration'),
        dbc.Tab([dbc.Row(dbc.Col(html.H3("Prediction model", className='text-center text-info mb-4'), width=12)),
                 # 7th row prediction dropdown
                 dbc.Row(dcc.Markdown("""
                 By specifying the platform, genre, publisher, our model predicts the sales at the given region
                """)),
                 dbc.Row(
                     [dbc.Col(dcc.Dropdown(
                         id="pred-platform",
                         options=list(map(lambda x: {'label': x, 'value': x}, platforms)),
                         value='Console',

                         clearable=False,
                         ), width=3),
                         # 2nd col
                         dbc.Col(dcc.Dropdown(
                             id="pred-genre",
                             options=list(map(lambda x: {'label': x, 'value': x}, genres)),
                             value='Action',
                             clearable=False,
                             ), width=3),
                         # 3rd col
                         dbc.Col(dcc.Dropdown(
                             id="pred-publisher",
                             options=list(map(lambda x: {'label': x, 'value': x}, publishers)),
                             value='Nintendo',
                             clearable=False,
                             ), width=3),
                         # 4th col
                         dbc.Col(dcc.Dropdown(
                             id="pred-region",
                             options=[{'label': 'Global', 'value': 'Global_Sales'},
                                      {'label': 'North America', 'value': 'NA_Sales'},
                                      {'label': 'Europe', 'value': 'EU_Sales'},
                                      {'label': 'Japan', 'value': 'JP_Sales'},
                                      {'label': 'Others', 'value': 'Other_Sales'},
                                      ],
                             value='Global_Sales',
                             clearable=False,
                             ), width=3)]
                     ),

                 # 8th row returned text
                 dbc.Row(html.Div(id="pred-result", style={
                     'width': '75%', 'margin': 50, 'textAlign': 'center', 'display': 'inline-block'
                     }))], label='Data Prediction')])])


@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value"), Input("dropdown_tab", "value")])
def update_bar_chart(sales, category):
    dff = sale_visualization(category, sales)
    fig = px.bar(dff, x=category, y=sales, title='Sales(millions)')
    return fig


@app.callback(
    Output("pie-chart", "figure"),
    [Input("dropdown", "value"), Input("dropdown_tab", "value")])
def update_pie_chart(sales, category):
    dff = sale_visualization(category, sales)
    fig = px.pie(dff, values=sales, names=category)
    return fig


@app.callback(
    Output("line-chart", "children"),
    [Input("dropdown_line_genre", "value"), Input("dropdown_line_region", "value")])
def update_line_chart(genre, region):
    data = line_data.get_group((genre, region))
    hv_line = hv.Dataset(data=data, vdims=['Sales']).to(hv.Curve, 'Year', 'Sales').relabel('Sales(millions)')
    hv_line = to_dash(app, [hv_line])
    return hv_line.children


@app.callback(
    Output("bar-pie-chart", "children"),
    Input("dropdown_bar", "value"))
def update_bar_pie_chart(region):
    df_filtered = df.groupby(['Year', 'Genre'])[region].sum().unstack()
    value_max = int(df_filtered.sum(1).max() * 1.1)
    hv_bar = df_filtered.hvplot.bar(stacked=True, rot=45) \
        .redim(value=hv.Dimension('value', label='Sales', range=(0, value_max))) \
        .relabel('Sales(millions)')

    hv_bar = to_dash(app, [hv_bar])

    return hv_bar.children


@app.callback(
    Output("pred-result", "children"),
    [Input("pred-platform", "value"), Input("pred-genre", "value"), Input("pred-publisher", "value"),
     Input("pred-region", "value")])
def predicti9on_model(selected_platform, selected_genre, selected_publisher, selected_region):
    # platform, genre, publisher, region,
    pred_result = predict_sales(selected_platform, selected_genre, selected_publisher, selected_region)
    return "The predicted sales is: {} million USD".format(round(pred_result, 3))


@app.callback(
    [Output("bar-fet-importance", "figure"), Output("bar-p-value", "figure")],
    Input("dropdown_anova", "value"))
def fet_anova_bars(region):
    fets = ['Genre', 'Platform', 'Publisher']

    colors = ['blue', 'blueviolet', 'brown']
    result = {}
    for fet in fets:
        sales_grouped = df.groupby(by=fet)[region].agg(list).values.tolist()
        # result = {fet:(importance, p-value)}
        result[fet] = tuple(stats.f_oneway(*sales_grouped))

    fet_importance = list(map(lambda x: x[0], result.values()))
    p_value = list(map(lambda x: x[1], result.values()))
    fet_importance_fig = go.Figure(go.Bar(
        x=list(result.keys()),
        y=fet_importance,
        marker={'color': colors},
        ),
        layout=dict(title="Categorical Feature Importance")
        )
    p_value_fig = go.Figure([
        go.Bar(
            x=list(result.keys()),
            y=p_value,
            marker={'color': colors},
            ),
        go.Scatter(
            x=[list(result.keys())[0], list(result.keys())[-1]],
            y=[0.05, 0.05],
            mode='lines',
            line=dict(dash='dash'),
            text='0.05'
            ),
        ],
        layout=dict(
            title="Statistical Significance (p-value)",
            showlegend=False,
            yaxis=dict(type="log"),
            ),
        )
    return fet_importance_fig, p_value_fig


if __name__ == '__main__':
    #     app.run_server(host='moss8',debug=True)
    app.run_server(debug=True)
