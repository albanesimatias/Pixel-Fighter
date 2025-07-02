import time
from constants import ROUND_DURATION, timer_mtx, time_round, FIGHTING

def timer_thread():
    global timer_mtx, time_round
    start_time = time.time()
    while  FIGHTING['is_running']:
        elapsed = time.time() - start_time
        remaining = max(0, ROUND_DURATION - int(elapsed))
       
        with timer_mtx:
            time_round[0] = remaining

        if remaining <= 0:
            FIGHTING['is_running'] = False
            break

        time.sleep(0.2) 

def draw_timer(surface, font, screen_width):
    x = screen_width // 2
    y = 10

    with timer_mtx:
        text_str = f"{time_round[0]}"

    # Render principal (amarillo)
    text = font.render(text_str, True, (255, 255, 0))

    # Borde negro (efecto sombra)
    border = 2
    for dx in [-border, border]:
        for dy in [-border, border]:
            shadow = font.render(text_str, True, (0, 0, 0))
            surface.blit(shadow, (x - text.get_width() // 2 + dx, y + dy))

    # Texto encima
    surface.blit(text, (x - text.get_width() // 2, y))
