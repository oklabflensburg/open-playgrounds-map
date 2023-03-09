# Open Playgrounds


![Screenshot interaktive Karte](https://raw.githubusercontent.com/p3t3r67x0/open-playgrounds/master/spielplaetze_in_flensburg.png)


## Datenquelle

Die Stadt Flensburg stellt hier eine [Liste im PDF Format](https://www.flensburg.de/media/custom/2306_4212_1.PDF) für Besucher der Spielplätze zur Verfügung. Unser Ziel ist es Interessierten eine Nutzung der offenen Daten mit wenig Arbeit und einem Mehrwert anzubieten.


## Interaktive Karte

Diese interaktive webbasierte Karte ist auf Basis der Daten der oben aufgeführten Liste entstanden. Doch wir mussten für die Darstellung der Spielplätze auf einer webbasierten Karte noch weitere Informationen finden, so haben wir auf den Seiten des [TBZ Flensburg](https://www.tbz-flensburg.de/%C3%96ffentliches-Gr%C3%BCn/Spielfl%C3%A4chen/) recherchiert und sogar eine Karte gefunden. Doch ist diese Karte der "Spielfächen" sowie sie im Amtsdeutsch bezeichnet wurde, weder schnell im Netz auffindbar noch für den nicht IT interessierten Besucher gut nutzbar. Nach einigen Stunden des reverse Engineerings konnten wir die Daten extrahieren und mittels einem selbst geschriebenen Python Skripts in ein maschinenlesbares offenes Format nach der Spezifikation [RFC 7946](https://geojson.org/) umgewandelt und auf Basis der OpenSteetMap Karte dargestellt.
