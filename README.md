## 1. Cel projektu
Celem projektu jest implementacja rozproszonego systemu komunikacji. System pozwala na tworzenie oddzielnych chatów rozmów, ustawianie nazw oraz jednoczesną obsługę wielu użytkowników.

## 2. Zastosowane mechanizmy

* **Protokół TCP/IP**: Komunikacja oparta jest na gniazdach sieciowych (`socket`), co pozwala na fizyczne rozproszenie klientów i serwera na różne maszyny w sieci lokalnej lub internecie.
* **Architektura Klient-Serwer**: Centralny węzeł (serwer) zarządza stanem połączeń, routingiem wiadomości do odpowiednich pokoi oraz synchronizacją nazw użytkowników.

* **Wielowątkowość**: 
* **Na serwerze**: Każde nowe połączenie przychodzące jest obsługiwane w osobnym wątku (`threading.Thread`), dzięki czemu operacje wejścia/wyjścia jednego użytkownika nie blokują pozostałych.
* **U klienta**: Interfejs graficzny działa w głównym wątku, podczas gdy odbieranie wiadomości z sieci odbywa się w równoległym wątku tła, co zapobiega "zamrażaniu" okna aplikacji.

## 3. Funkcje systemu
* **Prywatne pokoje**: Możliwość dołączenia do konkretnego kanału (np. "projekt", "ogólny"). Wiadomości są filtrowane i trafiają tylko do osób w tym samym pokoju.

## 4. Instrukcja uruchomienia (VS Code)

### Krok 1: Przygotowanie środowiska
1. Upewnij się, że masz zainstalowanego Pythona w wersji 3.x.
2. Otwórz folder projektu w VS Code.
3. Jeśli korzystasz ze środowiska wirtualnego, aktywuj je komendą:
   ```powershell
   .\venv\Scripts\activate

## 5. Opis interfejsu i funkcji (Instrukcja użytkownika)

Aplikacja kliencka składa się z trzech głównych sekcji, które zarządzają stanem połączenia i komunikacją:

### Sekcja A: Logowanie i Przynależność (Górny Panel)
* **Pole Nick**: Służy do identyfikacji użytkownika w sieci. Po wpisaniu nazwy i kliknięciu **"Ustaw"**, klient wysyła do serwera komendę `/nick [nazwa]`. Serwer aktualizuje te dane w słowniku `clients`.
* **Pole Pokój**: Pozwala na izolację rozmów. Po kliknięciu **"Dołącz"**, wysyłana jest komenda `/join [nazwa_pokoju]`. Od tego momentu serwer filtruje wiadomości tak, aby trafiały one tylko do osób o tym samym identyfikatorze pokoju.

### Sekcja B: Wysyłanie Wiadomości (Dolny Panel)
* **Pole Wiadomość**: Główne pole wejściowe. Użytkownik może zatwierdzić tekst klawiszem **Enter** lub przyciskiem **"Wyślij"**.
* **Mechanizm wysyłki**: Tekst jest kodowany do formatu binarnego (`.encode()`) i przesyłany przez gniazdo sieciowe (Socket) do serwera, który pełni rolę brokera wiadomości.

## 6. Jak uruchomić system?

1.  **Uruchom serwer** otwórz nowy terminal i uruchom 'python chat_server.py'.
2.  **Uruchom klientów** otwórz dwa nowe terminale i uruchom 'python chat_client.py'.
2.  Na obu klientach ustaw ten sam pokój (np. `ogolny`). Wyślij wiadomość, otrzyma ją drugi klient.
3.  Otwórz trzeciego klienta i ustaw mu inny pokój (np. `TEST`).

4.  Wyślij wiadomość z Klienta3 zauważysz, że Klient1 i Klient2 jej nie otrzymali.
