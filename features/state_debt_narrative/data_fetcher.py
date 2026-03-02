import pandas as pd
import requests
import urllib3

# Desabilitar avisos de SSL (necessário para macOS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_state_debts():
    """
    Busca dados de dívida consolidada dos estados brasileiros
    Fonte: Tesouro Transparente - CSV Público
    """
    url = "https://www.tesourotransparente.gov.br/ckan/dataset/01aa8c02-4f77-4fcf-a850-ff8f13decb00/resource/de4a234e-1712-4a50-8d31-ae4748a5f715/download/Divida-Consolidada-dos-Estados---PAF.csv"
    
    try:
        print("📥 Baixando dados de dívida dos estados...")
        
        # Baixar com requests (ignora SSL para sites gov.br)
        response = requests.get(url, verify=False, timeout=30)
        response.raise_for_status()
        
        # Salvar temporariamente
        with open('/tmp/divida_estados.csv', 'wb') as f:
            f.write(response.content)
        
        # Ler com pandas
        df = pd.read_csv('/tmp/divida_estados.csv', sep=';', encoding='latin-1', decimal=',', thousands='.')
        
        print(f"✅ Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"Colunas: {df.columns.tolist()[:5]}...")  # Mostrar só as primeiras 5
        return df
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

    