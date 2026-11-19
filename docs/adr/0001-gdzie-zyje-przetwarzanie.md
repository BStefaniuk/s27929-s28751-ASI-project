# ADR-1: Podział przetwarzania danych

- **Status:** przyjęty
- **Sprint:** S2
- **Autor:** Bartosz Stefaniuk
- **Recenzent:** Gabriela Anioł

## Kontekst

Przenosimy trening Bank Marketing z notebooka do Kedro. Chcemy zachować te same zasady przygotowania danych i móc później wykorzystać część kodu w API. Kontrakt wymaga podziału chronologicznego oraz wykluczenia cechy duration.

## Rozważone opcje

1. Umieszczenie całego przetwarzania w notebooku lub jednej funkcji.
2. Oddzielenie normalizacji wejścia, filtrowania danych treningowych i przetwarzania wewnątrz modelu.

## Decyzja

Wybieramy drugi wariant:

- **Input normalization** pozostaje w `normalize_input()` w `data.py`. Zamienia unknown w wybranych kolumnach oraz pdays = -1 na braki danych. Działa bez targetu i statystyk zbioru, dlatego będzie wspólna dla treningu i przyszłego API.
- **Training-only filtering** pozostaje w `filter_training_rows()`. Usuwa rekordy bez targetu podczas przygotowania danych do treningu. Nie będzie używane podczas predykcji.
- **Model preprocessing** pozostaje wewnątrz sklearn Pipeline: imputacja, skalowanie i kodowanie kategorii dopasowują się wyłącznie do zbioru treningowego.

Kedro łączy te funkcje z podziałem danych, treningiem i ewaluacją. Ścieżki plików definiujemy w Data Catalog, a parametry splitu przekazujemy przez konfigurację Kedro.

| Wielkość | Wartość | Skąd pochodzi |
|---|---|---|
| Liczba rekordów przed i po filtrowaniu | 45 211 → 45 211 | notebook EDA, sekcja 7 |
| Rekordy z pdays = -1 | 36 954 | inspekcja danych w notebooku EDA |
| Podział pełnych danych | 36 168 train, 9 043 test | evaluation_metrics.json |

Liczna grupa z pdays = -1 uzasadnia zachowanie rekordów i obsługę braków zamiast ich usuwania.

## Odrzucone alternatywy

Odrzucamy pozostawienie całej logiki w notebooku, ponieważ wymagałoby ręcznego wykonywania komórek i utrudniało ponowne użycie kodu. Odrzucamy też imputację i skalowanie przed splitem, ponieważ wykorzystywałyby informacje ze zbioru testowego.

## Konsekwencje

Trening można uruchomić jedną komendą. Przy predykcji trzeba będzie zastosować tę samą normalizację i użyć zapisanego sklearn Pipeline, bez ponownego fitowania. Zmiany reguł przygotowania danych wymagają aktualizacji testów i ponownego treningu.

## Historia

| Data | Zmiana |
|---|---|
| 2026-11-19 | Przyjęcie ADR-1 |
