Das steht doch alles schon im PDF, warum hier nochmal?

##Setup
### Python 3.4.
Wenn du ein Mac benutzt, oder eine frühere Version von Python nutzt, möchtest du das Alias "python3" nutzen.

### Installiere "pip"
**Ubuntu/Linux Mint:** 

- sudo apt-get install python3-pip

**Mac:**

- Ab Python 3.4 sollte pip3 mitinstalliert sein.

### Installiere Django
- pip install Django
- pip3 install Django

### Starte den Entwicklungsserver im PROJECT/pizza Verzeichnis:
- python manage.py runserver
- python3 manage.py runserver

(Erreichbar unter 127.0.0.1:8000)

##Whitebox Testing
### Teste die App im PROJECT/pizza Verzeichnis:
- python manage.py test
- python3 manage.py test

##Blackbox Testing
- Download Firefox 51.0.1
- Add Selenium IDE as Add-on to Firefox, 2.9.1 (https://addons.mozilla.org/de/firefox/addon/selenium-ide/)
- Add Selenium IDE: Flow Control (Due to Errors with the FF 51) (https://addons.mozilla.org/en-US/firefox/addon/flow-control/?src=dp-dl-othersby)
- Reopen Firefox
- Open Selenium in Tools (EN)/Extras(DE) -> Selenium IDE
- Go to File(EN)/Datei(DE) -> "Open Test Suite" to import the test suite
- Click on "Play Entire Test Suite" button
- Watch the magic happening