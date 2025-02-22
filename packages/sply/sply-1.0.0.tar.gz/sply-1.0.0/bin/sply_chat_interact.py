#!/usr/bin/env python3

import sys
import random
import sply

def print_cmds ():
    print("\n* commands:\n"
          "/?: this help\n"
          "/p: display prompt (surrounded by **'s)\n"
          "/i: print current input (surrounded by ***'s)\n"
          "/c: clear current input\n"
          "//: input /\\n\n"
          "/q: quit\n"
          "/e: edit prompt\n"
          "*")

def print_usage ():
    print(f"Usage: {sys.argv[0]} [options]\n"
          f"  where [options] are zero or more of:"
          )
    for arg in sply.chat.arg_desc:
        print(f"    {arg["name"]}=({arg["type"].__name__}): "
              f"{arg["desc"]} (default: \"{sply.chat.default_args[arg["name"]]}\")"
              )

def main ():
    chat_args = sply.chat.default_args.copy()

    for argv in sys.argv[1:]:
        if argv.find("--help") == 0:
            print_usage()
            exit(-1)
        for arg in sply.chat.arg_desc:
            name = arg["name"]
            name_len_p1 = len(name) + 1
            tp = arg["type"]
            if argv.find(name + "=") == 0:
                if tp == str:
                    chat_args[name] = argv[name_len_p1:]
                elif tp == bool:
                    chat_args[name] = True if argv[name_len_p1:] == "True" else False
                elif tp == int:
                    chat_args[name] = int(argv[name_len_p1:])
                elif tp == float:
                    chat_args[name] = float(argv[name_len_p1:])

    print("chat_args = ", end="")
    print(chat_args)

    c = sply.chat(**chat_args)

    print("")
    print(c.prompt, end="", flush=True)

    running_ = True
    while running_:
        c.read(show=True)

        add = ""
        while True:
            inp = input()
            if not inp:
                add += "\n"
                break
            elif inp[0] == "/" and len(inp) == 2:
                if inp == "/?":
                    print_cmds()
                    continue
                elif inp == "/p":
                    print("**" + c.prompt + "**")
                    continue
                elif inp == "/i":
                    print("***" + add + "***")
                    continue
                elif inp == "/c":
                    add = ""
                    continue
                elif inp == "//":
                    inp = "/\n"
                    break
                elif inp == "/q":
                    running_ = False
                    break
                elif inp == "/e":
                    c.edit_prompt()
                    add = ""
                    break
                else:
                    print_cmds()
                    continue

            inp_tail = len(inp) - 1
            if inp[inp_tail] == "\\":
                add += inp[:inp_tail] + "\n"
            else:
                add += inp + "\n"
                break
            # end while True

        if not running_:
            break

        if add:
            c.write(add)
            if in_suffix_enabled:
                print(c.in_suffix, end="", flush=True)
        # end while running_
    return 0

if __name__ == "__main__":
    exit(main())

