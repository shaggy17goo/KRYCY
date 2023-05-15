# KRYCY LAB 1C
### Paweł Popiołek,Michał Wawrzyńczak, Mateusz Borkowski, Paweł Gryka


### Testowanie dostępnych silników reguł
Zdecydowaliśmy się przetestować silnik ElastAlert, który jest częścią środowiska HELK. Zdecydowaliśmy się postawić środowisko HELK lokalnie na maszynie wirtualnej. 

Zdecydowaliśmy się zaimportować dane podane jako przykladowe w tutorialu na [https://securitydatasets.com/consume/helk.html](https://securitydatasets.com/consume/helk.html)

#### Import danych
![](https://i.imgur.com/HvSv40z.png)



#### Kibana 
Sprawdziliśmy czy dane zostały poprawnie zaimportowane do Elasticsearch'a i możemy przeglądać je w Kibane. Dodatkowo sprawdziliśmy z jakiego okresu pochodzą te dane co następnie przyda nam się w testowaniu reguł.
![](https://i.imgur.com/88CC4Rj.png)

#### Rule
Sprawdziliśmy dostępne typy reguł wspierane przes silnik Elastalert'a. Zapoznaliśmy się z możliwościami reguł każdego typu. Postanowiliśmy stworzyć najprostszą regułę, wykrywającą sprawdzającą zawartości danych parametrów każdego z logów.
![](https://i.imgur.com/Z5ySfTr.png)


Napisana przez nas reguła wygląda w następujący sposób. Jako zapytanie KQL wykorzystaliśmy to podane w tutorialu [https://securitydatasets.com/consume/helk.html](https://securitydatasets.com/consume/helk.html)
![](https://i.imgur.com/H3PHsas.png)

W momencie spełnienia się reguły wysłany zostaje alert na Slacka'a


#### Uruchomienie
Uruchomiliśmy silnik elastalert'a który sprawdza napisaną przez nas regułe. Dodatkowym problemem była konieczność wpisania daty początkowej, od której silnik ma analizować logi tak aby zaimportowane wcześniej logi zostały przeanalizowane
![](https://i.imgur.com/XUURvvs.png)
![](https://i.imgur.com/n0OTr5W.png)


#### Slack
Dopasowanie reguł i wysłanie alertów możemy zaobserwować na kanale SLACK
![](https://i.imgur.com/vC0Hp0c.png)


### Model detekcji anomalii - detekcja progowa
#### Wybranie opcji do realizacji
Wybraliśmy opcję z przygotowaniem modelu detekcji anlomalii dla ruchu sieciowego.

#### Propozycja przykładu anomalii
##### Zaproponowane metryki
W ramach tego laboratorium proponujemy aż trzy metryki anomalii:
 - **Anomalia długości połączeń między hostami** - korzystając z pliku ground truth (w przypadku wybranych przez nas danych zrzutu ruchu z poniedziałku), obliczmy ile proporcjonalnie powinno być połączeń zawierających się w danym przdziale długości okna czasowego i sprawdzamy czy w danych testowanych nie długości połączeń nie odbiegają za bardzo (0.5*gt,1.5*gt) od danych z ground truth. W ten sposób mieliśmy nadzieję orzymać alerty gdy na przykład system będzie intensywnie skanowany. Jednakże w danych, które analizowaliśmy nie udało się to - wszystkie mają podobne rozkłady czasowe - dlatego włąśnie powstały dwie kolejne metryki
 - **Anomalia w postaci nieznanych portów** - korzystając z pliku ground truth znajdujemy wszystkie używane numery portów i sprawdzamy czy w pliku testów nie znajdują się zapisy o połączeniach z i na inne porty (niebędące w pliku z gt). Ta analiza dla odmiany była zbyt szeroka i dawała zbyt dużo alertów.
- **Anomalie w średnich z wszystkich możliwych metryk** - bardzo ogólna analiza sprawdzająca średnią z wszystkich możliwych metryk w danych testowych. Alert jest podnoszony gdy średnia z danej metryki z danych testowanych znajduje się poza zakresem 0.1\*(średnia z tej samej metryki w danych gt), 1.9\*(średnia z tej samej metryki w danych gt). Ta metryka często pokazuje alerty przy wielu przykładowych atakach.
##### Źródło danych i faktyczne dane
Źródłem danych są przetworzone dane o ruchu sieciowym z CIC-IDS2017. Badana sieć składa się z modemu, direwall'a, kilku switchy, routerów i wielu maszyn z systemem Windows/Ubuntu lub Mac OS X. Dane zawierają zrzuty dane w formie csv z 5 dni - poniedziałek jest dniem przykłądowym (w którym nie ma ataków), a przez kolejne dmni następują ataki takie jak Brute Force FTP, Brute Force SSH, DoS, Heartbleed, Web Attack, Infiltration, Botnet i DDoS.

![](https://i.imgur.com/jbrT41r.png)

##### Notatnik
Poniżej przedstawiamy wymagania i sekcje kodu(w notatniku) je realizujące:


| Wymaganie                                                    | Realizacja                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **ANO.PROG.3.1**                                             | ![](https://i.imgur.com/QlUcUek.png)                         |
| **ANO.PROG.3.2**                                             | ![](https://i.imgur.com/bJUNXDe.png) ![](https://i.imgur.com/UEQjuMx.png) ![](https://i.imgur.com/OC7bMCF.png) |
| **ANO.PROG.3.3, ANO.PROG.3.4, ANO.PROG.3.5**                 | ![](https://i.imgur.com/ytuFFmB.png) ![](https://i.imgur.com/n5MdAG5.png) ![](https://i.imgur.com/3VpFLgu.png) |
| ##### Integracja analizy z notatnika z rozwiązaniem z Lab 1A |                                                              |
| W celu zintegrowania notatnkia powstał nowy plik **threshold_detection.py** (i został dodany jako funkcja **click**), który był adaptacją kodu z notatnika. |                                                              |

##### Test i prezentacja działania zintegrowanego projektu:
Poniżej znajdują się wyniki analizy długości połączeń oraz średnich z wszystkich możliwych metryk:
![](https://i.imgur.com/R7SVnMv.png)
Poniżej znajduje się kawałek analizy występowania połączeń z nieznanch portów. Wyników jest jeszcze więcej niż pokazane jest na zrzucie ekranu, ale nie jest to bardzo zaskakujące biorąc pod uwagę, że pliki mają po około 500000 logów:
![](https://i.imgur.com/zWRKZPd.png)



### Wykorzystanie znanych rozwiązań dla reguł YARA

| Wymaganie       | Realizacja                                                   |
| --------------- | ------------------------------------------------------------ |
| **REG.DET.1**   | YARA                                                         |
| **REG.DET.2.1** | ![](https://i.imgur.com/ZbqdhMl.png) ![](https://i.imgur.com/ni3i3bc.png) |
| **REG.DET.2.2** | ![](https://i.imgur.com/Dyi08vk.png)                         |
| **REG.DET.3.1** | N/D                                                          |
| **REG.DET.3.2** | ![](https://i.imgur.com/ZaIVHnB.png)                         |