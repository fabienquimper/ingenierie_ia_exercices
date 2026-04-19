import pytest
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.services import matcher as matcher_module


@pytest.fixture(autouse=True)
def load_test_data(tmp_path):
    """Charge 3 CSV de test minimaux avant chaque test."""
    naf_data = pd.DataFrame([
        {"code_naf": "62.01Z", "name": "Programmation informatique",
         "desc": "Écriture et test de logiciels informatiques sur mesure."},
        {"code_naf": "62.02A", "name": "Conseil en systèmes informatiques",
         "desc": "Conseil aux entreprises sur les systèmes d'information."},
        {"code_naf": "86.21Z", "name": "Médecine généraliste",
         "desc": "Consultations de médecine générale en cabinet."},
    ])
    rome_data = pd.DataFrame([
        {"code_rome": "M1805", "name": "Développement de logiciels",
         "desc": "Conception et développement d'applications informatiques."},
        {"code_rome": "M1802", "name": "Expertise systèmes d'information",
         "desc": "Analyse et conseil sur l'architecture des SI."},
        {"code_rome": "J1110", "name": "Médecine de premier recours",
         "desc": "Consultation et suivi de patients en médecine générale."},
    ])
    matching_data = pd.DataFrame([
        {"code_naf": "62.01Z", "code_rome": "M1805", "name": "Dev logiciel / Programmation",
         "desc": "Correspondance informatique logiciels."},
        {"code_naf": "62.02A", "code_rome": "M1802", "name": "SI / Conseil",
         "desc": "Correspondance systèmes d'information conseil."},
        {"code_naf": "86.21Z", "code_rome": "J1110", "name": "Médecine / Généraliste",
         "desc": "Correspondance médecine générale consultations."},
    ])

    naf_path = tmp_path / "naf.csv"
    rome_path = tmp_path / "rome.csv"
    matching_path = tmp_path / "matching.csv"
    naf_data.to_csv(naf_path, index=False)
    rome_data.to_csv(rome_path, index=False)
    matching_data.to_csv(matching_path, index=False)

    matcher_module.init_matcher(naf_path, rome_path, matching_path)
    yield


@pytest.fixture
def client():
    return TestClient(app)
