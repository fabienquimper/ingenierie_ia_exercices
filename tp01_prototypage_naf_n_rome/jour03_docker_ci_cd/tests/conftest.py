import pytest
import pandas as pd
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.services import matcher as matcher_module


@pytest.fixture(autouse=True)
def load_test_data(tmp_path):
    """Charge des données de test en mémoire avant chaque test."""
    # Crée un CSV de test minimal
    test_data = pd.DataFrame([
        {"code_naf": "62.01Z", "code_rome": "M1805", "name": "Programmation informatique",
         "desc": "Écriture et test de logiciels informatiques sur mesure.", "type": "naf"},
        {"code_naf": "62.02A", "code_rome": "M1802", "name": "Conseil en systèmes informatiques",
         "desc": "Conseil aux entreprises sur les systèmes d'information.", "type": "naf"},
        {"code_naf": "86.21Z", "code_rome": "J1110", "name": "Médecine généraliste",
         "desc": "Consultations de médecine générale en cabinet.", "type": "naf"},
        {"code_naf": "", "code_rome": "M1805", "name": "Développement de logiciels",
         "desc": "Conception et développement d'applications informatiques.", "type": "rome"},
        {"code_naf": "", "code_rome": "M1802", "name": "Expertise systèmes d'information",
         "desc": "Analyse et conseil sur l'architecture des SI.", "type": "rome"},
        {"code_naf": "", "code_rome": "J1110", "name": "Médecine de premier recours",
         "desc": "Consultation et suivi de patients en médecine générale.", "type": "rome"},
    ])
    csv_path = tmp_path / "test_data.csv"
    test_data.to_csv(csv_path, index=False)
    matcher_module.init_matcher(csv_path)
    yield


@pytest.fixture
def client():
    return TestClient(app)
