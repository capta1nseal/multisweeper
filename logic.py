from random import sample

class Logic:
    def __init__(self, field_size: tuple[int, int] = (18, 10), mine_count: int = 35) -> None:
        self.field_size = field_size
        self.mine_count = mine_count

        self.clear_state()

        self.undiscovered_squares = self.field_size[0] * self.field_size[1]

        self.running = False
        self.started = False

    def clear_state(self) -> None:
        '''set to a state with no mines and nothing discovered'''
        self.mine_field = [[0
        for y in range(0, self.field_size[1])]
        for x in range(0, self.field_size[0])]
        self.mask_layer = [[
            False
            for y in range(0, self.field_size[1])]
            for x in range(0, self.field_size[0])]
        self.flags = []

    def generate(self, location: tuple[int, int]) -> None:
        '''generate minefield with starting click at specified position'''
        coordinate_list = [
            (i, j)
            for j in range(0, self.field_size[1])
            for i in range(0, self.field_size[0])
            if not ((i, j) in self.get_neighbours(location) or (i, j) == location)]
        mine_locations = sample(coordinate_list, self.mine_count)
        for mine_location in mine_locations:
            self.place_mine(mine_location)

    def place_mine(self, mine_location: tuple[int, int]) -> None:
        '''
        place a mine at a position
        also increments numbers on safe squares bordering the mine
        '''
        self.mine_field[mine_location[0]][mine_location[1]] = 9

        # increment the counter of all non-mine neighbouring squares
        for location in self.get_neighbours(mine_location):
            if self.mine_field[location[0]][location[1]] != 9:
                self.mine_field[location[0]][location[1]] += 1

    def get_size(self) -> tuple[int, int]:
        '''get size of minefield'''
        return self.field_size

    def get_field(self) -> list[list[int]]:
        '''
        get state of minefield
        changing all unknowns to 10
        '''
        return [[
            self.mine_field[x][y] if self.mask_layer[x][y] else 10
            for y in range(0, self.field_size[1])]
            for x in range(0, self.field_size[0])]

    def stop(self) -> None:
        '''quit game'''
        self.running = False

    def lose_game(self) -> None:
        '''lose game'''
        print("L")
        self.running = False

    def win_game(self) -> None:
        '''win game'''
        print("W")
        self.running = False

    def get_flags(self) -> list[tuple[int, int]]:
        '''get a list of flag coordinates'''
        return self.flags

    def check_win(self) -> None:
        '''check if game won'''
        if self.undiscovered_squares == self.mine_count:
            self.win_game()

    def get_neighbours(self, location: tuple[int, int]) -> list[tuple[int, int]]:
        '''
        get coordinates of squares neighbouring the specified location
        exclude anything outside minefield
        '''
        x, y = location

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

        return [(i, j) for j in y_neighbours for i in x_neighbours if (i, j) != (x, y)]

    def dig(self, location: tuple[int, int]) -> None:
        '''
        dig at a location
        spread if 0 neighbouring mines
        spread if number of flags matches number
        lose if mine
        '''
        if not self.started:
            self.started = True
            self.generate(location)

        dug_value = self.mine_field[location[0]][location[1]]

        if dug_value == 9:
            self.lose_game()

        if not self.running:
            return None

        if dug_value and self.mask_layer[location[0]][location[1]]:
            neighbours = self.get_neighbours(location)
            neighbouring_flags = [
                flag for flag in self.flags
                if flag in neighbours]
            if dug_value == len(neighbouring_flags):
                for neighbour in neighbours:
                    if not self.mask_layer[neighbour[0]][neighbour[1]] and \
                            not neighbour in neighbouring_flags:
                        self.dig(neighbour)

        else:
            island = [location]
            while island:
                x, y = island.pop(0)
                if not self.mask_layer[x][y]:
                    self.mask_layer[x][y] = True
                    self.undiscovered_squares -= 1
                    self.check_win()
                    if not self.mine_field[x][y]:
                        island += self.get_neighbours((x, y))

        if location in self.flags:
            self.flags.remove(location)

    def flag(self, location: tuple[int, int]) -> None:
        '''
        place flag on a square
        remove flag if already flagged
        do nothing if game not started
        '''
        if self.started and not self.mask_layer[location[0]][location[1]]:
            if not location in self.flags:
                self.flags.append(location)
            else:
                self.flags.remove(location)
