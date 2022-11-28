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
                pos = pygame.mouse.get_pos
                # - event.button: 1=left click, 3=right click
                if event.button == 1:
                    print("left click")
                elif event.button == 3:
                    print("right click")
    
    def draw(self) -> None:
        '''draw game state to pygame display'''
        pygame.display.update()