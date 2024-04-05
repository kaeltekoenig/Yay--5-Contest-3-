def find_missing_parts(g, gdgts, dst):
    return set(dst) - gdgts[g]


def choose_part(mset, dst):
    '''
    mset - множество недостающих пакетов
    dst - словарь пакеты:устройства
    '''
    rarest = n + 1
    rarpck = k + 1
    for pck, hlrdset in dst.items():
        if pck in mset:
            if len(hlrdset) < rarest:
                rarest = len(hlrdset)
                rarpck = pck

    return rarpck
        
def choose_giver(pck, dst, gdg):
    '''
    gdg - словарь устройства:пакеты
    pck - запрашиваемый пакет
    dst - словарь пакеты:устройства
    '''   
    mindwn = k + 1
    trgt = 1
    for p, gset in dst.items():
        if p == pck:
            for g in sorted(gset):
                if len(gdg.get(g)) < mindwn:
                    mindwn = len(gdg.get(g))
                    trgt = g
            return trgt
    return trgt


def give(gv, rqsts, wrthmp, gdgts):
    '''
    gv - текущее устройство-донор
    wrth - матрица ценностей
    rqsts - множество запрашивающих устройств
    '''
    # Сначала ищем наиболее ценное устройство
    wrthrset = set()
    maxv = 0
    for t in wrthmp[gv]:
        if rqsts[gv].get(t):
            if wrthmp[gv][t] < maxv:
                del rqsts[gv][t]
            elif wrthmp[gv][t] == maxv:
                wrthrset.add(t)
            elif wrthmp[gv][t] > maxv:
                maxv = wrthmp[gv][t]
                wrthrset = {t}
    
    # Проверяем количество скачанных частей
    if len(wrthrset) > 1:
        dwnld_dpnd_set = set()
        mindwnld = k
        for g, prts in gdgts.items():
            if g in wrthrset:
                if len(prts) < mindwnld:
                    mindwnld = len(prts)
                    dwnld_dpnd_set = {g}
                elif len(prts) == mindwnld and mindwnld != k:
                    dwnld_dpnd_set.add(g)
        
        tkr = min(dwnld_dpnd_set)
        prt = rqsts[gv][tkr]
    else:
        tkr = min(wrthrset)
        prt = rqsts[gv][tkr]
    return tkr, prt


def take(g, prt, gdgts, dst):
    gdgts[g].add(prt)
    dst[prt].add(g)


def check_update_status(dst):
    elems = 0
    for x in dst.values():
        elems += len(x)
    if elems != n * k:
        return False

    return True

#######################################################
# Множество запросов из кортежей типа устройство:запрашиваемый пакет

with open('input.txt', 'r') as f:
    n, k = map(int, f.readline().split())

# Пакет: Устройства, скачавшие пакет
distributive = {p:{1} for p in range(1, k + 1)}
# Устройство: Установленный пакеты
gadgets = {g:(set() if g > 1 else set(distributive)) for g in range(1, n + 1)}
# Матрица ценностей: устройство:{другое устройство:ценность}
worthmap = {g:{xg:0 for xg in gadgets.keys() if xg != g} for g in range(1, n + 1)}
# Сколько таймслотов на каждый апдейт. Устройство:минут
slots = {p:0 for p in range(2, n + 1)}
######################################################
cycle = 0

with open('output.txt', 'w') as z:
    while True:
        cycle += 1
        if check_update_status(distributive):
            break
        else:
            # ЦИКЛ ЗАПРОСОВ
            requests = {g:{} for g in range(1, n + 1)}
            for gadget in gadgets:
                missingset = find_missing_parts(gadget, gadgets, distributive)
                if missingset:
                    totakepart = choose_part(missingset, distributive)
                    targetgiver = choose_giver(totakepart, distributive, gadgets)
                    requests[targetgiver][gadget] = totakepart
                    slots[gadget] += 1
            
            # ЦИКЛ ОТВЕТОВ
            answers = []
            for gadget in gadgets:
                if requests.get(gadget):
                    taker, part = give(gadget, requests, worthmap, gadgets)
                    take(taker, part, gadgets, distributive)
                    answers.append([gadget, taker])
            for ans in answers:
                worthmap[ans[1]][ans[0]] += 1


    print(' '.join(map(str, list(slots.values()))), file=z)