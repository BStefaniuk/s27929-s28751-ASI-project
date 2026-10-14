# Sprint 4 — Usługa, stan i pierwszy kontener

**Daty:** 26.11.2026 – 17.12.2026 · **Spotkania:** 26.11 (start sprintu), 03.12 i 10.12 (pełne), 17.12 (zamknięcie sprintu i start Sprintu 5) · **Deadline:** stan gałęzi `main` na początku zajęć 17.12.2026

## Cel

Model jest dostępny przez usługę z walidowanym kontraktem i prostym tokenem dostępu, zapisuje
predykcje przez konfigurowalne persistence i działa w kontenerze.

## Pytanie architektoniczne

Jaki jest kontrakt między modelem a światem i gdzie trzymamy stan?

## Co powinniście rozumieć po tym sprincie

- Walidacja na granicy usługi i semantyka błędów 4xx/5xx.
- Model ładowany raz.
- Na wejściu usługi działa input normalization; model preprocessing jest wewnątrz modelu.
- Różnica między sekretem a zwykłą konfiguracją.
- Stan poza procesem i jawne tryby persistence.
- Wstrzykiwanie zależności w testach; obraz kontenera jako artefakt.

## CORE

Kontrakt (start 26.11):

- [ ] `/healthz` zwraca status, wersję modelu i tryb persistence.
- [ ] `/predict` ze schematem Pydantic zespołu; odpowiedź: etykieta, prawdopodobieństwo klasy
  pozytywnej, wersja modelu.
- [ ] Model wczytywany raz; input normalization na wejściu.

Stan i konfiguracja (03.12):

- [ ] Warstwa persistence (repository) z trybami `sql` i `disabled`.
- [ ] Model tabeli predykcji w SQLAlchemy (bez ręcznego DDL); SQLite w pliku poza obrazem.
- [ ] Ustawienia przez pydantic-settings z `env_file`; `.env.example` bez prawdziwego sekretu.
- [ ] Prosty token dostępu do usługi (service API key, `API_KEY`): nagłówek wymagany przez
  `/predict`; `/healthz` pozostaje otwarte. To nie jest uwierzytelnianie użytkowników.
- [ ] Jedna linia logu JSON na każdą predykcję.
- [ ] Testy: błąd walidacji 422, brak lub zły token 401, zapis przez repository na tymczasowej
  bazie, tryb `disabled`.

Kontener (10.12):

- [ ] Dockerfile API: bez condy, wersje bibliotek modelu takie jak w treningu, port z `$PORT`,
  `.dockerignore`.
- [ ] Decyzja, jak model trafia do usługi i obrazu — szkic ADR-3.
- [ ] Wolumen na plik SQLite; test z limitem pamięci (`--memory`).
- [ ] Pierwsza wersja wspólnego skryptu smoke (używanego do Sprintu 6).

Pre-flight GCP (do 17.12) — patrz niżej.

## OPTIONAL

- `GET /predictions`.
- Alembic.
- Budowanie obrazu w CI.

## Miejsce w repozytorium

Scaffold przygotowany od startu Sprintu 1 (README w katalogach):

- `src/asi_project/api/` — usługa, schematy, ustawienia, repository
- `tests/api/` — testy API
- `docker/api.Dockerfile`, `.dockerignore`, `.env.example` — kontener API
- wspólny skrypt smoke — kontrakt opisany w `scripts/README.md`
- `docs/adr/` — szkic ADR-3

## Wymagane artefakty

Kod usługi API · repository · testy API · Dockerfile API · `.env.example` · skrypt smoke ·
sekcje README: API, konfiguracja, persistence · szkic ADR-3.

## Definition of Done

- `docker run` z `.env` → smoke zielony w trybie `sql`: `/healthz` raportuje `sql`,
  `/predict` z tokenem zwraca poprawny kontrakt, rekord jest zapisany w SQLite na wolumenie.
- `/predict` bez tokenu zwraca 401.
- Testy API przechodzą w CI.
- W repozytorium nie ma sekretów.
- Pre-flight GCP zespołu jest wykonany.
- Szkic ADR-3 jest zmergowany.

## CI

Dochodzą testy API bez prawdziwego modelu i bez prawdziwej bazy.

## Smoke test / pre-flight

Automatyczny smoke (jeden skrypt od Sprintu 4 do Sprintu 6, wyłącznie warstwa API):

1. `/healthz`;
2. odczyt trybu persistence;
3. `/predict` z tokenem;
4. kontrakt odpowiedzi: etykieta, prawdopodobieństwo klasy pozytywnej, wersja modelu;
5. tryb `sql`: rekord zapisany w bazie wskazanej przez tę samą konfigurację co usługa;
   tryb `disabled`: brak wymogu zapisu.

W Sprincie 4 smoke działa na kontenerze w trybie `sql`.

Pre-flight GCP zespołu (wchodzi do DoD): dostęp na student credentials, działający projekt,
billing lub kredyty (jeśli są wymagane), włączone API, Artifact Registry i prosty test
techniczny. Rola Viewer dla prowadzącej jest warunkowa: wykorzystujemy ją tylko wtedy, gdy
pozwalają na to uprawnienia; jej brak nie wpływa na zaliczenie. Zakres zależy od wyniku
pre-flightu prowadzącej (`docs/GCP_CREDENTIALS_PREFLIGHT.md`).

Pre-flight gotowości do Sprintu 5: `docker compose version`.

## Decyzja zespołu

Kontrakt API, schemat rekordu predykcji, co jest sekretem, jak model trafia do usługi i obrazu.

## ADR

**ADR-3 — szkic:** jak model trafia do usługi i obrazu.

## Indywidualna odpowiedzialność

Owned items, np.: kontrakt / persistence / testy i token / Docker i szkic ADR-3.
Merytoryczne review, rotacyjny integrator, krótki checkpoint ustny.

## Poziom wsparcia

Średnio-niski: demo na starcie sprintu; zespół najpierw projektuje kontrakt i schemat,
PR referencyjny pojawia się dopiero po pierwszym spotkaniu.

## Co musi być gotowe przed Sprintem 5

Obraz API, skrypt smoke, `.env.example`, działający projekt GCP, szkic ADR-3.

## Największe ryzyko

Najwięcej nowych elementów w jednym sprincie — jedna rzecz na spotkanie. Problemy z kredytami
i uprawnieniami GCP — pre-flight przed świętami, gdy jest jeszcze wsparcie.
