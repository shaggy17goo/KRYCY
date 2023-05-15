**Autorzy:**
- Borkowski Mateusz
- Gryka Paweł
- Popiołek Paweł
- Wawrzyńczak Michał


# LAB 1a

## Scenariusz 1

|**ID wymagania**|**Opis wymagania**|**Zrzut ekranu z krótkim opisem**|
| :-----------: |:-------------------:| :----:|
| OFF.1 | Opracować aplikację z interfejsem CLI, która pozwoli na realizację wskazanych wymagań. Moduł do tworzenia aplikacji CLI | ![](images/vmware_RVKaCOMgUy.png) |
|      OFF.2       | Aplikacja działania w trybie CLI z wypisywaniem akcji | ![](images/vmware_biMmPHDIYP.png) |
| OFF.2.1 | Automatycznie tworzony jest log z działania o nazwie składającej się z nazwy aplikacji oraz znacznika czasu jej uruchomienia | ![](images/vmware_DzWKFIjvja.png) |
| OFF.2.2 | Efekty operacji są wypisywane jednocześnie na CLI oraz do otwartego pliku loga | ![](images/vmware_BtVlOFV8p1.png) |
| OFF.2.3 | Aplikacja utrzymuje także bazę zdarzeń - w bazie danych SQL | ![](images/vmware_UeQYz4sGCh.png) |
| OFF.3 | Aplikacja ma możliwość wskazania pojedynczych plików, folderu lub grupy folderów do przeszukania w poszukiwaniu plików, które mają być wykorzystane do analizy | ![](images/vmware_deXvLdvy6F.png) |
| OFF.4 | Obsługiwane formaty wejściowe plików do analizy:<br />- pliki tekstowe w formatach .txt , .xml , .json<br />- pliki ze zrzutami ruchu PCAP .pcap<br />- pliki logów Sysmon Windows EVTX - .evtx | ![](images/vmware_9GkkNlCkH5.png) |
| OFF.5 | Aplikacja ma możliwość wyświetlania zawartości pakietów z wczytanych danych z plików PCAP. | ![](images/vmware_IY7Iix9gk6.png) |
| OFF.6 | Aplikacja ma możliwość przekazania filtru zgodnego z formatem BPF (wykorzystywanego przez libpcap / tshark / pyshark / Wireshark / Scapy ) do funkcji otwierającej i wczytującej plik PCAP. | ![](images/vmware_IxQoZswjC4.png) |
| OFF.7 | Aplikacja ma możliwość wywołania operacji systemowej grep na wskazanych plikach tesktowych. Argumentem przekazywanym do operacji jest właściwe wyrażenie regularne. | ![](images/vmware_yg25ZEKjSw.png) |
| OFF.8 | Aplikacja ma możliwość wywołania działania wyrażenia regularnego z modułu Python re . Argumentem przekazywanym do operacji jest właściwe wyrażenie regularne. | ![](images/vmware_1Xj0UFxFqO.png) |
| OFF.9 | Aplikacja ma możliwość załadowania reguł analitycznych do detekcji zdarzeń opisanych za pomocą tych reguł i przechowywania ich w wybranej strukturze danych. | ![](images/vmware_IQztJL2EtB.png) |
| OFF.9.1 | Reguły będą opisywane jako funkcje Pythona w pliku detection-rules.py (nazwa na sztywno) | ![](images/vmware_bhqau2AbNZ.png) |
| OFF.9.2 | Każda reguła ma być zdefiniowana jako oddzielna funkcja w języku Python we wskzanym pliku w OFF.9.1 . Format pojedynczej reguły: | ![](images/vmware_K5vM60WEYs.png) |
| OFF.9.3 | Ładowanie reguł ma odbywać się na żądanie, tj. po wywołaniu żądania ładowania - tj. plik z regułami ma nie być załadowany statycznie od początku działania aplikacji OFF.9.4 Każdorazowane wywołanie ładowania reguł ma oznaczać usunięcie i | ![](images/vmware_L3J64XOxc0.png) |
| OFF.9.4 | Każdorazowe wywołanie ładowania reguł ma oznaczać usunięcie istniejących w pamięci programu i załadowanie nowego zestawu reguł | Tak się dzieje |
| OFF.9.5 | Informacjami zwrotnymi z reguły są:<br />- action_alert<br />- action_block<br />- description | ![](images/vmware_7B1vvRYfH5.png) |
| OFF.10 | Interfejs wywołania reguł analitycznych umożliwa ich użycie w kilku trybach: | ![](images/vmware_EAAAnxj8ne.png) |
| OFF.10.1 | Wywołanie całego zestawu reguł na wybranym zestawie plików | ![](images/vmware_cIxZSP2QFV.png) |
| OFF.10.2 | Wywołanie wybranej reguły - poprzez wskazanie jej nazwy (nazwa funkcji z OFF.9.2 ) - i na wybranym zestawie plików przekazanym do reguły | ![](images/vmware_ooEGLPlzeu.png) |
| OFF.11 | Przygotować aplikację CLI (nie musi być oparta na Click jak w Wymaganiu OFF.1 ) do odbierania wiadomości po REST API i wypisywaniu ich na CLI - alert. | ![](images/vmware_QIwkRCt57D.png) |
| OFF.12 | Przygotować aplikację CLI (nie musi być oparta na Click jak w Wymaganiu OFF.1) do odbierania wiadomości po REST API i wypisywaniu ich na CLI - akcja dla firewalla. | ![](images/vmware_QIwkRCt57D.png) |
| OFF.12.1 | \* (opcjonalnie) Można wykonać prostą integrację np. z iptables , ufw czy w inny proponowany sposób z firewallem w wybranym hoście. | ![](images/vmware_Vml1cYzp2K.png) |


## Scenariusz 2

|**ID wymagania**|**Opis wymagania**|**Zrzut ekranu z krótkim opisem**|
| :-----------: |:-------------------:| :----:|
| ON.1 | Opracować oddzielną aplikację od tej w Scenariuszu 1 lub wprowadzić dla niej tryb zarządzania zdalnym agentem na potrzeby analizy online. Moduł do tworzenia aplikacji CLI - Click | Opracowano |
| ON.2 | W ramach architektury rozwiązania wykorzystujemy host z aplikacją główną oraz host z aplikacją agenta. | Tak jest |
| ON.3 | Metodą komunikacji aplikacji głównej z agentem jest REST API. |         Zaimplementowano          |
| ON.MAIN.1.1 | Pobierz informację o konfiguracji sieciowej zdalnego hosta. | ![](images/vmware_E8LZDWAF3Z.png) |
| ON.MAIN.1.2 | Zbieraj plik PCAP ze wskazanymi parametrami. Przekazać za pomocą JSON konfigurację zbierania dla wybranej metody zbierania PCAP w agencie. Plik po zebraniu ma być transferowany na host głównej aplikacji | ![](images/vmware_vfOyoIPbyp.png) |
| ON.MAIN.1.3 | Pobieraj listę plików PCAP na zdalnym hoście z agentem. | ![](images/vmware_HTneQDgI36.png) |
| ON.MAIN.1.4 | Pobierz wskazany plik lub grupę plików PCAP ze zdalnego hosta z agentem. | ![](images/vmware_tGVb8q0LMY.png) |
| ON.MAIN.2 | Aplikacja ma możliwość wskazania akcji i wykonania jej na zdalnym agencie w zakresie zarządzania plikami logów | Zgadza się |
| ON.MAIN.2.1 | Pobieraj listę plików logów na zdalnym hoście z agentem | ![](images/vmware_M60pBOnG2W.png) |
| ON.MAIN.2.2 | Pobierz wskazany plik lub grupę plików logów ze zdalnego hosta z agentem. | ![](images/vmware_qzCdBQ4SrC.png) |
| ON.MAIN.3 | Aplikacja ma możliwość wskazania akcji systemowej i wykonania jej na zdalnym agencie | Ma możliwość |
| ON.MAIN.3.1 | Zdefiniowanie komendy systemowej do wykonania na zdalnym hoście | ![](images/vmware_XK5QJv1wKE.png) |
| ON.MAIN.3.2 | Przekazanie komendy do wykonania na zdalnym hoście i odebranie odpowiedzi | ![](images/vmware_1H9EWO9DQw.png) |

## Testy

|**ID testu**|**Opis testu**|**Zrzut ekranu z krótkim opisem**|
| :-----------: |:-------------------:| :----:|
| 1 | Prawidłowe wczytywanie każdego z 5 typów danych do analizy. | ![](images/vmware_GKSfoFsGqB.png) |
| 2 | Działanie filtra przy wczytywaniu pliku PCAP. | ![](images/vmware_IxQoZswjC4.png) |
| 3 | Działanie grep . | ![](images/vmware_yg25ZEKjSw.png) |
| 4 | . Działanie wyrażenia regularnego z modułem re . | ![](images/vmware_1Xj0UFxFqO.png) |
| 5 | Wczytanie reguł detekcyjnych z pliku detection-rules.py . | ![](images/vmware_IQztJL2EtB.png) |
| 6 | Wykonanie reguły detekcyjnej - wszystkich (co najmniej 2), pojedynczej po nazwie. | ![](images/vmware_cIxZSP2QFV.png)![](images/vmware_ooEGLPlzeu.png) |
| 7 | Zaprezentowanie akcji alert-local , alert-remote oraz block . | ![](images/vmware_QIwkRCt57D.png) |
| 8 | Zdalne uruchomienie zbierania pliku PCAP i pobranie do aplikacji głównej. | ![](images/vmware_vfOyoIPbyp.png) |
| 9 | Zdalne pobranie logów systemowych. | ![](images/vmware_M60pBOnG2W.png)![](images/vmware_qzCdBQ4SrC.png) |
| 10| Zdalne wykonanie komendy systemowej i pobranie jej wyniku do wyświetlenia | ![](images/vmware_1H9EWO9DQw.png) |