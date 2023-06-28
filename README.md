# EnergySync

Project Algoritmes en Heuristieken. In deze case proberen we met het gebruik van algoritmes een zo een goedkoop mogelijk oplossing creëren van het SmartGrid probleem.

In dit probleem zijn er een aantal huizen en batterijen dat aan elkaar verbonden moet worden.
Door middel van algoritmes proberen wij een zo goedkoop mogelijke oplossing te vinden voor het verbinden van de huizen met de batterijen en de kabels daartussen.

---

## Installatie en gebruik

Voor het gebruik van dit programma is een versie van pygame nodig. Wij hebben zelf versie 2.4.0 gebruikt.

``` pip install pygame```

Er zijn twee modi die gebruikt kunnen worden door de gebruiker:

De visualisation mode is de standaard modus en kan gestart worden met:

``` python3 smart_grid.py ```

De console mode die met een optional argument kan worden gestart:

``` python3 smart_grid.py --console```

Voor het gebruik van de console mode kunnen er in smart_grid.py aanpassingen
worden gedaan aan bijvoorbeeld het aantal iteraties (alleen voor de non iteratieve algoritmes)
en de keuze van het algoritme zelf

Voor visualisation mode kan het zijn dat het venster groter is dan het scherm.
Om dit te verhelpen kan er worden gekozen voor een SCREEN_WIDTH en SCREEN_HEIGHT van 765.

In de visualisation mode kan er voor worden gekozen om:
- Een algoritme te kiezen en uit te voeren
- De snelheid van het tekenen van de lijnen aanpassen
- Het tekenen van de lijnen pauzeren of hervatten
- Van Neighbourhood wisselen
- De positie van de batterijen verbeteren met een algoritme
---
![visualisation screenshot](/sprites/images/visualisation.png)
![visualisation screenshot in action](/sprites/images/visualisation_2.png)


## Algoritmes

Voor deze case hebben wij een aantal algoritmes gebruikt om dit probleem zo goedkoop mogelijk op te lossen:

| Algoritme | Beschrijving |
| ----------- | ----------- |
| Random | Dit is onze baseline. Dit algoritme geeft aan ieder huis een valide batterij met genoeg capaciteit. Dit algoritme houd geen rekening met gedeelde bekabeling. |
| Greedy | Dit algoritme kiest voor iets huis de batterij die het minst ver van het huis verwijderd is, zolang deze genoeg capaciteit heeft. Dit algoritme houd geen rekening met gedeelde bekabeling. |
| Greediest | Dit algoritme is een combinatie van Greedy en Random en kan met een threshold worden ingesteld. Dit algoritme houd geen rekening met gedeelde bekabeling. |
| Greedy Shared | Dit algoritme is een verbetering van het Greedy algoritme omdat hier gebruik wordt gemaakt van gedeelde bekabeling. |
| Greedy Beam Search | Dit constructieve algoritme is een beam search algoritme in combinatie met een greedy lookahead. Dit algoritme kan worden ingesteld met een beam width (stelt de hoeveelheid staten in die bij elke generatie maximaal worden bewaard), een lookahead depth (De hoeveelheid generaties die het algoritme vooruit gaat kijken) en een hoeveelheid van huizen die door dit algoritme worden toegewezen aan batterijen. De rest wordt toegediend door het Greedy shared algoritme om tijd te besparen. |
| Evolution | |


---
## Experiment

Het is waarschijnlijk nodig om pygame geïnstalleerd te hebben (pygame versie 2.4.0 of later)

 De verschillende algoritme zijn uit te testen door run_tests.py te runnen. Hier zijn een aantal opties die aan te passen zijn zijn.
 - ITERATIONS: Hoe vaak een algoritme moet draaien (Niet van toepassing voor Evolution)
 - NEIGHBOURHOOD: Selecteer in welke neighbourhood het algoritme moet draaien. Kies uit "1", "2" of "3" (In str format)
 - ALGORITHM: Selecteer welk algoritme gedraaid zal worden. Keuze uit alle algoritme in de import (muv Algorithm want dit is een abstracte class)

 Een paar details om op te letten:
 - Evolution blijft doorgaan totdat deze handmatig gestopt wordt
 - In ./code/algorithms/greedy_beam_search.py in de `__init__()` kunnen nog extra parameters worden aangepast als dat gewenst is
 - In ./data/test_results zijn de test resultaten van greedy_shared.py en greedy_beam_algorithm.py the zien (N = 100)