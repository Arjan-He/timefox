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

    tijdID = int(urenArray[2])
    tijd = urenArray[4].strip()
    tijd = 0 if tijd == '' else float(tijd)

    if tijd==0:
        if tijdID != 0:
            GeschrevenTijd.objects.filter(id=tijdID).delete()

    if tijd != 0:

        if tijdID == 0: 
            aboID = int(urenArray[1])
            GeschrevenTijd.objects.create(AbonnementID=Abonnement.objects.get(id=aboID),
                                          Datum=urenArray[3],
                                          TijdsDuur=tijd)
        
        else:
            GeschrevenTijd.objects.filter(id=tijdID).update(TijdsDuur=tijd)



    
    return False