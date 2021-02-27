from tijdschrijven.models import GeschrevenTijd, Abonnement

def walkTheGrid(formfields):

    velden = []
    token = True
    date = []

    for row in formfields:

        x = row.split('_')

        if x[0] == 'cell':
            x.append(formfields[row])
            schrijfUrenNaarDb(x)
            velden.append(x)

    return velden


def schrijfUrenNaarDb(urenArray):

    Tijdid = int(urenArray[2])

    if Tijdid != 0 and urenArray[4] == '':
        GeschrevenTijd.objects.filter(id=Tijdid).delete()

    if Tijdid != 0 and urenArray[4] != '':
        tijd = float(urenArray[4])
        GeschrevenTijd.objects.filter(id=Tijdid).update(TijdsDuur=tijd)

    if Tijdid == 0 and urenArray[4] != '': 
        aboID = int(urenArray[1])
        tijd = float(urenArray[4])
        GeschrevenTijd.objects.create(AbonnementID=Abonnement.objects.get(id=aboID),
                                Datum=urenArray[3],
                                TijdsDuur=tijd)

    
    return False