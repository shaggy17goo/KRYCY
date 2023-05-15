# KRYCY LAB 1B
## Autorzy:
### Mateusz Borkowski, Michał Wawrzyńczak, Paweł Gryka, Paweł Popiołek

## Zadanie do wykonania
Naszym zadaniem było zapoznanie się z środowiskiem i dostępnymi narzędziami w DetectionLab oraz HELK

## DetectionLab
### Środowisko i narzędzia (Zapoznanie się z nim)
DetectionLab to zestaw potrzebnych skryptów i plików używanych do szybkiego uruchomienia wirtualnego środowiska laboratoryjnego wyposażonego w narzędzia do cyberbezpieczeństwa obronnego. Środowisko składa się z czterech hostów w następującej architekturze:
![](https://i.imgur.com/eroDn1Q.png)

W dużej ogólności, hosty **DC** i **WIN10** przekazują logi z akcji na nich wykonanych do **Loggera** (albo bezpośrednio albo przez **WEF**)

Na hostach windows'owych znajdują się narzędzia do generowania podejrzanych akcji a następnie zbierania z nich logów:
- Atomic Red Team
- Microsoft ATA
- Sysmon
- Osquery
- Velociraptor

Na **Logger**'rze znajduje sie wiele narzędzi do oglądania i analizy logów:
- Splunk
    - Suricata
    - Zeek
- Fleet
- Apache Guacamole
- Velociraptor

### Wykonane działania na maszynach
#### Początkowe problemy
Do ćwiczenia podchodziliśmy w sumie czterokrotnie. Pierwszy raz (na samym początku udostępnienia ćwiczenia) jedynie zorientowaliśmy się jak wygląda środowisko. Niestety drugie podejście do lab zakończyło się niepowodzeniem przez wygaśnięcie licencji splunka. Trzecie podobnie, przez skończenie się miejca na hoście (vagrant nie potrafił wystartować). W czwartym podejściu znowu napotkaliśmy problem - host logger nie otrzymywał adresu ip:
![](https://i.imgur.com/0HgeE2w.png)

Mimo restartów vagranta nietety problem nie ustępował. Po dłuższej sesji debuggingu okazało się, że w konfiguracji netplan zostały trzykrotnie powtórzone komendy, po usunięciu nadmiaru sieć zaczęła działać.
#### Generowanie logów
Żeby wygenerować dane do analzy użyliśmy (zgodnie z sugestią) narzędzia **Atomic Red Team**, na hostach **WIN10** i **DC**:
![](https://i.imgur.com/x6UQkZE.png)

Powyżej wykonaliśmy jedynie dwa proponowane testy z dokumentacji ale potem (żeby wygenerować więcej logów), włączyliśmy także narzędzie z opcją *All*. 

#### Przeglądanie logów
Następnie na **logger**'ze włączyliśmy *Splunk*'a i sprawdziliśmy, czy pojawiły się jakieś alerty/logi. Większość z logów pochodziła z *zeek*, dlatego je wyświetliliśmy:
![](https://i.imgur.com/walE8qY.png)

Należy jeszcze dodać, że przedtem także sprawdziliśmy logi (przed wykonaniem Atomic Red Team-testów) i żadne się nie pojawiły - dlatego mamy prawie pewność, że logi pochodzą właśnie z tych wydarzeń. Zgadzało się także pochodzenie logów - najpierw pojawiły się logi z hosta **WIN10** a dopiero później z **DC** - czyli w takiej samej kolejności w jakiej włączaliśmy testy.

Dodatkowo znaleźliśmy opcję mapowania otrzymanych alertów na matrycę **MITRE**, gdy podchodziliśmy do ćwiczenia za pierwszym razem, udało się nam zobaczyć prawidłowo załadowane logi zmapowane do matrycy **MITRE**, jednakże w ostatecznym podejściu nie udało się już załadować danych do tej opcji. NIestety nie mamy screenshota potwierdzającego z pierwszego podejścia.

![](https://i.imgur.com/oCOlDVJ.png)


#### Stawianie środowiska na świeżo
Ze względu na istniejace problemy postanowiliśmy całe środowisko przywrócić do stanu początkowego. Tu także wystąpiły problemy ze względu na modyfikację url do pobrania Velociraptora, aktualizacja stanu do aktuanego z tym w repozytorium `https://github.com/clong/DetectionLab` także nie pomagała. Po zamianie url w skrypcie `install-velociraptor.ps1` udało się postawić poprawnie całe środowisko
![](https://i.imgur.com/UPuSLNF.png)


Wykonaliśmy podstawowy `Invoke-AtomicTest T1218.010 -TestNumbers 1,2`, logi były poprawnie przesyłane i widoczne w Splunku.
![](https://i.imgur.com/6bXUIn0.png)

Zakończyliśmy pracę i chcieliśmy wykonać więcej testów, następnego dnia. Po powrocie do środowiska zaczęły ponownie występować różne problemy. 

#### AtomicTests

Uruchomiliśmy kilka AtomicTestów i obserwowaliśmy winiki w Spunku.

#### T1218 - Signed Binary Proxy Execution
![](https://i.imgur.com/ioQfEvb.png)
![](https://i.imgur.com/sOhsydf.png)
Po wykonaniu testu możemy zaobserwować w splunku, że IDS wykrył to zagrożenie.

#### T1078 - Default Accounts
![](https://i.imgur.com/vE34QVB.png)
![](https://i.imgur.com/iwEPFo6.png)
![](https://i.imgur.com/meA0bCJ.png)

Nie udało nam się zaobserwować tej technik (uzyskania dostępy z wykorzystaniem istniejacych kont domyślnych) w splanku. Możliwe, że IDS nie wykrył tej techniki. widzimy jednak logi które, mogą dotyczyć innych uruchamianych przez nas testów. Jak np `T1107 - File Deletion`.


#### Podsumowanie wykrytych zagrożeń po uruchomionych przez nas testach.
![](https://i.imgur.com/ZLTu0MD.png)


## HELK
### Środowisko i narzędzia
*HELK* jest *open-source*'ową platformą wykorzystywaną w cyberbezpieczeństwie defensynym, składającą się z poniższych komponentów:

- *Kafka* - umożliwia obsługę danych (logów) pochodzących z wielu źródeł w czasie rzeczywstym,
- *Elasticsearch* - silnik do wyszukiwania i analizy danych,
- *Logstash* - przekazuje zagregowane przez *Kafk*'e logi dalej do *Elasticsearch*'a,
- *Kibana* - platforma służąca do wizualizacji i analizy danych, zaprojektowana aby współpracować z *Elasticsearch*,
- *Apache Spark* - platforma programistyczna dla obliczeń rozproszonych,
- *ES-Hadoop* - pozwala na interakcję pomiędzy *Elasticsearch*'em, a *Spark*'iem,
- *GraphFrames* - *package* do *Spark*'a, rozbudowuje jego możliwości obsługi grafów,
- *JupyterNotebook (JupyterLab)* - pozwala na tworzenie i udostępnianie dokumentów zawierających wykonywalny kod,
- *Elastalert* - rozwiązanie służące do powiadomiania o anomaliach, albo o dopasowaniach do określonych wzorców danych z *Elasticsearch*'a.

![](https://i.imgur.com/Az2mMwG.png)

### Wykonanie działania na maszynach

#### Ożywieie środowiska danymi
Aby poznać dostępne narzędzia, należało najpierw ożywić środowisko danymi. Przy próbie załadowania danych do środowiska napotkaliśmy na następujące problemy:
- dane ożywiające nie istniały w miesjcu zalinkowanym w podanym w instrukcji poradniku,
- brak komunikacji z *Elasticsearch* po domyślnym porcie (porzebne w celu wrzucenia tam danych za pomocą skryptu w *Pythonie*),
- problem z wczytaniem danych w formacie *json* po ich rozpakowaniu.

Aby uporać się z powyższymi problemami odpowiednio:
- odnaleźliśmy odpowiednie dane ożywiające w sieci (repozytorium z tymi danymi zmieniło nazwę dlatego link ze strony nie zadziałał - nowa nazwa repozytorium to *OTRF/Security-Datasets*),
- w celu zapewnienia komunikacji z *Elasticsearch* należało zmodyfikowac plik konfiguracyjny *helk-kibana-analysis-basic.yml*, tak aby *docker* wystawił odpowiedni port do komunikacji z bazą - *9200*,
- pliki do *Elasticsearch*'a należało przekazywać nie w formacie *json*, a spakować je do *tar.gz*.

Dla ułatwienia pracy i rozwiązywania problemów całe środowisko postanowiliśmy postawić u siebie lokalnie.

![](https://i.imgur.com/qewNtVT.png)

Na powyższym screenie widać że udało nam się załadować odpowiednie logi i mamy na nie podgląd z *Kiban*'y.

#### Kibana

Najbardziej interesującym z naszej perspektywy komponentem całego środowiska jest *Kibana*. Jest tak ponieważ oferuje ona wiele możliwości operowania na zebranych danych, a to wszystko za pomocą interfejsu użytkownika. Z powyższego powodu postanowiliśmy skupić nasze działania wokół tego programu.

##### Discover
Zakładka *Discover* pozwala na podgląd wszystkich zebranych logów. Oferuje ona wiele możliwości ułatwienia sobie pracy z przekopywaniem się przez ogromne ilości mało czytelnych logów. W tym celu możemy np.:
- rozwinąc konkretny, interesujący nas rekord, otrzymując tym samym bardziej czytelny format:

![](https://i.imgur.com/86LK4qk.png)

- podejrzeć ilość powtórzeń danej wartości konkretnego pola dla różnych logów:

![](https://i.imgur.com/agZXCoI.png)

- przeglądać wszystkie logi z podglądem tylko na interesujące nas pola:

![](https://i.imgur.com/p2ZWn2C.png)

- tworzyć i wysyłać zapytania KQL co pozwala na przefiltrowanie danych (przykład uzycia w dalszej częsci dokumentu - punkt *Dashboards*)



##### Visualization
Zakładka *Visualization* pozwala nam na tworzenie róznego rodzaju wykresów. Stworzenie dobrej wizualizacji może w dużym stopniu ułatwić dla człowieka zauważenie różnych anomalii.
Zakładka *Visualization* pozwala między innymi na:
- tworzenie histogramów:
![](https://i.imgur.com/qPgXGot.png)
- tworzenie wykresów kołowych:
![](https://i.imgur.com/e6PN5pb.png)

Jak widać dla powyższych duże znaczenie ma dobór odpowiedniej metody wizualizacji do analizowanych danych. W obu przykładach wyświetlane są czasy zachodzenia zdarzeń w systemie. Dla pierwszego przykładu (histogram) na pierwszy rzut oka widać jak wiele zdarzeń zaszło w jakim czasie i analityk bezpieczeństwa może z takiego widoku szybko wyciągnąć wnioski. W drugim przykładzie (wykres kołowy) widoczność jest zdecydowanie gorsza i wyciągniecie wniosków z takiego widoku może być zdecydowanie bardziej czasochłonne, a przy odpowiednich warunkach - niemożliwe.

##### Dashboards

Zakładka *Dashboards* oferuje rozwiązanie, które ostatecznie może być dla analityka bezpieczeństwa najczęściej odwiedzanym miejscem. Umożliwa ona tworzenie i zapisywanie wielu dashboard'ów. Pojedynczy dashboard może składać się z wielu wybranych komponentów. Komponentami możliwymi do dodania na taką talicę są np. różnego rodziaju wizualizacje, tablice danych czy inne informacje niepochodzące z zagregowanych logów, ale takie które chcielibyśmy mieć pod ręką.
Dla prezentowanego poniżej *dashboard*'a wykorzystaliśmy przedstawione w poprzenich punktach konstrukcje. Zostały one przez nas zapisane, co umożliwiło wykorzystanie ich w tym momencie. Tymi konstrukcjami są:
- lista wszystkich logów, ale z wyświetlonymi jedynie interesującymi nas polami,
- histogram czasu zachodzenia zdarzeń.

![](https://i.imgur.com/Isdp6Ch.png)

Na powyższym screenie mamy wiele spojrzeń na ten sam zbiór logów na jednej karcie, co już samo w sobie może stanowić duże ułatwienie przy analizowaniu logów. 
Przy operowaniu na takich tablicach możemy dodatkowo korzystać z zapytań *KQL*:

![](https://i.imgur.com/mSogMoK.png)

![](https://i.imgur.com/wcbLb99.png)

Takie rozwiązanie daje analitykom bezpieczeństwa dużą dowolność i praktycznie nieograniczone możliwości w tworzeniu tablic zgodnie z preferencjami danego zespołu. Dobrze przygotowany *dashboard* może skutkować oszczędznością czasu zespołu w przyszłości.

#### Elastalert
Elastalert jest kolejnym komponentem całego *HELK*'a, który pozwala nam na operowanie na logach z *Elasticsearch*'a. Tym razem mamy do czynienia  z brakiem interfejsu użytkownika. 
Możemy przygotować odpowiednie reguły np. w formacie zapytań *KQL* i w przypadku wykrycia dopasowania wysłać alert we wskazane miejsce.
- Przygotowana przez nas reguła wskazująca na *id* loga znajdującego się we wczytanym przez nas zestawie danych:
![](https://i.imgur.com/UDiJZMQ.png)

- Odebrany pod wskazanym adresem alert zawierający podejrzanego loga:
![](https://i.imgur.com/r47MzU3.png)

Powyższe rozwiązanie pozwala na zmniejszenie czasu reakcji zespołu na podejrzane zdarzenie.


#### Reszta komponentów 
Pozostałe komponenty *HELK*'a jak np. *Apache Spark* w połączeniu z *JupyterNotebook* i innymi pozwalają na dodatkowe zwiększenie możliwości analizy danych zebarnych w *Elasticsearch*'u. Przykładem takiego działania może być tworzenie diagramów relacyjnych. Takie działania otwierają badaczom nowe perspektywy na analizowane zbiory danych. 


### HELK - Podsumowanie
Wszelkie wykonane przez nas działania zostały wykonane na stosunkowo małych zbiorach danych. W normalnych warunkach takich logów może być znacznie więcej, dodatkowo mogą one pochodzic z zupełnie różnych źródeł. Sprawdzone przez nas w tym punkcie środowisko może okazać się bezcennym narzędziem w rękach doświadczonego analtyka. Dzięki dołączonym do niego narzędziom, analiza zdarzeń dla większych zbiorów danych staje się zdecydowanie łatwiejsza. 