# EnergySync
Project Algoritmes en Heuristieken. Wij maken de best mogelijke oplossing voor het SmartGrid probleem

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