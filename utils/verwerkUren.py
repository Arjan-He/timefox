from tijdschrijven.models import GeschrevenTijd, Abonnement

def walkTheGrid(formfields):

    velden = []
    token = True
    date = []

    for row in formfields:

        # deel de naam van het formfield op naar een array
        x = row.split('_')

        # het is een grid cell
        if x[0] == 'cell':

            # de inhoud van de cell
            x.append(formfields[row])

            # en evalueer het in de functie schrijfUrenNaarDb
            schrijfUrenNaarDb(x)
            
    return True


def schrijfUrenNaarDb(urenArray):

    tijdID = int(urenArray[2])
    tijd = urenArray[4].strip()
    tijd = 0 if tijd == '' else float(tijd)

    # als er geen tijd is gevuld, tijd is nul
    if tijd==0:

        # er is een record, tijd is leeg, dan weggooien
        if tijdID != 0:
            GeschrevenTijd.objects.filter(id=tijdID).delete()

    # er is tijd ingevuld, maar we willen niet de negatieve uren
    if tijd > 0:

        # er is nog geen record, aanmaken
        if tijdID == 0: 
            aboID = int(urenArray[1])
            GeschrevenTijd.objects.create(AbonnementID=Abonnement.objects.get(id=aboID),
                                          Datum=urenArray[3],
                                          TijdsDuur=tijd)
        
        # en anders updaten
        else:
            GeschrevenTijd.objects.filter(id=tijdID).update(TijdsDuur=tijd)

    return True