import streamlit as st
import json
import time
import os
from fetch_and_save import fetch_latest_result, salvar_resultado_em_arquivo
from roleta_ia import atualizar_e_prever

HISTORICO_PATH = "historico_resultados.json"

st.set_page_config(page_title="Roleta IA", layout="wide")
st.title("🎯 Previsão Inteligente de Roleta")

# Inicializar histórico
if "historico" not in st.session_state:
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r") as f:
            st.session_state.historico = json.load(f)
    else:
        st.session_state.historico = []

# Mostrar log temporário
log_area = st.empty()

# Captura automática do novo resultado
resultado = fetch_latest_result()

if resultado:
    ultimo_timestamp = (
        st.session_state.historico[-1]["timestamp"]
        if st.session_state.historico else None
    )

    if resultado["timestamp"] != ultimo_timestamp:
        novo_resultado = {
            "number": resultado["number"],
            "color": resultado["color"],
            "timestamp": resultado["timestamp"],
            "lucky_numbers": resultado.get("lucky_numbers", [])
        }
        st.session_state.historico.append(novo_resultado)
        salvar_resultado_em_arquivo([novo_resultado])
        log_area.success(f"✅ Novo sorteio capturado: {novo_resultado}")
        st.experimental_rerun()
    else:
        log_area.info("🔍 Aguardando novo sorteio...")
        time.sleep(5)
        st.experimental_rerun()
else:
    log_area.warning("⚠️ Nenhum resultado retornado por fetch_latest_result()")

# Exibir últimos sorteios
st.subheader("Últimos Sorteios")
if st.session_state.historico:
    st.write([h["number"] for h in st.session_state.historico[-10:]])
else:
    st.write("Sem sorteios ainda.")

# Previsão baseada em IA
st.subheader("🔮 Previsão de Próximos 4 Números Mais Prováveis")
previsoes = atualizar_e_prever(st.session_state.historico)

if previsoes:
    st.success(f"Números Prováveis: {previsoes}")
else:
    st.warning("Aguardando pelo menos 20 sorteios válidos para iniciar previsões.")

# Mostrar histórico completo
with st.expander("📜 Ver histórico completo"):
    st.json(st.session_state.historico)
