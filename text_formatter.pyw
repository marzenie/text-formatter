import json
import tkinter as tk

diff_letter = 120205
diff_number = 120734
additionall_big_letters_diff = 6
    
def main():

    # Create the main window
    root = tk.Tk()
    root.title("Text editor WITHOUT markdown [❌]")

    # Set the window size
    root.geometry("800x600")
    root.resizable(False, False)
    # Create a large text area
    text_area = tk.Text(root, wrap='word', font=("Cambria", 14) , height=20, width=70)
    text_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Function to handle button click event
    def effect_use(eff, status):
        text = get_selected(text_area)
        if text == "":
            return 0
        if ((eff == 3) and (status == 1)): # prevent underlining from accumulating because it is detected differently than diacritics
            text = remove_char_from_string(text, 863) # 863 - undeline
        replace_text=""

        for char in text:
            char_ed = change_letter(char)
            if status == 0:
                replace_text += remove_effect(char_ed, eff)
            if status == 1:
                replace_text += add_effect(char_ed, eff)
        text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        text_area.insert(tk.INSERT, replace_text)  
    
    bold_button_on = tk.Button(root, text="Bold [ON]", command=lambda: effect_use(1, 1))
    italic_button_on = tk.Button(root, text="Italic [ON]", command=lambda: effect_use(2, 1))
    underline_button_on = tk.Button(root, text="Underline [ON]", command=lambda: effect_use(3, 1))
    
    bold_button_off = tk.Button(root, text="Bold [OFF]", command=lambda: effect_use(1, 0))
    italic_button_off = tk.Button(root, text="Italic [OFF]", command=lambda: effect_use(2, 0))
    underline_button_off = tk.Button(root, text="Underline [OFF]", command=lambda: effect_use(3, 0))
    
    # Position the buttons using grid
    bold_button_on.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    italic_button_on.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    underline_button_on.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    # Right buttons below the text area
    bold_button_off.grid(row=1, column=2, padx=10, pady=10, sticky="e")
    italic_button_off.grid(row=2, column=2, padx=10, pady=10, sticky="e")
    underline_button_off.grid(row=3, column=2, padx=10, pady=10, sticky="e")
    # Start the GUI event loop
    root.mainloop()

def get_selected(text_area):
    if text_area.tag_ranges(tk.SEL):
        content = text_area.selection_get()
        return content
    return ""
def remove_char_from_string(string, chr_number):
    return ''.join([char for char in string if ord(char) != chr_number])
def change_letter(letter):
    letters_line_top = [243, 263, 324, 347, 378]  # ó, ć, ń, ś, ź
    letters_tails = [261, 281] # ą, ę
    replace_letters_tails = [97, 101] # a, e
    replace_letters_top = [111, 99, 110, 115, 122]# o, c, n, s, z
    ord_letter=ord(letter)
    try: # replace letters_line_top to diacritic letters
        replace_letter_index = letters_line_top.index(ord_letter)
        return chr(replace_letters_top[replace_letter_index]) + "́"
    except:
        pass
    
    if (ord_letter == 380):
        return "ż"
    if (ord_letter == 322):
        return "l̷"
        
    try: # replace letters_line_top to diacritic letters
        replace_letter_index = letters_tails.index(ord_letter)
        return chr(replace_letters_tails[replace_letter_index]) + "̨"
    except:
        pass
        
    return letter
    #return letter
def add_effect(letter, effect):
    """
    1 - bold
    2 - italic
    3 - bold & italic
    """
    ord_letter=ord(letter[0])
    status=check_current_effects(letter)
    diacritic = ""
    if (len(letter) > 1):
        diacritic = letter[1:]
    if (not status.__contains__('error')):
        if (effect == 1): # add bold from text
            if (status['bold'] == True or status['size'] == "U"): 
                return letter
            if (status['size'] == "N"): 
                #if(status['italic'] == True): # currently there is no font that contains italics in numbers
                    # return
                return chr(ord_letter + diff_number)
                
            if (status['italic'] == True): 
                return chr(ord_letter + 52)
            if (status['size'] == "B"): 
                return chr(ord_letter + diff_letter + additionall_big_letters_diff) + diacritic
            return chr(ord_letter + diff_letter) + diacritic

        elif (effect == 2):  # add italic from text
            if (status['italic'] == True or status['size'] == "U"):
                return letter
            if (status['size'] == "N"):  # currently there is no font that contains italics in numbers
                return letter
            if status['bold'] == True: 
                return chr(ord_letter + 104)
                
            if (status['size'] == "B"): 
                return chr(ord_letter + 52 + diff_letter + additionall_big_letters_diff) + diacritic
            return chr(ord_letter + 52 + diff_letter) + diacritic
        elif (effect == 3):  # add underline
            if (ord(letter[0]) == 863):
                return letter
            return letter + "͟"
        else:
            return letter
    return letter 
def remove_effect(letter, effect):
    """
    1 - bold
    2 - italic
    3 - bold & italic
    """
    ord_letter=ord(letter)
    status=check_current_effects(letter)
    diacritic = ""
    if (len(letter) > 1):
        diacritic = letter[1:]
    if (not status.__contains__('error')):
        if (effect == 1): # remove bold from text
            if (status['bold'] == False):
                return letter
            if (status['size'] == "N"): 
                #if(status['italic'] == True): # currently there is no font that contains italics in numbers
                    # return
                return chr(ord_letter - diff_number)
            if (status['italic'] == True): 
                return chr(ord_letter - 52)
                
            if (status['size'] == "B"): 
                return chr(ord_letter - diff_letter - additionall_big_letters_diff) + diacritic
            return chr(ord_letter - diff_letter) + diacritic
            
            
        elif (effect == 2):  # remove italic from text
            if (status['italic'] == False):
                return letter
            if (status['size'] == "N"):  # currently there is no font that contains italics in numbers
                return letter
            if (status['bold'] == True): 
                return chr(ord_letter - 104)
                
            if (status['size'] == "B"): 
                return chr(ord_letter - 52 - diff_letter - additionall_big_letters_diff) + diacritic
            return chr(ord_letter - 52 - diff_letter) + diacritic
        elif (effect == 3):  # remove underline
            if (ord(letter[0]) == 863):
                return ""
            return letter
        else:
            return letter
    return letter
    
def check_current_effects(letter):
    """
    bold | A-Z 1D5D4-1D5ED   |   120276-120301
    bold | a-z 1D5EE-1D607   |   120302-120327

    italic | A-Z 1D608-1D621   |   120328-120353
    italic | a-z 1D622-1D63B   |   120354-120379

    bold&italic | A-Z 1D63C-1D655   |   120380-120405
    bold&italic | a-z 1D656-1D66F   |   120406-120431
    """
    ord_letter=ord(letter[0])
    if (ord_letter in range(48, 58)): # normal numbers 48 - 57 + 1
        return { "size": "N", "bold": False, "italic": False }
    if (ord_letter in range(65, 91)): # bcs 90 need to be in range
        return { "size": "B", "bold": False, "italic": False }
    if (ord_letter in range(97, 123)): # bcs 122 need to be in range
        return { "size": "S", "bold": False, "italic": False }
    if (ord_letter in range(120276, 120432)):  # bcs 120431 need to be in range
        if ord_letter <= 120301:
            return { "size": "B", "bold": True, "italic": False }
        elif ord_letter <= 120327:
            return { "size": "S", "bold": True, "italic": False }
        elif ord_letter <= 120353:
            return { "size": "B", "bold": False, "italic": True }
        elif ord_letter <= 120379:
            return { "size": "S", "bold": False, "italic": True }
        elif ord_letter <= 120405:
            return { "size": "B", "bold": True, "italic": True }
        elif ord_letter <= 120431:
            return { "size": "S", "bold": True, "italic": True }
    if (ord_letter in range(120782, 120792)): # bold numbers 120782 - 120791 +1 to be in range
        return { "size": "N", "bold": True, "italic": False }
    if (ord_letter == 863): # underline
        return { "size": "U", "bold": False, "italic": False }
    return { "error": True }
    
if __name__ == "__main__":
    main()