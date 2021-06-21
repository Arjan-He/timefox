from django.contrib.auth.decorators import login_required
from tijdschrijven.models import GeschrevenTijd, Project_Activiteit,Persoon


def walkTheGrid(formfields,usr):

    for row in formfields:

        # deel de naam van het formfield op naar een array
        x = row.split('_')

        # het is een grid cell
        if x[0] == 'cell':

            # de inhoud van de cell
            x.append(formfields[row])

            # en evalueer het in de functie schrijfUrenNaarDb
            schrijfUrenNaarDb(x,usr)
            
    return True



def schrijfUrenNaarDb(urenArray,usr):

    tijdID = int(urenArray[2])
    tijd = urenArray[4].strip()
    tijd = 0 if tijd == '' else float(tijd)

    # als er geen tijd is gevuld, tijd is nul
    if tijd == 0:

        # er is een record, tijd is leeg, dan weggooien
        if tijdID != 0:
            GeschrevenTijd.objects.filter(id=tijdID).delete()

    # er is tijd ingevuld, maar we willen niet de negatieve uren
    if tijd > 0:

        # er is nog geen record, aanmaken
        if tijdID == 0:
            paID = int(urenArray[1])
            GeschrevenTijd.objects.create(projectactiviteit=Project_Activiteit.objects.get(pk=paID),
                                          persoon=Persoon.objects.get(pk=usr),
                                          datum=urenArray[3],
                                          tijdsduur=tijd)
        
        # en anders updaten
        else:
            GeschrevenTijd.objects.filter(id=tijdID).update(tijdsduur=tijd)

    return True
