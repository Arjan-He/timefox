
# Algemeen

In deze repository houden we de code voor het Django project TimeFox bij. Dit project bevat de online registratie van uren.

# Afgevangen URLS

Op dit moment worden de volgende url's afgevangen:
| Url                                      | Pagina                |
| ---------------------------------------- |-----------------------|
| /tijdschrijven/                          | Indexpagina           |
| /tijdschrijven/projecten                 | Projecten raadplegen  |
| /tijdschrijven/project/create/           | Project aanmaken      |
| /tijdschrijven/project/<int:pk>/update/  | Project wijzigen      |
| /tijdschrijven/project/<int:pk>/delete/  | Project verwijderen   |
| /tijdschrijven/abonnementen              | Toon abonnementen     |
| /tijdschrijven/abonnement/create/        | Abonnement toevoegen  |
| /tijdschrijven/urenschrijven             | Uren schrijven        |

# Apps

Overzicht van de apps die onder dit Django project vallen
* Tijdschrijven

### Tijdschrijven
De app tijdschrijven zorgt voor de registratie van uren. In de app zijn de volgende datamodellen uitgewerkt:
* Project -> De projecten waarop geschreven wordt
* Persoon -> De personen die tijd kunnen schrijven. Een aanvulling op de Django user-klasse
* Abonnement -> Koppeling van projecten aan personen. Op welke projecten mag men schrijven
* ProjectTemplate -> Templates van activiteiten voor de diverse soorten projecten
* GeschrevenTijd -> De geschreven uren

# Gebruikte packages

* Django 
* Python-decouple - afscherming wachtwoorden etc

Zie ook de file **requirements.txt**. Deze kun je ook uitvoeren via PIP. `pip install -r requirements.txt`

Met het uitvoeren van het script **load_model_data.py** kan de database initieel worden gevuld met projecten.
Deze kan worden aangeroep via `manage.py load_model_data` 

# Beheer
De productieserver draait met de volgende configuratie:
| Item          | Product       |
| ------------- |---------------|
| OS            | Centos 8      |
| Webserver     | Nginx 1.19    |
| Database      | Postgres 12.3 |

We hebben de volgende logging geconfigureerd:
| Software      | Locatie log      |
| ------------- | ---------------- |
| Nginx         | /var/log/nginx/  |
| Uwsgi         | /var/log/uwsgi/  |
| Django        | /var/log/django/ |

# Gebruikte javascript 
Bootstrap-4.5.3
Jquery-3.5.1
JQuery-Ui-1.12.1
Weekpicker: 
jquery.fancytree: https://www.npmjs.com/package/jquery.fancytree


# Wat zit er niet in dit project (zie ook Git Ignore)

* database (lokaal: sqlite3, server: postgres)
* migration mappen (match tussen db en project)
* settings.ini voor de toekenning van de variabelen: SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT,EMAIL_BACKEND)



