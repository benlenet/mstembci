import random
import string



# return a character for response stimulus
def gen_key(string_prompt, correct_rate = 0.5):
    trunc_chars = str.maketrans('', '', string_prompt)
    trunc_string = string.ascii_lowercase.translate(trunc_chars)
    valid_string = string_prompt.replace(" ", "")
    print("string pruned is", trunc_string)
    return random.choice(trunc_string) if correct_rate < random.random() else random.choice(valid_string)
    

# generate list of characters for encoding, must be stored for checking validity in sb_validate
def sb_rand(num_letters = 4):
    if num_letters > 26:
        return "Error: num_letters must be less than or equal to 26"
    else:
        return " ".join(random.sample(string.ascii_lowercase, num_letters))

# supply string_prompt and char_key to check if the key is valid
def sb_validate(string_prompt, char_key):
    return char_key in string_prompt

# after supplying sb_rand to the stimulus, run gen_key to generate a key.
# then run sb_validate to check if the key is valid. If sb_validate returns True,
# use bool response to display correct/incorrect response.
def input_val(validation, correct_key = ',', incorrect_key = '.'):
        return correct_key if validation else incorrect_key
    

# 
def testrun():
    prompty_dompt = sb_rand()
    key_prompty = gen_key(prompty_dompt)
    results = sb_validate(prompty_dompt, key_prompty)
    print("list of characters are",prompty_dompt)
    print("key generated is",key_prompty)
    print("is valid:", results)
    return results

def testrunloop():
    # check if correct response works
    valid_rate = 0
    for i in range(1_000):
        print("Test run", i+1)
        if testrun():
            valid_rate += 1
    print("Valid rate is", valid_rate / 1000 * 100, "%")  # print as percentage


# variables necessary in PsychoPy for stimulus generation
string_prompt = sb_rand()  # example string prompt
key_prompt = gen_key(string_prompt) # example key prompt
map_correct = input_val(sb_validate(string_prompt, key_prompt)) # example mapping
print("promped", string_prompt, "key given is", key_prompt, "correct button is", map_correct)
is_true = sb_validate(string_prompt, key_prompt) # example validation
