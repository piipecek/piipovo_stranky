from catan.board import Board

#class Tile - docela self explanatory
#class Board - generuje tiles se spravnejma sousedama podle id a umi je tisknout
def generate(data) -> dict:

    force_middle_desert = data["force_desert"]
    allow_same_neighbours = data["adjacent_land"]

    allow_ports_next_to_source = data["ports"]

    allow_same_adjacent_values = data["adjacent_values"]
    force_unique_six_eight = data["unique_68"]
    allow_adjacent_six_eight = data["adjacent_68"]

    b = Board()
    b.obsadit_typama(force_middle_desert, allow_same_neighbours)
    b.pridat_okraje(allow_ports_next_to_source)
    b.pridat_hodnoty(allow_same_adjacent_values, force_unique_six_eight, allow_adjacent_six_eight)

    return b.to_json()
