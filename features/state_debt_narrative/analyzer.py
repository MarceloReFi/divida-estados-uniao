import pandas as pd

# Mapeamento de estados para regiões
REGIOES = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'SC', 'RS']
}

def get_latest_year_data(df):
    """Pega dados do ano mais recente"""
    latest_year = df['ANO'].max()
    return df[df['ANO'] == latest_year].copy()

def add_region_column(df):
    """Adiciona coluna de região baseado na UF"""
    def get_region(uf):
        for region, states in REGIOES.items():
            if uf in states:
                return region
        return 'Desconhecido'
    
    df['REGIAO'] = df['UF'].apply(get_region)
    return df

def calculate_regional_totals(df):
    """Calcula total de dívida por região"""
    regional = df.groupby('REGIAO')['VALOR'].sum().reset_index()
    regional = regional.sort_values('VALOR', ascending=False)
    
    total = regional['VALOR'].sum()
    regional['PERCENTUAL'] = (regional['VALOR'] / total * 100).round(2)
    
    return regional

def calculate_state_ranking(df):
    """Ranking de estados por dívida"""
    ranking = df.sort_values('VALOR', ascending=False).copy()
    total = ranking['VALOR'].sum()
    ranking['PERCENTUAL'] = (ranking['VALOR'] / total * 100).round(2)
    
    return ranking

def calculate_sp_sul_total(df):
    """Calcula % de SP + Sul"""
    sp_sul = df[df['UF'].isin(['SP', 'PR', 'SC', 'RS'])]['VALOR'].sum()
    total = df['VALOR'].sum()
    percentual = (sp_sul / total * 100).round(2)
    
    return {
        'valor': sp_sul,
        'total': total,
        'percentual': percentual
    }

def calculate_regional_evolution(df):
    """Calcula evolução da dívida por região ao longo dos anos"""
    df = add_region_column(df)
    evolution = df.groupby(['ANO', 'REGIAO'])['VALOR'].sum().reset_index()
    return evolution

def calculate_regional_growth(df):
    """Calcula crescimento percentual da dívida por região (2015 vs 2022)"""
    df = add_region_column(df)
    
    first_year = df['ANO'].min()
    last_year = df['ANO'].max()
    
    first = df[df['ANO'] == first_year].groupby('REGIAO')['VALOR'].sum()
    last = df[df['ANO'] == last_year].groupby('REGIAO')['VALOR'].sum()
    
    growth = ((last - first) / first * 100).reset_index()
    growth.columns = ['REGIAO', 'VARIACAO_PCT']
    growth = growth.sort_values('VARIACAO_PCT', ascending=False)
    
    return growth