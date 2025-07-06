import time
from constants import ROUND_DURATION, timer_mtx, time_round, FIGHTING, Color, X_TIMER, Y_TIMER, X_SHADOW_TIMER, Y_SHADOW_TIMER, SLEEP

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

        time.sleep(SLEEP) 

def draw_timer(screen, font):
    with timer_mtx:
        text_str = f"{time_round[0]}"

    text = font.render(text_str, True, Color.YELLOW.value)

    shadow = font.render(text_str, True, Color.BLACK.value)
    screen.blit(shadow, (X_SHADOW_TIMER, Y_SHADOW_TIMER))

    screen.blit(text, (X_TIMER, Y_TIMER))
