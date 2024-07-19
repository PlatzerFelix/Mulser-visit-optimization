import datetime

# Defining the rankClient and rankLead functions


def rankClient(
    KundenVolumen,
    LetzterBesuch,
    offeneRechnung,
    aktiverVertrag,
    alterTore,
    vertragsAblauf,
):
    value = 0
    deltaTime = datetime.date.today() - LetzterBesuch
    deltaTime = deltaTime.total_seconds() / 60 / 60 / 24

    if deltaTime < 30 * 3:
        value = 80
    elif deltaTime < 30 * 6:
        value = 90
    elif deltaTime < 30 * 12:
        value = 120
    elif deltaTime < 30 * 24:
        value = 150
    elif deltaTime < 30 * 36:
        value = 170
    else:
        value = 180

    if KundenVolumen <= 25000:
        value -= 70
    elif KundenVolumen <= 50000:
        value -= 60
    elif KundenVolumen <= 100000:
        value -= 50
    elif KundenVolumen <= 200000:
        value -= 40
    elif KundenVolumen <= 300000:
        value -= 30
    elif KundenVolumen <= 500000:
        value -= 20
    elif KundenVolumen <= 1000000:
        value -= 10

    if value >= 110:
        kundenBuchstabe = "A"
    elif value >= 70:
        kundenBuchstabe = "B"
    else:
        kundenBuchstabe = "C"

    value = 0
    deltaTime = datetime.date.today() - vertragsAblauf
    deltaTime = divmod(deltaTime.total_seconds(), 31536000)[0]
    if deltaTime <= 1:
        value = 15
    elif deltaTime <= 2:
        value = 8
    elif deltaTime <= 3:
        value = 6
    elif deltaTime <= 5:
        value = 4
    else:
        value = 2

    if aktiverVertrag:
        value += 2
    if not offeneRechnung:
        value += 2
    if alterTore <= 1:
        value += 1
    elif alterTore <= 4:
        value += 2
    elif alterTore <= 6:
        value += 3
    elif alterTore <= 15:
        value += 4
    else:
        value += 5

    if value >= 17:
        kundenZahl = 1
    elif value >= 14:
        kundenZahl = 2
    else:
        kundenZahl = 3

    return kundenBuchstabe + str(kundenZahl)


def rankLead(umsatz, status):
    value = 0
    if status == 0:
        value = 90
    elif status == 50:
        value = 120
    else:
        value = 180

    if umsatz <= 100000:
        value -= 70
    elif umsatz <= 500000:
        value -= 60
    elif umsatz <= 1000000:
        value -= 50
    elif umsatz <= 5000000:
        value -= 40
    elif umsatz <= 10000000:
        value -= 30
    elif umsatz <= 2500000:
        value -= 20
    elif umsatz <= 5000000:
        value -= 10

    if value >= 110:
        leadBuchstabe = "A"
    elif value >= 60:
        leadBuchstabe = "B"
    else:
        leadBuchstabe = "C"

    return leadBuchstabe
