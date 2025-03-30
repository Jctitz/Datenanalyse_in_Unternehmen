# Fondsanalyse – Kennzahlen, Peergroups & Machine Learning

## Ziel des Projekts

Ziel dieses Projekts ist es, eine skalierbare Python-Lösung zur Berechnung und Analyse von Fondskennzahlen zu implementieren.

Im Unternehmen werden Fondsanalysen zur Zeit primär mit Excel und VBA durchgeführt. Die Performance und Stabilität wird bei großen Datenmengen, wie sie bei rollierenden Zeitreihenanalysen entstehen, zunhemend schlechter. Daher soll geprüft werden, ob sich die Berechnung der Kennzahlen und die Analysen effizienter und robuster in Python umsetzen lassen.

Zusätzlich wird untersucht, ob Machine-Learning-Modelle für die Klassifikation von Fonds in Peergroups eingesetzt werden können, da dieser Prozes derzeit noch manuell erfolgt.

---

## Überblick & Aufbau

### 1. Datenverarbeitung & Kennzahlenberechnung (`Datenberechnen.ipynb`)
- Datenquellen: `Returns.xlsx` & `Benchmarks.xlsx`
- Berechnung:  
  - Basis-Kennzahlen
  - Benchmark-Fit-Kennzahlen
  - Perzentil-Ränge innerhalb der Peergroup  
  - Korrelationen zu allgemeinen Benchmarks aus unterschiedlichen Anlageklassen
- Ausgabe: Pickle + Excel-Dateien zur Weiterverwendung

→ Siehe auch: [formeln.py](./formeln.py) zur Definition aller Berechnungsfunktionen

---

### 2. Interaktive Visualisierung (`Dashboard.py`)
- Umsetzung mit Streamlit
- Beispiel für Analysen außerhalb von Excel
- Auswahl einzelner Fonds & Zeiträume
- Visualisierung:
  - Rollierende Kennzahlen vs. Benchmark
  - Peergroup-Perzentil-Zeitreihen
  - Benchmark-Fit-Kennzahlen
  - Korrelationen mit Marktbenchmarks

---

### 3. Klassifikation mit Machine Learning (`ML-Modelle.ipynb`)
- Ziel: automatische Klassifikation von Fonds in Peergroups
- Modelle: Random Forest & MLP (Multi-Label-Ansatz)
- Features:
  - Rollierende Kennzahlen
  - Rolling-12M-Blöcke
  - Fondsname-Similarität (TF-IDF)
  - Korrelationen mit Benchmarks
- Clustering: K-Means zur Überprüfung der Peergroup-Zusammensetzung

---

## Inhalt der Dateien

| Datei                                 | Beschreibung |
|--------------------------------------|--------------|
| `Datenberechnen.ipynb`               | Hauptpipeline zur Berechnung aller Kennzahlen |
| `formeln.py`                         | Modul mit allen mathematischen Formeln & Metriken |
| `Dashboard.py`                       | Interaktive Analyse-Oberfläche mit Streamlit |
| `ML-Modelle.ipynb`                   | Machine Learning zur Klassifikation & Clusteranalyse |
| `Daten/Returns.xlsx`                 | Fondsdaten & Renditezeitreihen |
| `Daten/Benchmarks.xlsx`              | Benchmarkdaten (Peergroup + allgemeine Marktindizes) |
| `Ergebnisse/`                        | Output: Pickle- & Excel-Dateien für weitere Nutzung |
| `Formeln_Glossar.pdf`                | Glossar der verwendeten Kennzahlen (interne Quelle) |
| `Präsentation_Datenanalyse_in_Unternehmen.pptx` | Präsentation zum Projektfortschritt |

---

## Kommentare zu zusätzlichen Dateien

- `Formeln_Glossar.pdf`: Enthält die Definitionen und Formeln der verwendeten Kennzahlen – dient als fachliche Grundlage aus dem Unternehmen.
- `Präsentation_Datenanalyse_in_Unternehmen.pptx`: Präsentation aus der Vorlesung. (Die Anmerkungen nach der Präsentation wurden noch mit eingearbeitet)

---

## Installation & Nutzung

### Voraussetzungen
- Python 3.9 oder höher
- Empfohlene Installation in virtueller Umgebung

### Abhängigkeiten installieren
```bash
pip install -r requirements.txt
