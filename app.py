import pandas as pd
import streamlit as st

# Caricamento del dataset da file CSV con gestione automatica di virgole/punti e virgola
try:
    try:
        df_paesi = pd.read_csv("paesi.csv", sep=";", encoding="utf-8-sig")
        if not any(col.strip().lower() == "nome" for col in df_paesi.columns):
            df_paesi = pd.read_csv("paesi.csv", sep=",", encoding="utf-8-sig")
    except Exception:
        df_paesi = pd.read_csv(
            "paesi.csv", sep=None, engine="python", encoding="utf-8-sig"
        )

    # Pulizia automatica dei nomi delle colonne (rimuove spazi ed converte in minuscolo)
    df_paesi.columns = df_paesi.columns.str.strip().str.lower()
    paesi = df_paesi.to_dict("records")
except FileNotFoundError:
    st.error(
        "⚠️ File 'paesi.csv' non trovato! Assicurati che sia nella stessa cartella di app.py."
    )
    st.stop()
except Exception as e:
    st.error(f"⚠️ Errore durante la lettura del file paesi.csv: {e}")
    st.stop()

st.title("✈️ Travel Matcher")
st.write("Imposta le tue preferenze per trovare la destinazione ideale.")

# Pannello Opzioni (Sidebar)
st.sidebar.header("I tuoi filtri")
clima_pref = st.sidebar.selectbox(
    "Clima preferito", ["Tutti", "Caldo", "Temperato", "Freddo"]
)
budget_pref = st.sidebar.slider("Budget max (1=Economico, 3=Lusso)", 1, 3, 2)
natura_pref = st.sidebar.slider("Importanza Natura (1-5)", 1, 5, 4)
citta_pref = st.sidebar.slider("Importanza Città/Cultura (1-5)", 1, 5, 3)
diff_pref = st.sidebar.slider("Difficoltà max tollerata (1-5)", 1, 5, 3)

# Calcolo Scoring
risultati = []
for p in paesi:
    score = 0
    # Lettura sicura dei campi dal CSV
    clima_p = str(p.get("clima", "")).strip()
    budget_p = int(p.get("budget", 3))
    natura_p = int(p.get("natura", 3))
    citta_p = int(p.get("citta", 3))
    diff_p = int(p.get("difficolta", 3))

    if clima_pref == "Tutti" or clima_p.lower() == clima_pref.lower():
        score += 30
    if budget_p <= budget_pref:
        score += 20
    score += (5 - abs(natura_p - natura_pref)) * 6
    score += (5 - abs(citta_p - citta_pref)) * 6
    if diff_p <= diff_pref:
        score += 10

    percentuale = min(100, int((score / 90) * 100))
    risultati.append((p, percentuale))

risultati.sort(key=lambda x: x[1], reverse=True)

# Risultati
if risultati:
    migliore, pct = risultati[0]
    st.subheader("La destinazione consigliata:")
    st.success(f"🏆 **{migliore['nome']}** - Compatibilità: {pct}%")
    st.write(
        f"- **Clima:** {migliore.get('clima', '')} | **Servizi:** {migliore.get('servizi', '')}"
    )
    st.write(
        f"- **Natura:** {migliore.get('natura', '')}/5 | **Città:** {migliore.get('citta', '')}/5 | **Budget:** {migliore.get('budget', '')}/3"
    )

    st.markdown("---")
    st.subheader("Alternative valide")
    for p, pct in risultati[1:3]:
        st.write(
            f"• **{p['nome']}** ({pct}% affinità) — Clima {p.get('clima', '')}, Difficoltà {p.get('difficolta', '')}/5"
        )