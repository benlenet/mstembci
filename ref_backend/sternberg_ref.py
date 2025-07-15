# code_initfunction code block in intro routine
# using before experiment

import random
import string
import socket

# constants declaration
TIMEOUT_DURATION = 10
CHARACTER_INCREMENT = 2
DEFAULT_FEEDBACK = 1

# timing of each stimulus (global variables)
"""
dCross: duration of cross stimulus
dPrompt: duration of characters on screen
dBlank: duration of blank screen after cross
dResponse: duration of single character on screen (timeout)
dFb: duration of feedback (correct/incorrect)
"""
timing_map = {"dCross": 2,
              "dBlank": 1,
              "dPrompt": 1,
              "dResponse": 1,
              "dFb": 1,
              # start at high values of practice,
              # will change after 1st runtime
              "p_dCross": 5,
              "p_dBlank": 2,
              "p_dPrompt": 4,
              "p_dResponse": 1,
              "p_dFb": 2
              }

# stimulus text, feedback, and loop count
# before each cycle, update each variable
# string_prompt: stimulus display
# key_prompt: key selected to display
# map_correct: button press validation
# loop_iter: used to keep track of loops
# loop_count: set max loop count
# cross_en: keep track of fixation period

stim_map = {"loop_iter": 0,
                "loop_count": 3,
                "loop_maxcount": 9,
                "char_length": 3,
                "string_prompt": "",
                "key_prompt": "",
                "map_correct": None,
                "cross_en": False,
                "instruction_text": "",
                "iter_text_list": 0,
                "p_loop_maxcount": 6,
                "p_loop_count": 2
                }

text_list = ["+", 
             "b y g d f",
             "",
             "g",
             "*feedback*",
             "We will now begin the practice trial."]
# variables to move text
loopcount_text_list = len(text_list)
# ensure it is initialized (bruh)
stim_map["instruction_text"] = text_list[stim_map["iter_text_list"]]



# initialize udp connection to MATLAB
UDP_IP = "127.0.0.1"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# UDP int values, sent to MATLAB
udp_map = {"fixation": bytes([1]),
           "encoding": bytes([2]),
           "maintenance": bytes([3]),
           "retrieval": bytes([4])}

# send value to UDP Port, mapped via udp_map
def matlab_send(stage):
    if stage in udp_map:
        sock.sendto(udp_map[stage], (UDP_IP, UDP_PORT))

# return a character for response stimulus
def gen_key(string_prompt, correct_rate = 0.5):
    trunc_chars = str.maketrans('', '', string_prompt)
    trunc_string = string.ascii_lowercase.translate(trunc_chars)
    valid_string = string_prompt.replace(" ", "")
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
def input_val(validation, correct_key = 'period', incorrect_key = 'comma'):
        return correct_key if validation else incorrect_key

"""
these changes are made to switch from a button press to a mouse click
"""
mouse_map = {"left":  [1, 0, 0],
             "right": [0, 0, 1],
             "middle": [0, 1, 0],
             "none": [0, 0, 0]}

def input_val(validation, correct_key = [1, 0, 0], incorrect_key = [0, 0, 1]):
        return correct_key if validation else incorrect_key
try:
    if mouse.getPressed() == mouse_map["none"]:
        # add timeout text, decrement loop, enable fixation
        fb_text = 'please respond within a shorter time period.\nPress any key to continue.'
        timing_map["dFb"] = TIMEOUT_DURATION
        fb_col = 'white'
        stim_map["loop_iter"] -= 1
        stim_map["cross_en"] = False
    elif mouse.getPressed() == stim_map["map_correct"]:
        fb_text = 'Correct!'
        fb_col = 'green'
    else:
        fb_text = 'Incorrect'
        fb_col = 'red'
except:
    print("fb not accurately recorded.")

# located in eachframe for button_record and intro
if mouse_fb.getPressed() == mouse_map["middle"]:
    continueRoutine = False
    break
# remember to add mouse_fb, mouse_intro, and mouse to button_record, intro, and response  

# make sure all text boxes are initialized!
intro_disp_text = "Hello! Thank you for participating in the Sternberg Working Memory Task."
intro_small_text = "Please wait for the experimenter to continue."
maintrial_text = "The main experiment will now begin. Please press any key to begin."

# code_textshift code block in instruction_page routine
# using end routine

# go to next text 

stim_map["iter_text_list"] += 1
if stim_map["iter_text_list"] != loopcount_text_list:
    print("now on text", stim_map["iter_text_list"], "\n")
    stim_map["instruction_text"] = text_list[stim_map["iter_text_list"]]


# p_codeinit code block in p_code_init routine
# using begin routine

# initialize values in map
stim_map["string_prompt"] = sb_rand(stim_map["char_length"])
stim_map["key_prompt"] = gen_key(stim_map["string_prompt"])
stim_map["map_correct"] = input_val(sb_validate(stim_map["string_prompt"],
                                      stim_map["key_prompt"]))
if stim_map["char_length"] == 3: 
    p_cross_text = "focus on the cross"
    p_string_prompt_text = "memorize these characters"
else:
    p_cross_text = ""
    p_string_prompt_text = ""

print("string prompt is", stim_map["string_prompt"], "\n",
      "key prompt is", stim_map["key_prompt"], "\n",
      "button to indicate correct is", stim_map["map_correct"], "\n")


# p_code_crossen code block in p_cross_fix routine
# using end routine


# set in routine to skip if cross_en == True
stim_map["cross_en"] = True
timing_map["p_dCross"]

# p_code_fb code block in p_button_record routine
# using begin routine



# display feedback to log
print(p_key_resp.keys,"was pressed\n")


p_timing_shift_text = ""

try:
    if p_key_resp.keys == None:
        # add timeout text, decrement loop, enable fixation
        fb_text = 'please respond within a shorter time period.\nPress any key to continue.'
        fb_col = 'white'
        # add duration for user to pause/orient
        timing_map["p_dFb"] = TIMEOUT_DURATION
        # adjust loop values
        stim_map["loop_iter"] -= 1
        # reenable cross
        stim_map["cross_en"] = False
    elif p_key_resp.corr:
        fb_text = 'Correct!'
        fb_col = 'green'
    else:
        fb_text = 'Incorrect'
        fb_col = 'red'        
except:
    print('Make sure that you have:\n1. a routine with a keyboard component in it called "key_resp"\n 2. In the key_Resp component in the "data" tab select "Store Correct".\n in the "Correct answer" field use "$corrAns" (where corrAns is a column header in your conditions file indicating the correct key press')


# increment loop, enable cross if loop reaches max
stim_map["loop_iter"] += 1
if ((stim_map["char_length"] == 3) and (stim_map["loop_iter"] == 2)):
    p_timing_shift_text = "the stimulus will now speed up"


# p_code_fb code block in p_button_record routine
# using end routine



# print after displaying things
# display loop information 
print("loop_iter =", stim_map["loop_iter"], '\n',
      "p_loop_count =", stim_map["p_loop_count"], '\n')




# ensure that fb is reset to 1, clear prompting text
timing_map["p_dFb"] = DEFAULT_FEEDBACK
p_cross_text = ""
p_string_prompt_text = ""
# set different timings after 
if ((stim_map["char_length"] == 3) and (stim_map["loop_iter"] == 2)):
    timing_map["p_dCross"] = 5
    timing_map["p_dBlank"] = 2
    timing_map["p_dPrompt"] = 1
    timing_map["p_dResponse"] = 1
    timing_map["p_dFb"] = 3

# increment characters after specified loop count
if stim_map["loop_iter"] == stim_map["p_loop_count"]:
    stim_map["loop_iter"] = 0
    stim_map["char_length"] += CHARACTER_INCREMENT
    stim_map["cross_en"] = False

# print out trial information for debugging
print("timing information is: \n")
print("timing_map[\"p_dCross\"]:", timing_map["p_dCross"])
print("timing_map[\"p_dBlank\"]:", timing_map["p_dBlank"])
print("timing_map[\"p_dPrompt\"]:", timing_map["p_dPrompt"])
print("timing_map[\"p_dResponse\"]:", timing_map["p_dResponse"])
print("timing_map[\"p_dFb\"]:", timing_map["p_dFb"])
print("current loop that ended is:", currentLoop.thisTrial)

# rewind trial to overwrite timeout data
if p_key_resp.keys == None:
    currentLoop.rewindTrials()