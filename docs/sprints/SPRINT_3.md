# Sprint 3 — Eksperymenty, wybór modelu i artefakt

**Daty:** 12.11.2026 – 26.11.2026 · **Spotkania:** 12.11 (start sprintu), 19.11 (pełne), 26.11 (zamknięcie sprintu i start Sprintu 4) · **Deadline:** stan gałęzi `main` na początku zajęć 26.11.2026

## Cel

Zespół porównuje eksperymenty, świadomie wybiera model produkcyjny i oddaje go jako pakiet
ładowalny poza treningiem.

## Pytanie architektoniczne

Który model idzie dalej i w jakiej postaci opuszcza środowisko treningowe?

## Co powinniście rozumieć po tym sprincie

- Lineage: dane + kod + parametry → metryka → artefakt.
- Kryteria niefunkcjonalne wyboru modelu.
- Wersje i aliasy artefaktów.
- Kontrakt artefaktu i zgodność bibliotek między treningiem a serwowaniem.

## CORE

- [ ] Runy W&B z pipeline'u: parametry, metryki, git SHA oraz prosty identyfikator wersji
  danych (fingerprint, hash albo identyfikator snapshotu); pierwszym runem jest baseline.
- [ ] AutoGluon jako node z limitem czasu: co najmniej dwie sensowne konfiguracje plus baseline.
- [ ] Świadomy wybór modelu produkcyjnego na podstawie tabeli: metryka główna, czas predykcji,
  rozmiar artefaktu, pamięć przy ładowaniu. Model produkcyjny nie musi być AutoGluonem.
- [ ] Pakiet modelu: katalog z modelem i `metadata.json` (m.in. cechy, target i klasa
  pozytywna, metryki, git SHA, fingerprint danych, wersje bibliotek), zapisywany i wczytywany
  wspólnymi funkcjami; w W&B jako Artifact z aliasem `production`.
- [ ] Smoke artefaktu w czystym procesie.
- [ ] Minimalna Model Card.
- [ ] ADR-2.

## OPTIONAL

- W&B Sweeps.
- Feature importance.
- Preset `optimize_for_deployment`.
- Pełne wersjonowanie datasetu przez W&B Data Artifacts.
- AutoGluon jako model produkcyjny.

## Miejsce w repozytorium

Scaffold przygotowany od startu Sprintu 1 (README w katalogach):

- `src/asi_project/pipelines/data_science/` — tracking W&B i node AutoGluona
- `conf/base/` — parametry eksperymentów
- pakiet modelu — kontrakt opisany w `src/asi_project/README.md`
- smoke modelu — kontrakt opisany w `scripts/README.md`
- `docs/model_card.md` — Model Card
- `docs/adr/` — ADR-2

## Wymagane artefakty

Projekt W&B · porównanie runów · pakiet `production` · skrypt smoke modelu ·
`docs/model_card.md` · ADR-2.

## Definition of Done

- Pakiet `production` ładuje się w świeżym środowisku wyłącznie z W&B i zwraca predykcje
  dla próbki.
- ADR-2 i Model Card są zmergowane.

## CI

Jak w Sprincie 2, a dodatkowo: `WANDB_MODE=disabled`; AutoGluon w środowisku `ci` wyłączony
parametrem albo z kilkusekundowym limitem; test zapisu i odczytu pakietu modelu.

## Smoke test / pre-flight

Pobranie `production` → wczytanie → predykcja 5 wierszy → sprawdzenie schematu odpowiedzi.
To jest wejście dla API w Sprincie 4.

## Decyzja zespołu

Model produkcyjny i kryteria wyboru.

## ADR

**ADR-2** — wybór modelu produkcyjnego i jego postać jako artefaktu, poparte liczbami
z własnego W&B.

## Indywidualna odpowiedzialność

Owned items, np.: eksperymenty / tracking / pakiet i smoke / Model Card i ADR-2.
Merytoryczne review, rotacyjny integrator, krótki checkpoint ustny.

## Poziom wsparcia

Średni: PR referencyjny na starcie sprintu, ale projekt eksperymentów i kryteria wyboru
należą do zespołu.

## Co musi być gotowe przed Sprintem 4

Zielony smoke pakietu modelu. Dane dostępowe GCP (student credentials) przekazane zespołom —
o ile pozwala na to wynik pre-flightu prowadzącej.

## Największe ryzyko

Ciężki sprint z jednym pełnym spotkaniem. Ograniczenie: AutoGluon sprawdzony już w Sprincie 2,
limity czasu treningu, model sklearn dopuszczalny jako produkcyjny, kontrakt pakietu
dostarczony z referencji.
