# Sprint 6 — Wdrożenie, obserwowalność i release

**Daty:** 07.01.2027 – 21.01.2027 · **Spotkania:** 07.01 (start sprintu), 14.01 (pełne — release candidate), 21.01 (finał) · **Deadline:** release candidate 14.01.2027 (wewnętrzny, twardy), finał i release v1.0 21.01.2027

## Cel

API i UI działają publicznie w Cloud Run, z tokenem dostępu z Secret Managera, jawnym trybem
persistence, logami i smoke testem. Projekt jest wydany jako v1.0.

## Pytanie architektoniczne

Co się zmienia, gdy system jest publiczny, bezstanowy i działa na cudzej platformie?

## Co powinniście rozumieć po tym sprincie

- Skalowanie do zera i cold start.
- Różnica między sekretem a konfiguracją.
- System plików kontenera nie jest trwały.
- Ograniczenia platformy.
- Obserwowalność po wdrożeniu; release i powrót do poprzedniej wersji.

## CORE

- [ ] Deploy API i UI przez `deploy.sh` zgodnie z checklistą ograniczeń platformy:
  - port z `$PORT`;
  - architektura obrazu `linux/amd64`;
  - pamięć dobrana testem `--memory`;
  - min instances i cold start;
  - dla Streamlita dodatkowo: WebSocket, request timeout rzędu minut, session affinity,
    jeśli jest potrzebna.
- [ ] `API_KEY` przechowywany w Secret Managerze; obie usługi w Cloud Run otrzymują go przez
  integrację z Secret Managerem. Reszta konfiguracji przez env.
- [ ] Persistence: bez zewnętrznej bazy tryb `disabled` ustawiony jawnie; `/healthz` go
  raportuje; SQLite w Cloud Run jest blokowany przy starcie usługi.
- [ ] Logi predykcji w Cloud Logging.
- [ ] Smoke na adresach URL usług.
- [ ] README, aktualna Model Card, finalny ADR-3.
- [ ] Release v1.0 z notatkami.
- [ ] Demo.

## OPTIONAL

- Trwała baza w chmurze (Cloud SQL albo zewnętrzny Postgres; `DATABASE_URL` jako sekret).
- Deploy z CI.
- Alerty i dashboard.
- Model pobierany z W&B przy starcie usługi.

## Miejsce w repozytorium

Scaffold przygotowany od startu Sprintu 1 (README w katalogach):

- `deploy/` — `deploy.sh` i checklista ograniczeń platformy
- `docs/GCP_CREDENTIALS_PREFLIGHT.md` — wynik pre-flightu prowadzącej
- `docs/adr/` — finalny ADR-3

## Wymagane artefakty

Adresy URL usług · `deploy.sh` · sekret w Secret Managerze · logi · wynik smoke · README ·
finalny ADR-3 · release v1.0.

## Definition of Done

- 14.01 (release candidate): API i UI wdrożone; smoke zielony w trybie skonfigurowanym dla
  chmury — w trybie `disabled` predykcja działa i ma poprawny kontrakt bez zapisu stanu,
  a w trybie `sql` (przy OPTIONAL bazie w chmurze) rekord jest zapisany.
- Działanie UI na Cloud Run potwierdzone tym samym manualnym UI checkiem co w Sprincie 5
  (podczas release candidate i demo).
- 21.01: finalny smoke, dokumentacja, release v1.0, demo.
- `API_KEY` nie jest hardcodowany, nie trafia do repozytorium i nie jest wpisywany ręcznie
  jako jawna konfiguracja; usługi otrzymują go przez integrację z Secret Managerem.

## CI

Jak dotąd. Deploy z CI jest OPTIONAL.

## Smoke test / pre-flight

Ten sam skrypt smoke co od Sprintu 4, uruchomiony na adresach URL 14.01 i 21.01, w trybie
raportowanym przez `/healthz`. Wykonalność usług GCP na student credentials potwierdza
wcześniej pre-flight prowadzącej (`docs/GCP_CREDENTIALS_PREFLIGHT.md`).

## Decyzja zespołu

Zasoby usług (pamięć, timeout, min instances), co jest sekretem, tryb persistence w chmurze.

## ADR

**ADR-3 — finalizacja:** sekrety, cloud persistence i deployment.

## Indywidualna odpowiedzialność

Owned items, np.: deploy API / deploy UI i sekret / logi i smoke / dokumentacja, finalny ADR-3
i release. Na demo pytanie trafia do losowej osoby z zespołu.

## Poziom wsparcia

Minimalny: checklista ograniczeń platformy i szkielet `deploy.sh`, bez rozwiązania
referencyjnego.

## Największe ryzyko

Pierwszy deployment musi się udać między 07.01 a 14.01. Ograniczenie: pre-flighty ze Sprintów
4 i 5, wdrażane są obrazy, które już działają lokalnie, a 14.01 jest twardym wewnętrznym
terminem. 21.01 nie jest dniem pierwszego działającego deploymentu.
