from random import sample

class Logic:
    def __init__(self, field_size: tuple[int, int] = (18, 10), mine_count: int = 35) -> None:
        self.field_size = field_size
        self.mine_count = mine_count

        self.clear_state()

        self.running = False

    def clear_state(self) -> None:
        '''set to a state with no mines and nothing discovered'''
        self.mine_field = [[0 for y in range(0, self.field_size[1])] for x in range(0, self.field_size[0])]
        self.mask_layer = [[False for y in range(0, self.field_size[1])] for x in range(0, self.field_size[0])]


    def place_mine(self, mine_location: tuple[int, int]) -> None:
        '''
        place a mine at a position
        also increments numbers on safe squares ordering the mine
        '''
        x = mine_location[0]
        y = mine_location[1]

        self.mine_field[x][y] = 9
        
        # - find neighbouring squares, accounting for edges
        if not (x < 1 or x > self.field_size[0] - 2):
            x_neighbours = (x-1, x, x+1)
        else:
            if x < 1:
                x_neighbours = (x, x+1)
            else:
                x_neighbours = (x-1, x)
        if not (y < 1 or y > self.field_size[1] - 2):
            y_neighbours = (y-1, y, y+1)
        else:
            if y < 1:
                y_neighbours = (y, y+1)
            else:
                y_neighbours = (y-1, y)
        
        for i in x_neighbours:
            for j in y_neighbours:
                if (i, j) != (x, y) and self.mine_field[i][j] != 9:
                    self.mine_field[i][j] += 1

    def get_size(self) -> tuple[int, int]:
        '''get size of minefield'''
        return self.field_size

    def stop(self) -> None:
        '''quit game'''
        self.running = False