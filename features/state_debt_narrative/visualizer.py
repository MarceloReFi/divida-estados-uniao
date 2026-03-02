import plotly.graph_objects as go
import plotly.express as px

def create_bar_chart(df, x_col, y_col, title):
    """Template reutilizável para gráfico de barras"""
    fig = go.Figure(data=[
        go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker_color='#1f77b4',
            text=df[y_col],
            texttemplate='R$ %{text:.2s}',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title='Dívida (R$)',
        height=500,
        showlegend=False
    )
    
    return fig

def create_pie_chart(df, names_col, values_col, title):
    """Template reutilizável para gráfico de pizza"""
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        hole=0.3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='label+percent',
        textfont_size=14
    )
    
    return fig

def create_state_ranking_chart(df_ranking, top_n=10):
    """Gráfico: Top N estados por dívida"""
    top_states = df_ranking.head(top_n)
    
    return create_bar_chart(
        top_states,
        'UF',
        'VALOR',
        f'Top {top_n} Estados por Dívida com a União'
    )

def create_regional_chart(df_regional):
    """Gráfico: Comparação por região"""
    return create_pie_chart(
        df_regional,
        'REGIAO',
        'VALOR',
        'Distribuição da Dívida por Região'
    )

def create_narrative_chart(sp_sul_stats):
    """Gráfico: SP + Sul vs Resto do Brasil"""
    import pandas as pd
    
    data = {
        'Categoria': ['SP + Sul', 'Resto do Brasil'],
        'Percentual': [
            sp_sul_stats['percentual'],
            100 - sp_sul_stats['percentual']
        ]
    }
    
    df = pd.DataFrame(data)
    
    fig = px.pie(
        df,
        names='Categoria',
        values='Percentual',
        title='SP + Sul vs Resto do Brasil',
        color='Categoria',
        color_discrete_map={
            'SP + Sul': '#e74c3c',
            'Resto do Brasil': '#95a5a6'
        },
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='label+percent',
        textfont_size=16
    )
    
    return fig

def create_regional_evolution_chart(df_evolution):
    """Gráfico: Evolução da dívida por região ao longo do tempo"""
    fig = px.line(
        df_evolution,
        x='ANO',
        y='VALOR',
        color='REGIAO',
        title='Evolução da Dívida por Região (2015-2022)',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Dívida (R$)',
        height=500,
        hovermode='x unified'
    )
    
fig.update_yaxes(tickformat='.2s')    
    return fig