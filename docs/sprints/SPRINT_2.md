# Sprint 2 — Reprodukowalny pipeline

**Daty:** 29.10.2026 – 12.11.2026 · **Spotkania:** 29.10 (start sprintu), 05.11 (pełne), 12.11 (zamknięcie sprintu i start Sprintu 3) · **Deadline:** stan gałęzi `main` na początku zajęć 12.11.2026

## Cel

`kedro run` odtwarza od surowych danych model i metryki, z jawnie rozdzielonymi input
normalization, training-only filtering i model preprocessing.

## Pytanie architektoniczne

Gdzie żyje logika przetwarzania, żeby działała tak samo przy każdym uruchomieniu — i przy
predykcji?

## Co powinniście rozumieć po tym sprincie

- Pipeline jako graf czystych funkcji.
- Podział na kod, konfigurację i dane; środowiska konfiguracji (`base`, `local`, `ci`).
- Które przetwarzanie powtarza się przy predykcji (input normalization), które wykonuje się
  tylko przy treningu (training-only filtering), a które jest częścią modelu
  (model preprocessing).

## CORE

- [ ] Projekt Kedro w przypiętej wersji (`requirements/preflight-s2.txt`).
- [ ] Pipeline `data_processing`: walidacja kontraktu → input normalization → training-only
  filtering (funkcje z `src/asi_project/data.py` jako nody).
- [ ] Pipeline `data_science`: split zgodny z kontraktem → trening sklearn Pipeline
  (model preprocessing i model) → ewaluacja.
- [ ] Catalog z klasami `…Dataset` i plik `parameters.yml` (m.in. parametry splitu).
- [ ] Środowisko konfiguracji `ci` na próbce; pełne dane w `base` / `local`.
- [ ] Testy nodów.
- [ ] ADR-1.

## OPTIONAL

- kedro-viz.
- Hooki Kedro.

## Miejsce w repozytorium

Scaffold przygotowany od startu Sprintu 1 (README w katalogach):

- `conf/` (`base`, `local`, `ci`) — konfiguracja Kedro
- `src/asi_project/pipelines/` (`data_processing`, `data_science`) — pipeline'y
- `data/02_intermediate/`, `data/06_models/`, `data/08_reporting/` — wyjścia (poza gitem)
- `tests/pipelines/` — testy nodów
- `docs/adr/` — ADR-1

## Wymagane artefakty

Projekt Kedro · `conf/ci/` · model i metryki jako wyjścia pipeline'u (poza gitem) · testy
nodów · ADR-1 w `docs/adr/` · sekcja „Kedro quickstart” w README.

## Definition of Done

- `kedro run --env ci` przechodzi w CI.
- Lokalny `kedro run` na pełnych danych daje model i metryki.
- Notebook przestaje być źródłem prawdy: baseline powstaje w pipeline.
- ADR-1 jest zmergowany (autor ≠ recenzent).
- Pre-flight Sprintu 3 jest wykonany u każdej osoby.

## CI

Jak w Sprincie 1, a dodatkowo `kedro run --env ci` i testy nodów.

## Smoke test / pre-flight

- Smoke: świeży klon → `kedro run`; metryki zgodne ze Sprintem 1 w granicach tolerancji.
- Pre-flight gotowości do Sprintu 3 (koniec sprintu, bez pełnych eksperymentów):
  - konto W&B, `wandb login` i dołączenie do projektu zespołu;
  - instalacja przypiętego AutoGluona, import i mini-trening:

    ```bash
    python -m pip install -r requirements/preflight-s3.txt -c constraints.txt
    python scripts/check_env.py --autogluon
    ```

## Decyzja zespołu

Granice nodów, co jest parametrem, przypisanie każdej operacji do jednego z trzech typów
przetwarzania.

## ADR

**ADR-1** — gdzie żyje przetwarzanie i dlaczego: input normalization jest wspólne dla treningu
i API, training-only filtering działa tylko przy treningu, model preprocessing jest częścią
modelu.

## Indywidualna odpowiedzialność

Owned items, np.: `data_processing` / `data_science` / testy i CI / ADR-1 (autor ≠ recenzent).
Pre-flight AutoGluona wykonuje każda osoba. Merytoryczne review, rotacyjny integrator,
krótki checkpoint ustny.

## Poziom wsparcia

Średnio-wysoki: na starcie sprintu PR referencyjny i omówienie migracji notebooka do Kedro.

## Co musi być gotowe przed Sprintem 3

Odtwarzalny `kedro run`, działające W&B u wszystkich, zainstalowany i sprawdzony AutoGluon.

## Największe ryzyko

Tylko jedno pełne spotkanie na Kedro. Ograniczenie: PR referencyjny, minimalny zakres
(dwa pipeline'y), pre-flight `kedro info` już w Sprincie 1. Instalacja AutoGluona:
przypięte wersje i mini-trening zamiast samego importu.
