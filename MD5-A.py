from os import path, walk, get_terminal_size
from time import time
from hashlib import md5 as calc_md5_for


IgnoreFilesize = 99 ** 99
OnlyNames      = False
InputFolder    = ""
CurrentInput   = ""
op = ['1', '2', '3']

GREEN  = "\u001b[38;5;114m"
RED    = "\u001b[38;5;160m"
YELLOW = "\u001b[38;5;229m"
ORANGE = "\u001b[38;5;214m"
ENDC   = "\u001b[0m"
def ec(): print(ENDC, end='')

s = 0
def IgnoreFilesizeSet(InputFolder):
    global IgnoreFilesize

    try:
        IgnoreFilesize = float(InputFolder.split("*")[-1])
        print(f"{' ' * s}   $ {ORANGE}Установлено игнорирование файлов весом более{ENDC} {IgnoreFilesize} МБ{ORANGE} в вводимом каталоге.{ENDC}")

    except: print(f"{' ' * s}   {RED}Вводите размер в числовом виде.{ENDC}")


def MD5_Calculate(InputFolder):

    t_start = time()

    f_passed = 0
    f_calced = 0
    f_errors = 0
    
    md5log   = ''
    
    for filefolder, dirs, files in walk(InputFolder):
        for filename in files:
            f_passed += 1
            
            fullpath    = f"{filefolder}\\{filename}"
            filesize_mb = path.getsize(fullpath) / (1024*1024)

            try:
                if filesize_mb < IgnoreFilesize and filename != "desktop.ini":

                    TerminalWidth = get_terminal_size()[0]
                    info = f"\r{' ' * 36}← {fullpath if not OnlyNames else filename}"
                    if len(info) > TerminalWidth: info = info[0:TerminalWidth-3] + " .."
                    print(info, end='')
                    
                    with open(fullpath, 'rb') as fp:
                        md5_hash = calc_md5_for(fp.read()).hexdigest()
                        md5log  += f"{fullpath if not OnlyNames else filename}\n{md5_hash}\n"
                        
                        f_calced += 1

                    print(f"\r   {md5_hash}", flush=True)

            except Exception as e: f_errors += 1; print(f"\r   {RED}{e}{ENDC}", flush=True)


    t_total = time() - t_start

    bordersize = ' ' * (22 + len(str(f_passed)))
    print(f"""
    ⌜{bordersize}⌝
      Файлов просмотрено: {YELLOW}{f_passed}{ENDC}
      Файлов с хэшэм:     {GREEN }{f_calced}{ENDC}
      Ошибок:             {RED   }{f_errors}{ENDC}
      
      Время: {ORANGE}{round(t_total, 2)} с{ENDC}.
    ⌞{bordersize}⌟
    """)

    while True:
        md5l_file = input(f" > Имя/Путь+имя сохраняемого файла с MD5 данными: {YELLOW}"); ec()

        if md5l_file == "*отмена": break
        else:
            try:
                md5l = open(md5l_file, 'w', encoding='utf-8')
                md5l.write(md5log), md5l.close()

                print(f"{ENDC}   $ {ORANGE}Файл{ENDC} {YELLOW}{path.abspath(md5l_file)}{ENDC} {ORANGE}сохранён.{ENDC}\n{'―' * TerminalWidth}")
                break

            except PermissionError : print(f"   $ {RED}Ошибка создания файла{ENDC} ({YELLOW}Нет разрешения{ENDC}).")
            except OSError         : print(f"   $ {RED}Ошибка создания файла{ENDC} ({YELLOW}Имя файла не должно содержать специальные символы{ENDC}).")
            except Exception as e  : print(f"   $ {RED}Ошибка создания файла{ENDC} ({YELLOW}{e}{ENDC}).")

def MD5_Search(InputFolder):

    t_start = time()

    f_founds = 0
    f_passed = 0
    f_errors = 0

    print(f"\n    $ {ORANGE}Выбранная для поиска папка:{ENDC} {YELLOW}{InputFolder}{ENDC}; {ORANGE}Файл с MD5 данными:{ENDC} {YELLOW}{path.abspath(md5_data_file)}{ENDC}.\n    $ События: ")
    print("    $ Поиск по списку MD5 данных в выбранной папке.. ", end='')

    with open(md5_data_file, encoding='utf-8') as md5log_file:
        md5log_IMPORTED = [row.strip() for row in md5log_file]

    f_count_total = sum(len(files) for root, dirs, files in walk(InputFolder))
    for filefolder, dirs, files in walk(InputFolder):
        for filename in files:

            f_passed   += 1

            fullpath    = f"{filefolder}\\{filename}"
            filesize_mb = path.getsize(fullpath) / (1024*1024)

            TerminalWidth = get_terminal_size()[0]
            searching = f"\r    $ Поиск по списку MD5 данных в выбранной папке: {f_passed}/{f_count_total} {filename if OnlyNames else fullpath}"
            searching += ' ' * (TerminalWidth - len(searching))
            if len(searching) > TerminalWidth: searching = searching[0:TerminalWidth-3] + " .."
            print(searching, end='', flush=True)

            try:
                if filesize_mb < IgnoreFilesize and filesize_mb > 0 and filename != "desktop.ini":
                    with open(fullpath, 'rb') as fp: curr_md5_hash = calc_md5_for(fp.read()).hexdigest()

                    if curr_md5_hash in md5log_IMPORTED:
                        md5log_IMPORTED_founded_md5index = md5log_IMPORTED.index(curr_md5_hash)

                        if md5log_IMPORTED_founded_md5index // 2 == 0:
                            md5log_IMPORTED_founded_md5      = md5log_IMPORTED[md5log_IMPORTED_founded_md5index]
                            md5log_IMPORTED_founded_filename = md5log_IMPORTED[md5log_IMPORTED_founded_md5index - 1]

                            print(f"\r      {GREEN}Найден: {md5log_IMPORTED_founded_filename}{ENDC} (MD5:{md5log_IMPORTED_founded_md5}) как {YELLOW}{fullpath}{ENDC}", flush=True)
                            f_founds += 1

            except Exception as e: f_errors += 1; print(f"\r      {RED}Ошибка: {fullpath}{ENDC}: {YELLOW}{e}{ENDC}", flush=True)     

    if f_founds == 0: print(f"\r{' ' * TerminalWidth}\n\r      Ничего не найдено . . .{' ' * (TerminalWidth - 29)}\n\n    $ {ORANGE}Поиск по списку MD5 данных в выбранной папке завершён.{ENDC}{' ' * (TerminalWidth - 60)}", flush=True)
    else: print(f"\r    $ {ORANGE}Поиск по списку MD5 данных в выбранной папке завершён.{ENDC}{' ' * (TerminalWidth - 60)}", flush=True)


    t_total = time() - t_start

    bordersize = ' ' * (22 + len(str(f_passed)))
    print(f"""
       ⌜{bordersize}⌝
         Файлов просмотрено: {YELLOW}{f_passed}{ENDC}
         Файлов найдено:     {GREEN }{f_founds}{ENDC}
         Ошибок:             {RED   }{f_errors}{ENDC}
         
         Время: {ORANGE}{round(t_total, 2)} с{ENDC}.
       ⌞{bordersize}⌟
    """)

    print(f"{'―' * TerminalWidth}\n") 


if __name__ == "__main__":
    print("\n(1)Составить контрольные суммы файлов | (2)Найти файлы по данным контрольной суммы | (3)Выйти")
    while True:
        
        while CurrentInput != op[0:2]:
            CurrentInput = input(f"> {YELLOW}"); ec()
        
            if CurrentInput == op[0]:
                while True:
                    InputFolder = input(f" > Папка с файлами: {YELLOW}"); ec()
    
                    if not ("*") in InputFolder:
                        if path.isdir(InputFolder): print(""); MD5_Calculate(InputFolder)
                        else: print(f"   $ {RED}Каталог не найден.{ENDC}")
    
                    elif InputFolder == "*назад": break
                    else: s = 0; IgnoreFilesizeSet(InputFolder)
    
            elif CurrentInput == op[1]:
                OnlyNamesOldState = OnlyNames
                OnlyNames = True
    
                while True:
                    md5_data_file = input(f" > Файл с MD5 данными: {YELLOW}"); ec()
    
                    if path.isfile(md5_data_file):
                        print(f"   $ {ORANGE}Используется:{ENDC} {YELLOW}{path.abspath(md5_data_file)}{ENDC}")
    
                        while True:
                            InputFolder = input(f"  > Папка с файлами для поиска: {YELLOW}"); ec()
    
                            if not ("*") in InputFolder:
                                if path.isdir(InputFolder): MD5_Search(InputFolder)
                                else: print(f"    $ {RED}Каталог не найден.{ENDC}")
    
                            elif InputFolder == "*назад": break
                            elif InputFolder == "*имена":  OnlyNames = True;  print(f"    $ {ORANGE}Только имена файлов.{ENDC}")
                            elif InputFolder == "*полные": OnlyNames = False; print(f"    $ {ORANGE}Полные пути ко всем файлам.{ENDC}")
                            else: s = 1; IgnoreFilesizeSet(InputFolder)
    
                    elif md5_data_file == "*назад": break
                    else: print(f"   $ {RED}Файл{ENDC} {YELLOW}{md5_data_file}{ENDC} {RED}не найден.{ENDC}")
                
                OnlyNames = OnlyNamesOldState
    
    
            elif CurrentInput == "*имена":  OnlyNames = True;  print(f"  $ {ORANGE}Только имена файлов.{ENDC}")
            elif CurrentInput == "*полные": OnlyNames = False; print(f"  $ {ORANGE}Полные пути ко всем файлам.{ENDC}")
            
            elif CurrentInput == op[2]: ec(); exit()
