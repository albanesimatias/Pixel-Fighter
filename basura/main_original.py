from Box2D.b2 import world as b2World
from Box2D import b2World, b2PolygonShape, b2_staticBody, b2_dynamicBody
from sound_manager import SoundManager

from character import Character
from background import Background
from screens.victory_screen import victory_screen
from timer import draw_timer  
from constants import *
from main_menu import run_main_menu
import IA_player
import threading

import pygame
pygame.init()

font = pygame.font.SysFont(None, 36)

TEXT_KO = font.render("KO", True, (200, 0, 0))
X_KO = WIDTH // 2 - TEXT_KO.get_width() // 2

X_BAR_P1 = X_KO - HEALTH_BAR_WIDTH - BAR_SPACING
X_BAR_P2 = X_KO + TEXT_KO.get_width() + BAR_SPACING
Y_BAR = Y_KO + 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pelea con Box2D")

clock = pygame.time.Clock()

# Crear mundo físico
world = b2World(gravity=(0, 30), doSleep=True)

# Piso
floor = world.CreateStaticBody(position=(WIDTH / 2 / PPM, (HEIGHT - 60) / PPM))
floor.CreatePolygonFixture(box=(WIDTH / 2 / PPM, 0.5), density=0, friction=0.8)

# Paredes laterales
left_wall = world.CreateStaticBody(
    position=(0.25, HEIGHT / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
)

right_wall = world.CreateStaticBody(
    position=((WIDTH - 10) / PPM, HEIGHT / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
)

# Barras de vida
def calculate_health_width(current_hp, max_hp, bar_width):
    hp = max(current_hp, 0)
    return int((hp / max_hp) * bar_width)

def draw_health_bars(surface, p1_hp, p2_hp):
    prog_p1 = calculate_health_width(p1_hp, MAX_HP, HEALTH_BAR_WIDTH)
    prog_p2 = calculate_health_width(p2_hp, MAX_HP, HEALTH_BAR_WIDTH)

    pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P1, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P2, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P1 + HEALTH_BAR_WIDTH - prog_p1, Y_BAR, prog_p1, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P2, Y_BAR, prog_p2, HEALTH_BAR_HEIGHT))

    surface.blit(TEXT_KO, (X_KO, Y_KO))

# Instanciar personajes y fondo
    #player = Character(world, 100, 300, controls, name=ID_Character.ESTEBAN.value)
    #player2 = Character(world, WIDTH * 0.8, 300, controls2, name=ID_Character.MAXIMO.value)
controls = {
    'left': pygame.K_a, 'right': pygame.K_d,
    'up': pygame.K_w, 'down': pygame.K_s,
    'attack': pygame.K_f, 'block': pygame.K_g
}
controls2 = {
    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
    'up': pygame.K_UP, 'down': pygame.K_DOWN,
    'attack': pygame.K_KP1, 'block': pygame.K_KP2
}
player, player2 = run_main_menu(screen, font, clock, controls, controls2)

if player is None or player2 is None:
    print("estan vaios los players")
    pygame.quit()
    exit()


print(player.name)
print(player2.name)
FIGHTING = {'is_running': True}
background = Background()

# Iniciar IA en otro hilo
thread = threading.Thread(target=IA_player.IA_PLAYER)
thread.start()



# ⏱️ Configuración del round
start_ticks = pygame.time.get_ticks()

try:
    while FIGHTING['is_running']:
        if not pygame.display.get_init():
         print("🔚 Display cerrado, saliendo del loop principal")
         break

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                FIGHTING['is_running'] = False
                pygame.quit()


        key_words = pygame.key.get_pressed()
        key_words2 = key_words
        if key_words[pygame.K_d]:
          print("A presionada")


        player.event_handler(key_words)
        player2.event_handler(key_words2)

        world.Step(1.0 / FPS, 6, 2)
     

        player.update()
        player2.update()

        player.hit_check(player2)
        player2.hit_check(player)
        player.projectile_hit_check(player2)
        player2.projectile_hit_check(player)

        player.update_character_direction(player2)
        player2.update_character_direction(player)


        background.update()
        background.draw(screen)
        player.draw(screen)
        player2.draw(screen)
        draw_health_bars(screen, player.hp, player2.hp)

        # ⏱️ Cronómetro y cálculo de tiempo restante
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, ROUND_DURATION - elapsed_seconds)
        font_timer = pygame.font.SysFont("arialblack", 60)

        draw_timer(screen, font, time_left, WIDTH)
   
        # 🎯 Finalización por vida o tiempo
        game_over = False
        winner = None

        if player.hp <= 0 or player2.hp <= 0:
            winner = player.name if player.hp > 0 else player2.name
            game_over = True
        elif time_left <= 0:
            if player.hp > player2.hp:
                winner = player.name
            elif player2.hp > player.hp:
                winner = player2.name
            else:
                winner = "empate"
            game_over = True

        print(player.hp,player2.hp,game_over)
        if game_over:
            print(f"El ganador es: {winner}")
            victory_screen(screen, font, WIDTH, HEIGHT, winner)
            FIGHTING['is_running'] = False
       
        print("dd")
        pygame.display.flip()
    
except Exception as e:
    print("💥 Ocurrió un error inesperado:", e)

thread.join()



