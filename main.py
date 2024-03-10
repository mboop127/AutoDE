import pyautogui
import pydirectinput
import time
import os

max_game_time = 100000

Images_Folder: str = os.getcwd() + "\\Images\\"

f = open("filepath.txt",'r')
AI_Path: str = f.read().replace("\\","/") + "/"
f.close()

AIs_Available: list = []
All_AI_Files : list = os.listdir(AI_Path)
for i in range(len(All_AI_Files)):
    if ".per" in All_AI_Files[i]:
        AIs_Available.append(All_AI_Files[i])

def clean_directory() -> None:
    for i in range(len(All_AI_Files)):
        if ".ai" in All_AI_Files[i]:
            os.remove(AI_Path + All_AI_Files[i])

    f = open(AI_Path + "AI_One.ai","w+")
    f.write("isn't matty the best?")
    f.close()

    f = open(AI_Path + "AI_Two.ai","w+")
    f.write("isn't matty the best?")
    f.close()

def set_ais(AI_One: str, AI_Two: str) -> None:
    if AI_One not in AIs_Available:
        print("AI NOT AVAILABLE: " + AI_One)
    elif AI_Two not in AIs_Available:
        print("AI NOT AVAILABLE: " + AI_Two)

    else:
        f = open(AI_Path + AI_One,'r')
        n = open(AI_Path + "AI_One.per","w+")
        n.write(f.read())
        f.close()
        n.close()

        f = open(AI_Path + AI_Two,'r')
        n = open(AI_Path + "AI_Two.per","w+")
        n.write(f.read())
        f.close()
        n.close()

def press_button_or_crash(image: str) -> None:
    image = Images_Folder + image

    while True:

        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=0.9)
            time.sleep(.1)
            pydirectinput.click(x, y)
            break
        except (pyautogui.ImageNotFoundException, TypeError):
            pass


def set_players() -> None:

    player_one_img: str = Images_Folder + "player_1.png"
    player_two_img: str = Images_Folder + "player_2.png"

    #player 1
    pydirectinput.click(390,390)
    press_button_or_crash("AI_One.png")
    time.sleep(.1)

    #player 2
    pydirectinput.click(390,430)
    press_button_or_crash("AI_Two.png")
    pydirectinput.press("enter")

def check_game() -> str:
    game_ended = False
    start = time.time()
    current = start

    while not game_ended:
        current = time.time()

        #print(current - start)

        if current - start < max_game_time:


            try:
                x, y = pyautogui.locateCenterOnScreen(Images_Folder + "AI_error.png", confidence=0.9)

                press_button_or_crash("ok.png")
                press_button_or_crash("open_menu.png")
                press_button_or_crash("quit.png")
                press_button_or_crash("yes.png")

                return "ai_error"

            except (pyautogui.ImageNotFoundException, TypeError):
                pass

            try:
                x, y = pyautogui.locateCenterOnScreen(Images_Folder + "error.png", confidence=0.9)
                for i in range (10):
                    try:
                        x, y = pyautogui.locateCenterOnScreen(Images_Folder + "dont_send.png", confidence=0.9)
                        time.sleep(.25)
                        pydirectinput.click(x, y)
                    except (pyautogui.ImageNotFoundException, TypeError):
                        pass

                return "crash"
            except (pyautogui.ImageNotFoundException, TypeError):
                pass

            time.sleep(1)

            try:
                x, y = pyautogui.locateCenterOnScreen(Images_Folder + 'leave.png', confidence=0.8)
                pyautogui.click(x, y)
                game_ended = True
                return False
            except (pyautogui.ImageNotFoundException, TypeError):
                pass

        #timed_out
        else:

            press_button_or_crash("open_menu.png")
            press_button_or_crash("quit.png")
            press_button_or_crash("yes.png")


            return "time out"

def game_loop(AI_One: str, AI_Two: str, games: int) -> dict:

    AI_One_Wins = 0
    AI_Two_Wins = 0
    timed_out = 0

    for i in range(games):

        clean_directory()
        set_ais(AI_One, AI_Two)
        press_button_or_crash("single_player.PNG")
        press_button_or_crash("skirmish.PNG")
        time.sleep(1)
        set_players()
        press_button_or_crash("start_game.PNG")
        time.sleep(1)

        result = check_game()
        time.sleep(5)

        if result == "crash":
            reset_game()
            return {"GAME CRASH" : 1}
        elif result == "ai_error":
            return {"AI CRASH" : 1}
        elif result == "time out":
            press_button_or_crash("main_menu.PNG")
            timed_out += 1

        try:
            x, y = pyautogui.locateCenterOnScreen(Images_Folder + 'won_1.PNG', confidence=0.8)
        except (pyautogui.ImageNotFoundException, TypeError):
            try:
                x, y = pyautogui.locateCenterOnScreen(Images_Folder + 'won_2.PNG', confidence=0.8)
            except (pyautogui.ImageNotFoundException, TypeError):
                print("could not identify winner")

        if y < 337 and result != "time out" and y != 0:
            AI_One_Wins += 1

        elif result != "time out" and y != 0:
            AI_Two_Wins += 1

        press_button_or_crash("main_menu.PNG")

    return {AI_One: AI_One_Wins, AI_Two: AI_Two_Wins, "TIMED OUT" : timed_out}

print(game_loop("best.per","HD.per",3))
