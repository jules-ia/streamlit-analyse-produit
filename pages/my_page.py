import streamlit as st
import pandas as pd
import altair as alt
from snowflake.snowpark.context import get_active_session

st.title("📊 Dashboard Ventes")

session = get_active_session()

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["📋 Données", "📈 Graphiques", "💰 Analyse Clients"])

with tab1:
    # Récupération d'une table
    query = "SELECT * FROM DHB_PROD.DNR.DN_VENTE LIMIT 100"
    df = session.sql(query).to_pandas()
    
    # Affichage
    st.subheader("Aperçu des données")
    st.dataframe(df)

with tab2:
    # Sélection d'une colonne pour analyse (ex: chiffre d'affaires par mois ou par rayon)
    colonnes_disponibles = df.columns.tolist()
    col_x = st.selectbox("Choisir la colonne pour l'axe X (catégorie)", colonnes_disponibles)
    col_y = st.selectbox("Choisir la colonne pour l'axe Y (valeur)", colonnes_disponibles)

    # Agrégation simple
    if pd.api.types.is_numeric_dtype(df[col_y]):
        chart_data = df.groupby(col_x)[col_y].sum().reset_index()
    
        # Création d'un graphique avec Altair
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(col_x, sort="-y"),
            y=col_y,
            tooltip=[col_x, col_y]
        ).properties(
            width=700,
            height=400,
            title=f"Répartition de {col_y} par {col_x}"
        )

        st.altair_chart(chart)
    else:
        st.warning("La colonne Y doit être numérique pour créer un graphique.")

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        montant_par_client = """select code_client, sum(montant_ttc_eur) from dhb_prod.dnr.dn_vente where date_ticket >= current_date - 60 group by code_client"""        
        df_montant_par_client = session.sql(montant_par_client).to_pandas()

        st.subheader("Montant par client")
        st.dataframe(df_montant_par_client)

    with col2:
        st.subheader("📈 Graphique interactif avec Altair")
        
        # Vérifier que les données sont disponibles
        if not df_montant_par_client.empty:
            # Renommer les colonnes pour plus de clarté
            df_montant_par_client.columns = ['code_client', 'montant_total']
            
            # Créer le graphique avec Altair
            chart = alt.Chart(df_montant_par_client.head(20)).mark_bar().encode(
                x=alt.X('code_client', sort="-y"),
                y='montant_total',
                tooltip=['code_client', 'montant_total']
            ).properties(
                width=600,
                height=400,
                title="Top 20 Clients par Montant (60 derniers jours)"
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # Afficher quelques statistiques
            st.metric("Total CA", f"{df_montant_par_client['montant_total'].sum():,.0f} €")
            st.metric("Moyenne par client", f"{df_montant_par_client['montant_total'].mean():,.0f} €")
            
        else:
            st.warning("Aucune donnée disponible pour la période sélectionnée")
