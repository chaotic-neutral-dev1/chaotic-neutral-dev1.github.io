import streamlit as st
import requests

st.set_page_config(page_title="Chaos Contained Dashboard", layout="wide", page_icon="🗃️")

st.title("🗃️ Chaos Contained Dashboard")
st.caption("System automatycznej agregacji danych z lokalnej bazy wiedzy")

# Panel boczny
st.sidebar.header("⚙️ Operacje")
if st.sidebar.button("🔄 Odśwież zadania", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📩 Powiadomienia")
if st.sidebar.button("🚀 Wyślij raport przez Infomaniak", use_container_width=True):
    st.sidebar.info("Integracja SMTP zostanie wpięta w kolejnym kroku!")

# Adres URL naszego lokalnego API
BACKEND_URL = "http://127.0.0.1:8000/api/moje_zadania"

try:
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        todos_data = response.json()
        
        if todos_data:
            st.success(f"🤖 Wykryto {len(todos_data)} aktywnych linii zawierających marker #todo.")
            # Interaktywna tabela danych na froncie
            st.data_editor(
                todos_data, 
                use_container_width=True,
                column_config={
                    "file_name": "Plik źródłowy .md",
                    "task": "Treść zidentyfikowanego zadania",
                    "char_count": "Ilość znaków w zadaniu"
                }
            )
        else:
            st.info("Brak zadań z tagiem #todo w przeszukiwanym katalogu Obsidiana.")
            
except requests.exceptions.ConnectionError:
    st.error("🚨 Brak łączności! Frontend nie widzi działającego Backend-u. Uruchom uvicorn!")