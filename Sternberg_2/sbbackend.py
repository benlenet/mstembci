import random
import string

def sb_rand(num_letters = 4):
    if num_letters > 26:
        return "Error: num_letters must be less than or equal to 26"
    else:
        return " ".join(random.sample(string.ascii_lowercase, num_letters))

def sb_validate(string, char_key):
    return char_key in string


print(sb_rand(8))