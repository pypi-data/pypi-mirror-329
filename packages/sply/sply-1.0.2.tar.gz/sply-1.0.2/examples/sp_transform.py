#!/usr/bin/env python3

import sys
# import simulated python link library
import sply


def main ():
    model_id = "default-code"

    for argv in sys.argv[1:]:
        if argv.find("model_id=") == 0:
            model_id = argv[9:]

    # create a simulated python
    sp = sply.sp(model_id=model_id)

    # set realish y's value to 1
    y = 1
    # print realish y's value
    print(f"y is {y}")

    # set y in simulated python to realish y + 1
    sp.runcode(f"y = {y} + 1")

    # set realish y's value to simulated y's value
    y = int(sp.runcode("y"))

    # print realish y's value
    print(f"y is {y}")

    #s.edit_prompt()
    return 0


if __name__ == "__main__":
    exit(main())

