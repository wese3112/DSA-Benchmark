DSA Charakter und Benchmark-Tool
================================

Benchmarkskript zur Analyse / Auswertung von 'Das Schwarze Auge'-Charaktären

Charakter Erzeugen
------------------
Wenn noch keine Charaktäre eingegeben wurden: Python starten

	python

dsatool importieren

	import dsatool as dsa

Neuen Charakter erzeugen, z.B. den Ambosszwerg 'Vracass'

	dsa.chreateNewChar()

Es folgen nun alle benötigten Angaben zum Charakter in folgender Reihenfolge abgefragt:

1. Körperliche Basistalente
2. Körperliche Spezialtalente
3. Gesellschaftliche Basistalente
4. Gesellschaftliche Spezialtalente
5. Gesellschaftliche Berufe
6. Natur Basistalente
7. Natur Spezialtalente
8. Natur Berufe
9. Wissens-Basistalente
10. Wissens-Spezialtalente
11. Wissens-Berufe
12. Handwerkliche Basistalente
13. Handwerkliche Spezialtalente
14. Handwerkliche Berufe

Bei den Spezialtalenten und Berufen muss ein 'x' angegeben werden, wenn der Charakter nicht über dieses Talent / diesen Beruf verfügt. Bei der Eingabe der Werte bitte sorgsam sein, eine programmgeführte Korrektur ist momentan nicht implementiert. Die Eingabe von Sprachen und Schriften ist nicht möglich.

Sind alle Angaben gemacht, wird der Ordner _characters/CHARAKTERNAME_ angelegt. Der Charakter wird jetzt folgendermaßen geladen:

	Vracass = dsa.Character('Vracass')

Jetzt gibt es zwei Funktionen, die man anwenden kann: _test()_ und _benchmark()_.

Proben auf Talentwerte durchführen
----------------------------------
Mit einem vorhandenen (oder erzeugten) Charakter können jetzt Testwürfe durchgeführt werden,
z.B. auf das Talent Sinnesschärfe:

	import dsatool as dsa
	Vracass = dsa.Character('Vracass')

	# Ich habe z.B. 12, 17, 14 für die Sinnesschärfe-Probe gewürfelt
	Vracass.test('sinnesschaerfe', 12, 17, 14)

Dann wird folgendes ausgegeben:

	###################################################
	Test auf           sinnesschaerfe beginnt
	Tests:             ['kl', 'in', 'in']
	TaW:               6
	Eigenschaftswerte: [14, 14, 14]
	Wurf: 12 Geschafft!
	Wurf: 17 Nicht geschafft, TaW - 3
	Wurf: 14 Geschafft!
	Erfolg! 3 TaW-Punkte übrig

Ein komplettes Charakter-Benchmark durchführen
----------------------------------------------

Bei einem kompletten Benchmark wird jedes Talent und jeder Beruf des Charakters statistisch untersucht. Die Benchmark-Ergebnisse werden in einem html-Dokument dargestellt. Dieses wird im Ordner

_characters/dsachar\_CHARACTERNAME/benchmark\_CHARACTERNAME.html_

abgelegt. Neben allgemeinen Angaben zum Charakter werden hier die Talente mit absteigender Gewinnchance und alphabetisch aufgelistet. Außerdem wird für jedes Talent (neben den gängigen Angaben) ein Histogramm mit der normalen und kumulativen Gewinnchance erzeugt (ohne Modifikation des Talentwertes) und eine Grafik, welche die Gewinnchancen bei Modifikation des Talentwertes aufführt.

Das Benchmark kann einige Zeit in Anspruch nehmen, da für jeden Talentwert eine hohe Anzahl (bestimmt durch das Argument _benchmarksize_, default = 50000) an Würfen simuliert und ausgewertet wird. Bei benchmarksize=50000 wird z.B. für jedes Talent 3 Würfe 50000 mal wiederholt und für die Gewinnchancenberechnung verwendet (also 3*50000 pro Talent). Das entspricht (quasi) einer Monte-Carlo Simulation.

Zur durchführung des Benchmarks (Charaktername z.B. Vracass)

	Vracass.benchmark(benchmarksize=1000) # Geht schneller als mit default = 50000, aber weniger genau

Im Terminal werden die Ergebnisse nun nacheinander aufgeführt:

	Test auf             athletik -> wins:    781, fails:    219 win-chance: 78.1 %
	Test auf       fischen_angeln -> wins:    370, fails:    630 win-chance: 37.0 %
	Test auf             heraldik -> wins:    339, fails:    661 win-chance: 33.9 %
	Test auf      fahrzeug_lenken -> wins:    233, fails:    767 win-chance: 23.3 %
	Test auf            schaetzen -> wins:    903, fails:     97 win-chance: 90.3 %
	Test auf               tanzen -> wins:    199, fails:    801 win-chance: 19.9 %
	Test auf           schneidern -> wins:    274, fails:    726 win-chance: 27.4 %

Sind alle Talente getestet, erscheint die Meldung:

	DATEI GESCHRIEBEN: characters/dsachar_Vracass/benchmark_Vracass.html

Diese kann man nun mit einem Browser öffnen und sich die Ergebnisse ansehen.

Einen vorhandenen Charakter laden
---------------------------------

Ist ein Charakter bereits vorhanden, sprich es existiert ein Ordner _characters/CHARACTERNAME_
wird er folgendermaßen geladen (Name z.B. Melchior):

	import dsatool as dsa
	Melchior = dsa.Character('Melchior')
