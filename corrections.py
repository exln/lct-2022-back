def torgCorr():
    return -4.50*0.01


def floorCorr(sample, analog, maxanalog, maxsample):
    if sample == analog:
        return 0
    else:
        if sample == 1 or sample == maxsample:
            if sample == 1:
                if analog == maxanalog:
                    return -3.1*0.01
                else:
                    return -7.0*0.01
            else:
                if analog == maxanalog:
                    return 0
                if analog == 1:
                    return 3.2*0.01
                else:
                    return -4.0*0.01
        else:
            if analog == 1 or analog == maxanalog:
                if analog == 1:
                    return 7.5*0.01
                else:
                    return 4.2*0.01
            else:
                return 0


def areaCorr(sample, analog):
    if (sample <= 30 and analog <= 30) or (50 >= sample > 30 and 50 >= analog > 30) or (65 >= sample > 50 and 65 >= analog > 50) or (90 >= sample > 65 and 90 >= analog > 65) or (120 >= sample > 90 and 120 >= analog > 90) or (120 < sample and 120 < analog):
        return 0
    else:
        if sample <= 30:
            if 50 >= analog > 30:
                return 6*0.01
            elif 65 >= analog > 50:
                return 14*0.01
            elif 90 >= analog > 65:
                return 21*0.01
            elif 120 >= analog > 90:
                return 28*0.01
            elif 120 < analog:
                return 31*0.01
        elif 50 >= sample > 30:
            if analog <= 30:
                return -6*0.01
            elif 65 >= analog > 50:
                return 7*0.01
            elif 90 >= analog > 65:
                return 14*0.01
            elif 120 >= analog > 90:
                return 21*0.01
            elif 120 < analog:
                return 24*0.01
        elif 65 >= sample > 50:
            if analog <= 30:
                return -12*0.01
            elif 50 >= analog > 30:
                return -7*0.01
            elif 90 >= analog > 65:
                return 6*0.01
            elif 120 >= analog > 90:
                return 13*0.01
            elif 120 < analog:
                return 16*0.01
        elif 90 >= sample > 65:
            if analog <= 30:
                return -17*0.01
            elif 50 >= analog > 30:
                return -12*0.01
            elif 65 >= analog > 50:
                return -6*0.01
            elif 120 >= analog > 90:
                return 6*0.01
            elif 120 < analog:
                return 9*0.01
        elif 120 >= sample > 90:
            if analog <= 30:
                return -22*0.01
            elif 50 >= analog > 30:
                return -17*0.01
            elif 65 >= analog > 50:
                return -11*0.01
            elif 90 >= analog > 65:
                return -6*0.01
            elif 120 < analog:
                return 3*0.01
        elif 120 < sample:
            if analog <= 30:
                return -24*0.01
            elif 50 >= analog > 30:
                return -19*0.01
            elif 65 >= analog > 50:
                return -13*0.01
            elif 90 >= analog > 65:
                return -8*0.01
            elif 120 >= analog > 90:
                return -3*0.01
        else:
            return 100*0.01


def kitchenCorr(sample, analog):
    if analog > 15 or sample > 15 or analog < 1 or sample < 1 or analog == None or sample == None:
        return 100*0.01
    if (sample <= 7 and analog <= 7) or (10 >= sample > 7 and 10 >= analog > 7) or (15 >= sample > 10 and 15 >= analog > 10):
        return 0
    else:
        if sample <= 7:
            if 10 >= analog > 7:
                return -2.9*0.01
            elif 15 >= analog > 10:
                return -8.3*0.01
        elif 10 >= sample > 7:
            if analog <= 7:
                return 3*0.01
            elif 15 >= analog > 10:
                return -5.5*0.01
        elif 15 >= sample > 10:
            if analog < 7:
                return -9*0.01
            elif 10 >= analog > 7:
                return 5.8*0.01


def balconyCorr(sample, analog):
    if (sample == analog) or (sample == "Есть" and analog == "Да") or (sample == "Да" and analog == "Есть"):
        return 0
    else:
        if sample == "Да" or sample == "Есть":
            if analog == "Нет":
                return 5.3*0.01
            else:
                return 100*0.01
        else:
            if analog == "Да" or analog == "Есть":
                return -5*0.01
            else:
                return 100*0.01


def metroCorr(sample, analog):
    if analog >= 20000:
        return 100*0.01
    elif (sample <= 5 and analog <= 5) or (10 >= sample > 5 and 10 >= analog > 5) or (15 >= sample > 10 and 15 >= analog > 10) or (30 >= sample > 15 and 30 >= analog > 15) or (60 >= sample > 30 and 60 >= analog > 30) or (90 >= sample > 60 and 90 >= analog > 60):
        return 0
    else:
        if sample <= 5:
            if 10 >= analog > 5:
                return 7*0.01
            elif 15 >= analog > 10:
                return 12*0.01
            elif 30 >= analog > 15:
                return 17*0.01
            elif 60 >= analog > 30:
                return 24*0.01
            elif 90 >= analog > 60:
                return 29*0.01
        elif 10 >= sample > 5:
            if analog <= 5:
                return -7*0.01
            elif 15 >= analog > 10:
                return 4*0.01
            elif 30 >= analog > 15:
                return 9*0.01
            elif 60 >= analog > 30:
                return 15*0.01
            elif 90 >= analog > 60:
                return 20*0.01
        elif 15 >= sample > 10:
            if analog <= 5:
                return -11*0.01
            elif 10 >= analog > 5:
                return -4*0.01
            elif 30 >= analog > 15:
                return 5*0.01
            elif 60 >= analog > 30:
                return 11*0.01
            elif 90 >= analog > 60:
                return 15*0.01
        elif 30 >= sample > 15:
            if analog <= 5:
                return -15*0.01
            elif 10 >= analog > 5:
                return -8*0.01
            elif 15 >= analog > 10:
                return -5*0.01
            elif 60 >= analog > 30:
                return 6*0.01
            elif 90 >= analog > 60:
                return 10*0.01
        elif 60 >= sample > 30:
            if analog <= 5:
                return -19*0.01
            elif 10 >= analog > 5:
                return -13*0.01
            elif 15 >= analog > 10:
                return -10*0.01
            elif 30 >= analog > 15:
                return -6*0.01
            elif 90 >= analog > 60:
                return 4*0.01
        elif 90 >= sample > 30:
            if analog <= 5:
                return -22*0.01
            elif 10 >= analog > 5:
                return -17*0.01
            elif 15 >= analog > 10:
                return -13*0.01
            elif 30 >= analog > 15:
                return -9*0.01
            elif 60 >= analog > 30:
                return -4*0.01
        else:
            return 100*0.01


def renovationCorr(sample, analog):
    if analog == "косметический":
        analog = "Муниципальный ремонт"
    elif analog == "дизайнерский" or analog == "евро":
        analog = "Современная отделка"
    elif analog == "Требует ремонта" or analog == "Информация неизвестна":
        analog = "Без отделки"
    elif analog == None:
        return 100000

    if sample == analog:
        return 0
    else:
        if sample == "Без отделки":
            if analog == "Муниципальный ремонт":
                return -13400
            elif analog == "Современная отделка":
                return -20100
        elif sample == "Муниципальный ремонт":
            if analog == "Без отделки":
                return 13400
            elif analog == "Современная отделка":
                return -6700
        elif sample == "Современная отделка":
            if analog == "Без отделки":
                return 20100
            elif analog == "Муниципальный ремонт":
                return 6700
        else:
            return 100000


def summOFCorrWithoutRenovation(sF, aF, smF, amF, sA, aA, sK, aK, sB, aB, sM, aM, sR, aR):
    ans = [torgCorr(), floorCorr(sF, aF, smF, amF), areaCorr(sA, aA), kitchenCorr(
        sK, aK), balconyCorr(sB, aB), metroCorr(sM, aM), renovationCorr(sR, aR)]
    return ans


def resultOFCorrWithoutRenovation(price_per_metre, cors):
    before = price_per_metre * \
        (1+cors[0])*(1+cors[1])*(1+cors[2])*(1+cors[3])*(1+cors[4])*(1+cors[5])
    return before


def resultOFCorr(price_per_metre, cors):
    return resultOFCorrWithoutRenovation(price_per_metre, cors)+cors[6]


def summOFCorr(price_per_metre, cors):
    summa = 0.0
    for i in cors[:-1]:
        summa += abs(i)
    return summa + abs(abs(cors[6])/resultOFCorrWithoutRenovation(price_per_metre, cors))
