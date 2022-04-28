from catan.tile import Tile
from typing import List
from random import randint, choice
import itertools

class Board:
    def __init__(self) -> None:
        self.tiles: List["Tile"] = []
        self.tiles.append(Tile(0,None,None,[1,3,4]))
        self.tiles.append(Tile(1,None,None,[0,2,4,5]))
        self.tiles.append(Tile(2,None,None,[1,5,6]))
        self.tiles.append(Tile(3,None,None,[0,4,7,8]))
        self.tiles.append(Tile(4,None,None,[0,1,3,5,8,9]))
        self.tiles.append(Tile(5,None,None,[1,2,4,6,9,10]))
        self.tiles.append(Tile(6,None,None,[2,5,10,11]))
        self.tiles.append(Tile(7,None,None,[3,8,12]))
        self.tiles.append(Tile(8,None,None,[3,4,7,9,12,13]))
        self.tiles.append(Tile(9,None,None,[4,5,8,10,13,14]))
        self.tiles.append(Tile(10,None,None,[5,6,9,11,14,15]))
        self.tiles.append(Tile(11,None,None,[6,10,15]))
        self.tiles.append(Tile(12,None,None,[7,8,13,16]))
        self.tiles.append(Tile(13,None,None,[8,9,12,14,16,17]))
        self.tiles.append(Tile(14,None,None,[9,10,13,15,17,18]))
        self.tiles.append(Tile(15,None,None,[10,11,14,18]))
        self.tiles.append(Tile(16,None,None,[12,13,17]))
        self.tiles.append(Tile(17,None,None,[13,14,16,18]))
        self.tiles.append(Tile(18,None,None,[14,15,17]))
        #vyznam: okraj "kamen" na pozici 2 sousedi s policky 11,15
        self.definice_okraju = {
            "kamen": {
                0:[0,1],
                1:[2,6],
                2:[11,15],
                3:[17,18],
                4:[12,16],
                5:[3,7]
            },
            "drevo": {
                0:[0,1],
                1:[2,6],
                2:[11,15],
                3:[17,18],
                4:[12,16],
                5:[3,7]
            },
            "cihly": {
                0:[1,2],
                1:[6,11],
                2:[15,18],
                3:[16,17],
                4:[7,12],
                5:[0,3]
            },
            "ovce": {
                0:[1,2],
                1:[6,11],
                2:[15,18],
                3:[16,17],
                4:[7,12],
                5:[0,3]
            },
            "obili": {
                0:[1,2],
                1:[6,11],
                2:[15,18],
                3:[16,17],
                4:[7,12],
                5:[0,3]
            },
            None:None
        }
        
    def __repr__(self) -> str:
        return str(self.tiles)

    def print_values(self):
        print(self._printing_pattern([str(x.value) for x in self.tiles]))

    def print_types(self):
        print(self._printing_pattern([str(x.type) for x in self.tiles]))
    
    def print_ids(self): 
        print(self._printing_pattern([str(x.id) for x in self.tiles]))

    def _printing_pattern(self, list_to_print: List[str]):
        unit = max([len(x) for x in list_to_print]) #kolik znaku ma nejdelsi vec co se bude tisknout
        result = []

        #leading spaces
        result.append((" "*(unit))*2)
        result.append(" "*(unit))
        result.append("")
        result.append(" "*(unit))
        result.append((" "*(unit))*2)

        

        for i, info in enumerate(list_to_print):
            novy_kousek = info.ljust(unit, " ") + "".ljust(unit, " ")
            if i < 3:
                result[0] += novy_kousek
                continue
            elif i < 7:
                result[1] += novy_kousek
                continue
            elif i < 12:
                result[2] += novy_kousek
                continue
            elif i < 16:
                result[3] += novy_kousek
                continue
            else:
                result[4] += novy_kousek
                continue


        return "\n".join(result)

    def obsadit_typama(self, force_middle_desert, allow_same_neighbours):

        def check_neighbour_types() -> bool:
            vyhovuje = True
            for tile in self.tiles:
                if tile.type in [x.type for x in list(filter(lambda y: y.id in tile.neighbours_id, self.tiles))]:
                    vyhovuje = False
            return vyhovuje

        while not check_neighbour_types():
            dostupne_typy = ["zlodej", "obili", "obili", "obili", "obili", "drevo", "drevo", "drevo", "drevo", "ovce", "ovce", "ovce", "ovce", "kamen", "kamen", "kamen", "cihly", "cihly", "cihly"]
            for tile in self.tiles:
                tile.type = None

            if force_middle_desert:
                self.tiles[9].type = "zlodej"
            else:
                self.tiles[randint(0,18)].type = "zlodej"
            dostupne_typy.remove("zlodej")

            for tile in self.tiles:
                if tile.type is None:
                    tile.type = choice(dostupne_typy)
                    dostupne_typy.remove(tile.type)
        
            if allow_same_neighbours:
                 break      
    
    def pridat_okraje(self, allow_ports_next_to_source):
        moznosti_okraju = list(itertools.permutations(["kamen","cihly","ovce","obili","drevo",None]))
        if allow_ports_next_to_source:
            self.okraje = choice(moznosti_okraju)
        else:
            # prochazim vsechny permutace a kontrouju, jestli vyhovujou
            vyhovujici_okraje = []
            for navrh_okraju in moznosti_okraju:
                vyhovuje = True
                for i, surovina in enumerate(navrh_okraju):
                    sousedi = self.definice_okraju[surovina]
                    if sousedi is None:
                        continue
                    else:
                        suroviny_sousedu = [y.type for y in list(filter(lambda x: x.id in sousedi[i], self.tiles))]
                        if surovina in suroviny_sousedu:
                            vyhovuje = False
                            break
                if vyhovuje:
                    vyhovujici_okraje.append(navrh_okraju)
            if len(vyhovujici_okraje) == 0:
                print("Divná věc, ani jeden okraj nevyhovoval.")
                self.okraje = None
            else:
                self.okraje = choice(vyhovujici_okraje)

    def pridat_hodnoty(self, allow_same_adjacent_values, force_unique_six_eight, allow_adjacent_six_eight):
        
        #tyhle checking fce returnujou true, kdyz rozhozeni vyhovuje
        def check_adjacent_values() -> bool:
            vyhovuje = True
            for tile in self.tiles:
                if tile.value in [x.value for x in list(filter(lambda y: y.id in tile.neighbours_id, self.tiles))]:
                    vyhovuje = False
                    break
            return vyhovuje
        
        def check_unique_six_eight() -> bool:
            suroviny_pod_six_eight = [x.type for x in list(filter(lambda y: y.value in [6,8], self.tiles ))]
            if len(suroviny_pod_six_eight) == len(list(set(suroviny_pod_six_eight))):
                return True
            return False

        def check_adjacent_six_eight() -> bool:
            sousedi_policek_s_six_eight = [x.neighbours_id for x in list(filter(lambda y: y.value in [6,8], self.tiles ))]
            sjednoceni_id_sousedu = []
            for l in sousedi_policek_s_six_eight:
                sjednoceni_id_sousedu += l

            hodnoty_tech_sousedu = [x.value for x in list(filter(lambda y: y.id in sjednoceni_id_sousedu, self.tiles))]
            if 6 in hodnoty_tech_sousedu:
                return False
            if 8 in hodnoty_tech_sousedu:
                return False
            return True


        list(filter(lambda x: x.type == "zlodej", self.tiles))[0].value = 0
        complete = False # na konci while loopu se dycky updatne. potrebuju ale mit defaultne true, aby to zkoncilo i pri nulovejch kontrolach
        while not complete:
            complete =  True
            dostupne_hodnoty = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
            for tile in self.tiles:
                if tile.value != 0:
                    tile.value = choice(dostupne_hodnoty)
                    dostupne_hodnoty.remove(tile.value)
            if not allow_same_adjacent_values:
                ajd_check = check_adjacent_values()
            else:
                ajd_check = True
            if not allow_adjacent_six_eight:
                adj_s_e = check_adjacent_six_eight()
            else:
                adj_s_e = True
            if force_unique_six_eight:
                force_unique = check_unique_six_eight()
            else:
                force_unique = True
            complete = all([adj_s_e, ajd_check, force_unique])
    
    def to_json(self) -> dict:
        result = {
            "tiles": [],
            "edges": self.okraje
        }
        for tile in self.tiles:
            result["tiles"].append(
                {
                    "id":tile.id,
                    "type":tile.type,
                    "value":tile.value
                }
            )

        return result

