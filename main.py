from Box2D.b2 import world as b2World
from Box2D import b2World, b2PolygonShape
from sound_manager import SoundManager
from screens.menu import main_menu_screen
from screens.character_select import character_selection_screen

from character import Character  # asumimos que guardaste la clase arriba aquí
from background import Background  # asumimos que guardaste la clase arriba aquí
from screens.victory_screen import victory_screen
from constants import *
import IA_player
import threading
from timer import draw_timer, timer_thread

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixel Fighter")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 36)
        self.font_timer = pygame.font.SysFont("arialblack", 60)

    def draw_health_bars(self, surface, p1_healt, p2_healt):
        prog_p1 = self.calculate_health_width(p1_healt, MAX_HP, HEALTH_BAR_WIDTH)
        prog_p2 = self.calculate_health_width(p2_healt, MAX_HP, HEALTH_BAR_WIDTH)

        TEXT_KO = pygame.font.SysFont(None, 36).render("KO", True, (200, 0, 0))
        X_KO = WIDTH // 2 - TEXT_KO.get_width() // 2

        X_BAR_P1 = X_KO - HEALTH_BAR_WIDTH - BAR_SPACING
        X_BAR_P2 = X_KO + TEXT_KO.get_width() + BAR_SPACING
        Y_BAR = Y_KO + 5

        pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P1, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P2, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P1 + HEALTH_BAR_WIDTH - prog_p1, Y_BAR, prog_p1, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P2, Y_BAR, prog_p2, HEALTH_BAR_HEIGHT))

        self.screen.blit(TEXT_KO, (X_KO, Y_KO))

    def create_world(self):
        self.world = b2World(gravity=(0, 30), doSleep=True)

        # floor (estático)
        floor = self.world.CreateStaticBody(position=(WIDTH / 2 / PPM, (HEIGHT-60) / PPM))
        floor.CreatePolygonFixture(box=(WIDTH / 2 / PPM, 0.5), density=0, friction=0.8)

        left_wall = self.world.CreateStaticBody(
            position=(0.25, HEIGHT / 2 / PPM),
            shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
        )

        right_wall = self.world.CreateStaticBody(
            position=((WIDTH - 10) / PPM, HEIGHT / 2 / PPM),
            shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
        )

    def calculate_health_width(self, current_hp, max_hp, bar_width):
        hp = max(current_hp, 0)
        return int((hp / max_hp) * bar_width)
    
    def run(self):
        choice = main_menu_screen(self.screen, self.font, MENU_OPTIONS)

        if choice == "exit":
            pygame.quit()
            return

        if choice == "play":
            str_player, str_player2 = character_selection_screen(self.screen, self.font)

            self.create_world()
            self.background = Background()
            self.player = Character(self.world, 100, 300, controls, name=str_player)
            self.player2 = Character(self.world, WIDTH * 0.8, 300, controls2, name=str_player2)

            FIGHTING['is_running'] = True

            thread_bot = threading.Thread(target=IA_player.IA_PLAYER, daemon=True)
            thread_timer = threading.Thread(target=timer_thread, daemon=True)
            thread_bot.start()
            thread_timer.start()

            while FIGHTING['is_running']:
                self.clock.tick(FPS)

                self.events()
                self.update()
                self.draw()

                if self.player.hp <= 0 or self.player2.hp <= 0:
                    FIGHTING['is_running'] = False
        
        #thread_bot.join()
        #thread_timer.join()

        self.handle_victory()

        self.run()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                FIGHTING['is_running'] = False

        key_words = pygame.key.get_pressed()
        key_words2 = IA_player.key_words  # IA_player.key_words  # if SINGLE_PLAYER else key_words

        self.player.event_handler(key_words)
        self.player2.event_handler(key_words2)

    def update(self):
         # Avanzar física
        self.world.Step(1.0 / FPS, 6, 2)

        # Actualizar personajes
        self.player.update()
        self.player2.update()

        self.detect_collisions()

        # Actualizar dirección de los personajes para que miren al oponente
        self.player.update_character_direction(self.player2)
        self.player2.update_character_direction(self.player)

        self.background.update()

    def detect_collisions(self):
        # Comprobar colisiones
        self.player.hit_check(self.player2)
        self.player2.hit_check(self.player)
        self.player.projectile_hit_check(self.player2)
        self.player2.projectile_hit_check(self.player)

    def draw(self):
        # Dibujar
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        self.player2.draw(self.screen)
        self.draw_health_bars(self.screen, self.player.hp, self.player2.hp)
        draw_timer(self.screen, self.font, WIDTH)

        pygame.display.flip()

    def handle_victory(self):
        winner = self.player.name if self.player.hp > 0 else self.player2.name
        winner = 'empate' if self.player.hp == self.player2.hp else winner
        victory_screen(self.screen, self.font, WIDTH, HEIGHT, winner)
        pygame.display.flip()

    
if __name__ == "__main__":
    game = Game()
    game.run()





























  

    

    

    

    


