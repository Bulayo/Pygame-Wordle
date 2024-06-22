import pygame, requests, random
from os.path import join

API_KEY = "" #Get API key from https://api-ninjas.com/

def check_word_validity(word: str) -> dict:
    # Checks if word is part of the english dictionary and returns a dictionary value
    # The words validity is checked through API NINJAS DICTIONARY API

    dictionary_api = f"https://api.api-ninjas.com/v1/dictionary?word={word}"
    dictionary_request = requests.get(dictionary_api, headers = {"X-Api-Key": API_KEY})
    return dictionary_request.json()


def choose_random_word() -> str:
    # Chooses a random word from Random Word API
    # Returns a string value

    while True:
        random_word_api = requests.get(f"https://random-word-api.herokuapp.com/word?length=5")
        random_word_response = random_word_api.json()
        random_word = ""
        random_word = random_word.join(random_word_response)

        verify_word = check_word_validity(random_word)
        
        if verify_word["valid"]:
            break

        else:
            continue

    return random_word


def main_menu():
    # SHOW MAIN MENU BUTTONS ON SCREEN

    WINDOW.blit(logo_surface, logo_rectangle)
    WINDOW.blit(play_button_surface, play_button_rectangle)
    WINDOW.blit(tutorial_button_surface, tutorial_button_rectangle)
    WINDOW.blit(exit_button_surface, exit_button_rectangle)

def game_menu():
    # SHOW THE BUTTONS ON THE MAIN GAME SCREEN

    WINDOW.blit(back_button_surface, back_button_rectangle)

    if show_hint_button:
        WINDOW.blit(hint_button_surface, hint_button_rectangle)


def tutorial_menu():
    # SHOW BUTTONS ON THE TUTORIAL SCREEN

    WINDOW.blit(back_button_surface, back_button_rectangle)
    WINDOW.blit(keyboard_image_surface, keyboard_image_rectangle)
    WINDOW.blit(tutorial_image_surface, tutorial_image_rectangle)
    WINDOW.blit(tutorial_hint_surf, tutorial_hint_button_rect)

    text_1 = TUTORIAL_FONT.render("Type letters using the keyboard.", True, COLOURS[0])
    text_1_rect = text_1.get_rect(topleft = (10, 80))

    text_2 = TUTORIAL_FONT.render("Press enter key to submit a word.", True, COLOURS[0])
    text_2_rect = text_2.get_rect(topleft= (10, 110))    

    text_3 = TUTORIAL_FONT.render("Press backspace key to delete a letter.", True, COLOURS[0])
    text_3_rect = text_3.get_rect(topleft= (10, 140))

    text_4 = TUTORIAL_FONT.render("Black font means the letter is not in the word.", True, COLOURS[0])
    text_4_rect = text_4.get_rect(topleft= (10, 240))

    text_5 = TUTORIAL_FONT.render("Green font means the letter is in the correct position.", True, COLOURS[0])
    text_5_rect = text_5.get_rect(topleft= (10, 270))

    text_6 = TUTORIAL_FONT.render("Orange font means the letter is in the incorrect position.", True, COLOURS[0])
    text_6_rect = text_6.get_rect(topleft= (10, 300))

    text_7 = TUTORIAL_FONT.render("Use the hint button to get a letter that is in the word.", True, COLOURS[0])
    text_7_rect = text_7.get_rect(topleft= (10, 380))

    text_8 = TUTORIAL_FONT.render("You have six attemps to guess the correct word!", True, COLOURS[0])
    text_8_rect = text_8.get_rect(topleft= (10, 410))

    WINDOW.blit(text_1, text_1_rect)
    WINDOW.blit(text_2, text_2_rect)
    WINDOW.blit(text_3, text_3_rect)
    WINDOW.blit(text_4, text_4_rect)
    WINDOW.blit(text_5, text_5_rect)
    WINDOW.blit(text_6, text_6_rect)
    WINDOW.blit(text_7, text_7_rect)
    WINDOW.blit(text_8, text_8_rect)


def add_text(letter: str):
    global word

    word += letter.upper()
    render_text(word, COLOURS[0])


def render_text(word: str, colour: list[str]):
    global text

    text = FONT.render(word, True, colour)


def wordle_display(letter: str, colour: list[str]):

    word_group.append(FONT.render(letter, True, colour))


def check_user_guess(random_word: str, user_guess: str):
    # COLOUR ADDED TO TEXT DEPENDING ON SET RULES

    global check_win
    check_win = True

    for letter in range(len(random_word)):
        if random_word[letter] == user_guess[letter]:
            wordle_display(user_guess[letter], COLOURS[3])

        elif (random_word[letter] != user_guess[letter]) and (user_guess[letter] in random_word):
            wordle_display(user_guess[letter], COLOURS[1])
            check_win = False
            
        elif user_guess[letter] not in random_word:
            wordle_display(user_guess[letter], COLOURS[0])
            check_win = False


def show_hint():
    # Displays a letter when hint button is pressed
    global hint_text, hint_rect

    hint_text = FONT.render(f"{random.choice(random_word)}", True, COLOURS[0])
    hint_rect = hint_text.get_rect(topleft = (540, 10))


def game_over():
    global check_win

    if len(guessed_words) == 6 and check_win is False:
        # Displays correct word when user loses
        lose_text = FONT.render("Game Over!", True, COLOURS[0])
        lose_rect = lose_text.get_rect(topleft = (175, 350))

        correct_word = FONT.render(f"The word was {random_word}", True, COLOURS[0])
        correct_word_rect = correct_word.get_rect(topleft = (70, 400))

        WINDOW.blit(lose_text, lose_rect)
        WINDOW.blit(correct_word, correct_word_rect)

    elif check_win:
        # Displays a You Win! text when user wins
        win_text = FONT.render("You won!", True, COLOURS[0])
        win_rect = win_text.get_rect(topleft = (210, 350))

        WINDOW.blit(win_text, win_rect)


def reset_game_variables():
    # Reset game variable when user goes to main menu
    global word, guessed_words, word_group, check_win, show_hint_button, hint_text

    word = ""
    guessed_words = []
    word_group = []
    show_hint_button = True
    check_win = False
    text_rect.y = 50
    hint_text = FONT.render("", True, COLOURS[0])
    render_text(word, COLOURS[0])


pygame.init()

# CONSTANTS
RESOLUTION = WIDTH, HEGHT = 600, 450
WINDOW = pygame.display.set_mode(RESOLUTION)
FONT = pygame.font.SysFont("arial", 50)
TUTORIAL_FONT = pygame.font.SysFont("arial", 24)
FPS = 10
COLOURS = ["Black", "Orange", "Red", "Green", "Grey"]
WINDOW_CAPTION = pygame.display.set_caption("Pygame Wordle By Bulayo")
CLOCK = pygame.time.Clock()

# ASSETS
logo_surface = pygame.image.load(join("assets", "logo.png")).convert_alpha()
logo_rectangle = logo_surface.get_rect(topleft = (225, 0))

play_button_surface = pygame.image.load(join("assets", "play_button.png")).convert_alpha()
play_button_rectangle = play_button_surface.get_rect(center = (WIDTH // 2, 220))

tutorial_button_surface = pygame.image.load(join("assets", "tutorial_button.png")).convert_alpha()
tutorial_button_rectangle = tutorial_button_surface.get_rect(center = (WIDTH // 2, 308))

exit_button_surface = pygame.image.load(join("assets", "exit_button.png")).convert_alpha()
exit_button_rectangle = exit_button_surface.get_rect(center = (WIDTH // 2, 395))

back_button_surface = pygame.image.load(join("assets", "back_button.png")).convert_alpha()
back_button_rectangle = back_button_surface.get_rect(topleft = (0, 0))

hint_button_surface = pygame.image.load(join("assets", "hint_button.png")).convert_alpha()
hint_button_rectangle = hint_button_surface.get_rect(topleft = (520, 0))

tutorial_hint_surf = pygame.transform.scale(hint_button_surface, (60, 60))
tutorial_hint_button_rect = hint_button_surface.get_rect(topleft = (100, 324))

keyboard_image_surface = pygame.image.load(join("assets", "keyboard.png")).convert_alpha()
keyboard_image_rectangle = keyboard_image_surface.get_rect(topleft= (100, 10))

tutorial_image_surface = pygame.image.load(join("assets", "tutorial_image.png")).convert_alpha()
tutorial_image_rectangle = tutorial_image_surface.get_rect(topleft= (100, 165))

# Current game screen
current_screen = "Main"

# Game Variables
word = ""
guessed_words = []
word_group = []
width_spacing = 50
height_spacing = 50

text = FONT.render("", False, COLOURS[0])
text_rect = text.get_rect(topleft = (230, 50))

hint_text = FONT.render("", True, COLOURS[0])
hint_rect = hint_text.get_rect()

check_win = False
show_hint_button = True

# MAIN LOOP
running = True
while running:
    # FPS LIMITER
    CLOCK.tick(FPS)

    # DISPLAY BACKGROUND COLOUR
    WINDOW.fill(COLOURS[4])

    # MOUSE POSITION
    mouse_position = pygame.mouse.get_pos()

    # EVENT HANDLER
    for event in pygame.event.get():
        # Ends program if exit button is clicked
        if event.type == pygame.QUIT:
            running = False

        # Checks if left mouse button was pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rectangle.collidepoint(mouse_position) and current_screen == "Main":
                current_screen = "Game"
                try:
                    random_word = choose_random_word().upper()

                except:
                    print("ERROR: Asign your API Ninjas API key to the variable 'API_KEY' and make sure you have an internet connection.")
                    running = False

            elif tutorial_button_rectangle.collidepoint(mouse_position) and current_screen == "Main":
                current_screen = "Tutorial"

            elif exit_button_rectangle.collidepoint(mouse_position) and current_screen == "Main":
                running = False

            elif back_button_rectangle.collidepoint(mouse_position) and (current_screen == "Game" or current_screen == "Tutorial"):
                current_screen = "Main"
                reset_game_variables()

            elif hint_button_rectangle.collidepoint(mouse_position) and current_screen == "Game":
                show_hint()
                show_hint_button = False

        elif event.type == pygame.KEYDOWN and current_screen == "Game":
            if (event.key >= 97 and event.key <= 122) and (len(word) <= 4): # A to Z buttons
                add_text(chr(event.key))

            elif event.key == 13 and len(word) == 5: # Enter button
                verify_word = check_word_validity(word)

                if verify_word["valid"]:
                    guessed_words.append(word)
                    text_rect.y += 60
                    check_user_guess(random_word, word)
                    word = ""
                    render_text(word, COLOURS[0])

                else:
                    render_text(word, COLOURS[2])

            elif event.key == 8: # Backspace button
                verify_word = False
                word = word[:-1]
                render_text(word, COLOURS[0])

    if current_screen == "Main":
        main_menu()

    elif current_screen == "Game":
        game_menu()

        # Checks if user has won or lost
        game_over()

        # Shows the current word the user is typing
        WINDOW.blit(text, text_rect)

        # Shows hint letter
        WINDOW.blit(hint_text, hint_rect)

    elif current_screen == "Tutorial":
        tutorial_menu()

    for i in range(len(word_group)):
        # Renders the different coloured letters and adds spaces between them
        if i <= 4:
            WINDOW.blit(word_group[i], ((i * width_spacing) + 190, height_spacing))

        elif i >= 5 and i <= 9:
            WINDOW.blit(word_group[i], (((i - 5) * width_spacing) + 190, height_spacing * 2))

        elif i >= 10 and i <= 14:
            WINDOW.blit(word_group[i], (((i - 10) * width_spacing) + 190, height_spacing * 3))

        elif i >= 15 and i <= 19:
            WINDOW.blit(word_group[i], (((i - 15) * width_spacing) + 190, height_spacing * 4))

        elif i >= 20 and i <= 24:
            WINDOW.blit(word_group[i], (((i - 20) * width_spacing) + 190, height_spacing * 5))

        elif i >= 25 and i <= 29:
            WINDOW.blit(word_group[i], (((i - 25) * width_spacing) + 190, height_spacing * 6))

    # UPDATE SCREEN
    pygame.display.flip()

# Quit program
pygame.quit()
