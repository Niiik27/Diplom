import inspect
import os
import re


class Print:
    def __init__(self):
        pass

    @staticmethod
    def del_private_members(fields_dict):
        return [x for x in fields_dict if not str(x).startswith("_")]

    @staticmethod
    def root_path():
        return (__file__[:__file__.rfind("\\")])

    __print_log = False
    __color = 0
    __black_color = 30
    __red_color = 31
    __green_color = 32
    __yellow_color = 33
    __blue_color = 34
    __purpur_color = 35
    __marine_color = 36
    __gray_color = 37
    __white_color = 38
    __reset_style = 0
    __bold = 1
    __thin = 2
    _italic = "\033[3m"
    _not_italic = ""
    __italic = _not_italic
    __underline = 4
    __swap = 7
    __log_path = __file__[:__file__.rfind("\\") + 1] + "\\print_log.html"
    __IDX = 1

    @staticmethod
    # @property
    def qwe(text=''):
        txt = '********* DBG:' + text + ' ' + str(Print.__IDX) + ' *********'
        Print.red(txt)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))
        Print.__IDX += 1

    @staticmethod
    def color_mark(code_color):
        if Print.__color != code_color:
            txt_color = "WHITE"
            match code_color:
                case Print.__black_color:
                    txt_color = "BLACK"
                case Print.__red_color:
                    txt_color = "RED"
                case Print.__green_color:
                    txt_color = "GREEN"
                case Print.__yellow_color:
                    txt_color = "YELLOW"
                case Print.__blue_color:
                    txt_color = "BLUE"
                case Print.__purpur_color:
                    txt_color = "PURPUR"
                case Print.__marine_color:
                    txt_color = "MARINE"
                case Print.__gray_color:
                    txt_color = "GRAY"
            Print.__color = code_color
            color = f"\033[{Print.__color}m"
            reset = f"\033[{Print.__reset_style}m"
            bold = f"\033[{Print.__bold}m"
            print(f"{color}{bold}[{txt_color}]:{reset}")
    @staticmethod
    def red(*args, **kwargs):
        Print.color_mark(Print.__red_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def yellow(*args, **kwargs):
        Print.color_mark(Print.__yellow_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def blue(*args, **kwargs):
        Print.color_mark(Print.__blue_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def green(*args, **kwargs):
        Print.color_mark(Print.__green_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def black(*args, **kwargs):
        Print.color_mark(Print.__black_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def purpur(*args, **kwargs):
        Print.color_mark(Print.__purpur_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def marine(*args, **kwargs):
        Print.color_mark(Print.__marine_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def gray(*args, **kwargs):
        Print.color_mark(Print.__gray_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    @staticmethod
    def white(*args, **kwargs):
        Print.color_mark(Print.__white_color)
        Print.__print(*args, **kwargs)
        print('')
        if Print.__print_log:
            with open(Print.__log_path, 'a') as f:
                f.write(Print.build_html_string(''))

    # "{'e': 'ACCOUNT_UPDATE', 'T': 1662998400163, 'E': 1662998400223, 'a': {'B': [{'a': 'USDT', 'wb': '2939.93450056',
    # 'cw': '2939.93450056', 'bc': '-0.79611757'}], 'P': [], 'm': 'FUNDING_FEE'}}"
    @staticmethod
    def reds(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.red(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.red(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.red(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.red(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def yellows(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.yellow(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.yellow(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.yellow(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.yellow(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def blues(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.blue(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.blue(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.blue(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.blue(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def greens(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.green(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.green(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.green(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.green(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def blacks(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.black(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.black(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.black(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.black(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def purpurs(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.purpur(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.purpur(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.purpur(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.purpur(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def marines(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.marine(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.marine(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.marine(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.marine(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def grays(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.gray(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.gray(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.gray(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.gray(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def whites(*args, **kwargs):
        for i in args:
            if type(i) == list or type(i) == tuple or type(i) == set or type(i) == range or type(i
                                                                                                 ) == dict or type(
                i) == int or type(i) == float or type(i) == bool or type(i
                                                                         ) == complex or type(i) == str or i is None:
                Print.white(type(i).__name__ + ":\n" + str(i))
            elif i != 'root':
                try:
                    fields = i.__dict__
                    Print.white(type(i).__name__ + ":\n" + str(fields))
                except AttributeError:
                    pass
        for i in kwargs:
            if type(kwargs[i]) == list or type(kwargs[i]) == tuple or type(kwargs[i]) == set or type(
                    kwargs[i]) == range or type(kwargs[i]
                                                ) == dict or type(kwargs[i]) == int or type(kwargs[i]) == float or type(
                kwargs[i]) == bool or type(kwargs[i]
                                           ) == complex or type(kwargs[i]) == str or kwargs[i] is None:
                Print.white(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(kwargs[i]))
            elif kwargs[i] != 'root':
                try:
                    fields = kwargs[i].__dict__
                    Print.white(i + " (" + type(kwargs[i]).__name__ + "):\n" + str(fields))
                except AttributeError:
                    pass

    @staticmethod
    def build_html_string(txt):
        html_color = "A9A9A9"
        if Print.__color == Print.__black_color:
            html_color = "000000"
        elif Print.__color == Print.__red_color:
            html_color = "eb5252"
        elif Print.__color == Print.__green_color:
            html_color = "52eb73"
        elif Print.__color == Print.__blue_color:
            html_color = "1E90FF"
        elif Print.__color == Print.__yellow_color:
            html_color = "e0e330"
        elif Print.__color == Print.__purpur_color:
            html_color = "de3ae0"
        elif Print.__color == Print.__marine_color:
            html_color = "65ebd2"
        elif Print.__color == Print.__gray_color:
            html_color = "888888"
        elif Print.__color == Print.__white_color:
            html_color = "EEEEEE"
        return f"<p style=\"margin-left: 50px; color:#{html_color};font-size:14px;font-family:'Comic Sans MS', cursive\">" + txt + "</br></p>\n"

    @staticmethod
    def varname(p):
        for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
            m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
            if m:
                return m.group(1)

    @staticmethod
    def __print(*args, **kwargs):
        color = f"\033[{Print.__color}m"
        reset = f"\033[{Print.__reset_style}m"
        bold = f"\033[{Print.__bold}m"
        italic = Print.__italic
        match Print.__color:
            case Print.__black_color:
                f"{color}{bold}[BLACK]:{reset}"
            case Print.__red_color:
                f"{color}{bold}[RED]:{reset}"
            case Print.__green_color:
                f"{color}{bold}[GREEN]:{reset}"
            case Print.__yellow_color:
                f"{color}{bold}[YELLOW]:{reset}"
            case Print.__blue_color:
                f"{color}{bold}[BLUE]:{reset}"
            case Print.__purpur_color:
                f"{color}{bold}[PURPUR]:{reset}"
            case Print.__marine_color:
                f"{color}{bold}[MARINE]:{reset}"
            case Print.__gray_color:
                f"{color}{bold}[GRAY]:{reset}"
            case Print.__white_color:
                f"{color}{bold}[WHITE]:{reset}"





        if not os.path.exists(Print.__log_path):
            with open(Print.__log_path, 'a') as f:
                f.write("<body bgcolor=\"#272727\">\n")

        if len(args) > 0:

            for i in args:
                if type(i) == dict:
                    for n in i:
                        val = i.get(n)

                        if type(val) == list or type(val) == tuple or type(val) == set or type(val) == range:
                            # print('')
                            print(f"{color}{bold}{italic}[{n}]:{reset}")
                            if Print.__print_log:
                                with open(Print.__log_path, 'a') as f:
                                    f.write(Print.build_html_string(''))
                                    f.write(Print.build_html_string(f"[{n}]:"))

                            Print.__print(val)
                        elif type(val) == dict:
                            # print()
                            print(f"{color}{bold}{italic}{{{n}}}:{reset}")
                            if Print.__print_log:
                                with open(Print.__log_path, 'a') as f:
                                    f.write(Print.build_html_string(''))
                                    f.write(Print.build_html_string(f"{{{n}}}:"))
                            Print.__print(val)
                        elif type(val) == int or type(val) == float or type(val) == bool or type(
                                val) == complex or val is None:
                            print(f"{color}{bold}{italic}{n}:{reset} {color}{italic}{val}{reset}")
                            if Print.__print_log:
                                with open(Print.__log_path, 'a') as f:
                                    f.write(Print.build_html_string(f"{n}: {val}"))
                        elif type(val) == str:
                            # print()
                            print(f"{color}{bold}{italic}{n}:{reset} {color}{italic}\"{val}\"{reset}")
                            if Print.__print_log:
                                with open(Print.__log_path, 'a') as f:
                                    f.write(Print.build_html_string(f"{n}: \"{val}\""))
                        else:
                            if n != 'root':
                                # print("Вход2")
                                print()
                                try:
                                    fields = dict(val.__dict__)
                                    # print(val.__class__.__name__)
                                    # print(n)
                                    Print.__italic = Print._not_italic
                                    italic = Print.__italic
                                    members = Print.del_private_members(dir(val))
                                    print(f"{color}{italic}{bold}Fields of obj ({val.__class__.__name__}):{reset}")
                                    if Print.__print_log:
                                        with open(Print.__log_path, 'a') as f:
                                            f.write(
                                                Print.build_html_string(f"Fields of obj ({val.__class__.__name__}):"))
                                            f.write(
                                                Print.build_html_string(f"Fields of obj ({val.__class__.__name__}):"))
                                            f.write(Print.build_html_string(f"({str(members)}):"))
                                    Print.__print(fields)
                                    Print.__italic = Print._italic
                                    italic = Print.__italic
                                    print(f"{color}{italic}{bold}{n}: obj ({val.__class__.__name__}) Methods:{reset}")
                                    Print.__print(Print.del_private_members(dir(val)))
                                    Print.__italic = Print._not_italic
                                    italic = Print.__italic


                                except BaseException:
                                    Print.__italic = Print._italic
                                    italic = Print.__italic
                                    members = Print.del_private_members(dir(val))
                                    print(f"{color}{italic}{bold}{n}: obj ({val.__class__.__name__}) Methods:{reset}")
                                    if Print.__print_log:
                                        with open(Print.__log_path, 'a') as f:
                                            f.write(
                                                Print.build_html_string(f"Fields of obj ({val.__class__.__name__}):"))
                                            f.write(Print.build_html_string(f"({str(members)}):"))
                                    Print.__print(Print.del_private_members(dir(val)))
                                    Print.__italic = Print._not_italic
                                    italic = Print.__italic

                    # print('')
                    if Print.__print_log:
                        with open(Print.__log_path, 'a') as f:
                            f.write(Print.build_html_string(''))
                elif type(i) == int or type(i) == float or type(i) == bool or type(i) == complex or i is None:
                    print(f"{color}{italic}{i}{reset}")
                    if Print.__print_log:
                        with open(Print.__log_path, 'a') as f:
                            f.write(Print.build_html_string(f"{i}"))
                elif type(i) == str:
                    print(f"{color}{italic}\"{i}\"{reset}")
                    if Print.__print_log:
                        with open(Print.__log_path, 'a') as f:
                            f.write(Print.build_html_string(f"\"{i}\""))
                elif type(i) == list or type(i) == tuple or type(i) == set or type(i) == range:
                    # print(f"\033[{color}m [", end='', file = Print.__print_file)
                    for n in i:
                        Print.__print(n)
                    # print(f"\033[{color}m]", file = Print.__print_file)
                else:
                    # print("Вход")
                    try:
                        fields = dict(i.__dict__)
                        Print.__italic = Print._not_italic
                        italic = Print.__italic
                        print(f"{color}{italic}{bold}Fields of CLASS ({i.__class__.__name__}):{reset}")
                        members = Print.del_private_members(dir(i))
                        if Print.__print_log:
                            with open(Print.__log_path, 'a') as f:
                                f.write(Print.build_html_string(f"Fields of CLASS ({i.__class__.__name__}):{reset}"))
                                f.write(Print.build_html_string(f"Fields of CLASS ({i.__class__.__name__}):{reset}"))
                                f.write(Print.build_html_string(f"Fields of CLASS ({str(members)}):{reset}"))
                        Print.__print(fields)
                        Print.__italic = Print._italic
                        italic = Print.__italic
                        print(f"{color}{italic}{bold}Methods of obj ({i.__class__.__name__}):{reset}")
                        Print.__print(members)
                        Print.__italic = Print._not_italic
                        italic = Print.__italic

                    except AttributeError:
                        Print.__italic = Print._italic
                        italic = Print.__italic
                        print(f"{color}{italic}{bold}obj ({i.__class__.__name__}) Methods:{reset}")
                        members = Print.del_private_members(dir(i))
                        if Print.__print_log:
                            with open(Print.__log_path, 'a') as f:
                                f.write(Print.build_html_string(f"CLASS ({i.__class__.__name__}) Fields:{reset}"))
                                f.write(Print.build_html_string(f"CLASS ({str(members)}) Fields:{reset}"))
                        Print.__print(members)
                        Print.__italic = Print._not_italic
                        italic = Print.__italic

                        # Print.del_privat_members(dir(i))

        if len(kwargs) > 0:
            for n in kwargs:
                val = kwargs.get(n)
                # print(f"\033[{color}m [{n}]:", file = Print.__print_file)
                if type(val) == dict:
                    print(f"{color}{italic}{bold}{{{n}}}:{reset}")
                    if Print.__print_log:
                        with open(Print.__log_path, 'a') as f:
                            f.write(Print.build_html_string(f"{{{n}}}:"))
                    Print.__print(val)
                elif type(val) == list or type(val) == tuple or type(val) == set or type(val) == range:
                    print(f"{color}{bold}{italic}[{n}]:{reset}")
                    if Print.__print_log:
                        with open(Print.__log_path, 'a') as f:
                            f.write(Print.build_html_string(f"[{n}]:"))
                    Print.__print(val)
                elif type(val) == int or type(val) == float or type(val) == bool or type(val) == complex or val is None:
                    # print(f"\033[{color}m {n}: {val}", file = Print.__print_file)
                    print(f"{color}{bold}{italic}{n}:{reset} {color}{italic}{val}{reset}")
                    if Print.__print_log:
                        with open(Print.__log_path, 'a') as f:
                            f.write(Print.build_html_string(f"{n}: {val}"))
                elif type(val) == str:
                    print(f"{color}{bold}{italic}{n}:{reset} {color}{italic}\"{val}\"{reset}")
                    if Print.__print_log:
                        with open(Print.__log_path, 'a') as f:
                            f.write(Print.build_html_string(f"{n}: \"{val}\""))
                else:
                    if n != 'root':
                        try:
                            fields = dict(val.__dict__)
                            Print.__italic = Print._not_italic
                            italic = Print.__italic
                            print(
                                f"{color}{color}{italic}{n} {reset}{color}{italic}({val.__class__.__name__}) Fields:{reset}")
                            members = Print.del_private_members(dir(i))
                            if Print.__print_log:
                                with open(Print.__log_path, 'a') as f:
                                    f.write(Print.build_html_string(f"{n} ({val.__class__.__name__}) Fields:"))
                                    f.write(Print.build_html_string(f"{n} ({val.__class__.__name__}) Methods:"))
                                    f.write(Print.build_html_string(f"{n} ({str(members)}):"))
                            Print.__print(fields)
                            Print.__italic = Print._italic
                            italic = Print.__italic
                            print(f"{color}{italic}{bold}{n} obj ({i.__class__.__name__})Methods:{reset}")
                            Print.__print(members)
                            Print.__italic = Print._not_italic
                        except AttributeError:
                            Print.__italic = Print._italic
                            italic = Print.__italic
                            print(f"{color}{italic}{bold}{n} obj ({i.__class__.__name__}) Methods:{reset}")
                            members = Print.del_private_members(dir(i))
                            if Print.__print_log:
                                with open(Print.__log_path, 'a') as f:
                                    f.write(Print.build_html_string(f"{n} ({val.__class__.__name__}) Methods:"))
                                    f.write(Print.build_html_string(f"{n} ({str(members)}):"))
                            Print.__print(members)
                            Print.__italic = Print._not_italic
