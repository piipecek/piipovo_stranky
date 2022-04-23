class Tile:
    def __init__(self, id: int, type: str, value: int, neighbours_id: list):
        self.type = type
        self.value = value
        self.neighbours_id = neighbours_id
        self.id = id
    
    def __repr__(self):
        return f"Typ: {self.type}, hodnota: {self.value}, sousedi: {self.neighbours_id}, id: {self.id}"

