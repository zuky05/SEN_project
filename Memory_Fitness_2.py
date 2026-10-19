#importujeme si library ktore potrebujeme
from random import *
from time import *
from tkinter import *
import customtkinter
from math import *
import hashlib
import os as os
import os.path
from datetime import datetime
from PIL import Image, ImageTk


#vytvorenie canvasu 
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
canvas = Canvas(root, height = screen_height, width = screen_width, bg = 'white')
canvas.pack()
root.withdraw()


login_window = Toplevel()
login_window.title("Prihlasovanie")
login_window.geometry("400x400")
login_window.resizable(False, False)
login_canvas = Canvas(login_window, width = 400, height = 400)
login_canvas.pack()

#velkost pisma zalezi od velkosti obrazovky
font_size = int(80 * screen_width/2560)

game_type = 0 #0 znamena menu naslede podla cisla bude hra
last_game_type = 0
score   = 0
Mode = "L"
#customtkinter
customtkinter.set_appearance_mode("dark")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#login shitfest
#kazdy file je v lokacii stats\{meno_hraca}\{meno_hry}.txt

meno = ""
def login():
    global meno
    if os.path.exists(f"stats\{login_meno_entry.get()}"):
        f=open(f"stats\{login_meno_entry.get()}\heslo.txt","r")
        lines = f.readlines()
        password = login_heslo_entry.get().encode("UTF-8")
        if lines[0] == hashlib.sha256(password).hexdigest():
            f.close()
            meno = login_meno_entry.get()
            login_canvas.delete("login_UI")
            login_window.destroy()
            root.deiconify()
            root.state("zoomed")
            root.title("Memory Fitness")
            load_game()
        else:
            information_text_label.configure(text="Nesprávne heslo/\nprihlasovacie meno")
            f.close()
    else:
        information_text_label.configure(text="Dané prihlasovacie \n meno neexistuje!")

def create_account():
    global meno
    if os.path.exists(f"stats\{login_meno_entry.get()}"):
        information_text_label.configure(text="Dané prihlasovacie \n meno už existuje!")
    else:
        os.makedirs(f"stats\{login_meno_entry.get()}")
        f=open(f"stats\{login_meno_entry.get()}\heslo.txt","a")
        password = login_heslo_entry.get().encode("UTF-8")
        f.write(hashlib.sha256(password).hexdigest())
        f.close()
        for i in ["Sequence Memory","Chimp Test","Aim Trainer","Typing","Verbal Memory","Number Memory", "Visual Memory", "Reaction Time"]:
            f=open(f"stats\{login_meno_entry.get()}\{i}.txt","a")
            f.close()
        meno = login_meno_entry.get()
        login_canvas.delete("login_UI")
        login_window.destroy()
        root.deiconify()
        root.state("zoomed")
        root.title("Memory Fitness")
        load_game()

login_meno_entry = customtkinter.CTkEntry(login_canvas, font = ("Arial", 30),width=380, corner_radius=15, placeholder_text="Zadajte meno")
login_meno_entry.pack()

login_heslo_entry = customtkinter.CTkEntry(login_canvas, font=("Arial",30), width=380, corner_radius=15, placeholder_text="Zadajte heslo")
login_heslo_entry.pack()
login_heslo_entry.configure(show="*")

def show_password(event):
    login_heslo_entry.configure(show="")
def hide_password(event):
    login_heslo_entry.configure(show="*")

login_heslo_entry.bind("<Enter>", show_password)
login_heslo_entry.bind("<Leave>", hide_password)

login_button = customtkinter.CTkButton(login_canvas, font = ("Arial", 30), width=380, corner_radius=15, text = "Prihlásiť sa", anchor = "center", command=login)
login_button.pack()
acc_creation_button = customtkinter.CTkButton(login_canvas, font = ("Arial", 30), width=380, corner_radius=15, text = "Registrovať sa", anchor = "center", command=create_account)
acc_creation_button.pack()
information_text_label = customtkinter.CTkLabel(login_canvas, text = "Prihlasovanie", font = ("Arial", 45),text_color = "red", fg_color = "transparent")
information_text_label.pack()

def login_UI():
    login_canvas.create_window(200, 175, window=login_heslo_entry, tags = "login_UI")
    login_canvas.create_window(200, 130, window=login_meno_entry, tags = "login_UI")
    login_canvas.create_window(200, 50, window=information_text_label, tags = "login_UI")
    login_canvas.create_window(200, 290, window=login_button, tags = "login_UI")
    login_canvas.create_window(200, 335, window=acc_creation_button, tags = "login_UI")
    
login_UI()
login_canvas.delete("login_UI")
login_UI()


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#menu

# farbenie     [pozadie,stvorceky/outline,text]
light_colours = [["#FFFFFF","#B87333","#000000","#e9cbaf"],["#FFFFFF","#009900","#000000","#99ff99"],["#FFFFFF","#6666ff","#000000","#b3b3ff"],["#FFFFFF","#e6c300","#000000","#fff4b3"],["#FFFFFF","#ff0080","#000000","#ffcce6"]]
dark_colours = [["#000000","#ff3333","#FFFFFF","#990000"],["#000000","#69b09f","#FFFFFF","#2c544a"],["#000000","#ffb380","#FFFFFF","#cc5200"],["#000000","#50C878","#FFFFFF","#184e2a"],["#000000","#ecb3ff","#FFFFFF","#600080"]]
light_order = 0
dark_order = 0
colour = ["#FFFFFF","#B87333","#000000","#e9cbaf"]
text_colour = colour[2]
bg_colour = colour[0]
outline_colour = colour[1]
box_colour = colour[3]
canvas.configure(bg=bg_colour)

def round_rectangle(x1, y1, x2, y2,color,tag,outline, radius=25, **kwargs):
        
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

    canvas.create_polygon(points, **kwargs, smooth=True,fill=color,tags=tag,outline = outline,width=2)

Name_Of_Games = ["Sequence Memory","Chimp Test","Aim Trainer","Typing","Verbal Memory","Number Memory", "Visual Memory", "Reaction Time"]


def menu():
    canvas.delete("all")

    round_rectangle(screen_width // 12-(screen_width // 6 + screen_width // 18)*0.2,
                    screen_height // 2.2 - screen_height // 6*0.2,
                    screen_width // 12 + screen_width // 6 + (screen_width // 6 + screen_width // 18)*3.2,
                    screen_height // 2.2 + screen_height // 8 + screen_height // 6*1.2, box_colour,"idk",outline=outline_colour)
    for row in range(2):
        for column in range(4):
            round_rectangle(screen_width // 12 + (screen_width // 6 + screen_width // 18) * column, 
                            screen_height // 2.2 + screen_height // 6 * row, 
                            screen_width // 12 + screen_width // 6 + (screen_width // 6 + screen_width // 18) * column, 
                            screen_height // 2.2 + screen_height // 8 + screen_height // 6 * row, 
                            bg_colour, (str(column + row * 4 + 1)+"box","menu"), outline_colour)
            canvas.create_text((screen_width // 12 + (screen_width // 6 + screen_width // 18) * column + 
                                screen_width // 12 + screen_width // 6 + (screen_width // 6 + screen_width // 18) * column) // 2, 
                               (screen_height // 2.2 + screen_height // 6 * row + 
                                screen_height // 2.2 + screen_height // 8 + screen_height // 6 * row) // 2,
                               text=Name_Of_Games[(column + row * 4)], 
                               font=f"Arial {font_size // 3} bold", fill=text_colour, tags=(str(column + row * 4 + 1),"menu","text"))
    if colour in light_colours:
        nadpis = canvas.create_text(screen_width//2,screen_height//3.5,text="Memory Fitness",font = (f'Arial {font_size*2} bold'),fill=text_colour)
        nadpis2 = canvas.create_text(screen_width//2+screen_width//400,screen_height//3.5+screen_height//200,text="Memory Fitness",font = (f'Arial {font_size*2} bold'),fill=outline_colour)
        vitanie = canvas.create_text(screen_width//5,screen_height//8,text=f"{meno} vitajte v",fill=text_colour,font = (f'Arial {font_size} bold italic'))
        vitanie2 = canvas.create_text(screen_width//5+screen_width//400,screen_height//8+screen_height//200,text=f"{meno} vitajte v",fill=outline_colour,font = (f'Arial {font_size} bold italic'))
    else:
        nadpis = canvas.create_text(screen_width//2,screen_height//3.5,text="Memory Fitness",font = (f'Arial {font_size*2} bold'),fill=outline_colour)
        nadpis2 = canvas.create_text(screen_width//2+screen_width//400,screen_height//3.5+screen_height//200,text="Memory Fitness",font = (f'Arial {font_size*2} bold'),fill=text_colour)
        vitanie = canvas.create_text(screen_width//5,screen_height//8,text=f"{meno} vitajte v",fill=text_colour,font = (f'Arial {font_size} bold italic'))
        vitanie2 = canvas.create_text(screen_width//5+screen_width//200,screen_height//8+screen_height//400,text=f"{meno} vitajte v",fill=outline_colour,font = (f'Arial {font_size} bold italic'))

            
    # DARK štvorček
    dark_left, dark_top = screen_width - 130, screen_height - 130
    dark_right, dark_bottom = screen_width - 80, screen_height - 80
    canvas.create_rectangle(dark_left, dark_top, dark_right, dark_bottom, tags=("0", "DARK"), fill=bg_colour, outline=outline_colour)

    # LIGHT štvorček
    light_left, light_top = screen_width - 80, screen_height - 130
    light_right, light_bottom = screen_width - 30, screen_height - 80
    canvas.create_rectangle(light_left, light_top, light_right, light_bottom, tags=("0", "LIGHT"), fill=bg_colour, outline=outline_colour)

    # Kreslenie mesiaca (v strede DARK štvorčeka)
    dark_center_x = (dark_left + dark_right) // 2
    dark_center_y = (dark_top + dark_bottom) // 2
    moon_radius = 20
    canvas.create_oval(dark_center_x - moon_radius, dark_center_y - moon_radius,dark_center_x + moon_radius, dark_center_y + moon_radius, fill=bg_colour, outline=outline_colour, tags=("0", "DARK"),width=4)
    canvas.create_oval(dark_center_x - moon_radius + 5, dark_center_y - moon_radius, dark_center_x + moon_radius + 5, dark_center_y + moon_radius, fill=bg_colour, outline="", tags=("0", "DARK"))

    # Kreslenie slnka (v strede LIGHT štvorčeka)
    light_center_x = (light_left + light_right) // 2
    light_center_y = (light_top + light_bottom) // 2
    sun_radius = 15
    canvas.create_oval(light_center_x - sun_radius, light_center_y - sun_radius, light_center_x + sun_radius, light_center_y + sun_radius, fill=bg_colour, outline=outline_colour, tags=("0", "LIGHT"))

    for angle in range(0, 360, 45):
        x1 = light_center_x + sun_radius * cos(radians(angle))
        y1 = light_center_y + sun_radius * sin(radians(angle))
        x2 = light_center_x + (sun_radius + 10) * cos(radians(angle))
        y2 = light_center_y + (sun_radius + 10) * sin(radians(angle))
        canvas.create_line(x1, y1, x2, y2, fill=outline_colour, width=2)

    for i in range(8):
        if i%2 == 0:
            farba = outline_colour
        else:
            farba = bg_colour
        canvas.create_oval(0-screen_height//(i+3.5),screen_height+screen_height//(i+3.5),0+screen_height//(i+3.5),screen_height-screen_height//(i+3.5),fill=farba,outline=farba)

    for i in range(24):
        if i%2 == 0:
            farba = outline_colour
        else:
            farba = bg_colour
        canvas.create_oval(screen_width-screen_height//(i+5.5),screen_height//(i+5.5),screen_width+screen_height//(i+5.5),-screen_height//(i+5.5),fill=farba,outline=farba)

    canvas.create_text(screen_width//2,screen_height-screen_height//10,fill=text_colour,font = (f'Arial {font_size//4} bold'),text="By RT ©2025")
def back():
    canvas.create_rectangle(screen_width//100,screen_height//100,screen_width//25,screen_height//20,tags=("backbox","krokspat"),outline=outline_colour)
       # Kreslenie šípky
    box_center_x = (screen_width // 100 + screen_width // 20) // 2
    box_center_y = (screen_height // 100 + screen_height // 20) // 2
    arrow_size = screen_width // 80  # Veľkosť šípky

    # Kreslenie šípky smerujúcej doľava
    canvas.create_line(box_center_x + arrow_size // 2, box_center_y, 
                       box_center_x - arrow_size, box_center_y, 
                       width=3, tags=("back","krokspat","text"), fill=text_colour)  # Hlavná línia
    
    canvas.create_line(box_center_x - arrow_size, box_center_y, 
                       box_center_x - arrow_size // 2, box_center_y - arrow_size // 2, 
                       width=3, tags=("back","krokspat","text"), fill=text_colour)  # Horná diagonála
    
    canvas.create_line(box_center_x - arrow_size, box_center_y, 
                       box_center_x - arrow_size // 2, box_center_y + arrow_size // 2, 
                       width=3, tags=("back","krokspat","text"), fill=text_colour)  # Dolná diagonála

vysvetlivky = ["Na obrazovke sa objaví 3x3 pole s krúžkami. Niektoré krúžky budú meniť farbu a vašou úlohou je zapamätať si poradie týchto krúžkov. Po správnom zadaní tejto postupnosti, postupujete o úroveň vyššie, kde sa do postupnosti pridá ďaľší krúžok",
                "Na obrazovke sa objavia krúžky s číslami v strede. Tieto čísla si treba zapamätať a vašou úlohou je v správnom poradí kliknúť na všetky krúžky, t.j. od najmenšieho čísla po najväčšie. Háčik je v tom, že po kliknutí na prvý krúžok čísla zmiznú, a je to už len na vašej pamäti, či ste si zapamätali celú postupnosť.",
                "Vašou úlohou v tejto hre je čo najrýchlejšie kliknúť na všetky postupne sa objavujúce terče. Dokopy musíte kliknúť na 20 terčov a výsledné skóre je priemerný čas, ktorý ste potrebovali na kliknutie jedného terča.",
                "Na obrazovke uvidíte 10 slov, ktoré musíte čo najrýchlejšie prepísať. Pri tejto hre je rovnako dôležitá rýchlosť ako aj presnosť, keďže slovo musíte prepísať správne, nakoľko pri každom chybnom písmene nedostanete bod. Nebojte sa, ak sa pomýlite, môžete písmeno opraviť Backspacom a následným zadaním správneho písmena.",
                "Vašou úlohou v tejto hre bude zapamätať si, či slovo, ktoré uvidíte na obrazovke, vidíte prvýkrát, teda je nové, alebo ste ho už videli. Podľa toho, čo si myslíte, budete klikať na jedno z dvoch tlačidiel „Videl“ alebo „Nové“. Po každej správnej odpovedi dostanete ďalšie slovo. Hra sa končí, keď sa pri jednom slove rozhodnete nesprávne.",
                "Na obrazovke uvidíte číslo na pár sekúnd, ktoré si musíte zapamätať a následne ho správne napísať. Vždy, keď číslo zadáte správne, posuniete sa ďalej a uvidíte číslo, ktoré má o jednu číslicu viac.",
                "Vašou úlohou v tejto hre bude správne si zapamätať, ktoré obdĺžniky boli rozsvietené a ktoré nie. Na pár sekúnd uvidíte niekoľko svietiacich obdĺžnikov, ktoré následne zmiznú. To je znamenie, že musíte kliknúť na políčka, na ktorých svietili obdĺžniky.",
                "Po zapnutí tejto hry budete čakať, kým sa na obrazovke objaví obrázok koňa. V takom prípade je vašou úlohou čo najrýchlejšie kliknúť (nemusíte klikať priamo na koňa, stačí len kliknúť kdekoľvek). Cieľom hry je reagovať čo najrýchlejšie."]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#images


obrazok = ""

RT_horses = []
for i in range(5):
    RT_horses.append(PhotoImage(file=f"images\horse{i+1}.png"))




def scaling(path,width,height):
    image = Image.open(path)
    image.thumbnail((width, height))
    return ImageTk.PhotoImage(image)

good_job = scaling("images/GJ2.png",screen_width,screen_height//2)    
bad_job = scaling("images/GJJ.png",screen_width//3,screen_height//3)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#games
#Sequence Memory          game function     game_type = 1     var prefix SM
#zadefinovanie policok a zoznamov so suradnicami stredov
radius = (screen_width + screen_height) // 40
SM_Sx = [screen_width//2 - screen_width//8, screen_width//2, screen_width//2 + screen_width//8, screen_width//2 - screen_width//8, screen_width//2, screen_width//2 + screen_width//8, screen_width//2 - screen_width//8, screen_width//2, screen_width//2 + screen_width//8]
SM_Sy = [screen_height//2 - screen_height//6, screen_height//2 - screen_height//6, screen_height//2 - screen_height//6, screen_height//2, screen_height//2, screen_height//2, screen_height//2 + screen_height//6, screen_height//2 + screen_height//6, screen_height//2 + screen_height//6]

#body + zaznamenavanie
SM_count = 0
SM_guess_step = 0
SM_guess_time = True
SM_sequence = [4]

def sequence_memory():
    global SM_guess_time
    canvas.delete("score")
    canvas.create_text(screen_width-screen_width//10,screen_height//20,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {SM_count-1} "),fill=outline_colour,tags = "score")
    for ii in range(len(SM_sequence)+1):
        SM_guess_time = False
        for i in range(9):
            #posledne vykreslenie kruzkov a povolenie hadania
            if ii == len(SM_sequence):
                canvas.create_oval(SM_Sx[i] - radius, SM_Sy[i] - radius, SM_Sx[i] + radius, SM_Sy[i] + radius,fill = outline_colour,outline=outline_colour, tags = "game")
                SM_guess_time = True

            #vykreslenie spravneho kruzku
            elif SM_sequence[ii] == i:
                canvas.create_oval(SM_Sx[i] - radius, SM_Sy[i] - radius, SM_Sx[i] + radius, SM_Sy[i] + radius, fill = text_colour, tags = "game",outline=box_colour)

            #vykreslenie nespravneho kruzku
            else:
                canvas.create_oval(SM_Sx[i] - radius, SM_Sy[i] - radius, SM_Sx[i] + radius, SM_Sy[i] + radius, fill = box_colour,outline=outline_colour, tags = "game")
        if SM_guess_time == False:
            canvas.update()
            sleep(2/(SM_count**(1/2)))
        #delay aby bolo vidiet ked je ten isty kruzok viac krat po sebe
            for i in range(9):
                canvas.create_oval(SM_Sx[i] - radius, SM_Sy[i] - radius, SM_Sx[i] + radius, SM_Sy[i] + radius,fill = box_colour,outline=outline_colour, tags = "game")
            canvas.update()
            sleep(0.2)
    back()
    
#zahajenie hry
def start_sequence_memory():
    global SM_count, SM_guess_step, SM_guess_time, SM_sequence
    SM_count = 1
    SM_guess_step = 0
    SM_guess_time = True
    SM_sequence = [randint(0,8)]
    sequence_memory()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Chimp Test          game function     game_type = 2     var prefix CT

CT_flag = True
CT_score = 0 
CT_size = 60
CT_columns = (screen_width - CT_size*3 ) // CT_size #pocet stlpcov
CT_rows = (screen_height - CT_size*3 ) // CT_size #pocet riadkov
CT_numbers = []
CT_array = []
CT_streak = 5 #pocet za sebou uhadnutych kol, urcuje pocet stvorcov

def Chimp_Test():
    canvas.delete("all")
    canvas.create_text(screen_width-screen_width//10,screen_height//40,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {CT_streak-5} "),fill=outline_colour,tags = "guess_UI")
    CT_array = [["0" for _ in range(CT_columns)] for _ in range(CT_rows)]
    for u in range(CT_streak):
        i = randrange(0,CT_columns)
        j = randrange(0,CT_rows)
        while CT_array[j][i] == "1":
            i = randrange(0,CT_columns)
            j = randrange(0,CT_rows)
        CT_array[j][i] = "1"
        CT_numbers.append(str(u+1))
    for row in range(len(CT_array)):
        for column in range(len(CT_array[row])):
            if CT_array[row][column] == "1":
                CT_name = choice(CT_numbers)
                CT_numbers.remove(CT_name)
                canvas.create_oval((column+1) * CT_size, (row+1) * CT_size, (column+2) * CT_size, (row+2) * CT_size, tags = CT_name,fill = bg_colour,outline=outline_colour,width=2)
                canvas.create_text((column+1.5) * CT_size, (row+1.5) * CT_size, text = CT_name, tags = (CT_name,"cisla"),fill=text_colour,font = (f'Arial {font_size//2} bold'))
    
        
def start_chimp_test():
    global CT_numbers, CT_array, CT_flag,CT_score,CT_streak
    CT_streak = 5
    CT_flag = True
    CT_score = 0
    Chimp_Test()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Aim Trainer          game function     game_type = 3     var prefix AT

#timer zacaitok
AT_start_time = time()

#gamemode info
AT_max_count = 20
AT_count = AT_max_count + 1
AT_radius = (screen_width + screen_height) // 80
AT_Sx = screen_width//2
AT_Sy = screen_height//2

def start_aim_trainer():
    global AT_start_time, AT_max_count, AT_count, AT_radius, AT_Sx, AT_Sy, last_game_type
    AT_start_time = time()
    AT_max_count = 20
    AT_count = AT_max_count
    AT_radius = (screen_width + screen_height) // 80
    AT_Sx = randrange(screen_width//4, screen_width-screen_width//4)
    AT_Sy = randrange(screen_height//4, screen_height-screen_height//4)
    canvas.create_oval(AT_Sx-AT_radius, AT_Sy-AT_radius, AT_Sx+AT_radius, AT_Sy+AT_radius, fill = outline_colour, outline = outline_colour, tags = "target")
    canvas.create_text(screen_width-screen_width//10,screen_height//20,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {AT_max_count-AT_count}/{AT_max_count}"),fill=outline_colour,tags = "target")
    canvas.create_text(screen_width//2,screen_height//20,font=(f'Arial {font_size} bold'),text=("Spustite kliknutím!"),fill=outline_colour,tags = "target")
    last_game_type = game_type

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Typing          game function     game_type = 4     var prefix T
T_points = 0
T_start_time = 0
def set_text_with_attributes(text_widget, texts_and_attributes):
    i_start = text_widget.index(INSERT)
    for i, (text, attributes) in enumerate(texts_and_attributes):
        text_widget.insert(END, text)
        i_end = text_widget.index(INSERT)
        tag_name = f'tag{i}'
        text_widget.tag_add(tag_name, i_start, i_end)
        text_widget.tag_config(tag_name, **attributes)
        i_start = i_end

def Typing():
    global T_index,T_letters,T_idk, text,T_points
    T_points = 0
    T_text = ""
    T_list = []
    T_index = 0
    
    for i in range(10):
        T_list.append((choice(VeM_lines)).strip())
    T_text += " ".join(T_list)+"\n\n"

    T_letters = []
    for i in T_text:
        T_letters.append(i.lower())
    while "\n" in T_letters:
        T_letters.remove("\n")
    T_idk = []
    for letter in T_letters:
        T_idk.append((letter,{}))

    text = Text(canvas, font = ("Arial",font_size),width = 30,wrap=WORD,bd=0,bg=bg_colour,fg=text_colour)
    set_text_with_attributes(text,T_idk)

    canvas.create_window(screen_width//2,screen_height//5,window = text,anchor="n")
    text.configure(state="disabled")
    
def on_key(event):
    global T_index,T_idk, text,T_points, game_type, last_game_type,score,T_start_time
    if game_type == 4:
        if Mode == "L":
            farba1 = "#c1f0c1"#zelena
            farba2= "#ffb3b3" #cervena
        else:
            farba1 = "#145214" #zelena
            farba2 = "#800000" #cervena
        canvas.delete("score")
        if T_index == 0:
            T_start_time = time()
        if T_letters[T_index] == f"{event.char}":
            T_idk[T_index] = (T_letters[T_index], {"background": farba1})
            text.configure(state="normal")
            text.delete(1.0,END)
            set_text_with_attributes(text,T_idk)
            #text.pack()
            text.configure(state="disabled")
            T_index += 1
            T_points += 1
        elif "BackSpace" == f"{event.keysym}":
            T_index -= 1
            if T_index < 0:
                T_index = 0
            if T_idk[T_index][1] == {"background": farba1}:
                T_points -= 1
            T_idk[T_index] = (T_letters[T_index], {"background": bg_colour})
            text.configure(state="normal")
            text.delete(1.0,END)
            set_text_with_attributes(text,T_idk)
            #text.pack()
            text.configure(state="disabled")
        else:
            T_idk[T_index] = (T_letters[T_index], {"background": farba2})
            text.configure(state="normal")
            text.delete(1.0,END)
            set_text_with_attributes(text,T_idk)
            #text.pack()
            text.configure(state="disabled")
            T_index += 1
        canvas.create_text(screen_width-screen_width//10,screen_height//20,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {T_points}/{len(T_letters)}"),fill=outline_colour,tags = "score")
        if T_index == len(T_letters):
            canvas.delete("all")
            T_final_time = time() - T_start_time
            score = round((T_points/5)/T_final_time*60,2)
            last_game_type = game_type
            game_type = 10
            load_game()

def start_typing():
    
    Typing()

root.bind("<Key>", on_key)



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Verbal Memory          game function     game_type = 5     var prefix VeM

#vytvorenie UI pre uzivatela ktore bude mat pri hadani


#flag ktory bude rozhodovat o spranosti odpovede
VeM_word = ""
VeM_seen = False
VeM_fail = False

#body
VeM_points = 0

#VeM_file zo slovami ktore budu pouzite
VeM_file = open("slovicka.txt", "r", encoding="utf-8")
VeM_flag = 0
#citanie txt filu
VeM_lines = VeM_file.readlines()
VeM_used = []
VeM_file.close()

def Verbal_Memory():
    global VeM_word, VeM_seen, VeM_fail, VeM_used, last_game_type,game_type, score,VeM_flag
    back()
    VeM_word = ""
    VeM_seen = False
    VeM_fail = False
    #vyberanie slovicka

    r = randrange(0+VeM_flag, 40+len(VeM_used)+VeM_flag)

    #toto sa pouziva ak budeme mat nove slovo
    if r < 40:

        VeM_flag += 3
        VeM_seen = False
        q = randrange(0,len(VeM_lines))
        VeM_word = VeM_lines[q]
        VeM_used.append(VeM_word)

    #toto sa pouziva ak budem pouzivat uz videne slovo
    else:

        VeM_flag = 0
        VeM_seen = True
        VeM_word = VeM_used[randrange(0,len(VeM_used)-1)]

    #vykreslenie slova a cakanie na kliknutie tlacitka
    canvas.delete("guess_UI")
    canvas.create_text(screen_width//2, screen_height//2, text = VeM_word, font = (f'Arial {font_size*2} bold'), tags = "guess_UI",fill=text_colour)
    canvas.create_text(screen_width-screen_width//10,screen_height//20,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {VeM_points} "),fill=outline_colour,tags = "guess_UI")
    canvas.create_rectangle(screen_width//5,screen_height//2+screen_height//10,2*(screen_width//5),screen_height//2+screen_height//5,outline=outline_colour,tags=("videlbox","VeMko", "guess_UI"))
    canvas.create_text(1.5*(screen_width//5),screen_height//2+1.5*(screen_height//10),fill=text_colour,text="Videl",font = (f'Arial {font_size} bold'),tags=("videl","VeMko", "guess_UI","text"))

    canvas.create_rectangle(3*(screen_width//5),screen_height//2+screen_height//10,4*(screen_width//5),screen_height//2+screen_height//5,outline=outline_colour,tags=("novebox","VeMko", "guess_UI"))
    canvas.create_text(3.5*(screen_width//5),screen_height//2+1.5*(screen_height//10),fill=text_colour,text="Nové",font = (f'Arial {font_size} bold'),tags=("nove","VeMko", "guess_UI","text"))
    canvas.update()



def start_verbal_memory():
    global VeM_used,VeM_points,VeM_flag
    VeM_flag = 0
    VeM_points = 0
    VeM_used = []
    Verbal_Memory()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Number Memory          game function     game_type = 6     var prefix NM

#cas ktory bude mat uzivatel na zapamatanie cisla
NM_delay = 2
NM_number = ""
NM_points = 0
#vytvorenie UI pre uzivatela ktore bude mat pri hadani
NM_entry = customtkinter.CTkEntry(canvas, font = ('Arial', font_size),width=screen_width//3, corner_radius=0, placeholder_text="Zadajte číslo",justify="center")
NM_entry.pack()



def guess_UI():
    canvas.create_window(screen_width//2, screen_height//2, window=NM_entry, tags = "guess_UI")
    NM_entry.focus()
    canvas.create_rectangle(screen_width//2-screen_width//15,screen_height//2+screen_height//20,screen_width//2+screen_width//15,screen_height//2+screen_height//10,outline=outline_colour,tags=("odovzdajbox","guess_UI"))
    canvas.create_text(screen_width//2,screen_height//2+screen_height//13,text="Hádajte",tags=("odovzdaj","guess_UI","text"),font = (f'Arial {font_size//2} bold'),fill=text_colour)
    canvas.create_text(screen_width//2, screen_height//2-screen_height//6, text = "?"*len(NM_number), font = (f'Arial {font_size} bold'), tags = "guess_UI",fill=text_colour)

#prvotne vytvorenie a premazanie Ui pre spravnu velkost canvasu
guess_UI()
canvas.delete("guess_UI")

def Number_Memory():
    global game_type,last_game_type, score, NM_number, NM_points
    back()
    #zakladne premenne ktore bume potrebovat pri tejto hre
    NM_number = ""
    NM_guess = ""

        #generacia cisla ktore budeme hadat
    for i in range(NM_points+1):
        NM_number = NM_number + str(randint(0,9))

        #samotne vykreslenie cisla do canvasu a nasledne odstranenie po urcitom case
    canvas.create_text(screen_width-screen_width//10,screen_height//20,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {NM_points} "),fill=outline_colour,tags = "score")
    canvas.create_text(screen_width//2, screen_height//2-screen_height//6, text = NM_number, font = (f'Arial {font_size} bold'), tags = "NM_number",fill=text_colour)
    canvas.update()
    sleep(NM_delay+0.25*NM_points)
    canvas.delete("NM_number")
    guess_UI()
    canvas.update()
##    canvas.create_text(screen_width//2, screen_height//2-screen_height//6, text = f'Zadal si nespravne cislo tvoje skore je {NM_points}', font = (f'Arial {font_size} bold'),fill=text_colour, tags = "NM_number")
##    canvas.delete("guess_UI")

def start_number_memory():
    global NM_points
    NM_points = 0
    Number_Memory()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Visual Memory          game function     game_type = 7     var prefix ViM

ViM_streak = 1
ViM_score = 0
ViM_flag = True
ViM_control = False

def Visual_Memory(ViM_array):
    global ViM_control
    ViM_control = False
    canvas.create_text(screen_width-screen_width//10,screen_height//20,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {ViM_streak-1} "),fill=outline_colour,tags = "score")
    ViM_SizeX = ((screen_width-screen_width//6)//len(ViM_array))
    ViM_SizeY = ((screen_height-screen_height//4)//len(ViM_array))
    for row in range(len(ViM_array)):
        for column in range(len(ViM_array)):
            if ViM_array[row][column] == "1":
                canvas.create_rectangle(ViM_SizeX*column+screen_width//12,ViM_SizeY*row+screen_height//8,ViM_SizeX*(column+1)+screen_width//12,ViM_SizeY*(row+1)+screen_height//8,fill = outline_colour,outline=text_colour,width=2,tags="spravne")
            else:
                canvas.create_rectangle(ViM_SizeX*column+screen_width//12,ViM_SizeY*row+screen_height//8,ViM_SizeX*(column+1)+screen_width//12,ViM_SizeY*(row+1)+screen_height//8,fill=bg_colour,outline=text_colour,width=2,tags="nespravne")
    canvas.update()
    canvas.after(3000)
    canvas.itemconfig("spravne", fill=bg_colour)
    canvas.update()
    ViM_control = True

#pole moze byt podla narocnosti
def start_visual_memory():
    global ViM_score, last_game_type, ViM_flag
    ViM_size = 4 + ViM_streak//3
    ViM_flag = True
    ViM_score = 0
    ViM_array = [["0" for _ in range(ViM_size)] for _ in range(ViM_size)]
    for u in range(ViM_streak):
        row = randrange(0,ViM_size)
        column = randrange(0,ViM_size)
        while ViM_array[row][column] == "1":
            row = randrange(0,ViM_size)
            column = randrange(0,ViM_size)
        ViM_array[row][column] = "1"
    back()
    Visual_Memory(ViM_array)
    last_game_type = game_type

    




#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Reaction time          game function     game_type = 8     var prefix RT

RT_start = 0
def Reaction_time():
    global RT_start,RT_flag
    RT_flag = False
    RT_spawn_time= randint(500, 12000)#mas tam chvilu cas na spawn
    canvas.create_text(screen_width//2,screen_height//2,text="Pripravte sa na K̷̲͑ö̶̮́ň̶͎̏a̶͍̕!",tag="zaciatok",fill=text_colour,font = (f'Arial {font_size} bold'))
    canvas.after(1500)
    canvas.update()
    canvas.delete("zaciatok")
    canvas.after(RT_spawn_time)
    RT_image = choice(RT_horses)
    canvas.create_image(screen_width//2,screen_height//2-screen_height//10,image=RT_image,tags="kon")
    RT_flag = True
    canvas.update()
    RT_start = time()

    

    
    
def start_reaction_time():
    global RT_start, last_game_type,RT_flag
    RT_flag = False
    RT_start = 0
    last_game_type = game_type
    Reaction_time()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Waiting room                                               game_type = 11

def start_waiting_room():
    global obrazok
    canvas.create_rectangle(screen_width//2-screen_width//9,screen_height//2+screen_height//3,screen_width//2+screen_width//100,screen_height//2+screen_height//25+screen_height//3,fill=bg_colour,outline = outline_colour,tags=("startbox","menu"),width=2)
    canvas.create_text(screen_width//2-screen_width//20, screen_height//2+screen_height//50+screen_height//3, fill=text_colour,tags=("start","menu","text"),text="Spustiť hru",font = (f'Arial {font_size//2} bold'))

    canvas.create_rectangle(screen_width//2+screen_width//50,screen_height//2+screen_height//3,screen_width//2+screen_width//12,screen_height//2+screen_height//25+screen_height//3,fill=bg_colour,outline = outline_colour,tags=("homebox","menu"),width=2)
    canvas.create_text(screen_width//2+screen_width//20, screen_height//2+screen_height//50+screen_height//3, fill=text_colour,tags=("home","menu","text"),text="Späť",font = (f'Arial {font_size//2} bold'))
    if colour in light_colours:
        nadpis = canvas.create_text(screen_width//2,screen_height//6-screen_height//50,text=Name_Of_Games[last_game_type-1],font = (f'Arial {font_size} bold'),fill=text_colour)
        nadpis2 = canvas.create_text(screen_width//2+screen_width//200,screen_height//6+screen_height//200-screen_height//50,text=Name_Of_Games[last_game_type-1],font = (f'Arial {font_size} bold'),fill=outline_colour)
    else:
        nadpis = canvas.create_text(screen_width//2,screen_height//6-screen_height//50,text=Name_Of_Games[last_game_type-1],font = (f'Arial {font_size} bold'),fill=outline_colour)
        nadpis2 = canvas.create_text(screen_width//2+screen_width//200,screen_height//6+screen_height//200-screen_height//50,text=Name_Of_Games[last_game_type-1],font = (f'Arial {font_size} bold'),fill=text_colour)



    canvas.create_text(screen_width//20, screen_height//3-screen_height//20, text = f"{vysvetlivky[last_game_type-1]}", font = (f'Arial {font_size//3} bold'), fill=text_colour,anchor="nw",width=(screen_width//5 - screen_width//20))

    
    rect_x1 = screen_width//2 + screen_width//4 + screen_width//40
    rect_x2 = screen_width - screen_width//40
    canvas.create_rectangle(rect_x1, screen_height//4, rect_x2, 3*(screen_height//4), outline=outline_colour, width=2)
    statistika_text = "štatistiky\n\nNajlepšie dosiahnuté\nskóre\n\n"
    stats_list = []
    stats_path = os.path.join("stats", meno, f"{Name_Of_Games[last_game_type-1]}.txt")
    if os.path.exists(stats_path):
        try:
            with open(stats_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [l.strip() for l in f if l.strip()]
            for i in range(0, len(lines)-1, 2):
                datum = lines[i]
                skore_riadok = lines[i+1]
                val = float(skore_riadok.split(":")[-1].strip())
                stats_list.append((val, datum))
            
            # Pri Aim Trainer (3) a Reaction Time (8) je menší čas lepší, pri ostatných je vyššie skóre lepšie
            if last_game_type in [3, 8]:
                stats_list.sort(key=lambda x: x[0])
            else:
                stats_list.sort(key=lambda x: x[0], reverse=True)
        except:
            pass

    for i in range(3):
        if i < len(stats_list):
            val, datum = stats_list[i]
            val_str = str(int(val)) if val == int(val) else str(val)
            statistika_text += f"{datum}\nSkóre: {val_str}\n\n"
        else:
            statistika_text += "Neodohral si dosť hier\nSkóre: 0\n\n"

    canvas.create_text(rect_x1 + screen_width//100, screen_height//4 + screen_height//70, text=statistika_text.strip(), font=(f'Arial {font_size//3} bold'), fill=text_colour, anchor="nw")

    if Mode == "L":
        Mode2 ="L"
    else:
        Mode2 = "D"
    obrazok = scaling(f"screenshots/Game{last_game_type}{Mode2}.png",screen_width//2,screen_height//2)
    canvas.create_image(screen_width//2,screen_height//2+screen_height//50, image=obrazok, anchor="center")
    canvas.create_rectangle(screen_width//2-screen_width//4,screen_height//2+screen_height//50-screen_height//4,screen_width//2+screen_width//4,screen_height//2+screen_height//50+screen_height//4,outline=outline_colour,width=5)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Losing screen and Winning screen         game function       game_type = 9  /  10     

def start_losing_screen():
    canvas.delete("krokspat")
    canvas.create_text(screen_width//2,screen_height//2 - screen_height//10, fill = text_colour, font = (f'Arial {font_size} bold'), text=f"Ľutujem, prehrali ste! Vaše skóre bolo {score}")
    canvas.create_image(screen_width//2,screen_height-screen_height//4,image=bad_job)
    canvas.create_rectangle(screen_width//2-screen_width//9,screen_height//2,screen_width//2+screen_width//150,screen_height//2+screen_height//25,fill=bg_colour,outline = outline_colour,tags=("restartbox","menu"))
    canvas.create_text(screen_width//2-screen_width//20, screen_height//2+screen_height//50, fill=text_colour,tags=("restart","menu","text"),text="Hrať znova",font = (f'Arial {font_size//2} bold'))

    canvas.create_rectangle(screen_width//2+screen_width//50,screen_height//2,screen_width//2+screen_width//12,screen_height//2+screen_height//25,fill=bg_colour,outline = outline_colour,tags=("homebox","menu"))
    canvas.create_text(screen_width//2+screen_width//20, screen_height//2+screen_height//50, fill=text_colour,tags=("home","menu","text"),text="Menu",font = (f'Arial {font_size//2} bold'))
    f = open(f"stats\{meno}\{Name_Of_Games[last_game_type-1]}.txt", "a")
    f.write(str(datetime.now())[0:len(str(datetime.now()))-7]+"\n")
    f.write("Score: "+str(score)+"\n")
    f.write("\n")

def start_winning_screen():
    canvas.delete("krokspat")
    if last_game_type == 3: #Aim trainer
        canvas.create_text(screen_width//2,screen_height//2 - screen_height//10, fill = text_colour, font = (f'Arial {font_size} bold'), text=f"Váš priemerný čas na kliknutie terča bol {score} ms")
    elif last_game_type == 4: #Typing
        canvas.create_text(screen_width//2,screen_height//2 - screen_height//10, fill = text_colour, font = (f'Arial {font_size} bold'), text=f"Váša rýchlosť písania je {score} slov za minútu")
    else: #Reaction time
        canvas.create_text(screen_width//2,screen_height//2 - screen_height//10, fill = text_colour, font = (f'Arial {font_size} bold'), text=f"Výborne! Váš čas bol {score} ms")
    
    canvas.create_rectangle(screen_width//2-screen_width//12,screen_height//2,screen_width//2-screen_width//50,screen_height//2+screen_height//25,fill=bg_colour,outline = outline_colour,tags=("homebox","menu"))
    canvas.create_text(screen_width//2-screen_width//20, screen_height//2+screen_height//50, fill=text_colour,tags=("home","menu","text"),text="Menu",font = (f'Arial {font_size//2} bold'))

    canvas.create_rectangle(screen_width//2-screen_width//100,screen_height//2,screen_width//2+screen_width//9,screen_height//2+screen_height//25,fill=bg_colour,outline = outline_colour,tags=("restartbox","menu"))
    canvas.create_text(screen_width//2+screen_width//20, screen_height//2+screen_height//50, fill=text_colour,tags=("restart","menu","text"),text="Hrať Znova",font = (f'Arial {font_size//2} bold'))
    f = open(f"stats\{meno}\{Name_Of_Games[last_game_type-1]}.txt", "a")
    f.write(str(datetime.now())[0:len(str(datetime.now()))-7]+"\n")
    f.write("Score: "+str(score)+"\n")
    f.write("\n")
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#bindovanie kliknutia podla typu hry

def on_enter(event):
    hovered_item = canvas.find_withtag("current")  # Získa ID objektu pod kurzorom
    current_tags = canvas.gettags(hovered_item)
    if "game" in current_tags:
        canvas.itemconfig(hovered_item, fill=text_colour)    
    elif "text" not in current_tags:
        canvas.itemconfig(hovered_item, fill=outline_colour)  # Zmení jeho farbu

    else:
        canvas.itemconfig(str(current_tags[0])+"box",fill=outline_colour)
        
        
def on_leave(event):
    hovered_item = canvas.find_withtag("current")  # Získa ID objektu pod kurzorom
    current_tags = canvas.gettags(hovered_item)
    if "game" in current_tags:
        canvas.itemconfig(hovered_item, fill=outline_colour)
    elif "text" not in current_tags:
        canvas.itemconfig(hovered_item, fill=bg_colour)
    else:
        canvas.itemconfig(str(current_tags[0])+"box",fill=bg_colour)
#vyfarbovanie menucka        

canvas.tag_bind("menu", "<Enter>", on_enter)
canvas.tag_bind("menu", "<Leave>", on_leave)
canvas.tag_bind("krokspat", "<Enter>", on_enter)
canvas.tag_bind("krokspat", "<Leave>", on_leave)
canvas.tag_bind("odovzdaj", "<Enter>", on_enter)
canvas.tag_bind("odovzdaj", "<Leave>", on_leave)
canvas.tag_bind("VeMko", "<Enter>", on_enter)
canvas.tag_bind("VeMko", "<Leave>", on_leave)

def klik(sur):
    global game_type, score, last_game_type, light_order, dark_order,Mode
    try:
        if game_type == 0:
            global bg_colour, text_colour, outline_colour, colour, box_colour
            x = sur.x
            y = sur.y
            Menu_Clicked = canvas.find_overlapping(x-2,y-2,x+2,y+2)
            if "LIGHT" in canvas.gettags(Menu_Clicked[0]):
                    Mode = "L"
                    light_order += 1
                    colour = light_colours[light_order%(len(light_colours))]
                    text_colour = colour[2]
                    bg_colour = colour[0]
                    box_colour = colour[3]
                    outline_colour = colour[1]
                    canvas["bg"] = bg_colour
                    menu()
            elif "DARK" in canvas.gettags(Menu_Clicked[0]):
                    Mode = "D"
                    dark_order += 1
                    colour = dark_colours[dark_order%(len(dark_colours))]
                    text_colour = colour[2]
                    bg_colour = colour[0]
                    box_colour = colour[3]
                    outline_colour = colour[1]
                    canvas["bg"] = bg_colour
                    menu()        
            else:
                    last_game_type = int(canvas.gettags(Menu_Clicked[-1])[0][0])
                    canvas.delete("all")
                    game_type = 11
                    load_game()

        if 0<game_type<9:
            x = sur.x
            y = sur.y
            Clicked = canvas.find_overlapping(x-2,y-2,x+2,y+2)
            if "back" in canvas.gettags(Clicked[0]) or "backbox" in canvas.gettags(Clicked[0]):
                canvas.delete("all")
                game_type = 11
                load_game()
            else:
        
                if game_type == 1:
                    global SM_sequence, SM_guess_step, SM_count, SM_guess_time
                    if SM_guess_time == True:

                        x = sur.x
                        y = sur.y

                    #v pripade ze hra uz prebieha pokracuje sa tu pri kliknuti a zistuje sa na ktory kruzok pouzivatel klikol ak klikol na kruzok a nie mimo hracej plochy
                        for i in range(9):
                            if radius >= sqrt((SM_Sx[i]-x)**2+(SM_Sy[i]-y)**2):
                                #ak pouzivatel klikol na kruzok zistuje sa ci klikol na spravny
                                if SM_sequence[SM_guess_step] == i:
                                    SM_guess_step += 1
                                    #ak ano tak zistujeme ci to nebol posledny v poradi
                                    if SM_guess_step == SM_count:
                                        SM_guess_step = 0
                                        SM_count += 1
                                        SM_sequence.append(randrange(0,9))
                                        canvas.delete("all")
                                        canvas.create_image(screen_width//2,screen_height//2,image=good_job)
                                        canvas.update()
                                        canvas.after(2000)
                                        canvas.delete("all")
                                        canvas.update()
                                        sequence_memory()

                                #v pripade ze pouzivatel klikol na kruzok ale bol nespravny tak sa hra ukoncuje
                                else:
                                    canvas.delete("all")
                                    score= len(SM_sequence) - 1
                                    SM_guess_time = False
                                    last_game_type = game_type
                                    game_type = 9
                                    load_game()


                elif game_type == 2:
                    global CT_score, CT_flag, CT_streak
                    x = sur.x
                    y = sur.y
                    if CT_flag:
                        if CT_streak != CT_score+1:
                            CT_clicked = canvas.find_overlapping(x-5, y-5,x+5,y+5)

                            if str(CT_score + 1) in canvas.gettags(CT_clicked[0]):
                                canvas.delete("cisla")
                                canvas.itemconfig(canvas.find_closest(x, y),fill=outline_colour)
                                CT_score += 1
                                
                            else:
                                CT_flag = False
                                canvas.update()
                                canvas.after(1000)
                                canvas.delete("all")
                                canvas.update()
                                score = CT_streak - 5
                                CT_streak = 5
                                last_game_type = game_type
                                game_type = 9
                                load_game()
                                
                        else:
                            CT_streak += 1
                            canvas.delete("all")
                            canvas.update()
                            canvas.create_image(screen_width//2,screen_height//2,image=good_job)
                            canvas.update()
                            canvas.after(2000)
                            CT_score = 0
                            Chimp_Test()
                            back()


                elif game_type == 3:#tuto tiez neprehras
                    global AT_Sx, AT_Sy, AT_count, AT_start_time, AT_max_count
                    y = sur.y
                    x = sur.x

                    #zistenie ci pouzivatel klikol na terc ak ano tak sa vygeneruje novy terc a odpocita sa 1 az kym ich nebude 0
                    if AT_radius >= sqrt((AT_Sx-x)**2+(AT_Sy-y)**2) and AT_count != 0:
                        AT_count -= 1
                        canvas.delete("target")
                        AT_Sx = randrange(screen_width//4, screen_width-screen_width//4)
                        AT_Sy = randrange(screen_height//4, screen_height-screen_height//4)
                        canvas.create_oval(AT_Sx-AT_radius, AT_Sy-AT_radius, AT_Sx+AT_radius, AT_Sy+AT_radius, fill = outline_colour, outline = outline_colour, tags = "target")
                        canvas.create_text(screen_width-screen_width//10,screen_height//20,font=(f'Arial {font_size//2} bold'),text=(f"Skóre: {AT_max_count-AT_count}/{AT_max_count}"),fill=outline_colour,tags = "target")

                        #v pripade ze pouzivate uz klikol na vsetky terce vypise sa vysledny cas
                        if AT_count == 0:
                            canvas.delete("target")
                            end_time = time()
                            elapsed_time = end_time - AT_start_time
                            score = int(elapsed_time*1000//AT_max_count)
                            last_game_type = game_type
                            game_type = 10
                            load_game()
                    
                        #v pripade ze pouzivatel klikol na prvy terc hra sa zacne a zacne sa pocitat cas
                        if AT_count == AT_max_count:
                            AT_start_time = time()

                elif game_type == 4:
                    pass

                elif game_type == 5:
                    global VeM_points
                    y = sur.y
                    x = sur.x
                    VeM_clicked = canvas.find_overlapping(x-2,y-2,x+2,y+2)
                    if VeM_seen and "videl" in canvas.gettags(VeM_clicked[0]) or VeM_seen and "videlbox" in canvas.gettags(VeM_clicked[0]):
                        VeM_points += 1
                
                        Verbal_Memory()
                    elif VeM_seen == False and "nove" in canvas.gettags(VeM_clicked[0]) or VeM_seen == False and "novebox" in canvas.gettags(VeM_clicked[0]):
                        VeM_points += 1

                        Verbal_Memory()
                    else:
                        canvas.delete("all")
                        last_game_type = game_type
                        score = VeM_points
                        game_type = 9
                        load_game()

                elif game_type == 6:
                    global NM_points
                    y = sur.y
                    x = sur.x
                    NM_clicked = canvas.find_overlapping(x-2,y-2,x+2,y+2)
                    
                    if "odovzdaj" in canvas.gettags(NM_clicked[0]) or "odovzdajbox" in canvas.gettags(NM_clicked[0]):
                        NM_guess = NM_entry.get()
                        NM_entry.delete(0, 'end')
                        canvas.delete("guess_UI")
                        
                        if NM_guess == NM_number:
                            NM_points += 1
                            canvas.delete("score")
                            Number_Memory()
                        else:
                            last_game_type = game_type
                            score = NM_points
                            game_type = 9
                            load_game()
                        

                elif game_type == 7:
                    global ViM_score, ViM_streak, ViM_flag
                    x = sur.x
                    y = sur.y
                    if ViM_flag and ViM_control:
                        ViM_clicked = canvas.find_closest(x, y)

                        if canvas.gettags(ViM_clicked)[0] == "spravne":
                            ViM_score += 1
                            canvas.itemconfig(str(canvas.find_closest(x, y)[0]),fill=outline_colour)
                            if ViM_score == ViM_streak:
                                canvas.update()
                                canvas.after(1200)
                                canvas.update()
                                ViM_streak += 1
                                canvas.delete("all")
                                canvas.create_image(screen_width//2,screen_height//2,image=good_job)
                                canvas.update()
                                canvas.after(3000)
                                canvas.delete("all")
                                canvas.update()
                                start_visual_memory()

                                
                        elif canvas.gettags(ViM_clicked)[0] == "nespravne":
                            canvas.itemconfig("spravne",fill=box_colour)
                            canvas.update()
                            canvas.delete("all")
                            canvas.after(3000)
                            canvas.update()
                            score = ViM_streak-1
                            game_type = 9
                            load_game()
                            ViM_flag = False
                            ViM_streak = 1
                

                elif game_type == 8:
                    global RT_flag
                    if RT_flag:
                        canvas.delete("kon")
                        RT_result = time() - RT_start
                        score =  RT_result*1000//1
                        RT_flag = False
                        last_game_type = game_type
                        game_type = 10
                        load_game()
            

        elif game_type == 9:
            x = sur.x
            y = sur.y
            Menu_Clicked = canvas.find_overlapping(x-2,y-2,x+2,y+2)
            if "home" in canvas.gettags(Menu_Clicked[0]) or "homebox" in canvas.gettags(Menu_Clicked[0]):
                canvas.delete("all")
                game_type = 0
                load_game()
            elif "restartbox" in canvas.gettags(Menu_Clicked[0]) or "restart" in canvas.gettags(Menu_Clicked[0]):
                canvas.delete("all")
                game_type = last_game_type
                load_game()

        elif game_type == 10:
            x = sur.x
            y = sur.y
            Menu_Clicked = canvas.find_overlapping(x-2,y-2,x+2,y+2)
            if "home" in canvas.gettags(Menu_Clicked[0]) or "homebox" in canvas.gettags(Menu_Clicked[0]):
                canvas.delete("all")
                game_type = 0
                load_game()
            elif "restartbox" in canvas.gettags(Menu_Clicked[0]) or "restart" in canvas.gettags(Menu_Clicked[0]):
                canvas.delete("all")
                game_type = last_game_type
                load_game()

        elif game_type == 11:
            x = sur.x
            y = sur.y
            Menu_Clicked = canvas.find_overlapping(x-2,y-2,x+2,y+2)
            if "home" in canvas.gettags(Menu_Clicked[0]) or "homebox" in canvas.gettags(Menu_Clicked[0]):
                canvas.delete("all")
                game_type = 0
                load_game()
            elif "startbox" in canvas.gettags(Menu_Clicked[0]) or "start" in canvas.gettags(Menu_Clicked[0]):
                canvas.delete("all")
                game_type = last_game_type
                load_game()
        
    except:
        pass
    
canvas.bind("<Button-1>", klik)


def entry_enter(event):
    global NM_guess,NM_points,game_type,score
    NM_guess = NM_entry.get()
    NM_entry.delete(0, 'end')
    canvas.delete("guess_UI")
    
    if NM_guess == NM_number:
        NM_points += 1
        canvas.delete("score")
        Number_Memory()
    else:
        last_game_type = game_type
        score = NM_points
        game_type = 9
        canvas.delete("all")
        load_game()    
NM_entry.bind("<Return>",entry_enter)


#spustenie hry
def load_game():
    if game_type == 0:
        menu()

    elif game_type == 1:
        start_sequence_memory()

    elif game_type == 2:
        start_chimp_test()
        back()

    elif game_type == 3:
        start_aim_trainer()
        back()

    elif game_type == 4:
        back()
        start_typing()

    elif game_type == 5:
        start_verbal_memory()

    elif game_type == 6:
        start_number_memory()

    elif game_type == 7:
        start_visual_memory()
        back()

    elif game_type == 8:
        back()
        start_reaction_time()

    elif game_type == 9:
        start_losing_screen()

    elif game_type == 10:
        start_winning_screen()

    elif game_type == 11:
        start_waiting_room()

canvas.mainloop()
