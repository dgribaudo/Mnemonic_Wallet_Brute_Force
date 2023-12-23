import time

from pybip39 import Mnemonic
import openpyxl
import pyautogui as p
import pyperclip as clip

def type_chain(k):
    p.doubleClick()
    p.write(k)
    if k == "ETH" or k == "TRON":
        copy_seq(1)
    else:
        copy_seq(0)

def copy_seq(k):
    global copy_all
    p.moveTo(p.center(copy_all[k]))
    p.click()

    
def tab_seq(n):
    for i in range(n):
        p.hotkey("tab")


def add_excel():
    global mnemonic, money
    dicvalues = list(chains.values())
    excel.append([mnemonic, money])
    for row in excel.iter_rows():
        if row[3].value is None:
            a = 0
            for i in range(10):
                row[i + 3 + a].value = dicvalues[i]
                a += 1
            break
    wb.save("wallet.xlsx")
    
def UntillFindImg(path):
    i = 0
    (x, y) = (0, 0)
    while (x, y) == (0, 0):
        try:
            if i % 100 and (path == 'img/import.png' or path == 'img/chainid.png'):
                p.leftClick()
            if i == 10000:
                input("Press a button, too many trials...")
            x, y = p.locateCenterOnScreen(path, confidence=0.9)
        except:
            time.sleep(0.01)
            i += 1
            continue
    return x, y

def seed_ins():
    global mnemonic
    x_word, y_word = UntillFindImg('img/word.png')

    p.moveTo(x_word, y_word)
    p.leftClick()

    mnemonic = str(Mnemonic())
    clip.copy(mnemonic)
    p.hotkey("ctrl", "v")

    p.moveTo(x_succ, y_succ)
    p.leftClick()
    
def open_w():
    x_openw, y_openw = UntillFindImg('img/openw.png')
    p.moveTo(x_openw, y_openw)
    p.leftClick()
    
def home():
    x_addall, y_addall = UntillFindImg('img/addall.png')
    try:
        x_zero, y_zero = p.locateCenterOnScreen('img/zero.png', confidence=0.9)
        money = False
    except:
        money = True
    p.moveTo(x_addall, y_addall)
    p.leftClick()
    
def copy_chain():
    global copy_all, mnemonic
    previous_w = mnemonic
    x_chainid, y_chainid = UntillFindImg('img/chainid.png')
    if copy_all == [0]:
        copy_all = list(p.locateAllOnScreen('img/copy.png'))
    for k in chains.keys():
        p.moveTo(x_chainid, y_chainid)
        type_chain(k)
        while previous_w == clip.paste():
            try:
                x_chainidact, y_chainidact = p.locateCenterOnScreen('img/chainid.png',confidence=0.9)
                type_chain(k)
                p.leftClick()
            except:
                x_back, y_back = UntillFindImg('img/back.png')
                p.leftClick()
            continue
        chains[k] = clip.paste()
        previous_w = clip.paste()
        
def back():
    global x_back, y_back
    if (x_back, y_back) == (0, 0):
        x_back, y_back = p.locateCenterOnScreen('img/back.png', confidence=0.9)
    p.moveTo(x_back, y_back)
    p.leftClick()
def manage():
    x_in, y_in = UntillFindImg('img/insidew.png')
    p.leftClick()

    x_manage, y_manage = UntillFindImg('img/manage.png')
    p.moveTo(x_manage, y_manage)
    p.leftClick()
def delete():
    x_wall, y_wall = UntillFindImg('img/wallets.PNG')
    tab_seq(2)
    p.hotkey("Enter")
    tab_seq(2)
    p.hotkey("Enter")
    p.hotkey("tab")
    p.hotkey("Enter")
def new():
    x_addnew, y_addnew = UntillFindImg('img/addnew.png')
    p.moveTo(x_addnew, y_addnew)
    p.leftClick()

    x_import, y_import = UntillFindImg('img/import.png')
    p.moveTo(x_import, y_import)
    p.leftClick()

    x_p, y_p = UntillFindImg('img/pass.PNG')
    p.hotkey("tab")
    p.typewrite(password)
    p.hotkey("Enter")

input("To start ... ")
password = "Trillion12345!"
chains = {"BITC": 0, "DO": 0, "ETH": 0, "XRP": 0, "TRON": 0, "DOT": 0, "KAVA": 0, "SOL": 0, "CARD": 0, "TON": 0}
wb = openpyxl.load_workbook("wallet.xlsx")
excel = wb.active
x_back, y_back = 0, 0
copy_all = [0]
mnemonic = ""
money = False

x_brave, y_brave = p.locateCenterOnScreen('img/brave.png', confidence=0.8)
p.moveTo(x_brave, y_brave)
p.leftClick()


x_succ, y_succ = p.locateCenterOnScreen('img/succ.png',confidence=0.90)


while True:
    
    seed_ins()
    open_w()
    home()
    copy_chain()
    add_excel()
    back()
    manage()
    delete()
    new()



