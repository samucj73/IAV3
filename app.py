import streamlit as st
import json
import time
import os
from fetch_and_save import fetch_latest_result, salvar_resultado_em_arquivo
from roleta_ia import atualizar_e_prever

HISTORICO_PATH = "historico_resultados.json"

st.set_page_config(page_title="Roleta IA", layout="wide")
st.title("🎯 Previsão Inteligente de Roleta")

if "historico" not in st.session_state:
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r") as f:
            st.session_state.historico = json.load(f)
    else:
        st.session_state.historico = []

# Atualização automática
placeholder = st.empty()
with placeholder.container():
    if st.button("⏳ Atualizar Sorteio"):
        resultado = fetch_latest_result()
        if resultado:
            if not st.session_state.historico or resultado["timestamp"] != st.session_state.historico[-1]["timestamp"]:
                st.session_state.historico.append({
                    "number": resultado["number"],
                    "color": resultado["color"],
                    "timestamp": resultado["timestamp"],
                    "lucky_numbers": resultado["lucky_numbers"]
                })
                salvar_resultado_em_arquivo([{
                    "number": resultado["number"],
                    "color": resultado["color"],
                    "timestamp": resultado["timestamp"],
                    "lucky_numbers": resultado["lucky_numbers"]
                }])

# Exibir últimos sorteios
st.subheader("Últimos Sorteios")
st.write([h["number"] for h in st.session_state.historico[-10:]])

# Previsão baseada em IA
st.subheader("🔮 Previsão de Próximos 4 Números Mais Prováveis")

previsoes = atualizar_e_prever(st.session_state.historico)
if previsoes:
    st.success(f"Números Prováveis: {previsoes}")
else:
    st.warning("Aguardando pelo menos 20 sorteios válidos para iniciar previsões.")

# Mostrar histórico completo opcional
with st.expander("📜 Ver histórico completo"):
    st.json(st.session_state.historico)
