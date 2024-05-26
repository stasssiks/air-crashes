# Analýza leteckých nehod

Tento projekt se zaměřuje na vytvoření interaktivní webové aplikace pro analýzu a statistiku leteckých nehod pomocí datasetu staženého z Kaggle. Aplikace umožňuje vizualizaci dat a poskytuje různé statistiky a analýzy týkající se leteckých nehod.

## Funkcionalita aplikace

Aplikace nabízí následující funkce:

1. **Analýza havárií podle roku, místa, příčin, provozovatele a typu letadla**: Uživatelé mohou procházet a filtrovat data podle různých kritérií.
2. **Vizualizace míry přežití a predikce na základě historických dat**: Aplikace zahrnuje různé grafy a vizualizace, které ukazují míru přežití a umožňují předpovědi budoucích trendů.
3. **Zobrazení surových a zpracovaných dat**: Uživatelé mohou nahlédnout do původních i zpracovaných dat a exportovat je ve formátech CSV a PDF.

## Instalace a spuštění aplikace

Pro spuštění aplikace je třeba provést následující kroky:

1. **Klonování repozitáře**
    ```bash
    git clone [link]
    cd [folder-name]
    ```

2. **Instalace potřebných balíčků**
    Ujistěte se, že máte nainstalovaný Python. Poté nainstalujte požadované balíčky pomocí příkazu:
    ```bash
    pip install -r requirements.txt
    ```

3. **Spuštění aplikace**
    Aplikaci spustíte příkazem:
    ```bash
    cd app
    cd src
    python app.py
    ```

4. **Přístup k aplikaci**
    Otevřete webový prohlížeč a přejděte na adresu:
    ```
    http://127.0.0.1:8050
    ```
5. **Spuštění testů**
    Testy spustíte příkazem:
    ```bash
    cd ..
    cd tests
    pytest -v test.py
    ```

## Použité nástroje a knihovny

Aplikace je vytvořena s využitím následujících nástrojů a knihoven:

- **Dash**: Framework pro vytváření webových aplikací v Pythonu.
- **Plotly**: Knihovna pro vytváření interaktivních grafů a vizualizací.
- **Pandas**: Knihovna pro manipulaci s daty a analýzu.
- **NumPy**: Knihovna pro numerické výpočty.
- **Scipy**: Knihovna pro vědecké a technické výpočty.
- **Statsmodels**: Knihovna pro statistické modelování a analýzu časových řad.
- **Matplotlib**: Knihovna pro vytváření grafů a vizualizací.
- **Joblib**: Knihovna pro efektivní ukládání a načítání Python objektů.
