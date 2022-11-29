from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

from logic import Logic
from ui import UI

if __name__ == "__main__":
    FPS = 30

    clock = pygame.time.Clock()
    logic = Logic(mine_count = 35)
    ui = UI(logic)

    logic.running = True
    while logic.running:
        ui.handle_events()
        ui.draw()
        clock.tick(FPS)
    pygame.quit()
