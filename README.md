
# Algemeen

In deze repository houden we de code voor het Django project TimeFox bij. Dit project bevat de online registratie van uren.

# Afgevangen URLS
```
Weergave welke urls worden afgevangen (zie urls.py)
```

# Apps

Overzicht van de apps die onder dit Django project vallen
* Tijdschrijven

### Tijdschrijven
De app tijdschrijven zorgt voor de registratie van uren. 
```
datamodel hier nog uitwerken
```

# Gebruikte packages

* Django (voor het framework)

Zie ook de file **requirements.txt**. Deze kun je ook uitvoeren via PIP. `pip install -r requirements.txt`

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

# Wat zit er niet in dit project (zie ook Git Ignore)

* database (lokaal: sqlite3, server: postgres)
* migration mappen (match tussen db en project)



