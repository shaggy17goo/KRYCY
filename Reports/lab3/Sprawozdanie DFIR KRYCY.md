# Sprawozdanie DFIR KRYCY

### Autorzy:
#### Paweł Gryka, Michał Wawrzyńczak


## Opis sprawy
Pracownik firmy na wysokim stanowisku zaakceptował dużą sumę pieniędzy od konkurencyjnej firmy w zamian za zrobienie poważnego wycieku danych. Otrzymaliśmy używane przez niego urządzenia i nośniki danych i naszym zadaniem jest znalezienie wszystkich dowodów cyfrowych mówiących o wycieku.

## Zadanie
Nasze zadanie polegało na przeanalizowaniu sprawy ```Data Leakage Case``` od NIST i odpowiedzeniu na co najmniej 7 wbranych pytań zawartych na  [tej stronie](https://cfreds-archive.nist.gov/data_leakage_case/data-leakage-case.html).

## Wybór pytań
Żeby nie wybrać najprostszych pytań zdecydowaliśmy się na użycie generatora liczb losowych w zakresie 1-60 by to on wybrał nam reaizowane zadania. Generator wybrał liczby:
[1,7,10,19,22,25,39,41]
Więc zadania o właśnie tych numerach zrealizowaliśmy.
Gdy na liście znajdowały się zadania powiązane z tymi wylosowanymi to także je wykonywaliśmy.

## Wykorzystane narzędzia
Do wykonania zadania używalismy obu zaproponowanych narzędzi (```AUTOPSY 4.19.3```, ```AXIOM v5.8.0.27495``` oraz ```FTKImager 4.7.1.2```) oraz innych, które potrzebne były do wykonania specyficznych zadań (np. ```Thumbnail database viewer```). Zadania realizowaliśmy oddzielnie na dwóch różnych komputerach. Oba posiadały system operacyjny Windows 10, oraz odpowiednio procesory I7-9750H oraz  R7-4800H.


![](https://i.imgur.com/Pj7qppd.png)



### 1. What are the hash values (MD5 & SHA-1) of all images? Does the acquisition and verification hash value match?

Dokonano sprawdzenia wartości skrótów wszystkich kopi binarnych, wartości wyliczone w trakcie weryfikacji zgadzają się z wartościami zapisanymi w czasie akwizycji.
- Komputer
![](https://i.imgur.com/dR6h0FH.png)

- Pendrive 1
![](https://i.imgur.com/oUcx2H7.png)


- Pendrive2
![](https://i.imgur.com/nutCCKe.png)


- Płyta
![](https://i.imgur.com/6cA7432.png)


### 7. Who was the last user to logon into PC?
Jako ostani na tym komputerze był urzytkownik o nawie urzytkownika **informant**
- Axiom
![](https://i.imgur.com/UDon63E.png)
- Autopsy
![](https://i.imgur.com/IJb0yo9.png)

W trakcie realizowania tego zadania zauważyliśmy, przesunięcie w czasie pomiędzy datami prezentowanymi przez Autopsy oraz Axiom. Sprawdziliśmy zgodność ustawionych stref czasowych w obu programach. Pomimo pozornej zgodności przesunięcie czasowe występuje i nie udało nam się tego "naprawić".
![](https://i.imgur.com/pm7oIat.png)
Dodatkowo w Axiomie widoczny jest dodatkowy rekord z późniejszą datą zalogowania przez tego samego urzytkownika **informant**, rekord ten różni się od pozostałych data source'em. Może to świadczyć o próbie zatarcia jakiś śladów.
![](https://i.imgur.com/2lL4kkf.png)


### 10. What applications were installed by the suspect after installing OS?
Data instalacja systemu operacyjnego:
![](https://i.imgur.com/OpXHmCm.png)
Programy instalowane przez urzytkownika:
![](https://i.imgur.com/8ts2Vr0.png)

| Program Name                                          | Date/Time               |
| ----------------------------------------------------- | ----------------------- |
| Google Chrome v.41.0.2272.101                         | 2015-03-22 10:11:51 EDT |
| Google Update Helper v.1.3.26.9                       | 2015-03-22 10:16:03 EDT |
| Apple Application Support v.3.0.6                     | 2015-03-23 15:00:45 EDT |
| Bonjour v.3.0.0.10                                    | 2015-03-23 15:00:58 EDT |
| Apple Software Update v.2.1.3.127                     | 2015-03-23 15:01:01 EDT |
| iCloud v.4.0.6.28                                     | 2015-03-23 15:01:54 EDT |
| Google Drive v.1.20.8672.3137                         | 2015-03-23 15:02:46 EDT |
| DXM\_Runtime                                          | 2015-03-25 05:15:21 EDT |
| MPlayer2                                              | 2015-03-25 05:15:21 EDT |
| Microsoft .NET Framework 4 Client Profile v.4.0.30319 | 2015-03-25 09:51:39 EDT |
| Microsoft .NET Framework 4 Client Profile v.4.0.30319 | 2015-03-25 09:52:06 EDT |
| Microsoft .NET Framework 4 Extended v.4.0.30319       | 2015-03-25 09:54:06 EDT |
| Microsoft .NET Framework 4 Extended v.4.0.30319       | 2015-03-25 09:54:33 EDT |
| Eraser 6.2.0.2962 v.6.2.2962                          | 2015-03-25 09:57:31 EDT |

Interesujący jest fak, że na komputerze zainstalowany został program **Eraser**.
Eraser - program przeznaczony do trwałego usuwania plików przez ich zamazanie, pracujący w środowisku Windows, wydany na licencji GPL. Trwale usuwa pliki przez ich wielokrotne nadpisanie wcześniej wybranym wzorcem.


### 19. Where is the e-mail file located?
Plik zawierający e-mail'e znajduje się w:
`Users/informant/AppData/Local/Microsoft/Outlook/iaman.informant@nist.gov.ost`
![](https://i.imgur.com/q2rJGrI.png)
W pliku tym znajduję się 14 wiadomości. Część z nich została usunięta. 
![](https://i.imgur.com/tvvDm45.png)
Wśród wiadomości usuniętych znajduję się m.in. następująca konwersacja między "spy" a "iaman".
![](https://i.imgur.com/IWTJBta.png)


## 22. List external storage devices attached to PC. 
Do komputera podłączone zostały następujące urządzenia usb:
![](https://i.imgur.com/m1BJtPE.png)


Wśród nich można wyróżnić następujące urządzenia pamięci masowej. Były to podobne urządzenia różniące się numerem seryjnym
| Date/Time               | Device Make   | Device Model | Serial Number        |
| ----------------------- | ------------- | ------------ | -------------------- |
| 2015-03-24 09:38:00 EDT | SanDisk Corp. | Cruzer Fit   | 4C530012450531101593 |
| 2015-03-24 15:38:09 EDT | SanDisk Corp. | Cruzer Fit   | 4C530012550531106501 |

Dodatkowo podłączone urządzenia pamięci masowej możemy obserwować przy pomocy artefaktów dotyczących shellbagów.
![](https://i.imgur.com/1ScdU5O.png)
W shellbag'ach widoczne są jakie podłączane urządzenia i przeglądane na nich katalogi. Analizując shellbagi oraz zawartość konkternych nośników możemy ustalić jaką literką podmontowane były poszczególne nośniki.
![](https://i.imgur.com/hlqzOeK.png)


Jak widać ostrzerzenie od spiega było jak najbardziej zasadne, podłączane urządzenia usb są łatwe do wykrycia.
![](https://i.imgur.com/A36jKVj.png)
Iaman choć próbował się nie pozostawawiać śladów, starał się zbyt słabo.




### 25. List all directories that were traversed in ‘RM#2’.

Ponieważ już wiedzieliśmy, że urządzenie ```RM#2``` mapowane jest na dysk ```E:``` to całkiem prosto było znaleźć listę przetrawersowanych folderów. Należało wejść w ```shellbags``` i znaleźć ścieżki odpowiadające temu wolumenowi (chodzi głównie o kolumnę ```Path```):


| Source Name  | Path                                                         | Key                                                          | Data Source                     | FIELD5                  | FIELD6                  | FIELD7                          | FIELD8                          |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------- | ----------------------- | ----------------------- | ------------------------------- | ------------------------------- |
| UsrClass.dat | My Computer\E:\                                              | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\  | cfreds_2015_data_leakage_pc.E01 |                         |                         |                                 |                                 |
| UsrClass.dat | My Computer\E:\RM#                                           | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\0\ | 2015-02-15 21:51:38 CET         | 2015-02-15 21:52:10 CET | 2015-02-15 21:52:08 CET | cfreds_2015_data_leakage_pc.E01 |                                 |
| UsrClass.dat | My Computer\E:\RM#\Secret Project Dat                        | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\0\0\ | 2015-03-24 13:38:31 CET         | 2015-02-15 21:51:38 CET | 2015-02-15 21:52:10 CET | 2015-02-15 21:52:08 CET         | cfreds_2015_data_leakage_pc.E01 |
| UsrClass.dat | My Computer\E:\RM#\Secret Project Dat\desig                  | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\0\0\0\ | 2015-03-24 13:38:52 CET         | 2015-02-15 21:51:38 CET | 2015-02-15 21:52:10 CET | 2015-02-15 21:52:08 CET         | cfreds_2015_data_leakage_pc.E01 |
| UsrClass.dat | My Computer\E:\Secret Project Dat                            | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\ | 2015-03-24 14:00:19 CET         | 2015-03-24 13:57:28 CET | 2015-03-24 13:59:28 CET | 2015-03-24 04:00:00 CET         | cfreds_2015_data_leakage_pc.E01 |
| UsrClass.dat | My Computer\E:\Secret Project Dat\technical revie            | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\0\ | 2015-03-24 13:56:22 CET         | 2015-03-24 14:00:14 CET | 2015-03-24 04:00:00 CET | cfreds_2015_data_leakage_pc.E01 |                                 |
| UsrClass.dat | My Computer\E:\Secret Project Dat\proposa                    | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\1\ | 2015-03-24 13:55:18 CET         | 2015-03-24 13:59:46 CET | 2015-03-24 04:00:00 CET | cfreds_2015_data_leakage_pc.E01 |                                 |
| UsrClass.dat | My Computer\E:\Secret Project Dat\progres                    | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\2\ | 2015-03-24 20:54:07 CET         | 2015-03-24 13:54:54 CET | 2015-03-24 13:59:44 CET | 2015-03-24 04:00:00 CET         | cfreds_2015_data_leakage_pc.E01 |
| UsrClass.dat | My Computer\E:\Secret Project Dat\pricing decisio            | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\3\ | 2015-03-24 13:57:32 CET         | 2015-03-24 13:59:40 CET | 2015-03-24 04:00:00 CET | cfreds_2015_data_leakage_pc.E01 |                                 |
| UsrClass.dat | My Computer\E:\Secret Project Dat\desig                      | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\4\ | 2015-03-24 13:57:14 CET         | 2015-03-24 13:59:28 CET | 2015-03-24 04:00:00 CET | cfreds_2015_data_leakage_pc.E01 |                                 |
| UsrClass.dat | My Computer\E:\Secret Project Dat\desig\winter_whether_advisory.zi | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\4\0\ | 2015-03-24 14:01:29 CET         | 2014-12-16 16:10:26 CET | 2015-03-24 13:59:38 CET | 2015-03-24 04:00:00 CET         | cfreds_2015_data_leakage_pc.E01 |
| UsrClass.dat | My Computer\E:\Secret Project Dat\desig\winter_whether_advisory.zi\Unknown Type (0x3a) | Local Settings\Software\Microsoft\Windows\Shell\BagMRU\1\0\1\4\0\0\|2015-03-24 14:01:32 CET | cfreds_2015_data_leakage_pc.E01 |                         |                         |                                 |                                 |



### 38 i 39. Where are 'Thumbcache' files located. Identify traces related to confidential files stored in Thumbcache. (Include ‘256’ only) 

Pliki thumbcache znajdują się pod ścieżką:
```
Users/informant/AppData/Local/Microsoft/Windows/Explorer
```

Wyeksportowaliśmy te pliki, a następnie, za pomocą programu ```Thumbnail database viewer``` odnaleźliśmy następujące artefakty:

![](https://i.imgur.com/uHPBDqC.png)

![](https://i.imgur.com/llZ9nrb.png)

![](https://i.imgur.com/XlffMwB.png)

![](https://i.imgur.com/0vFC1cN.png)

![](https://i.imgur.com/wyHvhzw.png)

![](https://i.imgur.com/b5wIJHi.png)







### 40 i 41. Where are Sticky Note files located? Identify notes stored in the Sticky Note file. 

Pliki sticky note znajdują się w folderze 
```Users/informant/AppData/Roaming/Microsoft/Sticky Notes```

![](https://i.imgur.com/9E0m8qK.png)

Ciekawym wydają się tutaj czytelne kawałki tekstu. Wyglądają albo jak uspokajanie kogoś zdenerwowanego. 

Próbowaliśmy także otworzyć odzyskany plik ale okazało się to bardzo trudne na Windows 10. Format odpowiada plikom z Windows 7 i Vista. Zastanawialiśmy się nad postawieniem maszyny wirtualnej, z którymś z wymienionych systemów ale stwierdziliśmy, że nie jest to warte zachodu.



## 53. Recover deleted files from USB drive ‘RM#2’.
Przy pomocy FTKImager'a nie jest możliwe odczytanie, żadnych plików z USB drive ‘RM#2’
![](https://i.imgur.com/72Yvbqm.png)
Narzędzie Autopsy potrafi już jednak odzyskać część plików która znajdowała się tam przed usunięciem
![](https://i.imgur.com/3m8p5qx.png)
Przykładowe odzyskane pliki:
![](https://i.imgur.com/XCKV8OM.png)
![](https://i.imgur.com/0pSDuho.png)




## Podsumowanie
Na tym laboratorium wcieliliśmy się w rolę pracowników działu DFIR i przeanalizowaliśmy wybrane pytania z ```Data Leakage Case``` i nauczyliśmy się podstaw obsługi narzędzi do autopsji cyfrowej. Oraz obudziliśmy naszego wewnętrznego Sherlocka Holmesa, żeby odkryć tajemnice spowitej ciemnością i grozą zagadki.