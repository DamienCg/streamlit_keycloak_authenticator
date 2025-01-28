import streamlit as st
import os
import requests
import json
import urllib.parse
from reserved_page import reserved_page
from streamlit_cookies_manager import EncryptedCookieManager

# Carica configurazione Keycloak
with open("credential.json", "r") as f:
    keycloak_config = json.load(f)

# Inizializza il gestore dei cookie
cookies = EncryptedCookieManager(
    prefix="my_app_prefix/",  # Modifica con un prefisso unico per la tua app
    password=os.environ.get("COOKIES_PASSWORD", "My secret password"),
)
if not cookies.ready():
    st.stop()  # Attendi che il componente sia pronto

# Recupera lo stato della sessione
authenticated = cookies.get("authenticated", "False") == "True"
username_from_cookie = cookies.get("username", "")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = authenticated
if "username" not in st.session_state:
    st.session_state["username"] = username_from_cookie

# Funzione per ottenere il link di autenticazione
def get_authorization_url():
    params = {
        "client_id": keycloak_config["CLIENT_ID"],
        "response_type": "code",
        "scope": keycloak_config["SCOPE"],
        "redirect_uri": keycloak_config["REDIRECT_URI"],
    }
    return f"{keycloak_config['AUTHORIZE_URL']}?{urllib.parse.urlencode(params)}"

# Funzione per scambiare il codice con un token
def exchange_code_for_token(auth_code):
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": keycloak_config["REDIRECT_URI"],
        "client_id": keycloak_config["CLIENT_ID"],
        "client_secret": keycloak_config["CLIENT_SECRET"],
    }
    response = requests.post(keycloak_config["TOKEN_URL"], data=payload)
    response_data = response.json()
    if "access_token" in response_data:
        return response_data
    else:
        st.error("Errore durante l'autenticazione. Riprova.")
        st.stop()

# Login con Keycloak
if not st.session_state["authenticated"]:
    st.title("Login con Keycloak")
    st.markdown(f"[Accedi con Keycloak]({get_authorization_url()})")

    # Leggi il parametro 'code' dall'URL dopo il redirect
    query_params = st.query_params
    if "code" in query_params:
        auth_code = query_params["code"] # Ottieni il codice
        token_data = exchange_code_for_token(auth_code)
        st.session_state["authenticated"] = True
        st.session_state["username"] = "Utente Keycloak"  # Puoi modificare questo se Keycloak fornisce un nome utente
        cookies["authenticated"] = "True"
        cookies["username"] = st.session_state["username"]
        cookies.save()
        st.success(f"Benvenuto, {st.session_state['username']}!")
        st.rerun()
else:
    # Reindirizza alla pagina riservata
    reserved_page(st.session_state["username"])
