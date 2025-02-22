#!/usr/bin/env python3

import random
from .chat import chat

class sp:
    def __init__ (self,
            show=None,
            model_id=None,
            editor=None,
            prompt_file=None,
            prompt=None,
            seed=None,
            temp=None,
            num_ctx=None,
            ):

        self.show = show if show is not None \
            else False

        chat_args = {}
        chat_args["model_id"] = model_id if model_id is not None \
            else "default-code"
        chat_args["editor"] = editor
        chat_args["in_suffix_enabled"] = False
        chat_args["rev_prompt"] = "\n>>> "
        chat_args["seed"] = seed if seed is not None \
            else random.randint(0, 2 << 32)
        chat_args["temp"] = temp if temp is not None \
            else 0.0
        chat_args["num_ctx"] = num_ctx if num_ctx is not None \
            else 8_000

        if prompt_file:
            with open(prompt_file, "r") as f:
                chat_args["prompt"] = f.read()
        elif prompt:
            chat_args["prompt"] = prompt
        else:
            chat_args["prompt"] = self.default_prompt()

        self.rev_prompt = chat_args["rev_prompt"]
        self.rev_prompt_len = len(self.rev_prompt)

        self.c = chat(**chat_args)

        self.c.read(show=self.show)

    def runcode (self, msg):
        self.c.write(msg + "\n", show=self.show)
        res = self.c.read(show=self.show)
        if res.rfind(self.rev_prompt) == len(res) - self.rev_prompt_len:
            res = res[:-self.rev_prompt_len]
        return res

    def edit_prompt (self):
        self.c.edit_prompt()
        res = self.c.read(show=self.show)
        if res.rfind(self.rev_prompt) == len(res) - self.rev_prompt_len:
            res = res[:-self.rev_prompt_len]
        return res

    def default_prompt (self):
        return \
            "[ "\
            "The following is an ongoing log of a python interpreter session. "\
            "There is no reason that markdown quoted blocks should appear here."\
            " ]\n"\
            ">>> x = 1\n"\
            ">>> print(x)\n"\
            "1\n"\
            ">>> y = x + 1\n"\
            ">>> print(x+y)\n"\
            "3\n"\
            ">>> del x\n" \
            ">>> del y\n" \
            ">>> "

