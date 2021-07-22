import pyautogui
import sys
import time
import python_imagesearch.imagesearch as imgsearch
from pyclick import HumanClicker
from pynput import keyboard
import numpy as np

'''
before start to work you should replace all screenshots in img folder
можно улучшить перехода аккаунта в fail,
перенеся его в конец поменяв координаты с последним и просто уменьшить amount_workers
'''
# global variable that stops the program if some key was pressed
exec_stop = False

'''
There are two mods of this bot
First - autoclicker
Second - prints position of cursor every second
'''
# mode = "autoclicker"
mode = "pos_logger"

# the number of accounts
amount_workers = 5
'''
The main array that stores the data of every account
First row - x-position of chrome browser
Second row - can store 0 if account is available for work and mine
    and it can store 1 if account doesn't work
Third row - store the time after success mining of each account
'''
worker = np.array([[154, 215, 281, 342, 400, 465, 530, 595, 660, 725, 790],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


hc = HumanClicker()


def click(x, y):
    """
    this function move cursor to position (x, y) and clicks
    :param x: x pos of cursor
    :param y: y pos of cursor
    :return:
    """
    hc.move((x, y), 1)
    hc.click()
    time.sleep(0.1)
    return


def minimize_current_chrome():
    """
    clicks on minimize button in browser
    :return:
    """
    click(1778, 65)
    return


def open_tab(i: int):
    """
    opens the next browser
    :param i: index in worker array
    :return:
    """
    # y-position is constant
    y = 22
    x = worker[0, i]
    click(x, y)
    return


def run():
    user = 0
    # While there's no 'execution stop' command passed
    while exec_stop is False:
        # If the script is in autoclicker mode
        if mode == "autoclicker":
            try:
                current_worker = user
                # if there are not errors with this account then open it
                if worker[1, current_worker] == 0:
                    open_tab(current_worker)
                    time.sleep(1)

                    # if it is mine time
                    if worker[2, current_worker] == 0 or time.time() - worker[2, current_worker] < 500:

                        # search the mine button
                        if imgsearch.imagesearch("img/mine.png")[0] != -1:
                            click(948, 998)
                            worker[2, current_worker] = time.time()

                        # Claim TLM button and claim process
                        elif imgsearch.imagesearch("img/claim.png")[0] != -1:
                            click(820, 745)
                            hc.move((387, 784), 1)
                            time.sleep(2)
                            checker = False
                            for index in range(30):
                                if imgsearch.imagesearch("img/approve.png")[0] != -1:
                                    click(387, 784)
                                    click(387, 784)
                                    checker = True
                                    break
                                time.sleep(1)
                            time.sleep(3)
                            if checker and imgsearch.imagesearch("img/approve.png")[0] != -1:
                                checker = False
                            if not checker:
                                pyautogui.press('f5')
                                click(735, 66)
                                pyautogui.press('f5')
                                click(1373, 411)
                            else:
                                worker[2, current_worker] = time.time()

                        # Back to mining hub button
                        elif imgsearch.imagesearch("img/go_to_hub.png")[0] != -1:
                            click(581, 919)
                            worker[2, current_worker] = 0
                        # If the failed to fetch error occur
                        elif imgsearch.imagesearch("img/failed.png")[0] != -1:
                            click(1372, 400)
                        # Find the exit button
                        elif imgsearch.imagesearch("img/exit.png")[0] != -1:
                            click(1373, 389)

                        # Main menu: Mine button
                        elif imgsearch.imagesearch("img/mine_main_menu.png")[0] != -1:
                            click(1478, 445)
                            time.sleep(1)
                            if imgsearch.imagesearch("img/mine.png")[0] != -1:
                                click(948, 998)

                        # Login button
                        elif imgsearch.imagesearch("img/login.png")[0] != -1:
                            click(970, 854)
                            click(948, 854)

                        # Main menu: Claim button
                        elif imgsearch.imagesearch("img/claim_main.png")[0] != -1:
                            click(959, 992)
                            hc.move((387, 784), 1)
                            time.sleep(2)
                            checker = False
                            for index in range(40):
                                if imgsearch.imagesearch("img/approve.png")[0] != -1:
                                    click(387, 784)
                                    click(387, 784)
                                    checker = True
                                    break
                                time.sleep(1)
                            time.sleep(3)
                            if checker and imgsearch.imagesearch("img/approve.png")[0] != -1:
                                checker = False
                            if not checker:
                                pyautogui.press('f5')
                                click(735, 66)
                                pyautogui.press('f5')
                                click(1373, 411)
                            else:
                                worker[2, current_worker] = time.time()
                    # if error occured
                    else:
                        pyautogui.press('f5')
                        worker[2, current_worker] = 0

                    minimize_current_chrome()

                    # finding next available account
                    if user == amount_workers - 1:
                        user = 0
                    else:
                        for index in range(user+1, amount_workers):
                            if worker[1, index] == 0:
                                user = index
                                break

            except:
                # If an error occurred
                print("An error occurred: ", sys.exc_info()[1])
                sys.exit(0)
        # If the script is in position logger mode
        else:
            try:
                # Print position to console every second
                print(pyautogui.position())
                time.sleep(1)
            except:
                # If an error occurred
                print("An error occurred: ", sys.exc_info()[2])


def on_press(key):
    # When F11 key is pressed, toggle modes between Autoclicker and Position Logger
    if key == keyboard.Key.f11:
        global mode
        mode = "pos_logger" if mode == "autoclicker" else "autoclicker"
        print(f"Changing mode to {mode}")
    # When Tab key is pressed, stop executing the script
    elif key == keyboard.Key.tab:
        global exec_stop
        exec_stop = True
        print("Shutting down...")
        sys.exit(0)


def main():
    # Listen for pressed keys
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    run()

if __name__ == '__main__':
    main()
