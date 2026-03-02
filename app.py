import streamlit as st
from features.state_debt_narrative.data_fetcher import fetch_state_debts
from features.state_debt_narrative.analyzer import (
    get_latest_year_data,
    add_region_column,
    calculate_regional_totals,
    calculate_state_ranking,
    calculate_sp_sul_total,
    calculate_regional_evolution,
    calculate_regional_growth
)
from features.state_debt_narrative.visualizer import (
    create_state_ranking_chart,
    create_regional_chart,
    create_narrative_chart,
    create_regional_evolution_chart
)

# Configuração da página
st.set_page_config(
    page_title="Dívida dos Estados",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("💰 Dívida dos Estados com a União")
st.markdown("### Desmentindo narrativas com dados reais")

# Buscar dados
with st.spinner("Carregando dados..."):
    df = fetch_state_debts()
    
    if df is not None:
        # Processar dados
        df_latest = get_latest_year_data(df)
        df_latest = add_region_column(df_latest)
        
        year = df_latest['ANO'].iloc[0]
        
        # Calcular métricas
        regional_totals = calculate_regional_totals(df_latest)
        state_ranking = calculate_state_ranking(df_latest)
        sp_sul_stats = calculate_sp_sul_total(df_latest)
        
        # Métricas principais
        st.markdown(f"**Dados de {int(year)}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "SP + Sul",
                f"{sp_sul_stats['percentual']}%",
                "da dívida total"
            )
        
        with col2:
            sudeste_pct = regional_totals[regional_totals['REGIAO'] == 'Sudeste']['PERCENTUAL'].values[0]
            st.metric(
                "Sudeste",
                f"{sudeste_pct}%",
                "da dívida total"
            )
        
        with col3:
            norte_nordeste = regional_totals[regional_totals['REGIAO'].isin(['Norte', 'Nordeste'])]['PERCENTUAL'].sum()
            st.metric(
                "Norte + Nordeste",
                f"{norte_nordeste:.2f}%",
                "da dívida total"
            )
        
        # Evolução temporal
        st.markdown("---")
        st.markdown("### 📈 Evolução Temporal (2015-2022)")
        
        regional_evolution = calculate_regional_evolution(df)
        st.plotly_chart(
            create_regional_evolution_chart(regional_evolution),
            use_container_width=True
        )
        
        # Crescimento por região
        growth = calculate_regional_growth(df)
        
        st.markdown("#### Variação 2015-2022:")
        cols = st.columns(5)
        for idx, row in growth.iterrows():
            with cols[idx]:
                st.metric(
                    row['REGIAO'],
                    f"{row['VARIACAO_PCT']:+.1f}%"
                )
        
        # Gráficos
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_state_ranking_chart(state_ranking, 10),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_regional_chart(regional_totals),
                use_container_width=True
            )
        
        st.plotly_chart(
            create_narrative_chart(sp_sul_stats),
            use_container_width=True
        )
        
        # Conclusão
        st.markdown("---")
        st.markdown("""
        ### 🎯 Conclusão
        
        Os dados mostram que:
        - **Sudeste concentra 65% da dívida** (principalmente SP, RJ, MG)
        - **SP + Sul juntos = ~48%** da dívida total
        - **Norte + Nordeste = ~14%** da dívida total
        
        **Fonte:** Tesouro Nacional - Dívida Consolidada dos Estados (PAF)
        """)
    else:
        st.error("Erro ao carregar dados. Tente novamente.")