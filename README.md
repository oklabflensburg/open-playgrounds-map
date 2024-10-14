# Spielplatzkarte Flensburg


![Screenshot interaktive Karte](https://raw.githubusercontent.com/oklabflensburg/open-playgrounds-map/main/screenshot_spielplatzkarte.jpg)


_Haftungsausschluss: Dieses Repository und die zugehörige Datenbank befinden sich derzeit in einer Beta-Version. Einige Aspekte des Codes und der Daten können noch Fehler enthalten. Bitte kontaktieren Sie uns per E-Mail oder erstellen Sie ein Issue auf GitHub, wenn Sie einen Fehler entdecken._


## Datenquelle

Die Stadt Flensburg stellt hier eine [Liste im PDF Format](https://www.flensburg.de/PDF/Spielpl%C3%A4tze_im_Stadtgebiet_Flensburg.PDF?ObjSvrID=2306&ObjID=4212&ObjLa=1&Ext=PDF&WTR=1) für Besucher der Spielplätze zur Verfügung. Unser Ziel ist es Interessierten eine Nutzung der offenen Daten mit wenig Arbeit und einem Mehrwert anzubieten.


## Interaktive Karte

Diese interaktive webbasierte Karte ist auf Basis der Daten der oben aufgeführten Liste entstanden. Doch wir mussten für die Darstellung der Spielplätze auf einer webbasierten Karte noch weitere Informationen finden, so haben wir auf den Seiten des [TBZ Flensburg](https://tbz-flensburg.de/de/spielplaetze) recherchiert und sogar eine Karte gefunden. Doch ist diese Karte der "Spielfächen" sowie sie im Amtsdeutsch bezeichnet wurde, weder schnell im Netz auffindbar noch für den nicht IT interessierten Besucher gut nutzbar. Nach einigen Stunden des reverse Engineerings konnten wir die Daten extrahieren und mittels einem selbst geschriebenen Python Skripts in ein maschinenlesbares offenes Format nach der Spezifikation [RFC 7946](https://geojson.org/) umgewandelt und auf Basis der OpenSteetMap Karte dargestellt.


## Aktualisierung der Daten

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 retrieve_geometries.py --url https://tbz-flensburg.de/de/spielplaetze --category 5 --target ../data/spielplaetze_flensburg.json --verbose
python3 generate_geojson.py ../data/spielplaetze_flensburg.json ../data/spielplaetze_flensburg.geojson
deactivate
```
