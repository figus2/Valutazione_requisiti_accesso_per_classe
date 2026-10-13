# 🎓 Valutatore Requisiti Accesso Docenti & Piano di Recupero CFU (UNISI)

Un'applicazione web interattiva sviluppata in **Python** e **Streamlit** per la verifica automatizzata dei requisiti curriculari d'accesso alle classi di concorso per l'insegnamento nella scuola secondaria di I e II grado e per i percorsi abilitanti ex **Art. 13 DPCM 23 agosto 2023**.

L'applicazione integra le più recenti riforme e tabelle ministeriali (**D.P.R. 19/2016**, **D.M. 259/2017**, **D.M. 255/2023**, **D.Lgs. 59/2017**), con un modulo dedicato al calcolo del piano di recupero dei crediti mancanti interfacciato con l'**Università degli Studi di Siena (UNISI)**.

---

## 🌟 Caratteristiche Principali

* **📝 Portfolio Unico Cumulativo**: Permette di accumulare ed analizzare l'intera carriera universitaria del candidato (Lauree Magistrali, Specialistiche, Vecchio Ordinamento, Lauree Triennali, Master, Dottorati e Corsi Singoli).
* **📄 Estrazione Automatica da PDF (OCR & Regex)**: Riconoscimento intelligente dei codici dei Settori Scientifico-Disciplinari (SSD, es. , , , ) e dei relativi CFU dai certificati di carriera in PDF, con tabella di convalida manuale prima dell'importazione.
* **⚡ Motore di Calcolo Data-Driven**: Algoritmo di backtracking per l'allocazione ottimale dei crediti alle sotto-soglie senza rischiare il *double-counting*. Gestisce in modo flessibile l'interpretazione ministeriale della dicitura **"e / o"** (D.M. 255/2023).
* **🎯 Piano di Recupero UNISI**: Calcolo puntuale dei debiti formativi con generazione di link dinamici per la ricerca degli insegnamenti sul **UNISI Course Catalogue (CINECA)** e collegamento diretto al **Manifesto degli Studi & Procedure**.
* **📚 Tabella A/1 & Equiparazioni DL-LS-LM**: Verifica dell'omogeneità degli esami del Vecchio Ordinamento (Tabella A/1) e tabella di corrispondenza legale tra i vecchi Diplomi di Laurea e le moderne Lauree Magistrali (D.I. 9 luglio 2009).
* **🧩 Modulo 24 CFU & DPCM 30/60 CFU**: Verifica dei 24 CFU/CFA (D.Lgs. 59/2017) negli ambiti antropo-psico-pedagogici e convalida per l'accesso ai percorsi abilitanti abbreviati da 30 CFU (Art. 13).
* **📄 Generazione Report PDF**: Esportazione ufficiale dell'esito della valutazione e del piano di recupero personalizzato in formato PDF (tramite ).

---

## 📁 Struttura del Repository



---

## 🏛️ Classi di Concorso Mappate (UNISI)

L'applicazione include il database multicriterio completo per le **19 classi di concorso** attive presso l'Università degli Studi di Siena:

1. **A-01**: Arte e immagine nella scuola secondaria di I e II grado (D.M. 255/2023 - ex A-01 ed ex A-17)
2. **A-11**: Discipline letterarie e latino nei licei
3. **A-12**: Discipline letterarie nell'istruzione secondaria di I e II grado (D.M. 255/2023 - ex A-12 ed ex A-22)
4. **A-13**: Discipline letterarie, latino e greco nel liceo classico
5. **A-18**: Filosofia e scienze umane
6. **A-19**: Filosofia e storia nei licei
7. **A-20**: Fisica
8. **A-26**: Matematica
9. **A-27**: Matematica e Fisica
10. **A-28**: Matematica e scienze nella scuola secondaria di I grado (132 CFU su 6 settori)
11. **A-41**: Scienze e tecnologie informatiche
12. **A-46**: Scienze giuridico-economiche
13. **A-47**: Scienze matematiche applicate
14. **A-50**: Scienze naturali, chimiche e biologiche
15. **AA22**: Lingue e culture straniere I e II grado (Francese)
16. **AB22**: Lingue e culture straniere I e II grado (Inglese)
17. **BA02**: Conversazione in lingua straniera (Francese)
18. **BB02**: Conversazione in lingua straniera (Inglese)
19. **B003**: Laboratorio di fisica

---

## 🚀 Guida all'Installazione ed Esecuzione

### 1. Esecuzione in Locale

Assicurati di avere **Python 3.10+** installato sul tuo computer, quindi:

1. Scarica i file nel tuo progetto.
2. Installa le dipendenze richieste:
   
3. Avvia l'applicazione Streamlit:
   

---

### 2. Deployment Gratuito su Streamlit Community Cloud

1. Carica i file di questo repository sul tuo account **GitHub**.
2. Accedi a Streamlit Community Cloud autenticandoti con GitHub.
3. Clicca su **"New app"**, seleziona il repository, imposta  come branch e  come file principale.
4. Clicca su **"Deploy!"**. L'applicazione installerà automaticamente tutte le librerie da  e sarà visibile online in circa 1 minuto.

---

## 📖 Riferimenti Normativi

* **D.P.R. 14 febbraio 2016, n. 19**: Regolamento recante disposizioni per la razionalizzazione ed accorpamento delle classi di concorso.
* **D.M. 9 maggio 2017, n. 259**: Revisione dei titoli di accesso alle classi di concorso.
* **D.M. 22 dicembre 2023, n. 255**: Modifiche e integrazioni alle tabelle di accesso alle classi di concorso della scuola secondaria.
* **D.Lgs. 13 aprile 2017, n. 59**: Riordino, adeguamento e semplificazione del sistema di formazione iniziale e di reclutamento dei docenti.
* **DPCM 23 agosto 2023**: Definizione del percorso universitario e accademico di formazione iniziale dei docenti delle scuole secondarie (incluso Art. 13 per seconde abilitazioni).
* **D.I. 9 luglio 2009**: Equiparazione tra i diplomi di laurea di vecchio ordinamento, lauree specialistiche e lauree magistrali ai fini della partecipazione ai concorsi pubblici.
