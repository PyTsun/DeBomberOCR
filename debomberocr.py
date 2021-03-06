import pyautogui
from PIL import Image
from pytesseract import *
import keyboard
import random
pyautogui.FAILSAFE = False

# DeBomber OCR Settings
triggerkey   = "delete"
clrbonuskey  = "home"
clearlistkey = "end"
sscoords     = 540, 395, 45, 20 #this is my own region, use this script: https://github.com/xacvwe/DeBomberOCR/blob/main/region.py to change it!
textfile     = "jklm_allwords.txt"
typespeed    = 0.02
ocrpath      = "C:\\path\\to\\Tesseract-OCR\\tesseract.exe"
ocrconfig    = "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 7 --oem 1"

# Debomber OCR Settings Help
# triggerkey   - You can choose any trigger key to trigger DeBomberOCR and type words for you, key names is on this link https://github.com/xacvwe/DeBomberOCR/blob/main/triggerkeys.txt
# clrbonuskey  - Resets the bonus letters list.
# clearlistkey - Clears the usedwords list.
# sscoords     - Screenshots the bomb's letter prompt and converts it into a word containing those letters. it should look something like this: https://github.com/xacvwe/DeBomberOCR/blob/main/letters.png
# textfile     - Where the OCR grabbs words containing the letters from sscoords.
# typespeed    - Changes the typespeed, for faster epic dejavu thing use 0.00000000001 if you want but you might get banned
# ocrpath      - Path for tesseract.exe, and also to make DeBomberOCR work.
# ocrconfig    - Keep this config put if you don't know what it does to the script.

pytesseract.tesseract_cmd = ocrpath
print("DeBomberOCR is now running.")
usedwords = []
bonus = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]
wgeneration_limit = 25 # keep this on 25!

while True:
    a = keyboard.read_key()
    
    if a == clrbonuskey:
        bonus.clear()
        fillbonus = "ABCDEFGHIJKLMNOPQRSTUV"
        for bonusfill in fillbonus:
            bonus.append(bonusfill)
        print("Resetted bonus letters.")
    
    if a == clearlistkey:
        usedwords.clear()
        print("Cleared usedwords list.")

    if a == triggerkey:
        reqltr = random.choice(bonus)
        print(reqltr)
        scltr = pyautogui.screenshot(region=(sscoords))
        scltr.save(r"./letters.png")
        ltrimg = Image.open("letters.png")
        ltrstr = pytesseract.image_to_string(ltrimg, config=ocrconfig)
        n = ltrstr.split()
        pltrs = ''.join(str(x) for x in n)
        print('Letters: ' + pltrs)
        
        if len(pltrs) == 0:
            print("Cannot choose letters with none.")
        
        if len(pltrs) != 0:
            x = open(textfile, "r")
            words = [w for w in x.read().split() if pltrs in w]
            while True:
                try:
                    a = random.choice(words)
                except:
                    print("Cannot choose from an empty sequence (IndexError)")

                if wgeneration_limit != 0:
                    if reqltr in a:
                        print(f"Word Accepted: {a}")
                        break
                    
                    if reqltr not in a:
                        print(f"Word Declined: {a}")
                        wgeneration_limit -= 1
                        continue
                    
                if wgeneration_limit == 0:
                    wgeneration_limit += 25
                    print("Word Generation reached generation limit. Stopped Generating words to avoid DeBomberOCR from generating in an endless loop.")
                    break

            used = [w for w in usedwords if a in w]

            if used:
                print("Word is already used!")

            if not used:
                print(f"Typing Word: {a}")
                pyautogui.write(a, typespeed)
                pyautogui.press('enter')
                result = "".join(dict.fromkeys(a))
                for letter in result:
                    letters = [w for w in bonus if letter in w]
                    if letters:
                        bonus.remove(letter)
                    if not letters:
                        print(f"Letter '{letter}' not in list")

                if bonus == []:
                    fillbonus = "ABCDEFGHIJKLMNOPQRSTUV"
                    for bonusfill in fillbonus:
                        bonus.append(bonusfill)
                print("Bonus Letters Left: " + ','.join(str(x) for x in bonus)) 
