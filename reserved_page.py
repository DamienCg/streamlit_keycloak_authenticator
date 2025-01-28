def reserved_page(username):
    import streamlit as st

    # Sidebar con campi da compilare
    st.sidebar.title("Menu")
    st.sidebar.text("Sample1")

    # Contenuto principale della pagina riservata
    st.title("Pagina Riservata")
    st.write(f"Benvenuto nella pagina protetta, {username}!")
    st.write("Questa pagina è visibile solo agli utenti autenticati.")
    st.write("Puoi compilare i campi nella sidebar per inviare dati o altro.")