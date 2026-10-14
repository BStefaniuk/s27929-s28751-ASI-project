# Sprint 1 — Problem, dane i poprawny baseline

**Daty:** 15.10.2026 – 29.10.2026 · **Spotkania:** 15.10, 22.10 (pełne), 29.10 (zamknięcie sprintu i start Sprintu 2) · **Deadline:** stan gałęzi `main` na początku zajęć 29.10.2026

## Cel

Zespół ma kontrakt danych, inference-safe input normalization i poprawny baseline w repozytorium
z działającym CI.

## Pytanie architektoniczne

Co jest kontraktem danych naszego systemu i skąd wiemy, że eksperyment jest poprawny?

## Co powinniście rozumieć po tym sprincie

- Czym jest kontrakt danych i kto za jaką jego część odpowiada (prowadząca: target, klasa
  pozytywna, ALLOWED / EXCLUDED FEATURES; zespół: typy cech i reguły input normalization).
- Czym różnią się trzy typy przetwarzania:
  - **input normalization** — działa na pojedynczym rekordzie, bez targetu i statystyk zbioru;
    ta sama funkcja trafi później do API;
  - **training-only filtering** — tylko przy przygotowaniu danych treningowych
    (np. rekordy bez targetu, duplikaty), nigdy przy predykcji;
  - **model preprocessing** — wszystko, co wymaga `fit` (imputacja, skalowanie, kodowanie);
    żyje wewnątrz sklearn Pipeline.
- Dlaczego split train/test musi poprzedzać `fit` i czym grozi leakage.
- Po co baseline (DummyClassifier) i dlaczego sama accuracy często nie wystarcza.
- Dlaczego pełne dane są poza gitem, a w repo jest tylko mała próbka do CI.
- Jak review i CI działają jako bramka jakości.

## CORE

- [ ] Repozytorium zespołu z zasadą review (PR przegląda osoba inna niż autor) i tablicą
  sprintu z ownerami.
- [ ] Dataset z listy w `docs/datasets.md`, wpisany w `project.yaml` (pole `dataset`).
- [ ] Karta projektu w README: dataset, źródło i licencja (z cytowaniem), data pobrania,
  odcisk SHA-256 pliku, informacja o danych osobowych, target i klasa pozytywna, metryka główna
  z uzasadnieniem, użytkownik systemu i decyzja, którą wspiera model.
- [ ] Pełne dane pobrane skryptem `scripts/download_data.py` (poza gitem) i próbka CI
  `data/01_raw/sample.csv` w repozytorium (`scripts/make_ci_sample.py`).
- [ ] Kontrakt danych jako kod: `validate()` przechodzi na próbce, typy cech zadeklarowane
  w `project.yaml`, target binarny z jawnie wskazaną klasą pozytywną.
- [ ] Input normalization w `normalize_input()` (`src/asi_project/data.py`) — reguły dla
  waszego datasetu, testy inference-safe przechodzą.
- [ ] Training-only filtering w `filter_training_rows()` — tylko jeśli dataset tego wymaga;
  decyzja opisana w notebooku 01.
- [ ] EDA w `notebooks/01_eda.ipynb` z obserwacjami i decyzjami.
- [ ] Baseline w `notebooks/02_baseline.ipynb`: DummyClassifier oraz sklearn Pipeline
  z LogisticRegression (`build_baseline_pipeline` w `src/asi_project/model.py`); model
  preprocessing wyłącznie wewnątrz Pipeline; `predict_proba`; accuracy, precision, recall, F1
  i confusion matrix.
- [ ] `metrics.json` z pełnych danych w katalogu głównym repozytorium.
- [ ] Diagram v0 systemu docelowego w `docs/architecture.md`.

W Sprincie 1 nie używamy AutoGluona, W&B ani Kedro.

## OPTIONAL

- Sekcja ograniczeń danych w karcie projektu (zakres czasowy, możliwe obciążenia, braki).
- Dodatkowe analizy EDA.

## Wymagane artefakty

`project.yaml` · karta projektu w `README.md` · `data/01_raw/sample.csv` ·
`src/asi_project/data.py` (input normalization, training-only filtering) ·
`src/asi_project/model.py` (Pipeline) · `notebooks/01_eda.ipynb` ·
`notebooks/02_baseline.ipynb` · `metrics.json` · `docs/architecture.md` · zielone CI.

## Definition of Done

- CI na gałęzi `main` jest zielone, a żaden test z `tests/test_project.py` nie jest pominięty.
- Świeży klon → środowisko → `scripts/download_data.py` → notebook 02 od zera
  (Restart & Run All) → `metrics.json`.
- Test kontraktu danych potwierdza dokładnie dwie klasy targetu i obecność klasy pozytywnej.
- LogisticRegression jest porównana z DummyClassifier na metryce głównej zespołu.
- `metrics.json` pochodzi z pełnych danych (`data_mode: full`) i przechodzi walidację.
- Karta projektu i diagram v0 są uzupełnione (bez znaczników TODO).
- Każda osoba ma owned item z merytorycznym review innej osoby.

Raport punktów sprawdzalnych automatycznie: `python scripts/check_dod.py --sprint 1`
(na zamknięciu sprintu: `python scripts/check_dod.py --sprint 1 --strict`).

## CI

- pre-commit: ruff (lint i formatowanie), nbstripout, podstawowe hooki plików;
- pytest: rejestr datasetów, logika kontraktu, testy projektu (kontrakt na próbce,
  input normalization inference-safe, brak EXCLUDED FEATURES w X, `predict_proba`,
  determinizm Pipeline, kontrakt `metrics.json`);
- po pojawieniu się `metrics.json`: wykonanie notebooka 02 od początku do końca na próbce CI
  i walidacja wyniku;
- raport Definition of Done w podsumowaniu joba (informacyjnie).

Testy projektu są pomijane z komunikatem, dopóki dany krok nie jest wykonany (np. nie ma
jeszcze próbki). Dzięki temu można scalać PR-y częściowe, a raport DoD pokazuje, czego brakuje.

## Smoke test / pre-flight

- Smoke: pełny baseline na świeżym klonie wykonuje osoba inna niż autor baseline'u.
- Pre-flight gotowości do Sprintu 2 (bez pracy z Kedro), u każdej osoby:

  ```bash
  python -m pip install -r requirements/preflight-s2.txt -c constraints.txt
  kedro info
  ```

## Decyzja zespołu

- Target i klasa pozytywna (z kontraktu) oraz metryka główna z uzasadnieniem.
- Które operacje są input normalization, które training-only filtering, a które model
  preprocessing.
- Typy cech: które ALLOWED FEATURES traktujecie jako numeryczne, a które jako kategoryczne.

## ADR

Nie dotyczy. Uzasadnienie metryki głównej jest w karcie projektu. Pierwszy ADR powstaje
w Sprincie 2.

## Indywidualna odpowiedzialność

- Każda osoba ma owned item, np.: kontrakt danych i input normalization / EDA / baseline /
  CI i karta projektu.
- Każda osoba robi co najmniej jedno merytoryczne review cudzego PR.
- Integrator sprintu (rotacyjnie) pilnuje DoD, smoke testu i krótkiego demo na zamknięciu.
- Krótki checkpoint ustny w trakcie zajęć (losowa osoba, „pokaż w repo…”).
- Pary realizują ten sam CORE (więcej owned items na osobę). Pracę w parach oznaczajcie
  w commitach dopiskiem `Co-authored-by:`.

## Krok po kroku

1. **Środowisko (15.10).** W aktywnym środowisku `asi-ml`:

   ```bash
   conda env update -n asi-ml -f environment.yml --prune
   python -m pip install --no-deps -e .
   pre-commit install
   python scripts/check_env.py
   ```

2. **Dataset (15.10).** Przeczytajcie `docs/datasets.md`, wybierzcie dataset, wpiszcie jego id
   w `project.yaml`. Uzupełnijcie pierwszą część karty projektu w README.
3. **Dane.** `python scripts/download_data.py` (zapiszcie SHA-256 w karcie), potem
   `python scripts/make_ci_sample.py` i commit próbki `data/01_raw/sample.csv`.
4. **EDA (notebook 01).** Inspekcja, kontrakt, target, EDA. Na tej podstawie:
   reguły input normalization w `normalize_input()`, decyzja o training-only filtering
   w `filter_training_rows()`, typy cech w `project.yaml`. Uruchomcie `pytest`.
5. **Baseline (22.10).** Zaimplementujcie `build_baseline_pipeline()` w
   `src/asi_project/model.py`, uzupełnijcie notebook 02, uruchomcie go od początku do końca
   na pełnych danych i scalcie PR z `metrics.json`.
6. **Diagram v0.** Uzupełnijcie `docs/architecture.md`.
7. **Domknięcie.** `python scripts/check_dod.py --sprint 1 --strict`, smoke na świeżym klonie
   wykonany przez inną osobę, pre-flight S2 u wszystkich.

Każdą zmianę wprowadzajcie przez gałąź i Pull Request do `main`. Zasady PR i review są
w README.

## Co musi być gotowe przed Sprintem 2

`validate()` i `normalize_input()` z zielonymi testami, baseline Pipeline, skrypt danych,
próbka CI i działające `kedro info` u wszystkich.

## Największe ryzyko

Operacje wymagające `fit` (np. uzupełnianie braków medianą) trafiają do input normalization.
Test inference-safe w CI to wykryje — przegląd tej funkcji jest też tematem checkpointu ustnego.
