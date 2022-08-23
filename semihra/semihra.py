import random
import json
import copy



# with open("example_jmena.txt") as file:
#     jmena = file.read()
# with open("example_indicie.txt") as file:
#     indicie = file.read()


def generate(string_jmen: str, string_indicii: str) -> list:
    """
    Naparsruje jmena a indicie a a rozradi je do struktury, podle ktere se budou tvorit karticky

    jmena: oddelena ", "
    indicie oddeleny ". ", radky indicii oddeleny "\\n"
    """
    def parser(string_jmen: str, string_indicii: str) -> list:

        # dalsi dva radky sjednotej mezery a tecky/carky
        string_jmen = string_jmen.replace(", ", ",")
        string_indicii = string_indicii.replace(". ", ".")

        # parser
        jmena = string_jmen.split(",")
        indicie = [radek.split(".") for radek in string_indicii.split("\n")]
        # dealuje s teckou na konci
        for i in indicie:
            if "" in i:
                i.remove("")
        for i, ind in enumerate(indicie):
            for j, veta in enumerate(ind):
                indicie[i][j] += "."
    
        return jmena, indicie
    
    def zalozeni_datastruktury(jmena):
            #zalozeni datastruktury
            """
            [
                {
                    jmeno: Kuba
                    mluvis_s: [
                        "jmeno",
                        "jmeno2",
                        "jmeno3"
                    ]
                    uvodni_veta: Tvuj dilek je idk kde
                    dale_vis: [
                        "abc",
                        "def"
                    ]
                },
                { 
                    jmeno:...
                }
            ]
            """
            data = [{"jmeno": jmeno, "mluvis_s": [], "uvodni_veta": "", "dale_vis": []} for jmeno in jmena]
            return data
        
    def vytvareni_grafu(data):
        pass
        #vytvareni grafu: 
        # 1) picknu jednoho co jeste nema 3 kontakty
        # 2) vyberu  dalsi takovy, co nemaj tri a jeste s nim nemluvej
        # 3) vyberu random z nich a spojim je, nebo prichazi dokoncovani
        # 4) dokoncovani: vybiram ty co jeste nemaj 3, k nim nejaky z tech co maj 3 a jeste nemluvej spolu a spojim je.
        # tak se stane, ze vsichni maj 3 a nekdo 4.
        
        while True:
            jednicka_candidates = list(filter(lambda x: len(x["mluvis_s"]) < 3, data))
            
            if len(jednicka_candidates)  ==  0:
                break
            else:
                # seradim je podle toho, kolik uz maj kontaktu a vemu toho kdo ma nejmin
                jednicka_candidates.sort(key = lambda x: len(x["mluvis_s"]))
                jednicka = jednicka_candidates[0]
            
            dvojka_cadidates = list(filter(lambda x: (len(x["mluvis_s"]) < 3) and (jednicka["jmeno"] not in x["mluvis_s"]) and (jednicka["jmeno"] != x["jmeno"]), data))

            # pokud nevyjde zadnej kandidat, tak povolim restrikci a dovolim i ty co maj 3 kontakty
            if len(dvojka_cadidates) == 0:
                dvojka_cadidates = list(filter(lambda x: (jednicka["jmeno"] not in x["mluvis_s"]) and (jednicka["jmeno"] != x["jmeno"]), data))
            dvojka = random.choice(dvojka_cadidates)

            jednicka["mluvis_s"].append(dvojka["jmeno"])
            dvojka["mluvis_s"].append(jednicka["jmeno"])
        
        return data
        
    def zaplnovani_indiciema(data):

        # zaplnovani indiciema
        # 100 pokusu, kdyz nevyjde tak hazim error no
        for i in range(100):
            data_copy = copy.deepcopy(data)
            nastala_chyba = False
            hotova_jmena =  []
            for ind in indicie:
                # picknu jmeno, co budu obsazovat
                base_karta = random.choice(list(filter(lambda x: x["jmeno"] not in hotova_jmena, data_copy)))
                hotova_jmena.append(base_karta["jmeno"])

                # vyberu kandidaty co muzou drzet info pro nej

                kandidati = list(filter(lambda x: x["jmeno"] != base_karta["jmeno"] and base_karta["jmeno"] not in x["mluvis_s"] and len(x["dale_vis"])<2, data_copy))
                
                # vyberu dva z nich - kdyz to nejde, reroll celeho

                if len(kandidati) < 2:
                    nastala_chyba = True
                    break
                else:
                    zvoleni = random.sample(kandidati, 2)
                    base_karta["uvodni_veta"] = ind[0]
                    zvoleni[0]["dale_vis"].append(ind[1])
                    zvoleni[1]["dale_vis"].append(ind[2])

            if nastala_chyba:
                continue
            else:
                return data_copy, i
        return False, i



    jmena, indicie = parser(string_jmen=string_jmen, string_indicii=string_indicii)

    if len(jmena) != len(indicie):
        return ["Není zadáno stejně jmen jako indicií. Naprav to prosím a zkus to znova."]
    elif len(jmena) <= 5:
        return ["Je málo jmen, tahle hra má smysl s minimálně 6 dětma."]
    else:
        for i in range(100):

            data = zalozeni_datastruktury(jmena=jmena)
            data = vytvareni_grafu(data)
            data, pokus_count = zaplnovani_indiciema(data)

            if data:
                print(f"Pro zajimavost, je to {i}. reroll grafu a {pokus_count}. reroll instrukci v nem.")
                return data
        return ["10000 pokusů nestačilo, idk proč, kontaktuj Pípa xd"]





# result = generate(jmena, indicie)

# with open("example_result.json", "w") as file:
#     file.write(json.dumps(result, indent=4))


