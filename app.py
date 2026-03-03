import streamlit as st
import pandas as pd

st.markdown("""
<style>
.main-header {
    text-align: center;
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📊 Calculateur d'Empreinte Carbone</h1>
    <p>Analyse complète des émissions de CO₂ par constituant</p>
    <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 1rem;">École Nationale des Ingénieurs de Monastir</p>
    <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.5rem;">TPE combustion / Halima Bouajina , Nermine Dardouri , Arwa khemira , Rima Yeferni , Ons Selmi</p>
</div>
""", unsafe_allow_html=True)

# Nom du produit
produit = st.text_input("Nom du produit", placeholder="Ex: Smartphone, Voiture, etc.")

st.divider()

# Scope 1 - Émissions directes
with st.expander("🟦 Scope 1 – Émissions directes", expanded=True):
    st.write("**Émissions directes provenant de sources possédées ou contrôlées**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quantités")
        diesel_q = st.number_input("Diesel – quantité (L)", min_value=0.0, value=0.0)
        gaz_q = st.number_input("Gaz naturel – quantité (m³)", min_value=0.0, value=0.0)
        ess_q = st.number_input("Essence – quantité (L)", min_value=0.0, value=0.0)
    
    with col2:
        st.subheader("Facteurs d'émission")
        diesel_f = st.number_input("Diesel – facteur (kg CO₂/L)", min_value=0.0, value=2.68)
        gaz_f = st.number_input("Gaz naturel – facteur (kg CO₂/m³)", min_value=0.0, value=2.02)
        ess_f = st.number_input("Essence – facteur (kg CO₂/L)", min_value=0.0, value=2.31)
    
    # Calculs Scope 1
    diesel_e = diesel_q * diesel_f
    gaz_e = gaz_q * gaz_f
    ess_e = ess_q * ess_f
    
    scope1 = diesel_e + gaz_e + ess_e
    
    st.write("---")
    st.write("**Détail des émissions Scope 1 :**")
    st.write(f"• Diesel : {diesel_e:.2f} kg CO₂")
    st.write(f"• Gaz naturel : {gaz_e:.2f} kg CO₂")
    st.write(f"• Essence : {ess_e:.2f} kg CO₂")
    st.success(f"**Total Scope 1 : {scope1:.2f} kg CO₂**")

# Scope 2 - Électricité
with st.expander("🟨 Scope 2 – Électricité", expanded=True):
    st.write("**Émissions indirectes liées à la consommation d'électricité**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        kwh = st.number_input("Consommation électrique (kWh)", min_value=0.0, value=0.0)
    
    with col2:
        fact_elec = st.number_input("Facteur électricité (kg CO₂/kWh)", min_value=0.0, value=0.059)
    
    scope2 = kwh * fact_elec
    st.success(f"**Total Scope 2 : {scope2:.2f} kg CO₂**")

# Scope 3 - Autres émissions
with st.expander("🟧 Scope 3 – Autres émissions indirectes", expanded=True):
    st.write("**Émissions indirectes de la chaîne de valeur**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quantités")
        trans_q = st.number_input("Transport – quantité (km)", min_value=0.0, value=0.0)
        mat_q = st.number_input("Matières premières – quantité (kg)", min_value=0.0, value=0.0)
        dech_q = st.number_input("Déchets – quantité (kg)", min_value=0.0, value=0.0)
    
    with col2:
        st.subheader("Facteurs d'émission")
        trans_f = st.number_input("Transport – facteur (kg CO₂/km)", min_value=0.0, value=0.12)
        mat_f = st.number_input("Matières premières – facteur (kg CO₂/kg)", min_value=0.0, value=1.5)
        dech_f = st.number_input("Déchets – facteur (kg CO₂/kg)", min_value=0.0, value=0.8)
    
    # Calculs Scope 3
    trans_e = trans_q * trans_f
    mat_e = mat_q * mat_f
    dech_e = dech_q * dech_f
    
    scope3 = trans_e + mat_e + dech_e
    
    st.write("---")
    st.write("**Détail des émissions Scope 3 :**")
    st.write(f"• Transport : {trans_e:.2f} kg CO₂")
    st.write(f"• Matières premières : {mat_e:.2f} kg CO₂")
    st.write(f"• Déchets : {dech_e:.2f} kg CO₂")
    st.success(f"**Total Scope 3 : {scope3:.2f} kg CO₂**")

st.divider()

# Résumé et résultats
st.subheader("📊 Résumé des émissions")

if produit:
    st.write(f"**Produit analysé :** {produit}")
else:
    st.write("**Produit analysé :** Non spécifié")

# Tableau récapitulatif
data = {
    "Scope": ["Scope 1 - Émissions directes", "Scope 2 - Électricité", "Scope 3 - Autres émissions", "TOTAL"],
    "Émissions (kg CO₂)": [scope1, scope2, scope3, scope1 + scope2 + scope3],
    "Pourcentage (%)": [
        f"{(scope1/(scope1+scope2+scope3)*100):.1f}" if (scope1+scope2+scope3) > 0 else "0.0",
        f"{(scope2/(scope1+scope2+scope3)*100):.1f}" if (scope1+scope2+scope3) > 0 else "0.0",
        f"{(scope3/(scope1+scope2+scope3)*100):.1f}" if (scope1+scope2+scope3) > 0 else "0.0",
        "100.0"
    ]
}

df = pd.DataFrame(data)

st.table(df)

total = scope1 + scope2 + scope3

# Visualisation simple
st.write("---")
st.subheader("📈 Répartition des émissions")

if total > 0:
    # Création d'un graphique simple avec des barres
    chart_data = pd.DataFrame({
        'Scope': ['Scope 1', 'Scope 2', 'Scope 3'],
        'Émissions (kg CO₂)': [scope1, scope2, scope3]
    })
    st.bar_chart(chart_data.set_index('Scope'))

# Résultat final
st.write("---")
if total > 0:
    st.success(f"🎯 **Empreinte carbone totale : {total:.2f} kg CO₂**")
else:
    st.info("🎯 **Empreinte carbone totale : 0.00 kg CO₂**")

# Export Excel
st.write("---")
st.subheader("📥 Export des résultats")

# Préparation des données pour export
export_data = {
    "Produit": [produit] if produit else ["Non spécifié"],
    "Scope 1 - Émissions directes (kg CO₂)": [scope1],
    "Scope 2 - Électricité (kg CO₂)": [scope2],
    "Scope 3 - Autres émissions (kg CO₂)": [scope3],
    "Total (kg CO₂)": [total],
    "Date": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")]
}

df_export = pd.DataFrame(export_data)

# Bouton de téléchargement
st.download_button(
    label="📥 Télécharger le bilan carbone (CSV)",
    data=df_export.to_csv(index=False, sep=';', decimal=','),
    file_name=f"bilan_carbone_{produit.replace(' ', '_') if produit else 'produit'}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# Informations supplémentaires
st.write("---")
st.markdown("""
### 📚 Informations utiles
- **Scope 1** : Émissions directes (combustion, véhicules entreprise)
- **Scope 2** : Électricité consommée
- **Scope 3** : Transport, matières premières, déchets, etc.

### 🔧 Facteurs d'émission par défaut
- Diesel : 2.68 kg CO₂/L
- Gaz naturel : 2.02 kg CO₂/m³  
- Essence : 2.31 kg CO₂/L
- Électricité (France) : 0.059 kg CO₂/kWh
- Transport (route) : 0.12 kg CO₂/km
- Matières premières : 1.5 kg CO₂/kg (moyenne)
- Déchets : 0.8 kg CO₂/kg (moyenne)

*Vous pouvez modifier ces facteurs selon vos données spécifiques*
""")
