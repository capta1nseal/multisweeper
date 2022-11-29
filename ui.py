from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame
from logic import Logic

class UI:
    def __init__(self, logic: Logic, window_size: tuple[int, int] = (640, 480)) -> None:
        self.logic = logic
        self.scale_constants = {
            "window_size": window_size,
            "scaled_size": (0, 0),
            "inset_position": (0,0)
        }

        self.background_colour = (0, 0, 0)

        self.screen = pygame.display.set_mode(self.scale_constants["window_size"], pygame.RESIZABLE)
        self.screen.fill(self.background_colour)

        self.calculate_scaling()

        self.small_surface = pygame.Surface(self.logic.get_size())
        self.pxgrid = pygame.PixelArray(self.small_surface)

        self.dark_unknown_colour = 0x444444
        self.light_unknown_colour = 0x666666
        self.dark_known_colour = 0xAAAAAA
        self.light_known_colour = 0xCCCCCC

        self.font_colour = 0x000000

        self.fullscreen = False

    def calculate_scaling(self):
        '''
        calculate some constants for drawing the game
        at the right scale in the right position in the window
        '''
        grid_size = self.logic.get_size()
        window_size = self.scale_constants["window_size"]
        if window_size[0] / grid_size[0] <= \
                window_size[1] / grid_size[1]:
            self.scale_constants["scaled_size"] = (
                window_size[0],
                window_size[0] * grid_size[1] / grid_size[0])
        else:
            self.scale_constants["scaled_size"] = (
                window_size[1] * grid_size[0] / grid_size[1],
                window_size[1])

        self.scale_constants["inset_position"] = (
            window_size[0] / 2 - self.scale_constants["scaled_size"][0] / 2,
            window_size[1] / 2 - self.scale_constants["scaled_size"][1] / 2)

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

        self.scale_constants["window_size"] = self.screen.get_size()
        self.calculate_scaling()

        self.screen.fill(self.background_colour)
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
                self.scale_constants["window_size"] = event.size
                self.calculate_scaling()

                if self.fullscreen:
                    self.screen = pygame.display.set_mode(
                        self.scale_constants["window_size"], pygame.RESIZABLE | pygame.FULLSCREEN)
                else:
                    self.screen = pygame.display.set_mode(
                        self.scale_constants["window_size"], pygame.RESIZABLE)
                self.screen.fill(self.background_colour)
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                inset_position = self.scale_constants["inset_position"]
                scaled_size = self.scale_constants["scaled_size"]
                field_size = self.logic.get_size()
                # - event.button: 1=left click, 3=right click
                if event.button == 1:
                    if mouse_position[0] >= inset_position[0] and \
                            mouse_position[0] < inset_position[0]+scaled_size[0] and \
                            mouse_position[1] >= inset_position[1] and \
                            mouse_position[1] < inset_position[1]+scaled_size[1]:
                        self.logic.dig(
                            (int((mouse_position[0] - inset_position[0]) /
                                (scaled_size[0] / field_size[0])),
                            int((mouse_position[1] - inset_position[1]) /
                                (scaled_size[1] / field_size[1]))))
                    else:
                        print(
                            f"left click outside of game area, coordinates \
                            ({mouse_position[0]},{mouse_position[1]})")
                elif event.button == 3:
                    if mouse_position[0] >= inset_position[0] and \
                            mouse_position[0] < inset_position[0]+scaled_size[0] and \
                            mouse_position[1] >= inset_position[1] and \
                            mouse_position[1] < inset_position[1]+scaled_size[1]:
                        self.logic.flag((
                            int((mouse_position[0] - inset_position[0]) /
                                (scaled_size[0] / field_size[0])),
                            int((mouse_position[1] - inset_position[1]) /
                                (scaled_size[1] / field_size[1]))))

    def draw(self) -> None:
        '''draw game state to pygame display'''
        field = self.logic.get_field()
        size = self.logic.get_size()
        self.small_surface.fill(self.dark_unknown_colour)
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                if field[x][y] == 10:
                    if (x + y) % 2:
                        self.pxgrid[x, y] = self.light_unknown_colour # type: ignore
                else:
                    if (x + y) % 2:
                        self.pxgrid[x, y] = self.light_known_colour # type: ignore
                    else:
                        self.pxgrid[x, y] = self.dark_known_colour # type: ignore
        scaled_size = self.scale_constants["scaled_size"]
        inset_position = self.scale_constants["inset_position"]
        self.screen.blit(pygame.transform.scale(
            self.small_surface,
            (int(scaled_size[0]), int(scaled_size[1]))),
            (int(inset_position[0]), int(inset_position[1])))
        pygame.display.update()
