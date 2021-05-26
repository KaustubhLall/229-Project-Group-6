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

hv.extension('plotly')
df = pd.read_csv("preprocess_data.csv")
genres = df.Genre.unique().tolist()
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


# newly added starts here




def gen_sales_vs_year(groupby):
    method = 'sum'
    aggdict = dict(zip(regions, [method] * len(regions)))
    data = df.groupby([groupby, 'Year']).agg(aggdict)
    data = data.reset_index()
    data = data.melt(id_vars=[groupby, 'Year'], value_vars=regions, var_name='Region', value_name='Sales')
    
    data.Region = data.Region.map(sales2region).fillna(data.Region)
    return data

groupby =  'Genre'
line_data = gen_sales_vs_year(groupby).groupby(['Genre','Region'])




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])


app.layout = dbc.Container([
    # 1st row
    dbc.Row(
        dbc.Col(html.H1("Interactive Video Games Sales Dashboard", className='text-center text-primary mb-4'), width=12)
    ),
    # 2nd row
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
        ),width=6)  # newly added
    ),
    # 5th row
    dbc.Row(
        dbc.Col(html.Div(id="bar-pie-chart"), width=12)  # newly added
    ),
    
   dbc.Row(
        [dbc.Col(dcc.Dropdown(
            id="dropdown_line_genre",
       
            options = list(map(lambda x: {'label':x,'value':x},genres)),
            value='Action',
            clearable=False,
        ),width=6), 
         dbc.Col(dcc.Dropdown(
            id="dropdown_line_region",
            options=list(map(lambda x: {'label':x,'value':x},regions_name)),
            value='Global',
            clearable=False,
        ),width=6)] # newly added
    ),
    
    dbc.Row(
        dbc.Col(html.Div(id="line-chart"), width=12)  # newly added
    )
   
])



@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value"), Input("dropdown_tab", "value")])
def update_bar_chart(sales, category):
    dff = sale_visualization(category, sales)
    fig = px.bar(dff, x=category, y=sales)
    return fig


@app.callback(
    Output("pie-chart", "figure"),
    [Input("dropdown", "value"), Input("dropdown_tab", "value")])
def update_pie_chart(sales, category):   
    dff = sale_visualization(category, sales)
    fig = px.pie(dff, values=sales, names=category)
    return fig

@app.callback(
    Output("bar-pie-chart", "children"),
    Input("dropdown_bar", "value"))
def update_bar_pie_chart(region):   
    df_filtered = df.groupby(['Year', 'Genre'])[region].sum().unstack()
    value_max = int(df_filtered.sum(1).max()*1.1)
    hv_bar = df_filtered.hvplot.bar(stacked=True, rot=45)\
            .redim(value=hv.Dimension('value', label='Sales', range=(0, value_max)))\
            .relabel('Sales(millions)')
    hv_bar = to_dash(app, [hv_bar])
    return hv_bar.children

@app.callback(
    Output("line-chart", "children"),
    [Input("dropdown_line_genre", "value"), Input("dropdown_line_region", "value")])
def update_line_chart(genre,region):
    data = line_data.get_group((genre,region))
    hv_line = hv.Dataset(data=data,vdims=['Sales']).to(hv.Curve,'Year','Sales')
    hv_line = to_dash(app, [hv_line])
    return hv_line.children



if __name__ == '__main__':
    app.run_server(host='moss8')
    
