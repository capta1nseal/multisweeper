from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame
from logic import Logic

class UI:
    def __init__(self, logic: Logic, window_size: tuple[int, int] = (640, 480)) -> None:
        pygame.init()

        self.logic = logic
        self.window_constants = {
            "window_size": window_size,
            "scaled_game_size": (0, 0),
            "inset_game_position": (0,0)
        }
        self.colours = {
            "background_colour": 0x000000,
            "dark_unknown_colour": 0x444444,
            "light_unknown_colour": 0x666666,
            "dark_known_colour": 0xAAAAAA,
            "light_known_colour": 0xCCCCCC,
            "flag_colour": 0xF11919,
            "font_colour": 0x000000
        }

        self.screen = pygame.display.set_mode(self.window_constants["window_size"], pygame.RESIZABLE)
        self.screen.fill(self.colours["background_colour"])

        self.calculate_scaling()
        self.render_numbers()

        self.small_surface = pygame.Surface(self.logic.get_size())
        self.pxgrid = pygame.PixelArray(self.small_surface)

        self.fullscreen = False

    def calculate_scaling(self):
        '''
        calculate some constants for drawing the game
        at the right scale in the right position in the window
        '''
        grid_size = self.logic.get_size()
        window_size = self.window_constants["window_size"]
        if window_size[0] / grid_size[0] <= \
                window_size[1] / grid_size[1]:
            self.window_constants["scaled_game_size"] = (
                window_size[0],
                window_size[0] * grid_size[1] / grid_size[0])
        else:
            self.window_constants["scaled_game_size"] = (
                window_size[1] * grid_size[0] / grid_size[1],
                window_size[1])

        self.window_constants["inset_game_position"] = (
            window_size[0] / 2 - self.window_constants["scaled_game_size"][0] / 2,
            window_size[1] / 2 - self.window_constants["scaled_game_size"][1] / 2)

    def render_numbers(self) -> None:
        '''render the numbers to surfaces at scale'''
        square_size = self.window_constants["scaled_game_size"][1] / self.logic.get_size()[1]
        font_size = int(square_size * 0.9)
        font = pygame.font.Font("./data/font/Lato/Lato-Bold.ttf", font_size)
        self.numbers = [
            font.render(str(number), True, self.colours["font_colour"])
            for number in range(1, 9)]
        self.number_offsets = [
            (square_size - surface.get_size()[0]) / 2
            for surface in self.numbers] + [(square_size - font_size) / 2]

    def toggle_fullscreen(self) -> None:
        '''change between fullscreen and windowed display modes'''
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (640, 480), pygame.RESIZABLE)
            self.fullscreen = False
        else:
            self.screen = pygame.display.set_mode(
                (0, 0), pygame.RESIZABLE | pygame.FULLSCREEN)
            self.fullscreen = True

        self.window_constants["window_size"] = self.screen.get_size()
        self.calculate_scaling()
        self.render_numbers()

        self.screen.fill(self.colours["background_colour"])
        pygame.display.update()

    def handle_events(self) -> None:
        '''
        handle pygame events
        such as key presses, window resizing and clicks
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logic.stop()

            elif event.type == pygame.VIDEORESIZE:
                self.window_constants["window_size"] = event.size
                self.calculate_scaling()
                self.render_numbers()

                if self.fullscreen:
                    self.screen = pygame.display.set_mode(
                        self.window_constants["window_size"], pygame.RESIZABLE | pygame.FULLSCREEN)
                else:
                    self.screen = pygame.display.set_mode(
                        self.window_constants["window_size"], pygame.RESIZABLE)
                self.screen.fill(self.colours["background_colour"])
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                inset_game_position = self.window_constants["inset_game_position"]
                scaled_game_size = self.window_constants["scaled_game_size"]
                field_size = self.logic.get_size()
                # - event.button: 1=left click, 3=right click
                if event.button == 1:
                    if mouse_position[0] >= inset_game_position[0] and \
                            mouse_position[0] < inset_game_position[0]+scaled_game_size[0] and \
                            mouse_position[1] >= inset_game_position[1] and \
                            mouse_position[1] < inset_game_position[1]+scaled_game_size[1]:
                        self.logic.dig(
                            (int((mouse_position[0] - inset_game_position[0]) /
                                (scaled_game_size[0] / field_size[0])),
                            int((mouse_position[1] - inset_game_position[1]) /
                                (scaled_game_size[1] / field_size[1]))))
                    else:
                        print(
                            f"left click outside of game area, coordinates \
                            ({mouse_position[0]},{mouse_position[1]})")
                elif event.button == 3:
                    if mouse_position[0] >= inset_game_position[0] and \
                            mouse_position[0] < inset_game_position[0]+scaled_game_size[0] and \
                            mouse_position[1] >= inset_game_position[1] and \
                            mouse_position[1] < inset_game_position[1]+scaled_game_size[1]:
                        self.logic.flag((
                            int((mouse_position[0] - inset_game_position[0]) /
                                (scaled_game_size[0] / field_size[0])),
                            int((mouse_position[1] - inset_game_position[1]) /
                                (scaled_game_size[1] / field_size[1]))))
                    else:
                        print(
                            f"right click outside of game area, coordinates \
                            ({mouse_position[0]},{mouse_position[1]})")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.logic.stop()
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()

    def draw(self) -> None:
        '''draw game state to pygame display'''
        field = self.logic.get_field()
        size = self.logic.get_size()
        self.small_surface.fill(self.colours["dark_unknown_colour"])
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                if field[x][y] == 10:
                    if (x, y) in self.logic.get_flags():
                        self.pxgrid[x, y] = self.colours["flag_colour"] # type: ignore
                    elif (x + y) % 2:
                        self.pxgrid[x, y] = self.colours["light_unknown_colour"] # type: ignore
                else:
                    if (x + y) % 2:
                        self.pxgrid[x, y] = self.colours["dark_known_colour"] # type: ignore
                    else:
                        self.pxgrid[x, y] = self.colours["light_known_colour"] # type: ignore
        scaled_game_size = self.window_constants["scaled_game_size"]
        inset_game_position = self.window_constants["inset_game_position"]
        square_size = scaled_game_size[1] / self.logic.get_size()[1]
        self.screen.blit(pygame.transform.scale(
            self.small_surface,
            (int(scaled_game_size[0]), int(scaled_game_size[1]))),
            (int(inset_game_position[0]), int(inset_game_position[1])))
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                square_value = field[x][y]
                if square_value not in (0, 10):
                    self.screen.blit(self.numbers[square_value - 1],(
                        inset_game_position[0] + x * square_size + self.number_offsets[square_value - 1],
                        inset_game_position[1] + y * square_size + self.number_offsets[8]))
        pygame.display.update()
