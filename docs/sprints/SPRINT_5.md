# Sprint 5 — System lokalny

**Daty:** 17.12.2026 – 07.01.2027 · **Spotkania:** 17.12 (start sprintu), 07.01 (zamknięcie sprintu i start Sprintu 6) · **Deadline:** stan gałęzi `main` na początku zajęć 07.01.2027

Realny czas pracy to ok. tydzień (17–23.12). Przerwa świąteczna 24.12.2026 – 06.01.2027 nie jest
planowanym czasem pracy — zakres sprintu da się zamknąć do 23.12.

## Cel

UI, API i Postgres uruchamiają się lokalnie jedną komendą, z konfiguracją przez zmienne
środowiskowe i healthcheckami.

## Pytanie architektoniczne

Jak usługi się odnajdują i skąd biorą konfigurację, żeby system działał tak samo na każdej
maszynie?

## Co powinniście rozumieć po tym sprincie

- Usługi odnajdują się po nazwach w sieci.
- Ten sam obraz działa z różną konfiguracją.
- Stan żyje w osobnej usłudze z wolumenem.
- Healthchecki i kolejność startu.
- Ten sam kontrakt persistence działa na innym backendzie.

## CORE

- [ ] Streamlit: formularz zgodny z kontraktem API, wynik i prawdopodobieństwo; adres API
  i token z env.
- [ ] Dockerfile UI bez zależności ML.
- [ ] docker compose z usługami `api`, `ui` i `db` (Postgres z nazwanym wolumenem);
  sterownik PostgreSQL w obrazie API.
- [ ] Konfiguracja przez env: hasła i token w `.env`, nie w pliku compose.
- [ ] Healthchecki.
- [ ] Automatyczny smoke całego systemu lokalnego w trybie `sql` (warstwa API).
- [ ] Manualny UI check (opis niżej).

Jedyną nową cięższą koncepcją architektoniczną jest docker compose. Streamlit i Postgres są
silnie scaffoldowane i używane w minimalnym zakresie.

## OPTIONAL

- Historia predykcji w UI.
- `docker compose config` w CI.

## Miejsce w repozytorium

Scaffold przygotowany od startu Sprintu 1 (README w katalogach):

- `ui/` — interfejs Streamlit
- `docker/ui.Dockerfile`, `docker-compose.yml` — obraz UI i system lokalny
- `.env.example` — uzupełniona konfiguracja
- `docs/adr/` — uzupełnienie ADR-3

## Wymagane artefakty

Kod UI · Dockerfile UI · `docker-compose.yml` · uzupełnione `.env.example` ·
„Docker quickstart” w README · wynik smoke · uzupełniony ADR-3.

## Definition of Done

- Świeży klon + `.env` z przykładu + `docker compose up --build` → automatyczny smoke zielony
  w trybie `sql` (rekord zapisany w Postgresie).
- UI check wykonany: Streamlit się uruchamia, formularz jest dostępny, co najmniej jedna
  predykcja wykonana ręcznie przez UI, wynik w UI odpowiada kontraktowi API.
- W repozytorium nie ma sekretów.
- ADR-3 jest uzupełniony.

## CI

Jak w Sprincie 4.

## Smoke test / pre-flight

- Automatyczny smoke (ten sam skrypt co w Sprincie 4) na compose w trybie `sql`. Skrypt nie
  testuje Streamlita.
- UI check: manualny check albo demo na zamknięciu sprintu (07.01), bez Selenium, Playwright
  ani podobnych frameworków.
- Pre-flight gotowości do Sprintu 6 (do 07.01, najlepiej przed 23.12): push obrazu API do
  Artifact Registry jako `linux/amd64` i hello deploy na Cloud Run. To przygotowanie, a nie
  główny efekt sprintu.

## Decyzja zespołu

Nazwy i źródła zmiennych środowiskowych, healthchecki, wolumeny.

## ADR

**ADR-3 — uzupełnienie:** stan, persistence i konfiguracja w lokalnym systemie wielousługowym.

## Indywidualna odpowiedzialność

Owned items, np.: UI / compose i Postgres / smoke i README / pre-flight chmury i uzupełnienie
ADR-3. Merytoryczne review, rotacyjny integrator, krótki checkpoint ustny.

## Poziom wsparcia

Niski: szkielety z TODO i kryteria rezultatu. Referencja compose jest dostępna od startu
sprintu, bo w przerwie świątecznej nie ma wsparcia.

## Co musi być gotowe przed Sprintem 6

Działający compose, obraz w Artifact Registry, działający hello deploy, uzupełniony ADR-3.

## Największe ryzyko

Realnie tylko tydzień pracy przed przerwą. Ograniczenie: jedna nowa cięższa koncepcja (compose),
GCP przygotowane już w Sprincie 4, zakres możliwy do zamknięcia do 23.12.
