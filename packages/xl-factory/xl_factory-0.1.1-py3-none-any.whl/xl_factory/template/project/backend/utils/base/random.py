import random as random_, string as string_


def number(n):
    chars = string_.digits 
    s = [random_.choice(chars) for i in range(n)] 
    return ''.join(s)

def captcha(n):
    chars = '02345689'
    s = [random_.choice(chars) for i in range(n)] 
    return ''.join(s)

def string(n):
    chars = string_.ascii_letters + string_.digits 
    s = [random_.choice(chars) for i in range(n)] 
    return ''.join(s)


