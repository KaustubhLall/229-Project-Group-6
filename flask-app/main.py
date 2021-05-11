import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dbm
import plotly.graph_objs as go
import re

from icecream import ic
from pandas import DataFrame as df
import pandas as pd

global colname
global metric1

def set_metric1(name):
    global metric1
    metric1 = name
    ic(metric1, 'set metric1')

def set_col(name):
    global colname
    colname = name
    ic(colname, 'set colname')


def load_data():
    """
    load actual video game data
    :return:
    """
    path = "../Cleaned Data.csv"
    data = pd.read_csv(path)
    return data


set_col('Genre')
# set_metric1('Global_Sales')

load_data()
# Set up the app
app = dash.Dash(__name__)
server = app.server

global product_df
global dict_products


def create_dict_list_of_product():
    global colname
    dictlist = []
    unique_list = product_df[colname].unique()
    for product_title in unique_list:
        dictlist.append({'value': product_title, 'label': product_title})
    ic(dictlist)
    return dictlist


def dict_product_list(dict_list):
    product_list = []
    for dict in dict_list:
        product_list.append(dict.get('value'))
    return product_list


product_df = load_data()
dict_products = create_dict_list_of_product()

app.layout = html.Div([
    html.Div([
        html.H1('Price Optimization Dashboard'),
        html.H2('Choose a product name'),
        dcc.Dropdown(
            id='product-dropdown',
            options=dict_products,
            multi=True,
            value=["Ben & Jerry's Cookie Dough Core Ice Cream", "Brewdog Punk IPA"]
            ),
        dcc.Graph(
            id='product-like-bar'
            )
        ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.H2('All product info'),
        html.Table(id='my-table'),
        html.P(''),
        ], style={'width': '55%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.H2('price graph'),
        dcc.Graph(id='product-trend-graph'),
        html.P('')
        ], style={'width': '100%', 'display': 'inline-block'}),
    html.Div(id='hidden-email-alert', style={'display': 'none'})
    ])


@app.callback(Output('product-like-bar', 'figure'), [Input('product-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    global colname
    product_df_filter = product_df[(product_df[colname].isin(selected_dropdown_value))]

    # Take the one with max datetime and remove duplicates for this bar chart
    product_df_filter = product_df_filter.sort_values('Year', ascending=False)
    # product_df_filter = product_df_filter.drop_duplicates(['index'])

    # Rating count check
    def format_rating(rating):
        return str(rating)
        # return re.sub('\((\d+)\)', r'\1', rating)
    global metric1
    product_df_filter[metric1] = product_df_filter[metric1].apply(format_rating)

    figure = {
        'data'  : [go.Bar(
            y=product_df_filter[colname],
            x=product_df_filter[metric1],
            orientation='h'
            )],
        'layout': go.Layout(
            title='Product Rating Trends',
            yaxis=dict(
                # autorange=True,
                automargin=True
                )
            )
        }
    return figure


# For the top topics graph
@app.callback(Output('product-trend-graph', 'figure'), [Input('product-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    global colname
    product_df_filter = product_df[(product_df[colname].isin(selected_dropdown_value))]

    data = timeline_top_product_filtered(product_df_filter, selected_dropdown_value)
    # Edit the layout
    layout = dict(title='Product Price Trends',
                  xaxis=dict(title='Year'),
                  yaxis=dict(title='Price'),
                  )
    figure = dict(data=data, layout=layout)
    return figure


def timeline_top_product_filtered(top_product_filtered_df, selected_dropdown_value):
    global colname
    # Make a timeline
    trace_list = []
    for value in selected_dropdown_value:
        top_product_value_df = top_product_filtered_df[top_product_filtered_df[colname] == value]
        trace = go.Scatter(
            y=top_product_value_df.Global_Sales,
            x=top_product_value_df.Year,
            name=value
            )
        trace_list.append(trace)
    return trace_list


# for the table
@app.callback(Output('my-table', 'children'), [Input('product-dropdown', 'value')])
def generate_table(selected_dropdown_value, max_rows=20):
    global colname
    product_df_filter = product_df[(product_df[colname].isin(selected_dropdown_value))]
    product_df_filter = product_df_filter.sort_values(['Year'], ascending=True)

    return [html.Tr([html.Th(col) for col in product_df_filter.columns])] + [html.Tr([
        html.Td(product_df_filter.iloc[i][col]) for col in product_df_filter.columns
        ]) for i in range(min(len(product_df_filter), max_rows))]


@app.callback(Output('hidden-email-alert', 'id'), [Input('product-dropdown', 'value')])
def send_alert(selected_dropdown_value):
    global colname
    # To send emails if the latest price is lower than original price
    for product_title in selected_dropdown_value:
        product_df_specific = product_df[product_df[colname] == product_title].sort_values('Year',
                                                                                           ascending=True)
        original_price = product_df_specific.Global_Sales.values[0]
        latest_price = product_df_specific.Global_Sales.values[-1]
        print(product_title, original_price, latest_price)
    return None


if __name__ == '__main__':
    app.run_server(debug=True)


