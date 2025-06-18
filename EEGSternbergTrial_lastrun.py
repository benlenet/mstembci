#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on June 18, 2025, at 12:12
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

import psychopy
psychopy.useVersion('2024.2.4')


# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from code_initfunction
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


# make sure all text boxes are initialized!
intro_disp_text = "Hello! Thank you for participating in the Sternberg Working Memory Task."
intro_small_text = "Please wait for the experimenter to continue."
maintrial_text = "The main experiment will now begin. Please press any key to begin."

# initialize logging function


# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'EEGSternberg'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1920, 1080]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\e203gtec\\Desktop\\mstembci\\EEGSternbergTrial_lastrun.py',
        savePickle=True, saveWideText=False,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    thisExp.setPriority('', )
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb',
            backgroundImage='', backgroundFit='fill',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [-1.0000, -1.0000, -1.0000]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'fill'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='initializing screen!')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_nex') is None:
        # initialise key_nex
        key_nex = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_nex',
        )
    if deviceManager.getDevice('key_resp_instruction') is None:
        # initialise key_resp_instruction
        key_resp_instruction = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_instruction',
        )
    if deviceManager.getDevice('p_key_resp') is None:
        # initialise p_key_resp
        p_key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='p_key_resp',
        )
    if deviceManager.getDevice('p_fb_keyboard_continue') is None:
        # initialise p_fb_keyboard_continue
        p_fb_keyboard_continue = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='p_fb_keyboard_continue',
        )
    if deviceManager.getDevice('continue_maintrial') is None:
        # initialise continue_maintrial
        continue_maintrial = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='continue_maintrial',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    if deviceManager.getDevice('fb_keyboard_continue') is None:
        # initialise fb_keyboard_continue
        fb_keyboard_continue = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='fb_keyboard_continue',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # enter 'rush' mode (raise CPU priority)
    if not PILOTING:
        core.rush(enable=True)
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "intro" ---
    intro_disp = visual.TextStim(win=win, name='intro_disp',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_nex = keyboard.Keyboard(deviceName='key_nex')
    intro_small = visual.TextStim(win=win, name='intro_small',
        text='',
        font='Arial',
        pos=(0, -.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    
    # --- Initialize components for Routine "instruction_page" ---
    instruction = visual.TextStim(win=win, name='instruction',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_instruction = keyboard.Keyboard(deviceName='key_resp_instruction')
    
    # --- Initialize components for Routine "p_code_init" ---
    
    # --- Initialize components for Routine "p_cross_fix" ---
    cross = visual.ShapeStim(
        win=win, name='cross', vertices='cross',
        size=(0.2, 0.2),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    p_cross_text_block = visual.TextStim(win=win, name='p_cross_text_block',
        text='',
        font='Arial',
        pos=(0, -0.2), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "p_prompt" ---
    p_string_prompt_disp = visual.TextStim(win=win, name='p_string_prompt_disp',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    p_black_screendelay = visual.ImageStim(
        win=win,
        name='p_black_screendelay', 
        image=None, mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    p_string_prompt_text_block = visual.TextStim(win=win, name='p_string_prompt_text_block',
        text='',
        font='Arial',
        pos=(0, -0.2), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "p_response" ---
    p_key_resp = keyboard.Keyboard(deviceName='p_key_resp')
    p_key_response_disp = visual.TextStim(win=win, name='p_key_response_disp',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "p_button_record" ---
    p_fb_disp = visual.TextStim(win=win, name='p_fb_disp',
        text='',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    p_timing_shift_text_block = visual.TextStim(win=win, name='p_timing_shift_text_block',
        text='',
        font='Arial',
        pos=(0, -0.2), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    p_fb_keyboard_continue = keyboard.Keyboard(deviceName='p_fb_keyboard_continue')
    
    # --- Initialize components for Routine "instruction_maintrial" ---
    text = visual.TextStim(win=win, name='text',
        text=maintrial_text,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    continue_maintrial = keyboard.Keyboard(deviceName='continue_maintrial')
    
    # --- Initialize components for Routine "countdown" ---
    text_countdown = visual.TextStim(win=win, name='text_countdown',
        text='',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "initcodevalues" ---
    
    # --- Initialize components for Routine "cross_fix" ---
    polygon = visual.ShapeStim(
        win=win, name='polygon', vertices='cross',
        size=(0.2, 0.2),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    
    # --- Initialize components for Routine "prompt" ---
    string_prompt_disp = visual.TextStim(win=win, name='string_prompt_disp',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    black_screendelay = visual.ImageStim(
        win=win,
        name='black_screendelay', 
        image=None, mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    
    # --- Initialize components for Routine "response" ---
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    key_response_disp = visual.TextStim(win=win, name='key_response_disp',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "button_record" ---
    fb_disp = visual.TextStim(win=win, name='fb_disp',
        text='',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    fb_keyboard_continue = keyboard.Keyboard(deviceName='fb_keyboard_continue')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "intro" ---
    # create an object to store info about Routine intro
    intro = data.Routine(
        name='intro',
        components=[intro_disp, key_nex, intro_small],
    )
    intro.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    intro_disp.setText(intro_disp_text)
    # create starting attributes for key_nex
    key_nex.keys = []
    key_nex.rt = []
    _key_nex_allKeys = []
    intro_small.setText(intro_small_text)
    # store start times for intro
    intro.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    intro.tStart = globalClock.getTime(format='float')
    intro.status = STARTED
    intro.maxDuration = None
    # keep track of which components have finished
    introComponents = intro.components
    for thisComponent in intro.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "intro" ---
    intro.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *intro_disp* updates
        
        # if intro_disp is starting this frame...
        if intro_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            intro_disp.frameNStart = frameN  # exact frame index
            intro_disp.tStart = t  # local t and not account for scr refresh
            intro_disp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(intro_disp, 'tStartRefresh')  # time at next scr refresh
            # update status
            intro_disp.status = STARTED
            intro_disp.setAutoDraw(True)
        
        # if intro_disp is active this frame...
        if intro_disp.status == STARTED:
            # update params
            pass
        
        # *key_nex* updates
        
        # if key_nex is starting this frame...
        if key_nex.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_nex.frameNStart = frameN  # exact frame index
            key_nex.tStart = t  # local t and not account for scr refresh
            key_nex.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_nex, 'tStartRefresh')  # time at next scr refresh
            # update status
            key_nex.status = STARTED
            # keyboard checking is just starting
            key_nex.clock.reset()  # now t=0
        if key_nex.status == STARTED:
            theseKeys = key_nex.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
            _key_nex_allKeys.extend(theseKeys)
            if len(_key_nex_allKeys):
                key_nex.keys = _key_nex_allKeys[-1].name  # just the last key pressed
                key_nex.rt = _key_nex_allKeys[-1].rt
                key_nex.duration = _key_nex_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *intro_small* updates
        
        # if intro_small is starting this frame...
        if intro_small.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            intro_small.frameNStart = frameN  # exact frame index
            intro_small.tStart = t  # local t and not account for scr refresh
            intro_small.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(intro_small, 'tStartRefresh')  # time at next scr refresh
            # update status
            intro_small.status = STARTED
            intro_small.setAutoDraw(True)
        
        # if intro_small is active this frame...
        if intro_small.status == STARTED:
            # update params
            pass
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            intro.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in intro.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "intro" ---
    for thisComponent in intro.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for intro
    intro.tStop = globalClock.getTime(format='float')
    intro.tStopRefresh = tThisFlipGlobal
    thisExp.nextEntry()
    # the Routine "intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    loop_instruction = data.TrialHandler2(
        name='loop_instruction',
        nReps=loopcount_text_list, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(loop_instruction)  # add the loop to the experiment
    thisLoop_instruction = loop_instruction.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLoop_instruction.rgb)
    if thisLoop_instruction != None:
        for paramName in thisLoop_instruction:
            globals()[paramName] = thisLoop_instruction[paramName]
    
    for thisLoop_instruction in loop_instruction:
        currentLoop = loop_instruction
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # abbreviate parameter names if possible (e.g. rgb = thisLoop_instruction.rgb)
        if thisLoop_instruction != None:
            for paramName in thisLoop_instruction:
                globals()[paramName] = thisLoop_instruction[paramName]
        
        # --- Prepare to start Routine "instruction_page" ---
        # create an object to store info about Routine instruction_page
        instruction_page = data.Routine(
            name='instruction_page',
            components=[instruction, key_resp_instruction],
        )
        instruction_page.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        instruction.setText(stim_map["instruction_text"])
        # create starting attributes for key_resp_instruction
        key_resp_instruction.keys = []
        key_resp_instruction.rt = []
        _key_resp_instruction_allKeys = []
        # store start times for instruction_page
        instruction_page.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        instruction_page.tStart = globalClock.getTime(format='float')
        instruction_page.status = STARTED
        instruction_page.maxDuration = None
        # keep track of which components have finished
        instruction_pageComponents = instruction_page.components
        for thisComponent in instruction_page.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "instruction_page" ---
        # if trial has changed, end Routine now
        if isinstance(loop_instruction, data.TrialHandler2) and thisLoop_instruction.thisN != loop_instruction.thisTrial.thisN:
            continueRoutine = False
        instruction_page.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instruction* updates
            
            # if instruction is starting this frame...
            if instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instruction.frameNStart = frameN  # exact frame index
                instruction.tStart = t  # local t and not account for scr refresh
                instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instruction, 'tStartRefresh')  # time at next scr refresh
                # update status
                instruction.status = STARTED
                instruction.setAutoDraw(True)
            
            # if instruction is active this frame...
            if instruction.status == STARTED:
                # update params
                pass
            
            # *key_resp_instruction* updates
            
            # if key_resp_instruction is starting this frame...
            if key_resp_instruction.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_instruction.frameNStart = frameN  # exact frame index
                key_resp_instruction.tStart = t  # local t and not account for scr refresh
                key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
                # update status
                key_resp_instruction.status = STARTED
                # keyboard checking is just starting
                key_resp_instruction.clock.reset()  # now t=0
                key_resp_instruction.clearEvents(eventType='keyboard')
            if key_resp_instruction.status == STARTED:
                theseKeys = key_resp_instruction.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
                _key_resp_instruction_allKeys.extend(theseKeys)
                if len(_key_resp_instruction_allKeys):
                    key_resp_instruction.keys = _key_resp_instruction_allKeys[-1].name  # just the last key pressed
                    key_resp_instruction.rt = _key_resp_instruction_allKeys[-1].rt
                    key_resp_instruction.duration = _key_resp_instruction_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                instruction_page.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in instruction_page.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "instruction_page" ---
        for thisComponent in instruction_page.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for instruction_page
        instruction_page.tStop = globalClock.getTime(format='float')
        instruction_page.tStopRefresh = tThisFlipGlobal
        # Run 'End Routine' code from code_textshift
        # go to next text 
        
        stim_map["iter_text_list"] += 1
        if stim_map["iter_text_list"] != loopcount_text_list:
            print("now on text", stim_map["iter_text_list"], "\n")
            stim_map["instruction_text"] = text_list[stim_map["iter_text_list"]]
        
        # check responses
        if key_resp_instruction.keys in ['', [], None]:  # No response was made
            key_resp_instruction.keys = None
        loop_instruction.addData('key_resp_instruction.keys',key_resp_instruction.keys)
        if key_resp_instruction.keys != None:  # we had a response
            loop_instruction.addData('key_resp_instruction.rt', key_resp_instruction.rt)
            loop_instruction.addData('key_resp_instruction.duration', key_resp_instruction.duration)
        # the Routine "instruction_page" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed loopcount_text_list repeats of 'loop_instruction'
    
    
    # set up handler to look after randomisation of conditions etc
    loop_practice = data.TrialHandler2(
        name='loop_practice',
        nReps=stim_map["p_loop_maxcount"], 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(loop_practice)  # add the loop to the experiment
    thisLoop_practice = loop_practice.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLoop_practice.rgb)
    if thisLoop_practice != None:
        for paramName in thisLoop_practice:
            globals()[paramName] = thisLoop_practice[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisLoop_practice in loop_practice:
        currentLoop = loop_practice
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisLoop_practice.rgb)
        if thisLoop_practice != None:
            for paramName in thisLoop_practice:
                globals()[paramName] = thisLoop_practice[paramName]
        
        # --- Prepare to start Routine "p_code_init" ---
        # create an object to store info about Routine p_code_init
        p_code_init = data.Routine(
            name='p_code_init',
            components=[],
        )
        p_code_init.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from p_codeinit
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
        # store start times for p_code_init
        p_code_init.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        p_code_init.tStart = globalClock.getTime(format='float')
        p_code_init.status = STARTED
        p_code_init.maxDuration = None
        # keep track of which components have finished
        p_code_initComponents = p_code_init.components
        for thisComponent in p_code_init.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "p_code_init" ---
        # if trial has changed, end Routine now
        if isinstance(loop_practice, data.TrialHandler2) and thisLoop_practice.thisN != loop_practice.thisTrial.thisN:
            continueRoutine = False
        p_code_init.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                p_code_init.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in p_code_init.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "p_code_init" ---
        for thisComponent in p_code_init.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for p_code_init
        p_code_init.tStop = globalClock.getTime(format='float')
        p_code_init.tStopRefresh = tThisFlipGlobal
        # the Routine "p_code_init" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "p_cross_fix" ---
        # create an object to store info about Routine p_cross_fix
        p_cross_fix = data.Routine(
            name='p_cross_fix',
            components=[cross, p_cross_text_block],
        )
        p_cross_fix.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        p_cross_text_block.setText(p_cross_text)
        # store start times for p_cross_fix
        p_cross_fix.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        p_cross_fix.tStart = globalClock.getTime(format='float')
        p_cross_fix.status = STARTED
        p_cross_fix.maxDuration = None
        # skip Routine p_cross_fix if its 'Skip if' condition is True
        p_cross_fix.skipped = continueRoutine and not (stim_map["cross_en"])
        continueRoutine = p_cross_fix.skipped
        # keep track of which components have finished
        p_cross_fixComponents = p_cross_fix.components
        for thisComponent in p_cross_fix.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "p_cross_fix" ---
        # if trial has changed, end Routine now
        if isinstance(loop_practice, data.TrialHandler2) and thisLoop_practice.thisN != loop_practice.thisTrial.thisN:
            continueRoutine = False
        p_cross_fix.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *cross* updates
            
            # if cross is starting this frame...
            if cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                cross.frameNStart = frameN  # exact frame index
                cross.tStart = t  # local t and not account for scr refresh
                cross.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cross, 'tStartRefresh')  # time at next scr refresh
                # update status
                cross.status = STARTED
                cross.setAutoDraw(True)
            
            # if cross is active this frame...
            if cross.status == STARTED:
                # update params
                pass
            
            # if cross is stopping this frame...
            if cross.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cross.tStartRefresh + timing_map["p_dCross"]-frameTolerance:
                    # keep track of stop time/frame for later
                    cross.tStop = t  # not accounting for scr refresh
                    cross.tStopRefresh = tThisFlipGlobal  # on global time
                    cross.frameNStop = frameN  # exact frame index
                    # update status
                    cross.status = FINISHED
                    cross.setAutoDraw(False)
            
            # *p_cross_text_block* updates
            
            # if p_cross_text_block is starting this frame...
            if p_cross_text_block.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_cross_text_block.frameNStart = frameN  # exact frame index
                p_cross_text_block.tStart = t  # local t and not account for scr refresh
                p_cross_text_block.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_cross_text_block, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_cross_text_block.status = STARTED
                p_cross_text_block.setAutoDraw(True)
            
            # if p_cross_text_block is active this frame...
            if p_cross_text_block.status == STARTED:
                # update params
                pass
            
            # if p_cross_text_block is stopping this frame...
            if p_cross_text_block.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_cross_text_block.tStartRefresh + timing_map["p_dCross"]-frameTolerance:
                    # keep track of stop time/frame for later
                    p_cross_text_block.tStop = t  # not accounting for scr refresh
                    p_cross_text_block.tStopRefresh = tThisFlipGlobal  # on global time
                    p_cross_text_block.frameNStop = frameN  # exact frame index
                    # update status
                    p_cross_text_block.status = FINISHED
                    p_cross_text_block.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                p_cross_fix.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in p_cross_fix.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "p_cross_fix" ---
        for thisComponent in p_cross_fix.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for p_cross_fix
        p_cross_fix.tStop = globalClock.getTime(format='float')
        p_cross_fix.tStopRefresh = tThisFlipGlobal
        # Run 'End Routine' code from p_code_crossen
        # set in routine to skip if cross_en == True
        stim_map["cross_en"] = True
        timing_map["p_dCross"]
        # the Routine "p_cross_fix" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "p_prompt" ---
        # create an object to store info about Routine p_prompt
        p_prompt = data.Routine(
            name='p_prompt',
            components=[p_string_prompt_disp, p_black_screendelay, p_string_prompt_text_block],
        )
        p_prompt.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        p_string_prompt_disp.setText(stim_map["string_prompt"])
        p_string_prompt_text_block.setText(p_string_prompt_text)
        # store start times for p_prompt
        p_prompt.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        p_prompt.tStart = globalClock.getTime(format='float')
        p_prompt.status = STARTED
        p_prompt.maxDuration = None
        # keep track of which components have finished
        p_promptComponents = p_prompt.components
        for thisComponent in p_prompt.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "p_prompt" ---
        # if trial has changed, end Routine now
        if isinstance(loop_practice, data.TrialHandler2) and thisLoop_practice.thisN != loop_practice.thisTrial.thisN:
            continueRoutine = False
        p_prompt.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *p_string_prompt_disp* updates
            
            # if p_string_prompt_disp is starting this frame...
            if p_string_prompt_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_string_prompt_disp.frameNStart = frameN  # exact frame index
                p_string_prompt_disp.tStart = t  # local t and not account for scr refresh
                p_string_prompt_disp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_string_prompt_disp, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_string_prompt_disp.status = STARTED
                p_string_prompt_disp.setAutoDraw(True)
            
            # if p_string_prompt_disp is active this frame...
            if p_string_prompt_disp.status == STARTED:
                # update params
                pass
            
            # if p_string_prompt_disp is stopping this frame...
            if p_string_prompt_disp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_string_prompt_disp.tStartRefresh + timing_map["p_dPrompt"]-frameTolerance:
                    # keep track of stop time/frame for later
                    p_string_prompt_disp.tStop = t  # not accounting for scr refresh
                    p_string_prompt_disp.tStopRefresh = tThisFlipGlobal  # on global time
                    p_string_prompt_disp.frameNStop = frameN  # exact frame index
                    # update status
                    p_string_prompt_disp.status = FINISHED
                    p_string_prompt_disp.setAutoDraw(False)
            
            # *p_black_screendelay* updates
            
            # if p_black_screendelay is starting this frame...
            if p_black_screendelay.status == NOT_STARTED and tThisFlip >= timing_map["p_dPrompt"]-frameTolerance:
                # keep track of start time/frame for later
                p_black_screendelay.frameNStart = frameN  # exact frame index
                p_black_screendelay.tStart = t  # local t and not account for scr refresh
                p_black_screendelay.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_black_screendelay, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_black_screendelay.status = STARTED
                p_black_screendelay.setAutoDraw(True)
            
            # if p_black_screendelay is active this frame...
            if p_black_screendelay.status == STARTED:
                # update params
                pass
            
            # if p_black_screendelay is stopping this frame...
            if p_black_screendelay.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_black_screendelay.tStartRefresh + timing_map["p_dBlank"]-frameTolerance:
                    # keep track of stop time/frame for later
                    p_black_screendelay.tStop = t  # not accounting for scr refresh
                    p_black_screendelay.tStopRefresh = tThisFlipGlobal  # on global time
                    p_black_screendelay.frameNStop = frameN  # exact frame index
                    # update status
                    p_black_screendelay.status = FINISHED
                    p_black_screendelay.setAutoDraw(False)
            
            # *p_string_prompt_text_block* updates
            
            # if p_string_prompt_text_block is starting this frame...
            if p_string_prompt_text_block.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_string_prompt_text_block.frameNStart = frameN  # exact frame index
                p_string_prompt_text_block.tStart = t  # local t and not account for scr refresh
                p_string_prompt_text_block.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_string_prompt_text_block, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_string_prompt_text_block.status = STARTED
                p_string_prompt_text_block.setAutoDraw(True)
            
            # if p_string_prompt_text_block is active this frame...
            if p_string_prompt_text_block.status == STARTED:
                # update params
                pass
            
            # if p_string_prompt_text_block is stopping this frame...
            if p_string_prompt_text_block.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_string_prompt_text_block.tStartRefresh + timing_map["p_dPrompt"]-frameTolerance:
                    # keep track of stop time/frame for later
                    p_string_prompt_text_block.tStop = t  # not accounting for scr refresh
                    p_string_prompt_text_block.tStopRefresh = tThisFlipGlobal  # on global time
                    p_string_prompt_text_block.frameNStop = frameN  # exact frame index
                    # update status
                    p_string_prompt_text_block.status = FINISHED
                    p_string_prompt_text_block.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                p_prompt.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in p_prompt.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "p_prompt" ---
        for thisComponent in p_prompt.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for p_prompt
        p_prompt.tStop = globalClock.getTime(format='float')
        p_prompt.tStopRefresh = tThisFlipGlobal
        # the Routine "p_prompt" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "p_response" ---
        # create an object to store info about Routine p_response
        p_response = data.Routine(
            name='p_response',
            components=[p_key_resp, p_key_response_disp],
        )
        p_response.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for p_key_resp
        p_key_resp.keys = []
        p_key_resp.rt = []
        _p_key_resp_allKeys = []
        p_key_response_disp.setText(stim_map["key_prompt"])
        # store start times for p_response
        p_response.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        p_response.tStart = globalClock.getTime(format='float')
        p_response.status = STARTED
        p_response.maxDuration = timing_map["p_dResponse"]
        # keep track of which components have finished
        p_responseComponents = p_response.components
        for thisComponent in p_response.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "p_response" ---
        # if trial has changed, end Routine now
        if isinstance(loop_practice, data.TrialHandler2) and thisLoop_practice.thisN != loop_practice.thisTrial.thisN:
            continueRoutine = False
        p_response.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # is it time to end the Routine? (based on local clock)
            if tThisFlip > p_response.maxDuration-frameTolerance:
                p_response.maxDurationReached = True
                continueRoutine = False
            
            # *p_key_resp* updates
            waitOnFlip = False
            
            # if p_key_resp is starting this frame...
            if p_key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_key_resp.frameNStart = frameN  # exact frame index
                p_key_resp.tStart = t  # local t and not account for scr refresh
                p_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_key_resp, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(p_key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(p_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if p_key_resp.status == STARTED and not waitOnFlip:
                theseKeys = p_key_resp.getKeys(keyList=['comma','period'], ignoreKeys=["escape"], waitRelease=False)
                _p_key_resp_allKeys.extend(theseKeys)
                if len(_p_key_resp_allKeys):
                    p_key_resp.keys = _p_key_resp_allKeys[-1].name  # just the last key pressed
                    p_key_resp.rt = _p_key_resp_allKeys[-1].rt
                    p_key_resp.duration = _p_key_resp_allKeys[-1].duration
                    # was this correct?
                    if (p_key_resp.keys == str(stim_map["map_correct"])) or (p_key_resp.keys == stim_map["map_correct"]):
                        p_key_resp.corr = 1
                    else:
                        p_key_resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # *p_key_response_disp* updates
            
            # if p_key_response_disp is starting this frame...
            if p_key_response_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_key_response_disp.frameNStart = frameN  # exact frame index
                p_key_response_disp.tStart = t  # local t and not account for scr refresh
                p_key_response_disp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_key_response_disp, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_key_response_disp.status = STARTED
                p_key_response_disp.setAutoDraw(True)
            
            # if p_key_response_disp is active this frame...
            if p_key_response_disp.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                p_response.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in p_response.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "p_response" ---
        for thisComponent in p_response.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for p_response
        p_response.tStop = globalClock.getTime(format='float')
        p_response.tStopRefresh = tThisFlipGlobal
        # check responses
        if p_key_resp.keys in ['', [], None]:  # No response was made
            p_key_resp.keys = None
            # was no response the correct answer?!
            if str(stim_map["map_correct"]).lower() == 'none':
               p_key_resp.corr = 1;  # correct non-response
            else:
               p_key_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for loop_practice (TrialHandler)
        loop_practice.addData('p_key_resp.keys',p_key_resp.keys)
        loop_practice.addData('p_key_resp.corr', p_key_resp.corr)
        if p_key_resp.keys != None:  # we had a response
            loop_practice.addData('p_key_resp.rt', p_key_resp.rt)
            loop_practice.addData('p_key_resp.duration', p_key_resp.duration)
        # the Routine "p_response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "p_button_record" ---
        # create an object to store info about Routine p_button_record
        p_button_record = data.Routine(
            name='p_button_record',
            components=[p_fb_disp, p_timing_shift_text_block, p_fb_keyboard_continue],
        )
        p_button_record.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from p_code_fb
        
        
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
        
        p_fb_disp.setColor(fb_col, colorSpace='rgb')
        p_fb_disp.setText(fb_text)
        p_timing_shift_text_block.setText(p_timing_shift_text)
        # create starting attributes for p_fb_keyboard_continue
        p_fb_keyboard_continue.keys = []
        p_fb_keyboard_continue.rt = []
        _p_fb_keyboard_continue_allKeys = []
        # store start times for p_button_record
        p_button_record.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        p_button_record.tStart = globalClock.getTime(format='float')
        p_button_record.status = STARTED
        p_button_record.maxDuration = None
        # keep track of which components have finished
        p_button_recordComponents = p_button_record.components
        for thisComponent in p_button_record.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "p_button_record" ---
        # if trial has changed, end Routine now
        if isinstance(loop_practice, data.TrialHandler2) and thisLoop_practice.thisN != loop_practice.thisTrial.thisN:
            continueRoutine = False
        p_button_record.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *p_fb_disp* updates
            
            # if p_fb_disp is starting this frame...
            if p_fb_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_fb_disp.frameNStart = frameN  # exact frame index
                p_fb_disp.tStart = t  # local t and not account for scr refresh
                p_fb_disp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_fb_disp, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_fb_disp.status = STARTED
                p_fb_disp.setAutoDraw(True)
            
            # if p_fb_disp is active this frame...
            if p_fb_disp.status == STARTED:
                # update params
                pass
            
            # if p_fb_disp is stopping this frame...
            if p_fb_disp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_fb_disp.tStartRefresh + timing_map["p_dFb"]-frameTolerance:
                    # keep track of stop time/frame for later
                    p_fb_disp.tStop = t  # not accounting for scr refresh
                    p_fb_disp.tStopRefresh = tThisFlipGlobal  # on global time
                    p_fb_disp.frameNStop = frameN  # exact frame index
                    # update status
                    p_fb_disp.status = FINISHED
                    p_fb_disp.setAutoDraw(False)
            
            # *p_timing_shift_text_block* updates
            
            # if p_timing_shift_text_block is starting this frame...
            if p_timing_shift_text_block.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_timing_shift_text_block.frameNStart = frameN  # exact frame index
                p_timing_shift_text_block.tStart = t  # local t and not account for scr refresh
                p_timing_shift_text_block.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_timing_shift_text_block, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_timing_shift_text_block.status = STARTED
                p_timing_shift_text_block.setAutoDraw(True)
            
            # if p_timing_shift_text_block is active this frame...
            if p_timing_shift_text_block.status == STARTED:
                # update params
                pass
            
            # if p_timing_shift_text_block is stopping this frame...
            if p_timing_shift_text_block.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_timing_shift_text_block.tStartRefresh + timing_map["p_dFb"]-frameTolerance:
                    # keep track of stop time/frame for later
                    p_timing_shift_text_block.tStop = t  # not accounting for scr refresh
                    p_timing_shift_text_block.tStopRefresh = tThisFlipGlobal  # on global time
                    p_timing_shift_text_block.frameNStop = frameN  # exact frame index
                    # update status
                    p_timing_shift_text_block.status = FINISHED
                    p_timing_shift_text_block.setAutoDraw(False)
            
            # *p_fb_keyboard_continue* updates
            
            # if p_fb_keyboard_continue is starting this frame...
            if p_fb_keyboard_continue.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                p_fb_keyboard_continue.frameNStart = frameN  # exact frame index
                p_fb_keyboard_continue.tStart = t  # local t and not account for scr refresh
                p_fb_keyboard_continue.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(p_fb_keyboard_continue, 'tStartRefresh')  # time at next scr refresh
                # update status
                p_fb_keyboard_continue.status = STARTED
                # keyboard checking is just starting
                p_fb_keyboard_continue.clock.reset()  # now t=0
                p_fb_keyboard_continue.clearEvents(eventType='keyboard')
            
            # if p_fb_keyboard_continue is stopping this frame...
            if p_fb_keyboard_continue.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_fb_keyboard_continue.tStartRefresh + timing_map["p_dFb"]-frameTolerance:
                    # keep track of stop time/frame for later
                    p_fb_keyboard_continue.tStop = t  # not accounting for scr refresh
                    p_fb_keyboard_continue.tStopRefresh = tThisFlipGlobal  # on global time
                    p_fb_keyboard_continue.frameNStop = frameN  # exact frame index
                    # update status
                    p_fb_keyboard_continue.status = FINISHED
                    p_fb_keyboard_continue.status = FINISHED
            if p_fb_keyboard_continue.status == STARTED:
                theseKeys = p_fb_keyboard_continue.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
                _p_fb_keyboard_continue_allKeys.extend(theseKeys)
                if len(_p_fb_keyboard_continue_allKeys):
                    p_fb_keyboard_continue.keys = _p_fb_keyboard_continue_allKeys[-1].name  # just the last key pressed
                    p_fb_keyboard_continue.rt = _p_fb_keyboard_continue_allKeys[-1].rt
                    p_fb_keyboard_continue.duration = _p_fb_keyboard_continue_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                p_button_record.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in p_button_record.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "p_button_record" ---
        for thisComponent in p_button_record.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for p_button_record
        p_button_record.tStop = globalClock.getTime(format='float')
        p_button_record.tStopRefresh = tThisFlipGlobal
        # Run 'End Routine' code from p_code_fb
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
        # the Routine "p_button_record" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed stim_map["p_loop_maxcount"] repeats of 'loop_practice'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    # get names of stimulus parameters
    if loop_practice.trialList in ([], [None], None):
        params = []
    else:
        params = loop_practice.trialList[0].keys()
    # save data for this loop
    loop_practice.saveAsExcel(filename + '.xlsx', sheetName='loop_practice',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    # --- Prepare to start Routine "instruction_maintrial" ---
    # create an object to store info about Routine instruction_maintrial
    instruction_maintrial = data.Routine(
        name='instruction_maintrial',
        components=[text, continue_maintrial],
    )
    instruction_maintrial.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for continue_maintrial
    continue_maintrial.keys = []
    continue_maintrial.rt = []
    _continue_maintrial_allKeys = []
    # Run 'Begin Routine' code from code_clear_p
    # reset values after practice
    stim_map["loop_iter"] = 0
    stim_map["char_length"] = 3
    # store start times for instruction_maintrial
    instruction_maintrial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instruction_maintrial.tStart = globalClock.getTime(format='float')
    instruction_maintrial.status = STARTED
    instruction_maintrial.maxDuration = None
    # keep track of which components have finished
    instruction_maintrialComponents = instruction_maintrial.components
    for thisComponent in instruction_maintrial.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instruction_maintrial" ---
    instruction_maintrial.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # *continue_maintrial* updates
        
        # if continue_maintrial is starting this frame...
        if continue_maintrial.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            continue_maintrial.frameNStart = frameN  # exact frame index
            continue_maintrial.tStart = t  # local t and not account for scr refresh
            continue_maintrial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(continue_maintrial, 'tStartRefresh')  # time at next scr refresh
            # update status
            continue_maintrial.status = STARTED
            # keyboard checking is just starting
            continue_maintrial.clock.reset()  # now t=0
            continue_maintrial.clearEvents(eventType='keyboard')
        if continue_maintrial.status == STARTED:
            theseKeys = continue_maintrial.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
            _continue_maintrial_allKeys.extend(theseKeys)
            if len(_continue_maintrial_allKeys):
                continue_maintrial.keys = _continue_maintrial_allKeys[-1].name  # just the last key pressed
                continue_maintrial.rt = _continue_maintrial_allKeys[-1].rt
                continue_maintrial.duration = _continue_maintrial_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            instruction_maintrial.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instruction_maintrial.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instruction_maintrial" ---
    for thisComponent in instruction_maintrial.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instruction_maintrial
    instruction_maintrial.tStop = globalClock.getTime(format='float')
    instruction_maintrial.tStopRefresh = tThisFlipGlobal
    thisExp.nextEntry()
    # the Routine "instruction_maintrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "countdown" ---
    # create an object to store info about Routine countdown
    countdown = data.Routine(
        name='countdown',
        components=[text_countdown],
    )
    countdown.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for countdown
    countdown.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    countdown.tStart = globalClock.getTime(format='float')
    countdown.status = STARTED
    thisExp.addData('countdown.started', countdown.tStart)
    countdown.maxDuration = None
    # keep track of which components have finished
    countdownComponents = countdown.components
    for thisComponent in countdown.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "countdown" ---
    countdown.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 10.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_countdown* updates
        
        # if text_countdown is starting this frame...
        if text_countdown.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_countdown.frameNStart = frameN  # exact frame index
            text_countdown.tStart = t  # local t and not account for scr refresh
            text_countdown.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_countdown, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_countdown.started')
            # update status
            text_countdown.status = STARTED
            text_countdown.setAutoDraw(True)
        
        # if text_countdown is active this frame...
        if text_countdown.status == STARTED:
            # update params
            text_countdown.setText(str(10-int(t)), log=False)
        
        # if text_countdown is stopping this frame...
        if text_countdown.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_countdown.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                text_countdown.tStop = t  # not accounting for scr refresh
                text_countdown.tStopRefresh = tThisFlipGlobal  # on global time
                text_countdown.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_countdown.stopped')
                # update status
                text_countdown.status = FINISHED
                text_countdown.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            countdown.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in countdown.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "countdown" ---
    for thisComponent in countdown.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for countdown
    countdown.tStop = globalClock.getTime(format='float')
    countdown.tStopRefresh = tThisFlipGlobal
    thisExp.addData('countdown.stopped', countdown.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if countdown.maxDurationReached:
        routineTimer.addTime(-countdown.maxDuration)
    elif countdown.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-10.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    loop_maintrial = data.TrialHandler2(
        name='loop_maintrial',
        nReps=stim_map["loop_maxcount"], 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(loop_maintrial)  # add the loop to the experiment
    thisLoop_maintrial = loop_maintrial.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLoop_maintrial.rgb)
    if thisLoop_maintrial != None:
        for paramName in thisLoop_maintrial:
            globals()[paramName] = thisLoop_maintrial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisLoop_maintrial in loop_maintrial:
        currentLoop = loop_maintrial
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisLoop_maintrial.rgb)
        if thisLoop_maintrial != None:
            for paramName in thisLoop_maintrial:
                globals()[paramName] = thisLoop_maintrial[paramName]
        
        # --- Prepare to start Routine "initcodevalues" ---
        # create an object to store info about Routine initcodevalues
        initcodevalues = data.Routine(
            name='initcodevalues',
            components=[],
        )
        initcodevalues.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_loopvalue
        # reset prompt
        stim_map["string_prompt"] = sb_rand(stim_map["char_length"])
        stim_map["key_prompt"] = gen_key(stim_map["string_prompt"])
        stim_map["map_correct"] = input_val(sb_validate(stim_map["string_prompt"],
                                              stim_map["key_prompt"]))
        
        
        print("string prompt is", stim_map["string_prompt"], "\n",
              "key prompt is", stim_map["key_prompt"], "\n",
              "button to indicate correct is", stim_map["map_correct"], "\n")
        # store start times for initcodevalues
        initcodevalues.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        initcodevalues.tStart = globalClock.getTime(format='float')
        initcodevalues.status = STARTED
        initcodevalues.maxDuration = None
        # keep track of which components have finished
        initcodevaluesComponents = initcodevalues.components
        for thisComponent in initcodevalues.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "initcodevalues" ---
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
        initcodevalues.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                initcodevalues.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in initcodevalues.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "initcodevalues" ---
        for thisComponent in initcodevalues.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for initcodevalues
        initcodevalues.tStop = globalClock.getTime(format='float')
        initcodevalues.tStopRefresh = tThisFlipGlobal
        # the Routine "initcodevalues" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "cross_fix" ---
        # create an object to store info about Routine cross_fix
        cross_fix = data.Routine(
            name='cross_fix',
            components=[polygon],
        )
        cross_fix.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for cross_fix
        cross_fix.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        cross_fix.tStart = globalClock.getTime(format='float')
        cross_fix.status = STARTED
        thisExp.addData('cross_fix.started', cross_fix.tStart)
        cross_fix.maxDuration = None
        # skip Routine cross_fix if its 'Skip if' condition is True
        cross_fix.skipped = continueRoutine and not (stim_map["cross_en"])
        continueRoutine = cross_fix.skipped
        # keep track of which components have finished
        cross_fixComponents = cross_fix.components
        for thisComponent in cross_fix.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "cross_fix" ---
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
        cross_fix.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *polygon* updates
            
            # if polygon is starting this frame...
            if polygon.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                polygon.frameNStart = frameN  # exact frame index
                polygon.tStart = t  # local t and not account for scr refresh
                polygon.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'polygon.started')
                # update status
                polygon.status = STARTED
                polygon.setAutoDraw(True)
            
            # if polygon is active this frame...
            if polygon.status == STARTED:
                # update params
                pass
            
            # if polygon is stopping this frame...
            if polygon.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon.tStartRefresh + timing_map["dCross"]-frameTolerance:
                    # keep track of stop time/frame for later
                    polygon.tStop = t  # not accounting for scr refresh
                    polygon.tStopRefresh = tThisFlipGlobal  # on global time
                    polygon.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'polygon.stopped')
                    # update status
                    polygon.status = FINISHED
                    polygon.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                cross_fix.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in cross_fix.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "cross_fix" ---
        for thisComponent in cross_fix.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for cross_fix
        cross_fix.tStop = globalClock.getTime(format='float')
        cross_fix.tStopRefresh = tThisFlipGlobal
        thisExp.addData('cross_fix.stopped', cross_fix.tStop)
        # Run 'End Routine' code from code_crossen
        # set in routine to skip if cross_en == True
        stim_map["cross_en"] = True
        # the Routine "cross_fix" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "prompt" ---
        # create an object to store info about Routine prompt
        prompt = data.Routine(
            name='prompt',
            components=[string_prompt_disp, black_screendelay],
        )
        prompt.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        string_prompt_disp.setText(stim_map["string_prompt"])
        # store start times for prompt
        prompt.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        prompt.tStart = globalClock.getTime(format='float')
        prompt.status = STARTED
        thisExp.addData('prompt.started', prompt.tStart)
        prompt.maxDuration = None
        # keep track of which components have finished
        promptComponents = prompt.components
        for thisComponent in prompt.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "prompt" ---
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
        prompt.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *string_prompt_disp* updates
            
            # if string_prompt_disp is starting this frame...
            if string_prompt_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                string_prompt_disp.frameNStart = frameN  # exact frame index
                string_prompt_disp.tStart = t  # local t and not account for scr refresh
                string_prompt_disp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(string_prompt_disp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'string_prompt_disp.started')
                # update status
                string_prompt_disp.status = STARTED
                string_prompt_disp.setAutoDraw(True)
            
            # if string_prompt_disp is active this frame...
            if string_prompt_disp.status == STARTED:
                # update params
                pass
            
            # if string_prompt_disp is stopping this frame...
            if string_prompt_disp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > string_prompt_disp.tStartRefresh + timing_map["dPrompt"]-frameTolerance:
                    # keep track of stop time/frame for later
                    string_prompt_disp.tStop = t  # not accounting for scr refresh
                    string_prompt_disp.tStopRefresh = tThisFlipGlobal  # on global time
                    string_prompt_disp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'string_prompt_disp.stopped')
                    # update status
                    string_prompt_disp.status = FINISHED
                    string_prompt_disp.setAutoDraw(False)
            
            # *black_screendelay* updates
            
            # if black_screendelay is starting this frame...
            if black_screendelay.status == NOT_STARTED and tThisFlip >= timing_map["dPrompt"]-frameTolerance:
                # keep track of start time/frame for later
                black_screendelay.frameNStart = frameN  # exact frame index
                black_screendelay.tStart = t  # local t and not account for scr refresh
                black_screendelay.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(black_screendelay, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'black_screendelay.started')
                # update status
                black_screendelay.status = STARTED
                black_screendelay.setAutoDraw(True)
            
            # if black_screendelay is active this frame...
            if black_screendelay.status == STARTED:
                # update params
                pass
            
            # if black_screendelay is stopping this frame...
            if black_screendelay.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > black_screendelay.tStartRefresh + timing_map["dBlank"]-frameTolerance:
                    # keep track of stop time/frame for later
                    black_screendelay.tStop = t  # not accounting for scr refresh
                    black_screendelay.tStopRefresh = tThisFlipGlobal  # on global time
                    black_screendelay.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'black_screendelay.stopped')
                    # update status
                    black_screendelay.status = FINISHED
                    black_screendelay.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                prompt.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in prompt.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "prompt" ---
        for thisComponent in prompt.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for prompt
        prompt.tStop = globalClock.getTime(format='float')
        prompt.tStopRefresh = tThisFlipGlobal
        thisExp.addData('prompt.stopped', prompt.tStop)
        # the Routine "prompt" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "response" ---
        # create an object to store info about Routine response
        response = data.Routine(
            name='response',
            components=[key_resp, key_response_disp],
        )
        response.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        key_response_disp.setText(stim_map["key_prompt"])
        # store start times for response
        response.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        response.tStart = globalClock.getTime(format='float')
        response.status = STARTED
        thisExp.addData('response.started', response.tStart)
        response.maxDuration = timing_map["dResponse"]
        # keep track of which components have finished
        responseComponents = response.components
        for thisComponent in response.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "response" ---
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
        response.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # is it time to end the Routine? (based on local clock)
            if tThisFlip > response.maxDuration-frameTolerance:
                response.maxDurationReached = True
                continueRoutine = False
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['comma','period'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
                    # was this correct?
                    if (key_resp.keys == str(stim_map["map_correct"])) or (key_resp.keys == stim_map["map_correct"]):
                        key_resp.corr = 1
                    else:
                        key_resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # *key_response_disp* updates
            
            # if key_response_disp is starting this frame...
            if key_response_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_response_disp.frameNStart = frameN  # exact frame index
                key_response_disp.tStart = t  # local t and not account for scr refresh
                key_response_disp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_response_disp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_response_disp.started')
                # update status
                key_response_disp.status = STARTED
                key_response_disp.setAutoDraw(True)
            
            # if key_response_disp is active this frame...
            if key_response_disp.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                response.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in response.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "response" ---
        for thisComponent in response.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for response
        response.tStop = globalClock.getTime(format='float')
        response.tStopRefresh = tThisFlipGlobal
        thisExp.addData('response.stopped', response.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
            # was no response the correct answer?!
            if str(stim_map["map_correct"]).lower() == 'none':
               key_resp.corr = 1;  # correct non-response
            else:
               key_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for loop_maintrial (TrialHandler)
        loop_maintrial.addData('key_resp.keys',key_resp.keys)
        loop_maintrial.addData('key_resp.corr', key_resp.corr)
        if key_resp.keys != None:  # we had a response
            loop_maintrial.addData('key_resp.rt', key_resp.rt)
            loop_maintrial.addData('key_resp.duration', key_resp.duration)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "button_record" ---
        # create an object to store info about Routine button_record
        button_record = data.Routine(
            name='button_record',
            components=[fb_disp, fb_keyboard_continue],
        )
        button_record.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_fb
        
        
        # display feedback to log
        print(key_resp.keys,"was pressed\n")
        try:
            if key_resp.keys == None:
                # add timeout text, decrement loop, enable fixation
                fb_text = 'please respond within a shorter time period.\nPress any key to continue.'
                timing_map["dFb"] = TIMEOUT_DURATION
                fb_col = 'white'
                stim_map["loop_iter"] -= 1
                stim_map["cross_en"] = False
            elif key_resp.corr:
                fb_text = 'Correct!'
                fb_col = 'green'
            else:
                fb_text = 'Incorrect'
                fb_col = 'red'
                
        except:
            print('ERROR: no key_resp keyboard component written.')
        
        
        # increment loop, enable cross if loop reaches max
        stim_map["loop_iter"] += 1
        
        fb_disp.setColor(fb_col, colorSpace='rgb')
        fb_disp.setText(fb_text)
        # create starting attributes for fb_keyboard_continue
        fb_keyboard_continue.keys = []
        fb_keyboard_continue.rt = []
        _fb_keyboard_continue_allKeys = []
        # store start times for button_record
        button_record.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        button_record.tStart = globalClock.getTime(format='float')
        button_record.status = STARTED
        thisExp.addData('button_record.started', button_record.tStart)
        button_record.maxDuration = None
        # keep track of which components have finished
        button_recordComponents = button_record.components
        for thisComponent in button_record.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "button_record" ---
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
        button_record.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fb_disp* updates
            
            # if fb_disp is starting this frame...
            if fb_disp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fb_disp.frameNStart = frameN  # exact frame index
                fb_disp.tStart = t  # local t and not account for scr refresh
                fb_disp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fb_disp, 'tStartRefresh')  # time at next scr refresh
                # update status
                fb_disp.status = STARTED
                fb_disp.setAutoDraw(True)
            
            # if fb_disp is active this frame...
            if fb_disp.status == STARTED:
                # update params
                pass
            
            # if fb_disp is stopping this frame...
            if fb_disp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fb_disp.tStartRefresh + timing_map["dFb"]-frameTolerance:
                    # keep track of stop time/frame for later
                    fb_disp.tStop = t  # not accounting for scr refresh
                    fb_disp.tStopRefresh = tThisFlipGlobal  # on global time
                    fb_disp.frameNStop = frameN  # exact frame index
                    # update status
                    fb_disp.status = FINISHED
                    fb_disp.setAutoDraw(False)
            
            # *fb_keyboard_continue* updates
            
            # if fb_keyboard_continue is starting this frame...
            if fb_keyboard_continue.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fb_keyboard_continue.frameNStart = frameN  # exact frame index
                fb_keyboard_continue.tStart = t  # local t and not account for scr refresh
                fb_keyboard_continue.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fb_keyboard_continue, 'tStartRefresh')  # time at next scr refresh
                # update status
                fb_keyboard_continue.status = STARTED
                # keyboard checking is just starting
                fb_keyboard_continue.clock.reset()  # now t=0
                fb_keyboard_continue.clearEvents(eventType='keyboard')
            
            # if fb_keyboard_continue is stopping this frame...
            if fb_keyboard_continue.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fb_keyboard_continue.tStartRefresh + timing_map["dFb"]-frameTolerance:
                    # keep track of stop time/frame for later
                    fb_keyboard_continue.tStop = t  # not accounting for scr refresh
                    fb_keyboard_continue.tStopRefresh = tThisFlipGlobal  # on global time
                    fb_keyboard_continue.frameNStop = frameN  # exact frame index
                    # update status
                    fb_keyboard_continue.status = FINISHED
                    fb_keyboard_continue.status = FINISHED
            if fb_keyboard_continue.status == STARTED:
                theseKeys = fb_keyboard_continue.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
                _fb_keyboard_continue_allKeys.extend(theseKeys)
                if len(_fb_keyboard_continue_allKeys):
                    fb_keyboard_continue.keys = _fb_keyboard_continue_allKeys[-1].name  # just the last key pressed
                    fb_keyboard_continue.rt = _fb_keyboard_continue_allKeys[-1].rt
                    fb_keyboard_continue.duration = _fb_keyboard_continue_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                button_record.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in button_record.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "button_record" ---
        for thisComponent in button_record.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for button_record
        button_record.tStop = globalClock.getTime(format='float')
        button_record.tStopRefresh = tThisFlipGlobal
        thisExp.addData('button_record.stopped', button_record.tStop)
        # Run 'End Routine' code from code_fb
        # display loop information 
        print("loop_iter =", stim_map["loop_iter"], '\n',
              "loop_count =", stim_map["loop_count"], '\n')
        
        # ensure that fb is reset to 1
        timing_map["dFb"] = DEFAULT_FEEDBACK
        # increment characters after specified loop count
        if stim_map["loop_iter"] == stim_map["loop_count"]:
            stim_map["loop_iter"] = 0
            stim_map["char_length"] += CHARACTER_INCREMENT
            stim_map["cross_en"] = False
        
        # print out debugging information
        print("timing information is: \n")
        print("timing_map[\"dCross\"]:", timing_map["dCross"])
        print("timing_map[\"dBlank\"]:", timing_map["dBlank"])
        print("timing_map[\"dPrompt\"]:", timing_map["dPrompt"])
        print("timing_map[\"dResponse\"]:", timing_map["dResponse"])
        print("timing_map[\"dFb\"]:", timing_map["dFb"])
        print("current loop that ended is:", currentLoop.thisTrial)
        
        # rewind trial to overwrite timeout data
        if key_resp.keys == None:
            currentLoop.rewindTrials()
        # the Routine "button_record" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed stim_map["loop_maxcount"] repeats of 'loop_maintrial'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    # get names of stimulus parameters
    if loop_maintrial.trialList in ([], [None], None):
        params = []
    else:
        params = loop_maintrial.trialList[0].keys()
    # save data for this loop
    loop_maintrial.saveAsExcel(filename + '.xlsx', sheetName='loop_maintrial',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)
    # end 'rush' mode
    core.rush(enable=False)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
