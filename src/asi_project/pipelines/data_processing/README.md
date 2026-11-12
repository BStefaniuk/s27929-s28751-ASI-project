
# Data Processing — Sprint 2

Pipeline przygotowuje dane Bank Marketing do modelowania.

## Etapy

1. **Walidacja** — sprawdzenie zgodności danych z kontraktem datasetu.
2. **Normalizacja** — uporządkowanie wartości tekstowych i oznaczeń braków.
3. **Filtrowanie** — usunięcie rekordów bez wartości targetu.

Wykorzystujemy funkcje przygotowane w Sprincie 1 w `asi_project.data`.

## Uruchomienie

Pełny zbiór danych:

```bash
kedro run --pipelines data_processing
```

Próbka CI:

```bash
kedro run --env ci --pipelines data_processing
```

## Wynik

Pipeline zapisuje przygotowane dane do `data/02_intermediate/processed_data.csv`.

W trybie CI wynik jest zapisywany w `data/02_intermediate/processed_ci.csv`.

## Testy

```bash
python -m pytest -q
```

Podczas lokalnego sprawdzenia wszystkie 47 testów zakończyły się sukcesem.
