from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

#criando o gráfico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
fig2 = px.bar(df, x="ID Loja", y="Quantidade", color="Produto", barmode="group")

opcoes = list(df['ID Loja'].unique())
opcoes.append('Todas as Lojas')

opcoes2 = list(df['Produto'].unique())
opcoes2.append('Todos os Produtos')

app.layout = html.Div(
    children=[
    html.H1(
        children = '''
        Faturamento das lojas
        '''
        ),

    html.Div(html.H3(
    children='''
        Gráfico com o faturamento de todos os produtos separados por loja.
    '''
    )),


    html.Div(html.H5(
    children = '''
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
    ''')),

    dcc.Dropdown(opcoes, value='Todas as Lojas', id='lista_lojas'),

    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    ),

    dcc.Dropdown(opcoes2, value='Todos os Produtos', id='lista_produtos'),

    dcc.Graph(
        id='grafico_quantidade_produtos',
        figure = fig2
    )
])

@app.callback(
    Output('grafico_quantidade_vendas', 'figure'),
    Input('lista_lojas', 'value')
)
def update_value(value):
    if value == 'Todas as Lojas':
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada= df.loc[df['ID Loja']==value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

@app.callback(
    Output('grafico_quantidade_produtos', 'figure'),
    Input('lista_produtos', 'value')
)
def value_produtos(value):
    if value == 'Todos os Produtos':
        fig2 = px.bar(df, x="ID Loja", y="Quantidade", color="Produto", barmode="group")
    else:
        tabela_filtrada2 = df.loc[df['Produto']==value, :]
        fig2 = px.bar(tabela_filtrada2, x="ID Loja", y="Quantidade", color="Produto", barmode="group")
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)