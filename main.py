import pygame as pg
import random

pg.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,255,0)
RED = (255, 0, 0)


WIDTH, HEIGHT = 800, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Hang man")

WORDS = [
    "атом", "лазер", "фотон", "вакуум", "квант", "плазма", "нейтрон",
    "протон", "заряд", "энергия", "импульс", "излучение", "инерция",
    "проводник", "магнит", "сила", "спектр", "ускорение", "масса",
    "трение", "частота", "плотность", "ток", "волна", "радиация",
    "отражение", "дифракция", "гравитация", "напряжение", "энтропия",
    "мощность", "разряд", "вес", "гироскоп"
]


font = pg.font.Font(None, 40)
small_font = pg.font.Font(None, 40)

used_words = set()

def reset_game():
    global word, word_length, guessed_letters, wrong_letters, remaining_tries
    global draw_line, show_text, input_text, input_active

    available_words = list(set(WORDS) - used_words)
    if not available_words:
        used_words.clear()

    word = random.choice(list(set(WORDS) - used_words))
    used_words.add(word)

    word_length = len(word)
    guessed_letters = ["_"] * word_length
    wrong_letters = []
    remaining_tries = 9
    draw_line = False
    show_text = True
    input_text = ""
    input_active = False


reset_game()

def draw_word():
    WORD_START_X = 280
    WORD_Y = 610
    LINE_WIDTH = 20
    SPACE_BETWEEN = 20

    for i in range(word_length):
        start_x = WORD_START_X + i * (LINE_WIDTH + SPACE_BETWEEN)
        pg.draw.line(screen, WHITE, (start_x, WORD_Y), (start_x + LINE_WIDTH, WORD_Y), 3)
        if guessed_letters[i] != "_":
            letter_surface = font.render(guessed_letters[i], True, WHITE)
            letter_rect = letter_surface.get_rect(center=(start_x + LINE_WIDTH // 2, WORD_Y - 30))
            screen.blit(letter_surface, letter_rect.topleft)

def draw_hangman():
    if remaining_tries <= 8:
        pg.draw.line(screen, WHITE, (270, 500), (450, 500), 5)

    if remaining_tries <= 7:
        pg.draw.line(screen, WHITE, (300, 500), (300, 300), 5)

    if remaining_tries <= 6:
        pg.draw.line(screen, WHITE, (300, 300), (400, 300), 5)
    if remaining_tries <= 5:
        pg.draw.circle(screen, WHITE, (400, 330), 30, 5)
    if remaining_tries <= 4:
        pg.draw.line(screen, WHITE, (400, 360), (400, 430), 5)
    if remaining_tries <= 3:
        pg.draw.line(screen, WHITE, (400, 430), (370, 480), 5)
    if remaining_tries <= 2:
        pg.draw.line(screen, WHITE, (400, 430), (430, 480), 5)
    if remaining_tries <= 1:
        pg.draw.line(screen, WHITE, (400, 390), (370, 360), 5)
    if remaining_tries == 0:
        pg.draw.line(screen, WHITE, (400, 390), (430, 360), 5)

text = font.render("чтобы начать нажмите сюда", True, WHITE)


text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
input_box = pg.Rect(300, 650, 200, 50)

running = True
while running:
    screen.fill(BLACK)

    if show_text:
        screen.blit(text, text_rect)

    if draw_line:
        draw_hangman()
        draw_word()

        wrong_text = small_font.render(f"Неправильные буквы: {' '.join(wrong_letters)}", True, WHITE)
        remaining_text = small_font.render(f"Попытки: {remaining_tries}", True, WHITE)
        screen.blit(wrong_text, (50, 700))
        screen.blit(remaining_text, (50, 750))

        pg.draw.rect(screen, WHITE, input_box, 2)
        input_surface = font.render(input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if show_text and text_rect.collidepoint(event.pos):
                reset_game()
                draw_line = True
                show_text = False
            elif input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
        if "_" not in guessed_letters:
            pg.display.update()
            screen.fill(BLACK)
            pg.time.wait(1000)

            game_result_text = font.render("Вы выйграли!", True, GREEN)

            screen.blit(game_result_text, (300, 400))

            pg.display.flip()
            pg.time.wait(1500)

            reset_game()

        if remaining_tries <= 0:
            pg.display.update()
            screen.fill(BLACK)
            pg.time.wait(1500)

            game_result_text = font.render("Вы проиграли!", True, RED)

            screen.blit(game_result_text, (300, 400))
            pg.display.flip()

            pg.time.wait(1500)
            screen.fill(BLACK)
            t = font.render(f'правильное слово:{word}',True,RED)
            screen.blit(t, (300, 400))
            pg.display.flip()
            pg.time.wait(1500)

            reset_game()

        elif event.type == pg.KEYDOWN and input_active:
            if event.key == pg.K_RETURN and input_text:
                if input_text in word:
                    for i, letter in enumerate(word):
                        if letter == input_text:
                            guessed_letters[i] = input_text
                else:
                    if input_text not in wrong_letters:
                        wrong_letters.append(input_text)
                        remaining_tries -= 1



                input_text = ""

            if event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]

            elif len(input_text) < 1 and event.unicode.isalpha():
                input_text += event.unicode.lower()

    pg.display.flip()

pg.quit()
