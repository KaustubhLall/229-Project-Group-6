import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

from holoviews.plotting.plotly.dash import to_dash
import holoviews as hv

from holoviews import opts
import hvplot.pandas
import panel as pn

hv.extension('plotly')
df = pd.read_csv("preprocess_data.csv")
df.head()


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


# newly added starts here
res = df.groupby(['Year', 'Genre']).NA_Sales.sum().unstack().hvplot.bar(stacked=True, rot=45) \
    .redim(value=hv.Dimension('value', label='Sales', range=(0, 500))) \
    .relabel('Sales(millions)')
# res.opts(tools=['hover'], legend_position='left', color_index='Variable', alpha=0.5, color=hv.Palette('Category20'),
#          width=800, height=400)


regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
regions_name = ['North America', 'Europe', 'Japan', 'Other Regions', 'Global']


def gen_sales_vs_year(groupby):
    method = 'sum'
    aggdict = dict(zip(regions, [method] * len(regions)))
    data = df.groupby([groupby, 'Year']).agg(aggdict)
    data = data.reset_index()
    data = data.melt(id_vars=[groupby, 'Year'], value_vars=regions, var_name='Region', value_name='Sales')
    r_dict = dict(zip(regions, regions_name))
    data.Region = data.Region.map(r_dict).fillna(data.Region)
    return data


groupby = 'Genre'
data = gen_sales_vs_year(groupby)
result = hv.Dataset(data=data, vdims=['Sales']).to(hv.Curve, 'Year', 'Sales', groupby=[groupby, 'Region'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

hv_comp = to_dash(app, [res, result])

# newly added ends here

app.layout = dbc.Container([
    # 1st row
    dbc.Row(
        dbc.Col(html.H1("interactive Video Games Sales Dashboard", className='text-center text-primary mb-4'), width=12)
    ),
    # 2nd row
    dbc.Row([
        # 1st col
        dbc.Col(dcc.Dropdown(
            id="dropdown",
            options=[{'label': 'Global_Sales', 'value': 'Global_Sales'},
                     {'label': 'NA_Sales', 'value': 'NA_Sales'},
                     {'label': 'EU_Sales', 'value': 'EU_Sales'},
                     {'label': 'JP_Sales', 'value': 'JP_Sales'}
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

    # 4nd row
    dbc.Row(
        dbc.Col(html.Div(hv_comp.children), width=12)  # newly added
    )

])


# app.layout = html.Div([
#     html.H1("interactive Video Games Sales Dashboard", className='text-center text-primary mb-4'),
#     dcc.Dropdown(
#         id="dropdown",
#         options=[{'label': 'Global_Sales', 'value': 'Global_Sales'},
#                  {'label': 'NA_Sales', 'value': 'NA_Sales'},
#                  {'label': 'EU_Sales', 'value': 'EU_Sales'},
#                  {'label': 'JP_Sales', 'value': 'JP_Sales'}
#                  ],
#         value='Global_Sales',
#         clearable=False,
#     ),
#     dcc.Dropdown(
#         id="dropdown_tab",
#         options=[{'label': 'Publisher', 'value': 'Publisher'},
#                  {'label': 'Genre', 'value': 'Genre'},
#                  {'label': 'Platform', 'value': 'Platform'}
#                  ],
#         value='Publisher',
#         clearable=False,
#     ),
#     dcc.Graph(id="bar-chart"),
#     html.H3("Corresponding Pie Chart based on above user inputs", className='text-center text-secondary'),
#     dcc.Graph(id="pie-chart"),
#     html.Div(hv_comp.children)  # newly added
# ])


@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value"), Input("dropdown_tab", "value")])
def update_bar_chart(sales, category):
    if sales == 'Global_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'Global_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'Global_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'NA_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'NA_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'NA_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'EU_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'EU_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'EU_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'JP_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'JP_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig
    elif sales == 'JP_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.bar(dff, x=category, y=sales)
        return fig


@app.callback(
    Output("pie-chart", "figure"),
    [Input("dropdown", "value"), Input("dropdown_tab", "value")])
def update_pie_chart(sales, category):
    if sales == 'Global_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'Global_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'Global_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'NA_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'NA_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'NA_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'EU_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'EU_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'EU_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'JP_Sales' and category == 'Publisher':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'JP_Sales' and category == 'Genre':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig
    elif sales == 'JP_Sales' and category == 'Platform':
        dff = sale_visualization(category, sales)
        fig = px.pie(dff, values=sales, names=category)
        return fig


if __name__ == '__main__':
    app.run_server()
