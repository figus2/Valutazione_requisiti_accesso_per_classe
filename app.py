import streamlit as st
import pandas as pd
import json
import os
import re

# =====================================================================
# CONFIGURAZIONE INIZIALE DELLA PAGINA (PRIMO COMANDO STREAMLIT)
# =====================================================================
st.set_page_config(
    page_title="Valutatore Requisiti Docenti, PDF OCR & UNISI Recovery",
    page_icon="🎓",
    layout="wide"
)

# =====================================================================
# 1. DATABASE EMBEDDED DELLE CLASSI DI CONCORSO (19 CLASSI UNISI & RIFORME)
# =====================================================================
@st.cache_data
def load_rules():
    possible_paths = [
        "rules_db.json",
        "../rules_db.json",
        "/workspace/artifacts/rules_db.json",
        "/workspace/scratch/rules_db.json"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    # Fallback embedded completo
    return {
        "A-01": {
            "class_name": "Arte e immagine nella scuola secondaria di I e II grado (DM 255/2023 - ex A-01 e ex A-17)",
            "degrees": ["LM-4", "LM-89", "LS-4", "LS-95", "LMR-02", "LM-3", "LM-12", "DA-Pittura", "DA-Scultura"],
            "total_cfu_required": 48,
            "valid_ssds": ["L-ART/01", "L-ART/02", "L-ART/03", "L-ART/04", "ICAR/17", "ICAR/18", "ICAR/19", "M-FIL/04"],
            "sub_conditions": [
                {"name": "Sotto-soglia 1: Estetica o Arte Contemporanea", "min_cfu": 12, "valid_ssds": ["L-ART/03", "M-FIL/04"]},
                {"name": "Sotto-soglia 2: Disegno o Museologia/Restauro", "min_cfu": 12, "valid_ssds": ["ICAR/17", "L-ART/04"]},
                {"name": "Sotto-soglia 3: Storia dell'Arte Medievale e Moderna", "min_cfu": 12, "valid_ssds": ["L-ART/01", "L-ART/02"]},
                {"name": "Sotto-soglia 4: Discipline Grafiche e Storico-Artistiche", "min_cfu": 12, "valid_ssds": ["L-ART/01", "L-ART/02", "L-ART/04"]}
            ]
        },
        "A-11": {
            "class_name": "Discipline letterarie e latino nei licei",
            "degrees": ["LM-1", "LM-2", "LM-5", "LM-10", "LM-11", "LM-14", "LM-15", "LM-39", "LM-43", "LM-45", "LM-80", "LM-84", "LM-89"],
            "total_cfu_required": 96,
            "valid_ssds": ["L-FIL-LET/04", "L-FIL-LET/10", "L-FIL-LET/12", "L-LIN/01", "M-GGR/01", "L-ANT/02", "L-ANT/03", "M-STO/01", "M-STO/02", "M-STO/04"],
            "sub_conditions": [
                {"name": "Lingua e Letteratura Latina (24 CFU)", "min_cfu": 24, "valid_ssds": ["L-FIL-LET/04"]},
                {"name": "Letteratura Italiana (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-FIL-LET/10"]},
                {"name": "Linguistica Italiana (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-FIL-LET/12"]},
                {"name": "Glottologia e Linguistica Generale (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-LIN/01"]},
                {"name": "Geografia (12 CFU)", "min_cfu": 12, "valid_ssds": ["M-GGR/01"]},
                {"name": "Storia Antica (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-ANT/02", "L-ANT/03"]},
                {"name": "Storia Medievale / Moderna / Contemporanea (12 CFU)", "min_cfu": 12, "valid_ssds": ["M-STO/01", "M-STO/02", "M-STO/04"]}
            ]
        },
        "A-12": {
            "class_name": "Discipline letterarie I e II grado (D.M. 255/2023 - Unificata ex A-12 e ex A-22)",
            "degrees": ["LM-1", "LM-2", "LM-5", "LM-10", "LM-11", "LM-14", "LM-15", "LM-39", "LM-43", "LM-45", "LM-65", "LM-80", "LM-84", "LM-89"],
            "total_cfu_required": 84,
            "valid_ssds": ["L-FIL-LET/04", "L-FIL-LET/10", "L-FIL-LET/12", "L-LIN/01", "M-GGR/01", "L-ANT/02", "L-ANT/03", "M-STO/01", "M-STO/02", "M-STO/04"],
            "sub_conditions": [
                {"name": "Lingua e Letteratura Latina (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-FIL-LET/04"]},
                {"name": "Letteratura Italiana (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-FIL-LET/10"]},
                {"name": "Linguistica Italiana (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-FIL-LET/12"]},
                {"name": "Glottologia e Linguistica Generale (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-LIN/01"]},
                {"name": "Geografia (12 CFU)", "min_cfu": 12, "valid_ssds": ["M-GGR/01"]},
                {"name": "Storia (24 CFU in L-ANT o M-STO)", "min_cfu": 24, "valid_ssds": ["L-ANT/02", "L-ANT/03", "M-STO/01", "M-STO/02", "M-STO/04"]}
            ]
        },
        "A-13": {
            "class_name": "Discipline letterarie, latino e greco nel liceo classico",
            "degrees": ["LM-1", "LM-2", "LM-5", "LM-10", "LM-11", "LM-14", "LM-15", "LM-39", "LM-43", "LM-45", "LM-84", "LM-89"],
            "total_cfu_required": 108,
            "valid_ssds": ["L-FIL-LET/02", "L-FIL-LET/04", "L-FIL-LET/10", "L-FIL-LET/12", "L-LIN/01", "M-GGR/01", "L-ANT/02", "L-ANT/03"],
            "sub_conditions": [
                {"name": "Lingua e Letteratura Greca (24 CFU)", "min_cfu": 24, "valid_ssds": ["L-FIL-LET/02"]},
                {"name": "Lingua e Letteratura Latina (24 CFU)", "min_cfu": 24, "valid_ssds": ["L-FIL-LET/04"]},
                {"name": "Letteratura Italiana (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-FIL-LET/10"]},
                {"name": "Linguistica Italiana (6 CFU)", "min_cfu": 6, "valid_ssds": ["L-FIL-LET/12"]},
                {"name": "Glottologia e Linguistica Generale (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-LIN/01"]},
                {"name": "Geografia (6 CFU)", "min_cfu": 6, "valid_ssds": ["M-GGR/01"]},
                {"name": "Storia Greca e Romana (24 CFU)", "min_cfu": 24, "valid_ssds": ["L-ANT/02", "L-ANT/03"]}
            ]
        },
        "A-18": {
            "class_name": "Filosofia e scienze umane",
            "degrees": ["LM-1", "LM-50", "LM-51", "LM-57", "LM-59", "LM-62", "LM-64", "LM-78", "LM-85", "LM-87", "LM-88", "LM-92", "LM-93"],
            "total_cfu_required": 96,
            "valid_ssds": [
                "M-FIL/01", "M-FIL/02", "M-FIL/03", "M-FIL/04", "M-FIL/05", "M-FIL/06", "M-FIL/07", "M-FIL/08", "M-STO/05",
                "M-PED/01", "M-PED/02", "M-PED/03", "M-PED/04",
                "M-PSI/01", "M-PSI/02", "M-PSI/03", "M-PSI/04", "M-PSI/05", "M-PSI/06", "M-PSI/07", "M-PSI/08",
                "SPS/07", "SPS/08", "SPS/09", "SPS/11", "SPS/12", "M-DEA/01"
            ],
            "sub_conditions": [
                {"name": "Filosofia (24 CFU)", "min_cfu": 24, "valid_ssds": ["M-FIL/01", "M-FIL/02", "M-FIL/03", "M-FIL/04", "M-FIL/06", "M-FIL/07", "M-FIL/08", "M-STO/05"]},
                {"name": "Pedagogia (24 CFU)", "min_cfu": 24, "valid_ssds": ["M-PED/01", "M-PED/02", "M-PED/03", "M-PED/04"]},
                {"name": "Psicologia (24 CFU)", "min_cfu": 24, "valid_ssds": ["M-PSI/01", "M-PSI/02", "M-PSI/03", "M-PSI/04", "M-PSI/05", "M-PSI/06", "M-PSI/07", "M-PSI/08"]},
                {"name": "Sociologia / Antropologia (24 CFU)", "min_cfu": 24, "valid_ssds": ["SPS/07", "SPS/08", "SPS/09", "SPS/11", "SPS/12", "M-DEA/01"]}
            ]
        },
        "A-19": {
            "class_name": "Filosofia e storia nei licei",
            "degrees": ["LM-1", "LM-50", "LM-57", "LM-64", "LM-78", "LM-84", "LM-85"],
            "total_cfu_required": 60,
            "valid_ssds": ["M-FIL/01", "M-FIL/02", "M-FIL/03", "M-FIL/04", "M-FIL/05", "M-FIL/06", "M-FIL/07", "M-FIL/08", "M-STO/01", "M-STO/02", "M-STO/04", "L-ANT/02", "L-ANT/03"],
            "sub_conditions": [
                {"name": "Discipline Filosofiche (24 CFU)", "min_cfu": 24, "valid_ssds": ["M-FIL/01", "M-FIL/02", "M-FIL/03", "M-FIL/04", "M-FIL/05", "M-FIL/06", "M-FIL/07", "M-FIL/08"]},
                {"name": "Discipline Storiche (24 CFU)", "min_cfu": 24, "valid_ssds": ["M-STO/01", "M-STO/02", "M-STO/04", "L-ANT/02", "L-ANT/03"]}
            ]
        },
        "A-20": {
            "class_name": "Fisica",
            "degrees": ["LM-17", "LM-20", "LM-21", "LM-22", "LM-23", "LM-24", "LM-25", "LM-26", "LM-27", "LM-28", "LM-29", "LM-30", "LM-31", "LM-32", "LM-33", "LM-34", "LM-35", "LM-40", "LM-44", "LM-53", "LM-58", "LM-72", "LM-79"],
            "total_cfu_required": 30,
            "valid_ssds": ["FIS/01", "FIS/02", "FIS/03", "FIS/04", "FIS/05", "FIS/06", "FIS/07", "FIS/08"],
            "sub_conditions": [
                {"name": "Fisica Sperimentale (6 CFU)", "min_cfu": 6, "valid_ssds": ["FIS/01"]}
            ]
        },
        "A-26": {
            "class_name": "Matematica",
            "degrees": ["LM-16", "LM-17", "LM-18", "LM-20", "LM-21", "LM-22", "LM-23", "LM-24", "LM-25", "LM-26", "LM-27", "LM-28", "LM-29", "LM-30", "LM-31", "LM-32", "LM-33", "LM-34", "LM-35", "LM-40", "LM-44", "LM-53", "LM-58", "LM-66", "LM-82", "LM-83", "LM-91"],
            "total_cfu_required": 80,
            "valid_ssds": ["MAT/02", "MAT/03", "MAT/05", "MAT/06", "MAT/07", "MAT/08"],
            "sub_conditions": [
                {"name": "Algebra e Geometria (24 CFU)", "min_cfu": 24, "valid_ssds": ["MAT/02", "MAT/03"]},
                {"name": "Analisi Matematica (24 CFU)", "min_cfu": 24, "valid_ssds": ["MAT/05"]},
                {"name": "Probabilità / Fisica Matematica (12 CFU)", "min_cfu": 12, "valid_ssds": ["MAT/06", "MAT/07", "MAT/08"]}
            ]
        },
        "A-27": {
            "class_name": "Matematica e Fisica",
            "degrees": ["LM-17", "LM-20", "LM-21", "LM-22", "LM-23", "LM-24", "LM-25", "LM-26", "LM-27", "LM-28", "LM-29", "LM-30", "LM-31", "LM-32", "LM-33", "LM-34", "LM-35", "LM-40", "LM-44", "LM-53", "LM-58"],
            "total_cfu_required": 90,
            "valid_ssds": ["MAT/02", "MAT/03", "MAT/05", "MAT/06", "MAT/07", "MAT/08", "FIS/01", "FIS/02", "FIS/03", "FIS/04", "FIS/05", "FIS/06", "FIS/07", "FIS/08"],
            "sub_conditions": [
                {"name": "Discipline Matematiche MAT (48 CFU)", "min_cfu": 48, "valid_ssds": ["MAT/02", "MAT/03", "MAT/05", "MAT/06", "MAT/07", "MAT/08"]},
                {"name": "Discipline Fisiche FIS (30 CFU)", "min_cfu": 30, "valid_ssds": ["FIS/01", "FIS/02", "FIS/03", "FIS/04", "FIS/05", "FIS/06", "FIS/07", "FIS/08"]}
            ]
        },
        "A-28": {
            "class_name": "Matematica e scienze nella scuola secondaria di I grado (DM 255/2023)",
            "degrees": ["LM-6", "LM-7", "LM-8", "LM-9", "LM-11", "LM-13", "LM-17", "LM-18", "LM-21", "LM-22", "LM-26", "LM-31", "LM-32", "LM-35", "LM-40", "LM-42", "LM-44", "LM-53", "LM-54", "LM-58", "LM-60", "LM-61", "LM-69", "LM-72", "LM-73", "LM-74", "LM-75", "LM-79", "LM-86"],
            "total_cfu_required": 132,
            "valid_ssds": ["MAT/01", "MAT/02", "MAT/03", "MAT/04", "MAT/05", "MAT/06", "MAT/07", "MAT/08", "FIS/01", "FIS/02", "FIS/03", "FIS/04", "FIS/05", "FIS/06", "FIS/07", "FIS/08", "CHIM/01", "CHIM/02", "CHIM/03", "CHIM/06", "GEO/01", "GEO/02", "GEO/03", "GEO/04", "BIO/01", "BIO/03", "BIO/05", "BIO/09", "BIO/18", "BIO/19", "INF/01", "ING-INF/05", "SECS-S/01"],
            "sub_conditions": [
                {"name": "Matematica MAT (30 CFU)", "min_cfu": 30, "valid_ssds": ["MAT/01", "MAT/02", "MAT/03", "MAT/04", "MAT/05", "MAT/06", "MAT/07", "MAT/08"]},
                {"name": "Fisica FIS (12 CFU)", "min_cfu": 12, "valid_ssds": ["FIS/01", "FIS/02", "FIS/03", "FIS/04", "FIS/05", "FIS/06", "FIS/07", "FIS/08"]},
                {"name": "Chimica CHIM (6 CFU)", "min_cfu": 6, "valid_ssds": ["CHIM/01", "CHIM/02", "CHIM/03", "CHIM/06"]},
                {"name": "Geologia GEO (6 CFU)", "min_cfu": 6, "valid_ssds": ["GEO/01", "GEO/02", "GEO/03", "GEO/04"]},
                {"name": "Biologia BIO (6 CFU)", "min_cfu": 6, "valid_ssds": ["BIO/01", "BIO/03", "BIO/05", "BIO/09", "BIO/18", "BIO/19"]},
                {"name": "Informatica o Statistica (6 CFU)", "min_cfu": 6, "valid_ssds": ["INF/01", "ING-INF/05", "SECS-S/01"]}
            ]
        },
        "A-41": {
            "class_name": "Scienze e tecnologie informatiche",
            "degrees": ["LM-17", "LM-18", "LM-20", "LM-25", "LM-27", "LM-29", "LM-31", "LM-32", "LM-40", "LM-66", "LM-91"],
            "total_cfu_required": 48,
            "valid_ssds": ["INF/01", "ING-INF/05", "MAT/01", "MAT/02", "MAT/03", "MAT/05"],
            "sub_conditions": [
                {"name": "Informatica e Sistemi (24 CFU)", "min_cfu": 24, "valid_ssds": ["INF/01", "ING-INF/05"]},
                {"name": "Matematica di Base (12 CFU)", "min_cfu": 12, "valid_ssds": ["MAT/01", "MAT/02", "MAT/03", "MAT/05"]}
            ]
        },
        "A-46": {
            "class_name": "Scienze giuridico-economiche",
            "degrees": ["LMG-01", "LM-16", "LM-52", "LM-56", "LM-62", "LM-63", "LM-77", "LM-81", "LM-82", "LM-83", "LM-88", "LM-90"],
            "total_cfu_required": 96,
            "valid_ssds": ["IUS/01", "IUS/02", "IUS/04", "IUS/09", "IUS/10", "IUS/12", "SPS/04", "SECS-P/01", "SECS-P/02", "SECS-P/03", "SECS-P/07", "SECS-P/08"],
            "sub_conditions": [
                {"name": "Diritto IUS (36 CFU)", "min_cfu": 36, "valid_ssds": ["IUS/01", "IUS/02", "IUS/04", "IUS/09", "IUS/10", "IUS/12", "SPS/04"]},
                {"name": "Economia Politica e Aziendale SECS-P (36 CFU)", "min_cfu": 36, "valid_ssds": ["SECS-P/01", "SECS-P/02", "SECS-P/03", "SECS-P/07", "SECS-P/08"]}
            ]
        },
        "A-47": {
            "class_name": "Scienze matematiche applicate",
            "degrees": ["LM-16", "LM-17", "LM-18", "LM-20", "LM-21", "LM-22", "LM-23", "LM-24", "LM-25", "LM-26", "LM-27", "LM-28", "LM-29", "LM-30", "LM-31", "LM-32", "LM-33", "LM-34", "LM-35", "LM-40", "LM-44", "LM-53", "LM-56", "LM-66", "LM-77", "LM-82", "LM-83", "LM-91"],
            "total_cfu_required": 48,
            "valid_ssds": ["MAT/05", "MAT/06", "MAT/08", "SECS-S/01", "SECS-S/06", "SECS-P/05"],
            "sub_conditions": [
                {"name": "Metodi Matematici e Modelli (12 CFU)", "min_cfu": 12, "valid_ssds": ["MAT/05", "MAT/08"]},
                {"name": "Statistica o Matematica Finanziaria (12 CFU)", "min_cfu": 12, "valid_ssds": ["SECS-S/01", "SECS-S/06", "SECS-P/05"]}
            ]
        },
        "A-50": {
            "class_name": "Scienze naturali, chimiche e biologiche",
            "degrees": ["LM-6", "LM-7", "LM-8", "LM-9", "LM-11", "LM-13", "LM-42", "LM-54", "LM-60", "LM-61", "LM-69", "LM-73", "LM-74", "LM-75", "LM-79"],
            "total_cfu_required": 60,
            "valid_ssds": ["CHIM/01", "CHIM/02", "CHIM/03", "CHIM/06", "BIO/01", "BIO/03", "BIO/05", "BIO/19", "GEO/01", "GEO/02", "GEO/03", "GEO/04"],
            "sub_conditions": [
                {"name": "Chimica CHIM (12 CFU)", "min_cfu": 12, "valid_ssds": ["CHIM/01", "CHIM/02", "CHIM/03", "CHIM/06"]},
                {"name": "Biologia BIO (12 CFU)", "min_cfu": 12, "valid_ssds": ["BIO/01", "BIO/03", "BIO/05", "BIO/19"]},
                {"name": "Scienze della Terra GEO (12 CFU)", "min_cfu": 12, "valid_ssds": ["GEO/01", "GEO/02", "GEO/03", "GEO/04"]}
            ]
        },
        "AA22": {
            "class_name": "Lingue e culture straniere I e II grado - Francese (DM 255/2023)",
            "degrees": ["LM-36", "LM-37", "LM-38", "LM-39", "LM-94"],
            "total_cfu_required": 72,
            "valid_ssds": ["L-LIN/03", "L-LIN/04", "L-LIN/01", "L-LIN/02"],
            "sub_conditions": [
                {"name": "Lingua Francese triennale (36 CFU)", "min_cfu": 36, "valid_ssds": ["L-LIN/04"]},
                {"name": "Letteratura Francese biennale (24 CFU)", "min_cfu": 24, "valid_ssds": ["L-LIN/03"]},
                {"name": "Linguistica Generale / Glottologia (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-LIN/01", "L-LIN/02"]}
            ]
        },
        "AB22": {
            "class_name": "Lingue e culture straniere I e II grado - Inglese (DM 255/2023)",
            "degrees": ["LM-36", "LM-37", "LM-38", "LM-39", "LM-94"],
            "total_cfu_required": 72,
            "valid_ssds": ["L-LIN/10", "L-LIN/11", "L-LIN/12", "L-LIN/01", "L-LIN/02"],
            "sub_conditions": [
                {"name": "Lingua Inglese triennale (36 CFU)", "min_cfu": 36, "valid_ssds": ["L-LIN/12"]},
                {"name": "Letteratura Inglese / Anglo-Americana biennale (24 CFU)", "min_cfu": 24, "valid_ssds": ["L-LIN/10", "L-LIN/11"]},
                {"name": "Linguistica Generale / Glottologia (12 CFU)", "min_cfu": 12, "valid_ssds": ["L-LIN/01", "L-LIN/02"]}
            ]
        },
        "BA02": {
            "class_name": "Conversazione in lingua straniera (Francese)",
            "degrees": ["LM-37", "LM-38", "LM-94", "Madrelingua"],
            "total_cfu_required": 1,
            "valid_ssds": ["L-LIN/04", "Madrelingua"],
            "sub_conditions": [
                {"name": "Titolo Madrelingua o Coerenza Lingua", "min_cfu": 1, "valid_ssds": ["L-LIN/04", "Madrelingua"]}
            ]
        },
        "BB02": {
            "class_name": "Conversazione in lingua straniera (Inglese)",
            "degrees": ["LM-37", "LM-38", "LM-94", "Madrelingua"],
            "total_cfu_required": 1,
            "valid_ssds": ["L-LIN/12", "Madrelingua"],
            "sub_conditions": [
                {"name": "Titolo Madrelingua o Coerenza Lingua", "min_cfu": 1, "valid_ssds": ["L-LIN/12", "Madrelingua"]}
            ]
        },
        "B003": {
            "class_name": "Laboratorio di fisica (ITP)",
            "degrees": ["LM-17", "LM-40", "Diploma ITP Tecnico/Fisica"],
            "total_cfu_required": 12,
            "valid_ssds": ["FIS/01", "FIS/02", "FIS/03", "FIS/04", "FIS/05", "FIS/06", "FIS/07", "FIS/08"],
            "sub_conditions": [
                {"name": "CFU in Discipline Fisiche (12 CFU)", "min_cfu": 12, "valid_ssds": ["FIS/01", "FIS/02", "FIS/03", "FIS/04"]}
            ]
        }
    }

RULES_DATABASE = load_rules()


# =====================================================================
# GENERATORE REPORT PDF PER STREAMLIT (REPORTLAB)
# =====================================================================
import io

try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus import (
        BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Flowable, KeepTogether, ListFlowable, ListItem
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def generate_evaluation_pdf(target_class, rule_def, portfolio_exams, eval_result, primary_title):
    buffer = io.BytesIO()
    
    COLORS = {
        'heading':   HexColor('#1E3A8A'),
        'body':      HexColor('#1F2937'),
        'accent':    HexColor('#2563EB'),
        'warn':      HexColor('#D97706'),
        'success':   HexColor('#059669'),
        'muted':     HexColor('#6B7280'),
        'bg_alt':    HexColor('#F3F4F6'),
        'bg_header': HexColor('#1E3A8A'),
        'white':     HexColor('#FFFFFF'),
    }

    PAGE_SIZE = LETTER
    MARGIN    = 0.65 * inch
    PAGE_W, PAGE_H = PAGE_SIZE
    USABLE_W  = PAGE_W - 2 * MARGIN

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=20, textColor=COLORS['heading'], leading=24, spaceAfter=6))
    styles.add(ParagraphStyle('DocSubtitle', fontName='Helvetica', fontSize=10, textColor=COLORS['muted'], leading=14, spaceAfter=12))
    styles.add(ParagraphStyle('H1_Custom', fontName='Helvetica-Bold', fontSize=12, textColor=COLORS['heading'], leading=15, spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle('Body_Custom', fontName='Helvetica', fontSize=9, textColor=COLORS['body'], leading=13, spaceAfter=5))
    styles.add(ParagraphStyle('TableHead', fontName='Helvetica-Bold', fontSize=8, textColor=COLORS['white'], leading=10))
    styles.add(ParagraphStyle('TableBody', fontName='Helvetica', fontSize=8, textColor=COLORS['body'], leading=11))
    styles.add(ParagraphStyle('TableBodyBold', fontName='Helvetica-Bold', fontSize=8, textColor=COLORS['body'], leading=11))

    class CalloutBox(Flowable):
        def __init__(self, text, width, colors, body_style, bar_color=None):
            super().__init__()
            self._width = width
            self.colors = colors
            self.bar_color = bar_color or colors['accent']
            self.bar_w = 5
            self.pad = 7
            inner_w = self._width - self.bar_w - 2 * self.pad
            self._para = Paragraph(text, body_style)
            self._para_w, self._para_h = self._para.wrap(inner_w, 10000)
            self._height = self._para_h + 2 * self.pad

        def wrap(self, availWidth, availHeight):
            return self._width, self._height

        def draw(self):
            self.canv.setFillColor(self.colors['bg_alt'])
            self.canv.rect(0, 0, self._width, self._height, fill=1, stroke=0)
            self.canv.setFillColor(self.bar_color)
            self.canv.rect(0, 0, self.bar_w, self._height, fill=1, stroke=0)
            self._para.drawOn(self.canv, self.bar_w + self.pad, self.pad)

    class SectionDivider(Flowable):
        def __init__(self, width, color):
            super().__init__()
            self._width = width
            self.color = color
            self._height = 6

        def wrap(self, availWidth, availHeight):
            return self._width, self._height

        def draw(self):
            self.canv.setStrokeColor(self.color)
            self.canv.setLineWidth(1)
            self.canv.line(0, 3, self._width, 3)

    def on_pages(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(COLORS['accent'])
        canvas.setLineWidth(0.8)
        y_rule = PAGE_H - MARGIN + 8
        canvas.line(MARGIN, y_rule, PAGE_W - MARGIN, y_rule)

        canvas.setFont('Helvetica-Bold', 8)
        canvas.setFillColor(COLORS['muted'])
        canvas.drawString(MARGIN, y_rule + 3, f'REPORT VALUTAZIONE CFU - CLASSE {target_class}')
        canvas.drawRightString(PAGE_W - MARGIN, y_rule + 3, 'VALUTATORE REQUISITI DOCENTI')

        y_footer = MARGIN - 18
        canvas.setStrokeColor(COLORS['bg_alt'])
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, y_footer + 10, PAGE_W - MARGIN, y_footer + 10)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(COLORS['muted'])
        canvas.drawString(MARGIN, y_footer, 'Documento generato da Valutatore Requisiti Docenti - Conforme D.M. 255/2023')
        canvas.drawRightString(PAGE_W - MARGIN, y_footer, f'Pagina {doc.page}')
        canvas.restoreState()

    doc = BaseDocTemplate(
        buffer,
        pagesize=PAGE_SIZE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 14, bottomMargin=MARGIN + 8
    )

    content_frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        USABLE_W, PAGE_H - doc.topMargin - doc.bottomMargin,
        id='main'
    )

    doc.addPageTemplates([
        PageTemplate(id='content', frames=content_frame, onPage=on_pages)
    ])

    story = []

    story.append(Paragraph(f'Report di Valutazione Curriculare: Classe {target_class}', styles['DocTitle']))
    story.append(Paragraph(f'<b>Denominazione:</b> {rule_def.get("class_name", "")} | <b>Titolo Dichiarato:</b> {primary_title if primary_title else "N/D"}', styles['DocSubtitle']))
    story.append(SectionDivider(USABLE_W, COLORS['accent']))
    story.append(Spacer(1, 6))

    status_str = '🟢 REQUISITI SODDISFATTI' if eval_result.get('eligible') else '🔴 REQUISITI NON SODDISFATTI'
    bar_col = COLORS['success'] if eval_result.get('eligible') else COLORS['warn']
    
    summary_text = (
        f'<b>Esito Finale:</b> {status_str}<br/>'
        f'<b>CFU Validi Riscontrati:</b> {eval_result.get("total_valid_cfu", 0)} / {rule_def.get("total_cfu_required", 0)} CFU richiesti.<br/>'
        f'<b>Note & Motivazione:</b> {eval_result.get("reason", "")}'
    )
    story.append(CalloutBox(summary_text, USABLE_W, COLORS, styles['Body_Custom'], bar_color=bar_col))
    story.append(Spacer(1, 8))

    story.append(Paragraph('1. Quadro Normativo & Interpretazione ("e / o")', styles['H1_Custom']))
    norma_text = (
        'Ai sensi della nota introduttiva della Tabella A del <b>D.M. 255/2023</b> e dei chiarimenti ministeriali ufficiali, '
        'qualora i requisiti d accesso indichino un totale di CFU distribuiti su piu settori (SSD) con la dicitura "e / o", '
        'tali crediti possono essere conseguiti, <i>senza vincoli numerici interni</i>, in uno solo o piu settori elencati, '
        'fatti salvi i minimi specifici prescritti.'
    )
    story.append(Paragraph(norma_text, styles['Body_Custom']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('2. Dettaglio Allocazione Crediti per Sotto-Soglia', styles['H1_Custom']))
    headers = ['Sotto-Soglia Ministeriale', 'SSD Validi', 'Minimo', 'Stato Insegnamenti Allocati']
    
    details_rows = []
    allocated_details = eval_result.get('details', [])
    
    for cond in rule_def.get('sub_conditions', []):
        matched_items = [d for d in allocated_details if d.get('condition') == cond.get('name')]
        allocated_cfu = sum(d.get('allocated_cfu', 0) for d in matched_items)
        
        status_cell = f'<font color="#059669"><b>Coperto ({allocated_cfu}/{cond["min_cfu"]} CFU)</b></font>' if allocated_cfu >= cond['min_cfu'] else f'<font color="#D97706"><b>Carente (Mancano {cond["min_cfu"] - allocated_cfu} CFU)</b></font>'
        
        details_rows.append([
            Paragraph(f'<b>{cond.get("name")}</b>', styles['TableBodyBold']),
            Paragraph(', '.join(cond.get('valid_ssds', [])), styles['TableBody']),
            Paragraph(f'{cond.get("min_cfu")} CFU', styles['TableBody']),
            Paragraph(status_cell, styles['TableBody'])
        ])

    t_details = Table([ [Paragraph(h, styles['TableHead']) for h in headers] ] + details_rows, colWidths=[150, 130, 84, 140])
    t_details.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['bg_header']),
        ('GRID', (0, 0), (-1, -1), 0.5, COLORS['muted']),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLORS['white'], COLORS['bg_alt']]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_details)
    story.append(Spacer(1, 8))

    story.append(Paragraph('3. Guida Operativa & Recupero Corsi Singoli UNISI', styles['H1_Custom']))
    unisi_info = (
        'In presenza di debiti formativi, e possibile acquisire i CFU mancanti iscrivendosi ai <b>Corsi Singoli Universitari</b> '
        'presso l <b>Universita degli Studi di Siena (www.unisi.it)</b>:<br/>'
        '• <b>UNISI Course Catalogue (CINECA):</b> unisi.coursecatalogue.cineca.it<br/>'
        '• <b>Manifesto degli Studi & Immatricolazioni:</b> unisi.it/didattica/immatricolazioni-e-iscrizioni/immatricolazioni-procedure'
    )
    story.append(Paragraph(unisi_info, styles['Body_Custom']))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# =====================================================================
# 2. MOTORE DI CALCOLO E BACKTRACKING PER IL MATCHING REQUISITI
# =====================================================================
def check_requirements(career_exams, rule_definition):
    total_required = rule_definition["total_cfu_required"]
    valid_ssds = set(rule_definition["valid_ssds"])
    sub_conditions = rule_definition["sub_conditions"]
    
    useful_exams = []
    total_available_cfu = 0
    for exam in career_exams:
        if exam["ssd"] in valid_ssds:
            useful_exams.append({
                "name": exam["name"],
                "ssd": exam["ssd"],
                "cfu": exam["cfu"],
                "remaining": exam["cfu"],
                "source": exam.get("source", "N/D")
            })
            total_available_cfu += exam["cfu"]
            
    if total_available_cfu < total_required:
        return {
            "eligible": False,
            "reason": f"Totale CFU validi nel Portfolio ({total_available_cfu}) inferiore al minimo assoluto richiesto di {total_required} CFU.",
            "total_valid_cfu": total_available_cfu,
            "missing_cfu_total": total_required - total_available_cfu,
            "details": []
        }
        
    conditions = [dict(cond) for cond in sub_conditions]
    conditions.sort(key=lambda x: len(x["valid_ssds"]))
    
    allocation_details = []
    
    def allocate_cfu(cond_index, current_exams):
        if cond_index == len(conditions):
            return True
            
        cond = conditions[cond_index]
        target_cfu = cond["min_cfu"]
        allowed_ssds = set(cond["valid_ssds"])
        matching_exams = [e for e in current_exams if e["ssd"] in allowed_ssds and e["remaining"] > 0]
        
        def dfs_sub(exam_idx, cfu_needed):
            if cfu_needed <= 0:
                return True
            if exam_idx >= len(matching_exams):
                return False
                
            exam = matching_exams[exam_idx]
            max_take = min(exam["remaining"], cfu_needed)
            
            for take in range(int(max_take), -1, -1):
                if take > 0:
                    exam["remaining"] -= take
                    if dfs_sub(exam_idx + 1, cfu_needed - take):
                        allocation_details.append({
                            "condition": cond["name"],
                            "exam_name": exam["name"],
                            "ssd": exam["ssd"],
                            "allocated_cfu": take,
                            "source": exam["source"]
                        })
                        return True
                    exam["remaining"] += take
                else:
                    if dfs_sub(exam_idx + 1, cfu_needed):
                        return True
            return False

        return dfs_sub(0, target_cfu) and allocate_cfu(cond_index + 1, current_exams)

    exams_working_copy = [dict(e) for e in useful_exams]
    if not allocate_cfu(0, exams_working_copy):
        return {
            "eligible": False,
            "reason": "La carriera possiede abbastanza CFU totali, ma non è possibile soddisfare contemporaneamente tutte le sotto-soglie senza incorrere in double-counting.",
            "total_valid_cfu": total_available_cfu,
            "missing_cfu_total": 0,
            "details": []
        }
        
    return {
        "eligible": True,
        "reason": f"Requisiti soddisfatti! Trovati {total_available_cfu} CFU idonei totali.",
        "total_valid_cfu": total_available_cfu,
        "missing_cfu_total": 0,
        "details": allocation_details
    }

# =====================================================================
# 3. INTERFACCIA UTENTE STREAMLIT (UX/UI)
# =====================================================================
st.markdown("""
<style>
    .reportview-container { background: #f0f2f6; }
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem; }
    .subheader { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
    .card-success { padding: 1.5rem; background-color: #ECFDF5; border-left: 6px solid #10B981; border-radius: 4px; margin-bottom: 1rem; }
    .card-error { padding: 1.5rem; background-color: #FEF2F2; border-left: 6px solid #EF4444; border-radius: 4px; margin-bottom: 1rem; }
    .card-info { padding: 1.5rem; background-color: #EFF6FF; border-left: 6px solid #3B82F6; border-radius: 4px; margin-bottom: 1rem; }
    .card-warning { padding: 1.5rem; background-color: #FFFBEB; border-left: 6px solid #F59E0B; border-radius: 4px; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎓 Portfolio Unico CFU: Valutatore Multi-Titolo & PDF</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Verifica integrata dei requisiti ministeriali (UNISI, D.P.R. 19/2016, D.M. 255/2023, D.Lgs. 59/2017 e DPCM 23 agosto 2023) accumulando Lauree Magistrali, Triennali, Master, Dottorati e Corsi Singoli con estrazione intelligente da PDF.</div>', unsafe_allow_html=True)

# Session State per il Portfolio
if "exams_portfolio" not in st.session_state:
    st.session_state["exams_portfolio"] = []

# Sidebar di configurazione
with st.sidebar:
    st.header("⚙️ Configurazione")
    
    # 1. Tipologia Titolo Principale
    primary_degree_type = st.selectbox(
        "1. Tipologia Titolo Principale",
        options=[
            "Nuovo Ordinamento (Laurea Magistrale LM / Specialistica LS)",
            "Vecchio Ordinamento (Ante D.M. 509/1999)",
            "Diploma Accademico di II Livello (AFAM / Conservatorio)",
            "Laurea Triennale",
            "Dottorato di Ricerca",
            "Master Universitario / Altro"
        ],
        index=0
    )
    
    # 2. Descrizione / Codice Titolo
    primary_degree_code = st.text_input(
        "2. Descrizione / Codice del Titolo",
        placeholder="Es. LM-14, LM-78, Lettere Classiche, ecc.",
        help="Inserisci il codice ministeriale (es. LM-14, LS-16) o la denominazione del titolo per verificare l'idoneità standard di accesso."
    ).strip()
    
    # 3. Selezione Classe di Concorso Target (UNISI)
    target_class = st.selectbox(
        "3. Classe di Concorso Target (UNISI)",
        options=list(RULES_DATABASE.keys()),
        format_func=lambda x: f"{x} - {RULES_DATABASE[x]['class_name']}"
    )
    
    rule = RULES_DATABASE[target_class]
    
    st.markdown("---")
    st.subheader("💡 Seconda Abilitazione?")
    art_13_enabled = st.checkbox(
        "Applica Art. 13 DPCM 23 agosto 2023",
        help="Attiva la logica percorsi abilitanti abbreviati da 30 CFU per chi possiede già altra abilitazione o specializzazione sul sostegno."
    )
    
    if art_13_enabled:
        st.info("ℹ️ Ai sensi dell'Art. 13, l'accesso è diretto esentando l'utente dai controlli dei CFU delle Tabelle standard, a patto che il titolo di studio a monte sia idoneo.")

# Layout principale a Schede (Tabs)
tab_manual, tab_pdf, tab_recovery, tab_a1_equip, tab_24cfu, tab_readme = st.tabs([
    "📝 Portfolio Unico (Inserimento)", 
    "📄 Estrazione da PDF (Transcripts OCR)",
    "🎯 Piano di Recupero CFU (UNISI)",
    "📚 Tabella A/1 & Equiparazioni",
    "🧩 24 CFU & DPCM 30/60",
    "📖 Guida & README"
])

# ---------------------------------------------------------------------
# TAB 1: PORTFOLIO UNICO (MANUALE)
# ---------------------------------------------------------------------
with tab_manual:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Costruisci il tuo Piano di Studi Cumulativo")
        
        with st.form("exam_form", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
            with f_col1:
                exam_name = st.text_input("Denominazione Insegnamento", placeholder="Es. Storia Romana")
            with f_col2:
                ssd = st.text_input("SSD (Settore)", placeholder="Es. L-ANT/03 o M-FIL/01").upper().strip()
            with f_col3:
                cfu = st.number_input("CFU", min_value=1, max_value=30, value=6, step=1)
                
            f_col_src, f_col_btn = st.columns([2, 2])
            with f_col_src:
                source_type = st.selectbox(
                    "Provenienza del Credito",
                    options=[
                        "Laurea Magistrale d'Accesso",
                        "Laurea Triennale",
                        "Corsi Singoli Integrativi",
                        "Master Universitario",
                        "Dottorato di Ricerca"
                    ]
                )
            with f_col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                submit_button = st.form_submit_button("➕ Aggiungi al Portfolio")
                
            if submit_button and exam_name and ssd:
                st.session_state["exams_portfolio"].append({
                    "name": exam_name,
                    "ssd": ssd,
                    "cfu": cfu,
                    "source": source_type
                })
                st.toast(f"Insegnamento '{exam_name}' aggiunto con successo!")
                st.rerun()

        if len(st.session_state["exams_portfolio"]) > 0:
            st.markdown("### 📊 Riepilogo del tuo Portfolio Unico")
            df_portfolio = pd.DataFrame(st.session_state["exams_portfolio"])
            st.dataframe(df_portfolio, use_container_width=True)
            col_del1, col_del2 = st.columns(2)
            with col_del1:
                if st.button("🗑️ Rimuovi Ultimo Insegnamento"):
                    st.session_state["exams_portfolio"].pop()
                    st.rerun()
            with col_del2:
                if st.button("🗑️ Svuota Intero Portfolio"):
                    st.session_state["exams_portfolio"] = []
                    st.rerun()
        else:
            st.warning("⚠️ Il tuo Portfolio CFU è vuoto. Aggiungi gli esami manualmente o estraili dal PDF nella scheda accanto.")

    with col2:
        st.subheader("🔍 Risultato della Valutazione Cumulativa")
        
        # Verifica titolarità d'accesso
        allowed_degrees = rule.get("degrees", [])
        degree_eligible = False
        matching_code = ""
        
        if primary_degree_code:
            search_str = primary_degree_code.upper()
            for deg in allowed_degrees:
                if deg.upper() in search_str or search_str in deg.upper():
                    degree_eligible = True
                    matching_code = deg
                    break
        
        if not primary_degree_code:
            title_message_html = f"""
            <div class="card-info">
                <h4>ℹ️ Titolo principale non specificato</h4>
                <p>Inserisci la sigla o descrizione del tuo titolo di studio nel campo di testo a sinistra (es. <b>LM-14</b> o <b>Lettere</b>) per convalidare l'accesso diretto alla classe <b>{target_class}</b>.</p>
                <p>I titoli idonei standard sono: <code>{', '.join(allowed_degrees)}</code>.</p>
            </div>
            """
        elif degree_eligible:
            title_message_html = f"""
            <div class="card-success">
                <h4>🟢 Titolo di Studio Idoneo standard</h4>
                <p>Il titolo <b>{primary_degree_code}</b> è un titolo di accesso idoneo per la classe <b>{target_class}</b>.</p>
            </div>
            """
        else:
            if "Triennale" in primary_degree_type:
                title_message_html = f"""
                <div class="card-warning">
                    <h4>⚠️ Attenzione: Laurea Triennale</h4>
                    <p>La laurea triennale inserita (<b>{primary_degree_code}</b>) non consente l'accesso diretto all'insegnamento ordinario, ma i suoi crediti sono validissimi se cumulati con una Laurea Magistrale.</p>
                </div>
                """
            else:
                title_message_html = f"""
                <div class="card-warning">
                    <h4>⚠️ Titolo personalizzato (Da convalidare equipollenza)</h4>
                    <p>Il titolo inserito (<b>{primary_degree_code}</b>) non è presente nell'elenco standard dei titoli ad accesso diretto per la classe <b>{target_class}</b>.</p>
                    <p>I titoli standard ammessi sono: <code>{', '.join(allowed_degrees)}</code>. Consulta la scheda "Tabella A/1 & Equiparazioni" per verificare la corrispondenza col Vecchio Ordinamento.</p>
                </div>
                """

        st.markdown(title_message_html, unsafe_allow_html=True)
        
        if len(st.session_state["exams_portfolio"]) > 0:
            if art_13_enabled:
                if degree_eligible or (not primary_degree_code):
                    st.markdown(
                        f"""
                        <div class="card-success">
                            <h3>🟢 IDONEO AL PERCORSO EX ART. 13</h3>
                            <p><b>Titolo d'accesso:</b> {primary_degree_code if primary_degree_code else 'Conforme'}</p>
                            <p>Ai sensi dell'Art. 13 DPCM 23 agosto 2023, hai diritto all'accesso diretto ai percorsi abilitanti abbreviati da <b>30 CFU</b> per la classe <b>{target_class}</b> senza l'obbligo di colmare i CFU integrativi ordinarie.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                result = check_requirements(st.session_state["exams_portfolio"], rule)
                
                if result["eligible"]:
                    st.markdown(
                        f"""
                        <div class="card-success">
                            <h3>🟢 REQUISITI CURRICULARI SODDISFATTI</h3>
                            <p><b>CFU totali validi nel Portfolio:</b> {result['total_valid_cfu']} su {rule['total_cfu_required']} richiesti.</p>
                            <p>Tutte le sotto-soglie minime sono state coperte combinando i tuoi esami senza double-counting.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("#### Allocazione Ottimale dei CFU alle Sotto-soglie:")
                    df_alloc = pd.DataFrame(result["details"])
                    st.table(df_alloc[["condition", "exam_name", "ssd", "allocated_cfu", "source"]])
                else:
                    st.markdown(
                        f"""
                        <div class="card-error">
                            <h3>🔴 REQUISITI CURRICULARI NON SODDISFATTI</h3>
                            <p><b>CFU totali validi nel Portfolio:</b> {result['total_valid_cfu']} su {rule['total_cfu_required']} richiesti.</p>
                            <p><b>Motivazione:</b> {result['reason']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if result["missing_cfu_total"] > 0:
                        st.metric(label="CFU Totali Mancanti", value=f"{result['missing_cfu_total']} CFU")
                    st.markdown("#### Requisiti Curriculari Richiesti:")
                    for cond in rule["sub_conditions"]:
                        st.write(f"* **{cond['name']}**: Minimo **{cond['min_cfu']} CFU** nei settori: `{', '.join(cond['valid_ssds'])}`")

                # Bottone di Download Report PDF
                if REPORTLAB_AVAILABLE:
                    try:
                        pdf_bytes = generate_evaluation_pdf(target_class, rule, st.session_state["exams_portfolio"], result, primary_degree_code)
                        st.download_button(
                            label="📄 Scarica Report PDF Completo (Esito + Piano Recupero)",
                            data=pdf_bytes,
                            file_name=f"Esito_Valutazione_CFU_{target_class}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e_pdf:
                        st.caption(f"Generazione Report PDF disponibile ({e_pdf})")
                else:
                    st.caption("💡 Nota: Installa 'reportlab' (pip install reportlab) per abilitare l'esportazione in PDF.")

# ---------------------------------------------------------------------
# TAB 2: CARICAMENTO DA PDF (TRANSCRIPTS OCR)
# ---------------------------------------------------------------------
with tab_pdf:
    st.subheader("📄 Caricamento Certificato Carriera / Statino Esami (PDF)")
    st.write("Carica il certificato di laurea scaricato dal portale dello studente (Esse3, GOMP, ecc.) per estrarre automaticamente la tabella degli esami con SSD e CFU.")

    uploaded_file = st.file_uploader("Scegli un file PDF del tuo piano di studi", type=["pdf"])
    
    col_pdf_l, col_pdf_r = st.columns([1, 1])
    
    with col_pdf_l:
        st.markdown("#### 💡 Come funziona l'algoritmo di estrazione?")
        st.markdown("""
        1. **Lettura del Testo**: L'app scansiona il testo del PDF usando la libreria `pypdf`.
        2. **Riconoscimento Pattern (Regex Avanzata)**: Un motore a espressioni regolari individua con precisione i codici SSD (es. `M-FIL/01`, `L-FIL-LET/10`, `SPS/07`, `SECS-P/01`, `ING-INF/05`) e i numeri di CFU adiacenti.
        3. **Validazione Utente**: Gli esami vengono presentati in una tabella modificabile per consentirti di verificare e confermare i dati prima dell'importazione.
        """)
        
    with col_pdf_r:
        if uploaded_file is not None:
            st.success(f"File '{uploaded_file.name}' caricato con successo!")
            
            parsed_exams = []
            try:
                import pypdf
                reader = pypdf.PdfReader(uploaded_file)
                full_text = ""
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        full_text += txt + "\n"
                    
                # Regex flessibile per codici SSD italiani (anche con spazi interni)
                ssd_pattern = re.compile(r'\b([A-Z]{1,4}(?:\s*-\s*[A-Z]{1,4}){0,2}\s*/\s*\d{2})\b')
                cfu_pattern = re.compile(r'(\d{1,2}(?:[\.,]0)?)\s*(?:CFU|CFA|CREDITI|CR|CRE)\b', re.IGNORECASE)
                
                lines = full_text.split('\n')
                for line in lines:
                    ssd_match = ssd_pattern.search(line)
                    if ssd_match:
                        raw_ssd = ssd_match.group(1)
                        ssd_found = re.sub(r'\s+', '', raw_ssd).upper()
                        cfu_match = cfu_pattern.search(line)
                        if cfu_match:
                            cfu_found = int(float(cfu_match.group(1).replace(',', '.')))
                        else:
                            line_no_ssd = line.replace(raw_ssd, '')
                            nums = [int(m) for m in re.findall(r'\b([1-9]|[12][0-9]|30)\b', line_no_ssd)]
                            cfu_found = nums[0] if nums else 6
                            
                        clean_name = line.replace(raw_ssd, '').strip()
                        clean_name = re.sub(r'\d{1,2}(?:[\.,]0)?\s*(?:CFU|CFA|CREDITI|CR|CRE)\b', '', clean_name, flags=re.IGNORECASE).strip()
                        if len(clean_name) < 3:
                            clean_name = f"Insegnamento in {ssd_found}"
                        parsed_exams.append({"name": clean_name[:45], "ssd": ssd_found, "cfu": cfu_found, "checked": True})
            except Exception as e:
                st.info(f"Modalità simulazione attivata ({e}).")

            if len(parsed_exams) == 0:
                st.warning("⚠️ Non sono stati identificati automaticamente codici SSD nel testo del PDF (il file potrebbe essere una scansione o avere un layout non testuale). Sono stati caricati degli slot esame di esempio che puoi personalizzare.")
                parsed_exams = [
                    {"name": "STORIA DELLA FILOSOFIA CONTEMPORANEA", "ssd": "M-FIL/06", "cfu": 12, "checked": True},
                    {"name": "ANTROPOLOGIA CULTURALE", "ssd": "M-DEA/01", "cfu": 6, "checked": True},
                    {"name": "SOCIOLOGIA GENERALE", "ssd": "SPS/07", "cfu": 12, "checked": True},
                    {"name": "PEDAGOGIA GENERALE", "ssd": "M-PED/01", "cfu": 12, "checked": True},
                    {"name": "PSICOLOGIA DELLO SVILUPPO", "ssd": "M-PSI/04", "cfu": 12, "checked": True}
                ]
                
            st.markdown("#### 🔍 Insegnamenti Rilevati dal PDF (Modificabili):")
            checked_list = []
            for idx, exam in enumerate(parsed_exams):
                c_chk, c_nm, c_ssd, c_cfu = st.columns([1, 4, 2, 2])
                with c_chk:
                    chk = st.checkbox("", value=exam.get("checked", True), key=f"chk_p_{idx}")
                with c_nm:
                    nm = st.text_input("Nome Insegnamento", value=exam["name"], key=f"nm_p_{idx}")
                with c_ssd:
                    sd = st.text_input("SSD", value=exam["ssd"], key=f"sd_p_{idx}").upper().strip()
                with c_cfu:
                    cf = st.number_input("CFU", value=exam["cfu"], min_value=1, max_value=30, key=f"cf_p_{idx}")
                if chk:
                    checked_list.append({"name": nm, "ssd": sd, "cfu": cf, "source": "Estratto da Certificato PDF"})
                    
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📥 Importa nel Portfolio Unico", type="primary"):
                if len(checked_list) > 0:
                    for ex in checked_list:
                        st.session_state["exams_portfolio"].append(ex)
                    st.success(f"🎉 Importati con successo {len(checked_list)} esami nel Portfolio Unico!")
                    st.rerun()
                else:
                    st.error("Seleziona almeno un esame spuntando la casella per poterlo importare.")

# ---------------------------------------------------------------------
# TAB 3: PIANO DI RECUPERO CFU (UNISI)
# ---------------------------------------------------------------------
with tab_recovery:
    st.subheader("🎯 Piano di Recupero CFU & Corsi Singoli (Università di Siena)")
    st.write("Questa scheda calcola esattamente i debiti formativi riscontrati e genera i link diretti per reperire gli insegnamenti attivi presso l'**Università degli Studi di Siena (www.unisi.it)**.")
    
    if len(st.session_state["exams_portfolio"]) == 0:
        st.info("Inserisci gli esami nel Portfolio per generare il piano di recupero crediti.")
    else:
        res = check_requirements(st.session_state["exams_portfolio"], rule)
        if res["eligible"]:
            st.success(f"🎉 Nessun debito formativo riscontrato! La tua carriera è già idonea per la classe {target_class}.")
        else:
            st.markdown(f"### ⚠️ Debiti Formativi Rilevati per la classe **{target_class}**")
            
            allocated_ssds = [d["ssd"] for d in res["details"]]
            for cond in rule["sub_conditions"]:
                cond_ssds = set(cond["valid_ssds"])
                matched_cfu = sum(d["allocated_cfu"] for d in res["details"] if d["ssd"] in cond_ssds)
                
                if matched_cfu < cond["min_cfu"]:
                    needed = cond["min_cfu"] - matched_cfu
                    primary_ssd = list(cond["valid_ssds"])[0]
                    
                    st.error(f"❌ **{cond['name']}**: Mancano **{needed} CFU** nei settori `{', '.join(cond['valid_ssds'])}`")
                    
                    col_u1, col_u2 = st.columns(2)
                    with col_u1:
                        st.link_button("🎓 UNISI Course Catalogue", "https://unisi.coursecatalogue.cineca.it/")
                    with col_u2:
                        google_unisi_url = f"https://www.google.com/search?q=site:unisi.coursecatalogue.cineca.it+{primary_ssd}"
                        st.link_button(f"🔍 Cerca {primary_ssd} nel Course Catalogue", google_unisi_url)

            st.markdown("---")
            st.markdown("""
            #### 📌 Risorse e Pagine di Riferimento UNISI
            * **UNISI Course Catalogue CINECA**: [https://unisi.coursecatalogue.cineca.it/](https://unisi.coursecatalogue.cineca.it/)
            * **Manifesto degli Studi e Procedure di Immatricolazione / Corsi Singoli**: [UNISI Immatricolazioni e Procedure](https://www.unisi.it/didattica/immatricolazioni-e-iscrizioni/immatricolazioni-procedure)
            """)

# ---------------------------------------------------------------------
# TAB 4: TABELLA A/1 & EQUIPARAZIONI DL-LM
# ---------------------------------------------------------------------
with tab_a1_equip:
    st.subheader("📚 Tabella A/1 (Esami Omogenei) & Equiparazioni DL-LS-LM (D.I. 9 luglio 2009)")
    
    col_a1, col_eq = st.columns(2)
    
    with col_a1:
        st.markdown("#### 📜 Tabella A/1 - Esami Omogenei (Vecchio Ordinamento)")
        st.write("Ai sensi del D.M. 39/1998 e D.P.R. 19/2016, per le lauree del Vecchio Ordinamento sprovviste di codice SSD, gli insegnamenti elencati nella colonna delle note della Tabella A si intendono ammessi anche se sostenuti con le denominazioni omogenee riportate in Tabella A/1:")
        
        tab_a1_data = [
            {"Classe / Settore": "A-23 / A-24 / A-25 (Linguistica Generale)", "Insegnamento Min. Richiesto": "LINGUISTICA GENERALE", "Esami Omogenei Equiparati": "Glottodidattica, Glottologia, Sociolinguistica, Storia della linguistica"},
            {"Classe / Settore": "A-12 / A-22 (Glottologia)", "Insegnamento Min. Richiesto": "GLOTTOLOGIA", "Esami Omogenei Equiparati": "Linguistica generale, Sociolinguistica, Dialettologia"},
            {"Classe / Settore": "A-01 / A-54 (Storia dell'Arte)", "Insegnamento Min. Richiesto": "STORIA DELL'ARTE", "Esami Omogenei Equiparati": "Teoria delle forme, Semiotica delle arti, Fenomenologia degli stili"},
            {"Classe / Settore": "A-30 / A-53 (Musica)", "Insegnamento Min. Richiesto": "STORIA DELLA MUSICA", "Esami Omogenei Equiparati": "Estetica musicale, Teoria musicale, Musicologia sistematica"}
        ]
        st.dataframe(pd.DataFrame(tab_a1_data), use_container_width=True)
        
    with col_eq:
        st.markdown("#### ⚖️ Equiparazioni Ufficiali Diplomi di Laurea (DL) a LS e LM")
        st.write("Ai sensi del Decreto Interministeriale 9 luglio 2009, i Diplomi di Laurea del Vecchio Ordinamento (DL) sono equiparati alle corrispondenti Lauree Specialistiche (LS) e Magistrali (LM):")
        
        tab_eq_data = [
            {"Diploma di Laurea DL (Vecchio Ord.)": "Lettere", "Laurea Specialistica LS": "15/S, 16/S, 40/S", "Laurea Magistrale LM": "LM-14 (Filologia moderna), LM-15 (Filologia classica)"},
            {"Diploma di Laurea DL (Vecchio Ord.)": "Filosofia", "Laurea Specialistica LS": "17/S, 18/S, 96/S", "Laurea Magistrale LM": "LM-78 (Scienze filosofiche)"},
            {"Diploma di Laurea DL (Vecchio Ord.)": "Matematica", "Laurea Specialistica LS": "45/S", "Laurea Magistrale LM": "LM-40 (Matematica)"},
            {"Diploma di Laurea DL (Vecchio Ord.)": "Fisica", "Laurea Specialistica LS": "20/S", "Laurea Magistrale LM": "LM-17 (Fisica)"},
            {"Diploma di Laurea DL (Vecchio Ord.)": "Giurisprudenza", "Laurea Specialistica LS": "22/S, 102/S", "Laurea Magistrale LM": "LMG/01 (Giurisprudenza)"}
        ]
        st.dataframe(pd.DataFrame(tab_eq_data), use_container_width=True)

# ---------------------------------------------------------------------
# TAB 5: MODULO 24 CFU (D.Lgs. 59/2017) & DPCM 30/60 CFU
# ---------------------------------------------------------------------
with tab_24cfu:
    st.subheader("🧩 Verifica Requisiti 24 CFU (D.Lgs. 59/2017) e Percorsi Abilitanti DPCM 30/60 CFU")
    
    st.write("Il D.Lgs. 59/2017 e il D.M. 616/2017 richiedevano l'acquisizione di almeno **24 CFU/CFA** distribuiti in almeno 3 tra i 4 ambiti antropo-psico-pedagogici. Nel Portfolio Unico attuale i tuoi esami in questi ambiti risultano:")
    
    if len(st.session_state["exams_portfolio"]) > 0:
        ped_cfu = sum(e["cfu"] for e in st.session_state["exams_portfolio"] if e["ssd"].startswith("M-PED"))
        psi_cfu = sum(e["cfu"] for e in st.session_state["exams_portfolio"] if e["ssd"].startswith("M-PSI"))
        ant_cfu = sum(e["cfu"] for e in st.session_state["exams_portfolio"] if e["ssd"] in ["M-DEA/01", "SPS/07", "SPS/08"])
        met_cfu = sum(e["cfu"] for e in st.session_state["exams_portfolio"] if "DIDATTICA" in e["name"].upper() or "METODOLOGI" in e["name"].upper())
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pedagogia (M-PED)", f"{ped_cfu} CFU")
        c2.metric("Psicologia (M-PSI)", f"{psi_cfu} CFU")
        c3.metric("Antropologia (M-DEA/SPS)", f"{ant_cfu} CFU")
        c4.metric("Metodologie Didattiche", f"{met_cfu} CFU")
        
        tot_24 = ped_cfu + psi_cfu + ant_cfu + met_cfu
        ambiti_coperti = sum(1 for v in [ped_cfu, psi_cfu, ant_cfu, met_cfu] if v >= 6)
        
        if tot_24 >= 24 and ambiti_coperti >= 3:
            st.success(f"🟢 **Requisito 24 CFU Potenzialmente Soddisfatto!** Trovati {tot_24} CFU distribuiti su {ambiti_coperti} ambiti disciplinari (minimo 6 CFU per ambito).")
        else:
            st.warning(f"⚠️ **Requisito 24 CFU Non Completo nel Portfolio:** Trovati {tot_24} CFU totali su 24 richiesti (Ambiti coperti con >=6 CFU: {ambiti_coperti}/3).")
    else:
        st.info("Inserisci gli esami nel Portfolio per verificare la copertura dei 24 CFU.")
        
    st.markdown("---")
    st.markdown("""
    #### 💡 Percorsi Abilitanti DPCM 23 Agosto 2023 (30, 36, 60 CFU)
    * **Art. 13 (Seconda Abilitazione - 30 CFU)**: Per chi è già abilitato su altra classe di concorso o specializzato sul sostegno. Accesso diretto al percorso abbreviato da 30 CFU senza dover colmare i debiti della Tabella A.
    * **Percorsi Ordinari da 60 CFU**: Per chi deve conseguire la prima abilitazione all'insegnamento.
    * **Percorsi Transitori da 30/36 CFU**: Riservati a chi possiede i 24 CFU conseguiti entro il 31 ottobre 2022 o 3 anni di servizio nelle scuole paritarie/statali.
    """)


# ---------------------------------------------------------------------
# TAB 6: GUIDA & DOCUMENTAZIONE (README.md)
# ---------------------------------------------------------------------
with tab_readme:
    st.subheader("📖 Guida all'Uso & Documentazione del Progetto")
    if os.path.exists("README.md"):
        try:
            with open("README.md", "r", encoding="utf-8") as f_readme:
                st.markdown(f_readme.read(), unsafe_allow_html=True)
        except Exception as e_rm:
            st.error(f"Errore nella lettura del file README.md: {e_rm}")
    else:
        st.info("ℹ️ Il file README.md non è stato trovato nella cartella principale del progetto.")
