import pyautogui
import pydirectinput
import time
import os
import tkinter as tk
from sys import exit

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

            f = open("AI_Backup/" + All_AI_Files[i],'w+')
            f.write("saved this for you")
            f.close()

            #easier to catch the error here than try to mess with the list above
            try:
                os.remove(AI_Path + All_AI_Files[i])
            except FileNotFoundError:
                pass

    f = open(AI_Path + "AI_One.ai","w+")
    f.write("isn't matty the best?")
    f.close()

    f = open(AI_Path + "AI_Two.ai","w+")
    f.write("isn't matty the best?")
    f.close()

def set_ais(AI_One: str, AI_Two: str) -> None:
    if AI_One not in AIs_Available:
        print("AI NOT AVAILABLE: " + AI_One)
        exit()
    elif AI_Two not in AIs_Available:
        print("AI NOT AVAILABLE: " + AI_Two)
        exit()

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
            pyautogui.locateCenterOnScreen(image, confidence=0.9)
        except OSError:
            print(image + " is not a valid civ name, reverting to huns")
            image = Images_Folder + 'huns.png'

        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=0.9)
            time.sleep(.1)
            pydirectinput.click(x, y)
            break
        except (pyautogui.ImageNotFoundException, TypeError):
            pass

def wait_until_seen(image: str) -> None:
    image = Images_Folder + image

    while True:

        try:
            x, y = pyautogui.locateCenterOnScreen(image, confidence=0.9)
            time.sleep(.1)
            break
        except (pyautogui.ImageNotFoundException, TypeError):
            pass

def set_players(civ_1: str, civ_2: str) -> None:

    player_one_img: str = Images_Folder + "player_1.png"
    player_two_img: str = Images_Folder + "player_2.png"

    #player 1
    pydirectinput.click(390,390)
    press_button_or_crash("AI_One.png")
    time.sleep(.1)

    pydirectinput.click(1000,390)
    press_button_or_crash("random.png")
    if civ_1.lower() != "random":
        press_button_or_crash(civ_1.lower() + ".png")
    press_button_or_crash("confirm.png")

    #player 2
    pydirectinput.click(390,430)
    press_button_or_crash("AI_Two.png")
    pydirectinput.press("enter")

    pydirectinput.click(1000,430)
    press_button_or_crash("random.png")
    if civ_2.lower() != "random":
        press_button_or_crash(civ_2.lower() + ".png")
    press_button_or_crash("confirm.png")

def check_game(max_game_time: int) -> str:
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
            time.sleep(.5)
            press_button_or_crash("quit.png")
            time.sleep(.5)
            press_button_or_crash("yes.png")
            time.sleep(.5)


            return "time out"

def game_loop(AI_One: str, AI_Two: str, games: int, max_game_time: int, Speedup: str, civ_1: str, civ_2: str) -> dict:

    AI_One_Wins = 0
    AI_Two_Wins = 0
    timed_out = 0
    start_time = time.time()

    for i in range(games):

        clean_directory()
        set_ais(AI_One, AI_Two)

        pydirectinput.press("escape")

        press_button_or_crash("single_player.PNG")
        press_button_or_crash("skirmish.PNG")
        time.sleep(1)
        set_players(civ_1, civ_2)
        press_button_or_crash("start_game.PNG")

        wait_until_seen("open_menu.PNG")

        if Speedup != "":
            for i in range(10):
                try:
                    pydirectinput.press(Speedup)
                    time.sleep(.1)
                except:
                    print("invalid key! takes win32 key codes")

        result = check_game(max_game_time)
        time.sleep(5)

        if result == "crash":
            reset_game()
            return {"GAME CRASH" : 1}
        elif result == "ai_error":
            return {"AI CRASH" : 1}
        elif result == "time out":
            press_button_or_crash("main_menu.PNG")
            timed_out += 1

        else:
            x = 0
            y = 0
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

    return {AI_One: AI_One_Wins, AI_Two: AI_Two_Wins, "TIMED OUT" : timed_out, "Total time" : time.time() - start_time}

def run_games(AI_One: str, AI_Two: str, games: int, max_game_time: int, Speedup: str, civ_1: str, civ_2: str) -> None:

    output = game_loop(AI_One, AI_Two, games, max_game_time, Speedup, civ_1, civ_2)
    f = open("Outputs/" + str(time.time()) + ".csv","w+")
    f.write("AI,score\n")
    for entry in output:
        f.write(entry + "," + str( output[entry] ) + "\n")
    f.close()

def run_from_csv() -> None:

    f = open("parameters.csv",'r')
    params = f.read().split("\n")
    f.close()


    f = open("Outputs/" + str(time.time()) + ".csv","w+")
    f.write("AI One,Civ,Score,AI Two,Civ,Score\n")
    f.close()

    for i in range(1,len(params)):
        matchup = params[i].split(",")

        if len(matchup) > 6:

            AI_One = matchup[0]
            civ_1 = matchup[1]
            AI_Two = matchup[2]
            civ_2 = matchup[3]
            games = int(matchup[4])
            max_game_time = int(matchup[5])
            Speedup = matchup[6]

            f = open("Outputs/" + str(time.time()) + ".csv","a")
            local_result = game_loop(AI_One, AI_Two, games, max_game_time, Speedup, civ_1, civ_2)

            civ_index = 0
            civs = [civ_1, civ_2,"",""]
            for entry in local_result:
                if civs[civ_index] != "":
                    print(entry + "," + civs[civ_index] + "," + str(local_result[entry]) + ",")
                    f.write(entry + "," + civs[civ_index] + "," + str(local_result[entry]) + ",")
                else:
                    print(entry + "," + str(local_result[entry]) + ",")
                    f.write(entry + "," + str(local_result[entry]) + ",")
                civ_index += 1
            f.write("\n")
            f.close()



#print(game_loop("best.per","HD.per",3))

root = tk.Tk()

Label_1 = tk.Label(root, text = "AI One:  (include .per)")
Label_1.pack()

AI_One_Input = tk.Text(root, height = 1, width = 15)
AI_One_Input.insert(tk.INSERT, "EXAMPLE.per")
AI_One_Input.pack()

civ_1_label = tk.Label(root, text = "Civ One:")
civ_1_label.pack()

Civ_One_Input = tk.Text(root, height = 1, width = 15)
Civ_One_Input.insert(tk.INSERT, "huns")
Civ_One_Input.pack()

Label_2 = tk.Label(root, text = "AI Two:  (include .per)")
Label_2.pack()

AI_Two_Input = tk.Text(root, height = 1, width = 15)
AI_Two_Input.insert(tk.INSERT, "EXAMPLE_2.per")
AI_Two_Input.pack()

civ_2_label = tk.Label(root, text = "Civ Two:")
civ_2_label.pack()

Civ_Two_Input = tk.Text(root, height = 1, width = 15)
Civ_Two_Input.insert(tk.INSERT, "huns")
Civ_Two_Input.pack()

Label_3 = tk.Label(root, text = "Games to run")
Label_3.pack()

Game_Count = tk.Text(root, height = 1, width = 15)
Game_Count.insert(tk.INSERT, "3")
Game_Count.pack()

Label_4 = tk.Label(root, text = "Timeout time (real life seconds)")
Label_4.pack()

Timeout_Time = tk.Text(root, height = 1, width = 15)
Timeout_Time.insert(tk.INSERT, "10000")
Timeout_Time.pack()

Label_5 = tk.Label(root, text = "(Optional) Speed-up Hotkey")
Label_5.pack()

Speedup = tk.Text(root, height = 1, width = 15)
Speedup.insert(tk.INSERT, "blank for no speed up")
Speedup.pack()

button1 = tk.Button(root, text = "Run", command = lambda: run_games(AI_One_Input.get(1.0,"end-1c"), AI_Two_Input.get(1.0,"end-1c"), int( Game_Count.get(1.0,"end-1c") ), int( Timeout_Time.get(1.0,"end-1c")) , Speedup.get(1.0,"end-1c"), Civ_One_Input.get(1.0,"end-1c"), Civ_Two_Input.get(1.0,"end-1c")))
button1.pack()

button2 = tk.Button(root, text = "Run from csv", command = lambda: run_from_csv())
button2.pack()


root.mainloop()
