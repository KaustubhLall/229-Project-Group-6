import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div([
    html.H1("interactive Video Games Sales Dashboard", className='text-center text-primary mb-4'),
    dcc.Dropdown(
        id="dropdown",
        options=[{'label': 'Global_Sales', 'value': 'Global_Sales'},
                 {'label': 'NA_Sales', 'value': 'NA_Sales'},
                 {'label': 'EU_Sales', 'value': 'EU_Sales'},
                 {'label': 'JP_Sales', 'value': 'JP_Sales'}
                 ],
        value='Global_Sales',
        clearable=False,
    ),
    dcc.Dropdown(
        id="dropdown_tab",
        options=[{'label': 'Publisher', 'value': 'Publisher'},
                 {'label': 'Genre', 'value': 'Genre'},
                 {'label': 'Platform', 'value': 'Platform'}
                 ],
        value='Publisher',
        clearable=False,
    ),
    dcc.Graph(id="bar-chart"),
    html.H3("Corresponding Pie Chart based on above user inputs", className='text-center text-secondary'),
    dcc.Graph(id="pie-chart"),
])


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
