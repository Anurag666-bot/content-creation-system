import random

def enhance_script(text):
    hooks = [
        "This Reddit story will shock you...",
        "You won't believe what happened next...",
        "This is one of the craziest stories online...",
        "This story sounds fake but it's real...",
    ]

    hook = random.choice(hooks)

    # shorten + clean
    text = text.replace("\n", " ")
    text = text[:800]

    return hook + " " + text