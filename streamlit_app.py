import streamlit as st
from common.hello import say_hello

st.title("🏠 Dashboard Principal")
st.write("Bienvenue dans votre application Streamlit déployée sur Snowflake")
st.write(f"Message de bienvenue : {say_hello()}")

st.markdown("---")

# Navigation vers les pages
st.subheader("📊 Pages disponibles")

# Utiliser st.page_link pour une navigation correcte
st.page_link("pages/my_page.py", label="📊 Dashboard Ventes", icon="📈")

# Alternative avec bouton
if st.button("🚀 Accéder au Dashboard Ventes", type="primary"):
    st.switch_page("pages/my_page.py")

# Métriques rapides
st.subheader("📈 Aperçu rapide")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Status", "🟢 Actif", "En ligne")

with col2:
    st.metric("Dernière MAJ", "Aujourd'hui", "✅")

with col3:
    st.metric("Version", "1.0", "🚀")