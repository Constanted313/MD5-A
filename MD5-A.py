from os import path, walk, get_terminal_size
from send2trash import send2trash
from hashlib import md5 as calc_md5_for
from datetime import date, datetime
from time import time


IgnoreFilesize_Max = 10 ** 10
IgnoreFilesize_Min = 0
IgnoreFolders  = []
AllfoundToggle = True
CopyDelToggle  = False
OnlyNames      = False
InputFolder    = ''
CurrentInput   = ''
op = ['1', '2', '3']


GREEN  = "\u001b[38;5;114m"
RED    = "\u001b[38;5;160m"
YELLOW = "\u001b[38;5;229m"
ORANGE = "\u001b[38;5;214m"
ENDC   = "\u001b[0m"
def ec(): print(ENDC, end='')


s = 0
def IgnoreFolders_Set(InputFolder):
    global IgnoreFilesize_Max
    global IgnoreFolders

    inputObjects = InputFolder.split("*")

    for i in inputObjects: IgnoreFolders.append(i) if not i in IgnoreFolders and len(i) != 0 else None
    if len(IgnoreFolders) > 0: print(f"{' ' * s}   $ {ORANGE}Установлено игнорирование каталогов с названиями{ENDC} ", end=''); print(*IgnoreFolders, sep=', ')

def IgnoreFilesize_Set(InputFolder):
    global IgnoreFilesize_Max
    global IgnoreFilesize_Min

    try:
        if   '>' in InputFolder: IgnoreFilesize_Max = float(InputFolder.split(">")[-1])
        elif '<' in InputFolder: IgnoreFilesize_Min = float(InputFolder.split("<")[-1])


        if '>' in InputFolder:

            if IgnoreFilesize_Min < IgnoreFilesize_Max:
                print(f"{' ' * s}   $ {ORANGE}Установлено игнорирование файлов весом более{ENDC} {IgnoreFilesize_Max} МБ {ORANGE}в вводимом каталоге.{ENDC} [{IgnoreFilesize_Min} < Filesize(MB) < {'10^10' if IgnoreFilesize_Max == 10**10 else IgnoreFilesize_Max}]")
            elif IgnoreFilesize_Max < 0: IgnoreFilesize_Min = 0; print(f"{' ' * s}   $ {RED}Максимальный вес не может быть отрицательным{ENDC}")
            else:
                print(f"{' ' * s}   $ {RED}Минимальный вес превышает максимальный{ENDC} [Мин: {ORANGE}{IgnoreFilesize_Min}{ENDC} > Макс: {ORANGE}{IgnoreFilesize_Max}{ENDC}]")
                IgnoreFilesize_Max = 10 ** 10


        elif '<' in InputFolder:

            if IgnoreFilesize_Min < IgnoreFilesize_Max and IgnoreFilesize_Min > 0: 
                print(f"{' ' * s}   $ {ORANGE}Установлено игнорирование файлов весом менее{ENDC} {IgnoreFilesize_Min} МБ {ORANGE}в вводимом каталоге.{ENDC} [{IgnoreFilesize_Min} < Filesize(MB) < {'10^10' if IgnoreFilesize_Max == 10**10 else IgnoreFilesize_Max}]")
            elif IgnoreFilesize_Min < 0: IgnoreFilesize_Min = 0; print(f"{' ' * s}   $ {RED}Минимальный вес не может быть отрицательным{ENDC}")
            else:
                print(f"{' ' * s}   $ {RED}Минимальный вес превышает максимальный{ENDC} [Мин: {ORANGE}{IgnoreFilesize_Min}{ENDC} > Макс: {ORANGE}{IgnoreFilesize_Max}{ENDC}]")
                IgnoreFilesize_Min = 0


    except: print(f"{' ' * s}   $ {RED}Вводите вес в числовом виде{ENDC}")


def CheckIgnore(filefolder):
    global Ignored

    filefolder_splitted = filefolder.split("\\")

    i=0
    while i < len(filefolder_splitted):
        if filefolder_splitted[i] in IgnoreFolders: Ignored = True; break
        else: i += 1

def ClearIgnore():
    global IgnoreFolders
    global IgnoreFilesize_Max
    global IgnoreFilesize_Min

    IgnoreFolders.clear()
    IgnoreFilesize_Max = 10 ** 10
    IgnoreFilesize_Min = 0

    print(f"{' ' * s}   $ {ORANGE}Список игнорируемых папок и игнорируемый размер файлов очищены.{ENDC}")




def MD5_Calculate(InputFolder):
    global Ignored

    print("")

    t_start  = time()

    md5log   = ''

    f_passed = 0
    f_hashed = 0
    f_errors = 0

    md5log_alt = f'```{date.today()} {datetime.now().strftime("%H:%M:%S")} | {path.abspath(InputFolder)}```\n\n'

    for filefolder, dirs, files in walk(InputFolder):
        for filename in files:

            fullpath    = f"{filefolder}\\{filename}"
            filesize_mb = path.getsize(fullpath) / (1024*1024)

            Ignored = False
            if len(IgnoreFolders) > 0: CheckIgnore(filefolder)

            if filename != "desktop.ini":

                f_passed += 1

                if not Ignored:
                    if IgnoreFilesize_Min < filesize_mb < IgnoreFilesize_Max:

                        try:
                            
                            fquestion = fullpath if not OnlyNames else filename

                            info = f"\r{' ' * 36}← {fquestion}"; TerminalWidth = get_terminal_size()[0]
                            if len(info) > TerminalWidth: info = info[0:TerminalWidth-3] + " .."
                            print(info, end='')

                            with open(fullpath, 'rb') as fp:
                                md5_hash = calc_md5_for(fp.read()).hexdigest()
                                md5log  += f"{fquestion}\n{md5_hash}\n"

                                print(f"\r   {md5_hash}", flush=True)
                                f_hashed += 1

                                md5log_alt += f"---\n  > {fquestion}\n\n    {md5_hash}\n"

                        except Exception as e: 
                            f_errors += 1
                            print(f"\r   {RED}{e}{ENDC}", flush=True)


    if f_hashed == 0: print(f"   Контрольные суммы не были составлены . . .{' ' * (get_terminal_size()[0] - 58)}")

    t_total = round(time() - t_start, 2)

    bordersize = ' ' * (23 + len(str(f_passed)))
    print(f"""
    ⌜{bordersize}⌝
      Файлов просмотрено:  {YELLOW}{f_passed}{ENDC}
      Файлов с хэшэм:      {GREEN }{f_hashed}{ENDC}
      Ошибок:              {RED   }{f_errors}{ENDC}

      Время: {ORANGE}{t_total} с{ENDC}.
    ⌞{bordersize}⌟
    """)

    if f_hashed > 0:

        md5log += "MD5LOG"

        while True:
            md5l_file = input(f" > Имя/Путь+имя сохраняемого файла с MD5 данными: {YELLOW}"); ec()

            if md5l_file == "*отмена": break

            elif '?' in md5l_file:

                print("   $ Сохранение Markdown-файла..", end='')
                md5l_file = md5l_file.split('?')[-1] + '.md'
                
                md5l = open(md5l_file, 'w', encoding='utf-8')
                md5l.write(md5log_alt), md5l.close()

                print(f"\r   $ {ORANGE}Файл{ENDC} {YELLOW}{path.abspath(md5l_file)}{ENDC} (Markdown) {ORANGE}сохранён.{ENDC}", flush=True)

            else:
                try:

                    print("   $ Сохранение файла..", end='')
                    md5l = open(md5l_file, 'w', encoding='utf-8')
                    md5l.write(md5log), md5l.close()

                    print(f"\r   $ {ORANGE}Файл{ENDC} {YELLOW}{path.abspath(md5l_file)} {ORANGE}сохранён.{ENDC}\n{'―' * get_terminal_size()[0]}\n", flush=True)
                    break

                except PermissionError : print(f"\r   $ {RED}Ошибка создания файла ({YELLOW}Нет разрешения{ENDC}).", flush=True)
                except OSError         : print(f"\r   $ {RED}Ошибка создания файла ({YELLOW}Имя файла не должно содержать специальные символы{ENDC}).", flush=True)
                except Exception as e  : print(f"\r   $ {RED}Ошибка создания файла ({YELLOW}{e}{ENDC}).", flush=True)


def MD5_Search(InputFolder):
    global Ignored

    InputFolder = path.abspath(InputFolder)

    t_start = time()

    f_founds = 0
    f_passed = 0
    f_errors = 0

    founded_log = f'```{date.today()} {datetime.now().strftime("%H:%M:%S")} | {md5_data_file} >> {path.abspath(InputFolder)}```\n\n'

    print(f"\n    $ {ORANGE}Выбранная для поиска папка: {YELLOW}{InputFolder}; {ORANGE}Файл с MD5 данными: {YELLOW}{path.abspath(md5_data_file)}{ENDC}.")

    print("\r    $ Подсчёт количества файлов в выбранном каталоге..", end='')
    f_count_total = sum(len(files) for root, dirs, files in walk(InputFolder))
    f_count_inlog = int(len(md5log_IMPORTED) / 2)

    print(f"\r    $ События:{' ' * 40}", flush=True)

    for filefolder, dirs, files in walk(InputFolder):
        for filename in files:

            fullpath    = f"{filefolder}\\{filename}"
            filesize_mb = path.getsize(fullpath) / (1024*1024)

            Ignored = False
            if len(IgnoreFolders) > 0: CheckIgnore(filefolder)

            searching = f"\r    $ Поиск по списку MD5 данных в выбранной папке: {f_passed}/{f_count_total} {filename if OnlyNames else fullpath}"
            TerminalWidth = get_terminal_size()[0]; searching += ' ' * (TerminalWidth - len(searching))
            if len(searching) > TerminalWidth: searching = searching[0:TerminalWidth-3] + " .."
            print(searching, end='', flush=True)

            if filename != "desktop.ini":

                if AllfoundToggle:
                    if f_founds == f_count_inlog:
                        break

                f_passed += 1

                if not Ignored:
                    if IgnoreFilesize_Min < filesize_mb < IgnoreFilesize_Max:

                        try:

                            with open(fullpath, 'rb') as fp:
                                curr_md5_hash = calc_md5_for(fp.read()).hexdigest()

                            if curr_md5_hash in md5log_IMPORTED:
                                md5log_IMPORTED_founded_md5index = md5log_IMPORTED.index(curr_md5_hash)

                                if md5log_IMPORTED_founded_md5index % 2 != 0:
                                    md5log_IMPORTED_founded_md5      = md5log_IMPORTED[md5log_IMPORTED_founded_md5index]
                                    md5log_IMPORTED_founded_filename = md5log_IMPORTED[md5log_IMPORTED_founded_md5index - 1]
                                    
                                    if not CopyDelToggle:

                                        f_founds += 1; print(f"\r      {GREEN}Найден: {md5log_IMPORTED_founded_filename}{ENDC} (MD5:{md5log_IMPORTED_founded_md5}) как {YELLOW}{fullpath}{ENDC}", flush=True)

                                        founded_log += f"---\n  > {md5log_IMPORTED_founded_filename}\n\n    {fullpath}\n"
                                        
                                    else: 
                                        print(f"\r      Копия объекта {YELLOW}{md5log_IMPORTED_founded_filename}{ENDC} ({ORANGE}{fullpath}{ENDC}) {ORANGE}отправлена в корзину.{ENDC}", flush=True)
                                        
                                        send2trash(fullpath)
                                        f_founds += 1


                        except Exception as e: 
                            f_errors += 1
                            print(f"\r      {RED}Ошибка: {filename}{ENDC}: {YELLOW}{e}{ENDC}", flush=True)


    TerminalWidth = get_terminal_size()[0]
    if f_founds == 0: print(f"\r{' ' * TerminalWidth}\n\r      Ничего не найдено . . .{' ' * (TerminalWidth - 29)}\n\n    $ {ORANGE}Поиск по списку MD5 данных в выбранной папке завершён.{ENDC}{' ' * (TerminalWidth - 60)}", flush=True)
    else: print(f"\r    $ {ORANGE}Поиск по списку MD5 данных в выбранной папке завершён.{ENDC}{' ' * (TerminalWidth - 60)}", flush=True)

    t_total = round(time() - t_start, 2)

    if len(str(f_count_inlog) + str(f_founds)) + 1   <   len(str(f_passed)):   bordersize = ' ' * ( 23 + len(str(f_passed)) )
    else: bordersize = ' ' * ( 23 + len(str(f_count_inlog) + str(f_founds)) + 1 )

    print(f"""
       ⌜{bordersize}⌝
         Файлов просмотрено:  {YELLOW}{f_passed}{ENDC}
         {'Файлов найдено:' if not CopyDelToggle else 'Копий удалено: '}      {GREEN }{f_founds}/{f_count_inlog}{ENDC}
         Ошибок:              {RED   }{f_errors}{ENDC}

         Время: {ORANGE}{t_total} с{ENDC}.
       ⌞{bordersize}⌟
    """)

    if f_founds > 0 and not CopyDelToggle:
        while True:
            founded_log_file = input(f"    > Имя/Путь+имя Markdown-лога найденных файлов: {YELLOW}"); ec()

            if founded_log_file == "*отмена": break

            else:
                try:
                    
                    print("    $ Сохранение файла..", end='')
                    founded_log_file += '.md'

                    md5l = open(founded_log_file, 'w', encoding='utf-8')
                    md5l.write(founded_log), md5l.close()
                    
                    print(f"\r    $ {ORANGE}Файл {YELLOW}{path.abspath(founded_log_file)}{ENDC} (Markdown) {ORANGE}сохранён.{ENDC}", flush=True)
                    break

                except PermissionError : print(f"\r    $ {RED}Ошибка создания файла ({YELLOW}Нет разрешения{ENDC}).", flush=True)
                except OSError         : print(f"\r    $ {RED}Ошибка создания файла ({YELLOW}Имя файла не должно содержать специальные символы{ENDC}).", flush=True)
                except Exception as e  : print(f"\r    $ {RED}Ошибка создания файла ({YELLOW}{e}{ENDC}).", flush=True)

    print(f"{'―' * get_terminal_size()[0]}\n")





if __name__ == "__main__":

    print("\n(1)Составить контрольные суммы файлов | (2)Найти файлы по данным контрольной суммы | (3)Выйти")

    while True:

        while CurrentInput != op[0:2]:
            CurrentInput = input(f"> {YELLOW}"); ec()

            if CurrentInput == op[0]:
                while True:
                    s = 0
                    InputFolder = input(f" > Папка с файлами: {YELLOW}"); ec()


                    if '*' in InputFolder:
                        if   InputFolder ==  '*назад'   : break
                        elif InputFolder ==  '*имена'   : OnlyNames = True ; print(f"   $ {ORANGE}Только имена файлов.{ENDC}")
                        elif InputFolder ==  '*полные'  : OnlyNames = False; print(f"   $ {ORANGE}Полные пути ко всем файлам.{ENDC}")
                        elif InputFolder == '*очистить' : ClearIgnore()

                        else: IgnoreFolders_Set(InputFolder)

                    elif '>' or '<' in InputFolder: IgnoreFilesize_Set(InputFolder)

                    if not '*' in InputFolder and not '>' in InputFolder and not '<' in InputFolder:
                        if path.isdir(InputFolder): MD5_Calculate(InputFolder)
                        else: print(f"   $ {RED}Каталог не найден.{ENDC}")

            elif CurrentInput == op[1]:
                OnlyNamesOldState = OnlyNames
                OnlyNames = True

                while True:
                    md5_data_file = input(f" > Файл с MD5 данными: {YELLOW}"); ec()

                    if path.isfile(md5_data_file):

                        with open(md5_data_file, encoding='utf-8') as md5log_file:
                            md5log_IMPORTED = [row.strip() for row in md5log_file]
                        
                            
                        if md5log_IMPORTED[-1] == "MD5LOG": 
                            md5log_IMPORTED.pop(-1)
                            print(f"   $ {ORANGE}Импортирован: {YELLOW}{path.abspath(md5_data_file)}{ENDC}")
                            
                            while True:
                                s = 1
                                InputFolder = input(f"{f'  > Папка с файлами для поиска: {YELLOW}' if not CopyDelToggle else f'  > {ORANGE}*copydel{ENDC} Папка с файлами для удаления копий: {YELLOW}'}"); ec()

                                if '*' in InputFolder:
                                    if   InputFolder ==  '*назад'   : break
                                    elif InputFolder ==  '*имена'   : OnlyNames = True ; print(f"   $ {ORANGE}Только имена файлов.{ENDC}")
                                    elif InputFolder ==  '*полные'  : OnlyNames = False; print(f"   $ {ORANGE}Полные пути ко всем файлам.{ENDC}")
                                    elif InputFolder == '*очистить' : ClearIgnore()
                                    
                                    elif InputFolder == '*allfound':   
                                        AllfoundToggle = False if AllfoundToggle else True
                                        print(f"    $ {ORANGE}{'Заканчивать поиск в папке после нахождения всех объектов из импортированного списка' if AllfoundToggle else 'Продолжать искать объекты несмотря на их количество в импортированном списке и количество найденных'}.{ENDC}")                               

                                    elif InputFolder == '*copydel':
                                        CopyDelToggle = False if CopyDelToggle else True
                                        if CopyDelToggle: AllfoundToggle = False
                                        print(f"    $ {ORANGE}{f'РЕЖИМ УДАЛЕНИЯ КОПИЙ (send2trash) {RED}Вкл{ENDC}; {ORANGE}(*allfound Выкл){ENDC}' if CopyDelToggle else f'РЕЖИМ УДАЛЕНИЯ КОПИЙ (send2trash) {GREEN}Выкл{ENDC}'}.\n")

                                    else: IgnoreFolders_Set(InputFolder)

                                elif '>' or '<' in InputFolder: IgnoreFilesize_Set(InputFolder)

                                if not '*' in InputFolder and not '>' in InputFolder and not '<' in InputFolder:
                                    if path.isdir(InputFolder): MD5_Search(InputFolder)
                                    else: print(f"   $ {RED}Каталог не найден.{ENDC}")

                        else: print(f"   $ {RED}Файл не содержит MD5 данные{ENDC} (Последней строкой должно быть {YELLOW}MD5LOG{ENDC})"); md5log_IMPORTED = ''


                    elif md5_data_file == "*назад": break
                    else: print(f"   $ {RED}Файл{ENDC} {YELLOW}{md5_data_file}{ENDC} {RED}не найден.{ENDC}")

                OnlyNames = OnlyNamesOldState


            elif CurrentInput == op[2]: ec(); exit()
