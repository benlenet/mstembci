﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on July 15, 2025, at 16:39
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
DEFAULT_FEEDBACK = 10
MAX_CHARACTERS = 7
# dBlank [3, 5] -- dITI [1.5, 3.5]
dBlank_lowbound = 3
dBlank_upbound = 5
dITI_lowbound = 1.5
dITI_upbound = 3.5

# record stats to give to participant upon finishing
average_rt = 0
average_accuracy = 0

# timing of each stimulus (global variables)
"""
dCross: duration of cross stimulus -- default 10
dPrompt: duration of characters on screen -- default 3.5
dBlank: duration of blank screen after cross -- default 4
dResponse: duration of single character on screen (timeout) -- default 1.5
dFb: duration of feedback (correct/incorrect) -- default 0.5
dITI: duration of blank screen -- default 2.5
"""
timing_map = {"dCross": 10,
              "dPrompt": 3.5,
              "dBlank": 4,
              "dResponse": 3,
              "dFb": TIMEOUT_DURATION,
              "dITI": 2.5,
              # start at high values of practice,
              # will change after 1st runtime
              "p_dCross": 5,
              "p_dBlank": 2,
              "p_dPrompt": 4,
              "p_dResponse": 1,
              "p_dFb": 2
              }

mouse_map = {"left":  [1, 0, 0],
             "right": [0, 0, 1],
             "middle": [0, 1, 0],
             "none": [0, 0, 0]}

# stimulus text, feedback, and loop count
# before each cycle, update each variable
# string_prompt: stimulus display
# key_prompt: key selected to display
# map_correct: button press validation
# loop_iter: used to keep track of loops
# loop_count: set max loop count
# cross_en: keep track of fixation period

stim_map = {"loop_iter": 0,
                "loop_count": 10,
                "loop_maxcount": 30,
                "char_length": 3,
                "string_prompt": "",
                "key_prompt": "",
                "map_correct": None,
                "cross_en": False,
                "instruction_text": "",
                "iter_text_list": 0,
                }



# initialize udp connection to MATLAB
UDP_IP = "10.68.17.253"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# UDP int values, sent to MATLAB
udp_map = {"f": bytes([1]),
           "e": bytes([2]),
           "m": bytes([4]),
           "r": bytes([8]),
           "fb": bytes([13]),
           "start": bytes([21]),
           "end": bytes([31]),
           "ITI": bytes([45]),
           "NA": bytes([66]),
           "timeout": bytes([81])}

# send value to UDP Port, mapped via udp_map
def matlab_send(stage):
    if stage in udp_map:
        sock.sendto(udp_map[stage], (UDP_IP, UDP_PORT))


# return a character for response stimulus
def gen_key(string_prompt, correct_rate = 0.5):
    consonants = "bcdfghjklmnpqrstvwxyz"
    trunc_chars = str.maketrans('', '', string_prompt)
    trunc_string = consonants.translate(trunc_chars)
    valid_string = string_prompt.replace(" ", "")
    return random.choice(trunc_string) if correct_rate < random.random() else random.choice(valid_string)
    

# generate list of characters for encoding, must be stored for checking validity in sb_validate
def sb_rand(num_letters = 4):
    consonants = "bcdfghjklmnpqrstvwxyz"
    if num_letters > 26:
        return "Error: num_letters must be less than or equal to 26"
    else:
        return " ".join(random.sample(consonants, num_letters))

# supply string_prompt and char_key to check if the key is valid
def sb_validate(string_prompt, char_key):
    return char_key in string_prompt

# after supplying sb_rand to the stimulus, run gen_key to generate a key.
# then run sb_validate to check if the key is valid. If sb_validate returns True,
# use bool response to display correct/incorrect response.
def input_val(validation, correct_key = [1, 0, 0], incorrect_key = [0, 0, 1]):
        return correct_key if validation else incorrect_key


# make sure all text boxes are initialized!
intro_disp_text = "Hello! Thank you for participating in the Sternberg Working Memory Task."
intro_small_text = "Please wait for the experimenter to continue."
maintrial_text = "The main experiment will now begin. Please press any key to begin."







# Run 'Before Experiment' code from code_fb
block_fb = ""
fb_text = ""
text_break = ""
skip_break = True
# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'maintrial_sternberg'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'birthday': 'MM-DD-YYYY',
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
_winSize = [1707, 1067]
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
    filename = u'data/%s_%s_%s' % (str(expInfo['birthday']), expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\benlenet\\mstembci\\maintrial_sternberg.py',
        savePickle=True, saveWideText=True,
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
        font=' Noto Mono',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    intro_small = visual.TextStim(win=win, name='intro_small',
        text='',
        font=' Noto Mono',
        pos=(0, -.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    mouse_intro = event.Mouse(win=win)
    x, y = [None, None]
    mouse_intro.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "initcodevalues" ---
    
    # --- Initialize components for Routine "cross_fix" ---
    text_cross = visual.TextStim(win=win, name='text_cross',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.3, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "prompt" ---
    string_prompt_disp = visual.TextStim(win=win, name='string_prompt_disp',
        text='',
        font=' Noto Mono',
        pos=(0, 0), draggable=False, height=0.17, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "blank" ---
    blank_screen = visual.ImageStim(
        win=win,
        name='blank_screen', 
        image=None, mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "response" ---
    key_response_disp = visual.TextStim(win=win, name='key_response_disp',
        text='',
        font=' Noto Mono',
        pos=(0, 0), draggable=False, height=0.18, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "button_record" ---
    fb_disp = visual.TextStim(win=win, name='fb_disp',
        text='',
        font=' Noto Mono',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    fb_break = visual.TextStim(win=win, name='fb_break',
        text='',
        font='Open Sans',
        pos=(0, -0.3), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    mouse_fb = event.Mouse(win=win)
    x, y = [None, None]
    mouse_fb.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "countdown" ---
    text_countdown = visual.TextStim(win=win, name='text_countdown',
        text='',
        font='Open Sans',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "ITI" ---
    black_screen = visual.Rect(
        win=win, name='black_screen',
        width=(0.5,0.5)[0], height=(0.5,0.5)[1],
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[-1.0000, -1.0000, -1.0000],
        opacity=None, depth=-1.0, interpolate=True)
    
    # --- Initialize components for Routine "calc_end_stat" ---
    # Run 'Begin Experiment' code from code_end_block
    end_text = ""
    
    # --- Initialize components for Routine "end" ---
    end_text_block = visual.TextStim(win=win, name='end_text_block',
        text='',
        font=' Noto Mono',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color=[1.0000, 1.0000, 1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    mouse_end = event.Mouse(win=win)
    x, y = [None, None]
    mouse_end.mouseClock = core.Clock()
    
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
        components=[intro_disp, intro_small, mouse_intro],
    )
    intro.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    intro_disp.setText(intro_disp_text)
    # Run 'Begin Routine' code from code_initfunction
    # send UDP signal indicating start to synchronize
    # stimulus with MATLAB EEG signals
    matlab_send("start")
    intro_small.setText(intro_small_text)
    # setup some python lists for storing info about the mouse_intro
    gotValidClick = False  # until a click is received
    # store start times for intro
    intro.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    intro.tStart = globalClock.getTime(format='float')
    intro.status = STARTED
    thisExp.addData('intro.started', intro.tStart)
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
        # Run 'Each Frame' code from code_initfunction
        if mouse_intro.getPressed() == mouse_map["middle"]:
            continueRoutine = False
            break
        
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
        # *mouse_intro* updates
        
        # if mouse_intro is starting this frame...
        if mouse_intro.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_intro.frameNStart = frameN  # exact frame index
            mouse_intro.tStart = t  # local t and not account for scr refresh
            mouse_intro.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_intro, 'tStartRefresh')  # time at next scr refresh
            # update status
            mouse_intro.status = STARTED
            mouse_intro.mouseClock.reset()
            prevButtonState = mouse_intro.getPressed()  # if button is down already this ISN'T a new click
        
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
    thisExp.addData('intro.stopped', intro.tStop)
    # store data for thisExp (ExperimentHandler)
    thisExp.nextEntry()
    # the Routine "intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
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
        # reset prompt and key values
        stim_map["string_prompt"] = sb_rand(stim_map["char_length"])
        stim_map["key_prompt"] = gen_key(stim_map["string_prompt"])
        stim_map["map_correct"] = input_val(sb_validate(stim_map["string_prompt"],
                                              stim_map["key_prompt"]))
        # initialize running average of RT and ACC
        if currentLoop.thisN == 0:
            RT_list = []
            ACC_list = []
        
        # jitter values for blank and ITI
        timing_map["dBlank"] = random.uniform(dBlank_lowbound, dBlank_upbound)
        timing_map["dITI"] = random.uniform(dITI_lowbound, dITI_upbound)
        
        # display prompt to terminal for debugging
        
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
            components=[text_cross],
        )
        cross_fix.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_crossen
        if not stim_map["cross_en"]:
            matlab_send("f")
        
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
            
            # *text_cross* updates
            
            # if text_cross is starting this frame...
            if text_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_cross.frameNStart = frameN  # exact frame index
                text_cross.tStart = t  # local t and not account for scr refresh
                text_cross.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_cross, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_cross.started')
                # update status
                text_cross.status = STARTED
                text_cross.setAutoDraw(True)
            
            # if text_cross is active this frame...
            if text_cross.status == STARTED:
                # update params
                pass
            
            # if text_cross is stopping this frame...
            if text_cross.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text_cross.tStartRefresh + timing_map["dCross"]-frameTolerance:
                    # keep track of stop time/frame for later
                    text_cross.tStop = t  # not accounting for scr refresh
                    text_cross.tStopRefresh = tThisFlipGlobal  # on global time
                    text_cross.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_cross.stopped')
                    # update status
                    text_cross.status = FINISHED
                    text_cross.setAutoDraw(False)
            
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
            components=[string_prompt_disp],
        )
        prompt.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        string_prompt_disp.setText(stim_map["string_prompt"])
        # Run 'Begin Routine' code from code_matlab_e
        matlab_send("e")
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
        
        # --- Prepare to start Routine "blank" ---
        # create an object to store info about Routine blank
        blank = data.Routine(
            name='blank',
            components=[blank_screen],
        )
        blank.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_matlab_m
        matlab_send("m")
        # store start times for blank
        blank.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        blank.tStart = globalClock.getTime(format='float')
        blank.status = STARTED
        thisExp.addData('blank.started', blank.tStart)
        blank.maxDuration = None
        # keep track of which components have finished
        blankComponents = blank.components
        for thisComponent in blank.components:
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
        
        # --- Run Routine "blank" ---
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
        blank.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blank_screen* updates
            
            # if blank_screen is starting this frame...
            if blank_screen.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blank_screen.frameNStart = frameN  # exact frame index
                blank_screen.tStart = t  # local t and not account for scr refresh
                blank_screen.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blank_screen, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blank_screen.started')
                # update status
                blank_screen.status = STARTED
                blank_screen.setAutoDraw(True)
            
            # if blank_screen is active this frame...
            if blank_screen.status == STARTED:
                # update params
                pass
            
            # if blank_screen is stopping this frame...
            if blank_screen.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > blank_screen.tStartRefresh + timing_map["dBlank"]-frameTolerance:
                    # keep track of stop time/frame for later
                    blank_screen.tStop = t  # not accounting for scr refresh
                    blank_screen.tStopRefresh = tThisFlipGlobal  # on global time
                    blank_screen.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blank_screen.stopped')
                    # update status
                    blank_screen.status = FINISHED
                    blank_screen.setAutoDraw(False)
            
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
                blank.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in blank.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "blank" ---
        for thisComponent in blank.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for blank
        blank.tStop = globalClock.getTime(format='float')
        blank.tStopRefresh = tThisFlipGlobal
        thisExp.addData('blank.stopped', blank.tStop)
        # the Routine "blank" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "response" ---
        # create an object to store info about Routine response
        response = data.Routine(
            name='response',
            components=[key_response_disp, mouse],
        )
        response.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        key_response_disp.setText(stim_map["key_prompt"])
        # Run 'Begin Routine' code from code_matlab_r
        matlab_send("r")
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        gotValidClick = False  # until a click is received
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
            # *mouse* updates
            
            # if mouse is starting this frame...
            if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mouse.frameNStart = frameN  # exact frame index
                mouse.tStart = t  # local t and not account for scr refresh
                mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('mouse.started', t)
                # update status
                mouse.status = STARTED
                mouse.mouseClock.reset()
                prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
            if mouse.status == STARTED:  # only update if started and not finished!
                buttons = mouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        pass
                        x, y = mouse.getPos()
                        mouse.x.append(x)
                        mouse.y.append(y)
                        buttons = mouse.getPressed()
                        mouse.leftButton.append(buttons[0])
                        mouse.midButton.append(buttons[1])
                        mouse.rightButton.append(buttons[2])
                        mouse.time.append(mouse.mouseClock.getTime())
                        
                        continueRoutine = False  # end routine on response
            
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
        # store data for loop_maintrial (TrialHandler)
        loop_maintrial.addData('mouse.x', mouse.x)
        loop_maintrial.addData('mouse.y', mouse.y)
        loop_maintrial.addData('mouse.leftButton', mouse.leftButton)
        loop_maintrial.addData('mouse.midButton', mouse.midButton)
        loop_maintrial.addData('mouse.rightButton', mouse.rightButton)
        loop_maintrial.addData('mouse.time', mouse.time)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "button_record" ---
        # create an object to store info about Routine button_record
        button_record = data.Routine(
            name='button_record',
            components=[fb_disp, fb_break, mouse_fb],
        )
        button_record.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_fb
        global block_fb
        global fb_text
        global text_break
        global skip_break
        
        mouse_rawval = mouse.getPressed()
        mouse_correct = int(mouse_rawval == stim_map["map_correct"])
        try:
            if  mouse_rawval == mouse_map["none"]:
                # add timeout text, decrement loop, enable fixation
                fb_text = 'Response took too long. Press middle mouse button to continue.'
                timing_map["dFb"] = TIMEOUT_DURATION
                stim_map["loop_iter"] -= 1
                stim_map["cross_en"] = False
                matlab_send("timeout")
            elif mouse_correct:
                timing_map["dFb"] = 0
                block_fb += u'\u2713 '
            else:
                timing_map["dFb"] = 0
                block_fb += u'\u2715 ' 
        except:
            print('ERROR: no mouse keyboard component written.')
        
        
        # increment loop, enable cross if loop reaches max
        stim_map["loop_iter"] += 1
        
        # display loop information 
        print("loop_iter =", stim_map["loop_iter"], '\n',
              "loop_count =", stim_map["loop_count"], '\n')
              
        # increment characters after specified loop count
        if stim_map["loop_iter"] == stim_map["loop_count"]:
            # display countdown unless end of experiment
            skip_break = (stim_map["char_length"] == MAX_CHARACTERS)
            # adjust variables for looping scheduler
            stim_map["loop_iter"] = 0
            stim_map["char_length"] += CHARACTER_INCREMENT
            # reenable fixation
            stim_map["cross_en"] = False
            timing_map["dFb"] = DEFAULT_FEEDBACK
            # display text during break
            fb_text = 'feedback:\n' + block_fb[:int(len(block_fb)/2)] + '\n' + block_fb[int(len(block_fb)/2):]
            text_break = "relax: test will resume in 20 seconds." if not skip_break else "the experiment has finished."
            
            # send signal to MATLAB showing it is a fb, ignore
            matlab_send("fb")
        fb_disp.setColor([1.0000, 1.0000, 1.0000], colorSpace='rgb')
        fb_disp.setText(fb_text)
        fb_break.setText(text_break)
        # setup some python lists for storing info about the mouse_fb
        gotValidClick = False  # until a click is received
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
            # Run 'Each Frame' code from code_fb
            if mouse_fb.getPressed() == mouse_map["middle"]:
                continueRoutine = False
                break
            
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
            
            # *fb_break* updates
            
            # if fb_break is starting this frame...
            if fb_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fb_break.frameNStart = frameN  # exact frame index
                fb_break.tStart = t  # local t and not account for scr refresh
                fb_break.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fb_break, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fb_break.started')
                # update status
                fb_break.status = STARTED
                fb_break.setAutoDraw(True)
            
            # if fb_break is active this frame...
            if fb_break.status == STARTED:
                # update params
                pass
            
            # if fb_break is stopping this frame...
            if fb_break.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fb_break.tStartRefresh + timing_map["dFb"]-frameTolerance:
                    # keep track of stop time/frame for later
                    fb_break.tStop = t  # not accounting for scr refresh
                    fb_break.tStopRefresh = tThisFlipGlobal  # on global time
                    fb_break.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fb_break.stopped')
                    # update status
                    fb_break.status = FINISHED
                    fb_break.setAutoDraw(False)
            # *mouse_fb* updates
            
            # if mouse_fb is starting this frame...
            if mouse_fb.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mouse_fb.frameNStart = frameN  # exact frame index
                mouse_fb.tStart = t  # local t and not account for scr refresh
                mouse_fb.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse_fb, 'tStartRefresh')  # time at next scr refresh
                # update status
                mouse_fb.status = STARTED
                mouse_fb.mouseClock.reset()
                prevButtonState = mouse_fb.getPressed()  # if button is down already this ISN'T a new click
            
            # if mouse_fb is stopping this frame...
            if mouse_fb.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > mouse_fb.tStartRefresh + timing_map["dFb"]-frameTolerance:
                    # keep track of stop time/frame for later
                    mouse_fb.tStop = t  # not accounting for scr refresh
                    mouse_fb.tStopRefresh = tThisFlipGlobal  # on global time
                    mouse_fb.frameNStop = frameN  # exact frame index
                    # update status
                    mouse_fb.status = FINISHED
            
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
        
        # ensure that fb is reset to 0
        timing_map["dFb"] = 0
        fb_text_size = 0.16
        if len(block_fb) >= (stim_map["loop_count"] * 2):
            block_fb = ""
            text_break = ""
        # print out debugging information
        print("timing information is: \n")
        print("timing_map[\"dCross\"]:", timing_map["dCross"])
        print("timing_map[\"dBlank\"]:", timing_map["dBlank"])
        print("timing_map[\"dPrompt\"]:", timing_map["dPrompt"])
        print("timing_map[\"dResponse\"]:", timing_map["dResponse"])
        print("timing_map[\"dFb\"]:", timing_map["dFb"])
        print("timing_map[\"dITI\"]:", timing_map["dITI"])
        
        print(mouse_rawval, "was pressed")
        print("current loop that ended is:", currentLoop.thisTrial)
        
        # log reaction time and accuracy percentage
        try:
            thisExp.addData('reactionTime', mouse.time[-1])
        except:
            thisExp.addData('reactionTime', "timed out")
        thisExp.addData('accuracy', "correct" if mouse_correct else "incorrect")
        thisExp.addData('prompt', stim_map["string_prompt"])
        thisExp.addData('character', stim_map["key_prompt"])
        
        # rewind trial to overwrite timeout data
        if mouse_rawval == mouse_map["none"]:
            currentLoop.rewindTrials()
        else:
            RT_list.append(mouse.time[-1])
            ACC_list.append(mouse_correct)
            
        # store data for loop_maintrial (TrialHandler)
        # the Routine "button_record" was not non-slip safe, so reset the non-slip timer
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
        # skip Routine countdown if its 'Skip if' condition is True
        countdown.skipped = continueRoutine and not (skip_break)
        continueRoutine = countdown.skipped
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
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
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
        # Run 'End Routine' code from code
        skip_break = True
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if countdown.maxDurationReached:
            routineTimer.addTime(-countdown.maxDuration)
        elif countdown.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-10.000000)
        
        # --- Prepare to start Routine "ITI" ---
        # create an object to store info about Routine ITI
        ITI = data.Routine(
            name='ITI',
            components=[black_screen],
        )
        ITI.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_ITI
        print("value is", mouse.getPressed())
        if (mouse.getPressed() != mouse_map["none"]) and (mouse.getPressed() != mouse_map["middle"]):
            matlab_send("ITI")
        # store start times for ITI
        ITI.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        ITI.tStart = globalClock.getTime(format='float')
        ITI.status = STARTED
        thisExp.addData('ITI.started', ITI.tStart)
        ITI.maxDuration = None
        # keep track of which components have finished
        ITIComponents = ITI.components
        for thisComponent in ITI.components:
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
        
        # --- Run Routine "ITI" ---
        # if trial has changed, end Routine now
        if isinstance(loop_maintrial, data.TrialHandler2) and thisLoop_maintrial.thisN != loop_maintrial.thisTrial.thisN:
            continueRoutine = False
        ITI.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *black_screen* updates
            
            # if black_screen is starting this frame...
            if black_screen.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                black_screen.frameNStart = frameN  # exact frame index
                black_screen.tStart = t  # local t and not account for scr refresh
                black_screen.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(black_screen, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'black_screen.started')
                # update status
                black_screen.status = STARTED
                black_screen.setAutoDraw(True)
            
            # if black_screen is active this frame...
            if black_screen.status == STARTED:
                # update params
                pass
            
            # if black_screen is stopping this frame...
            if black_screen.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > black_screen.tStartRefresh + timing_map["dITI"]-frameTolerance:
                    # keep track of stop time/frame for later
                    black_screen.tStop = t  # not accounting for scr refresh
                    black_screen.tStopRefresh = tThisFlipGlobal  # on global time
                    black_screen.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'black_screen.stopped')
                    # update status
                    black_screen.status = FINISHED
                    black_screen.setAutoDraw(False)
            
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
                ITI.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ITI.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ITI" ---
        for thisComponent in ITI.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for ITI
        ITI.tStop = globalClock.getTime(format='float')
        ITI.tStopRefresh = tThisFlipGlobal
        thisExp.addData('ITI.stopped', ITI.tStop)
        # the Routine "ITI" was not non-slip safe, so reset the non-slip timer
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
    
    # --- Prepare to start Routine "calc_end_stat" ---
    # create an object to store info about Routine calc_end_stat
    calc_end_stat = data.Routine(
        name='calc_end_stat',
        components=[],
    )
    calc_end_stat.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_end_block
    # demarcate MATLAB ending
    matlab_send("end")
    
    # calculate running response time and accuracy
    rt_arr = np.array(RT_list)
    acc_arr = np.array(ACC_list)
    disp_rt = int(rt_arr.mean() * 1000)
    disp_accuracy = int(acc_arr.mean() * 100)
    
    end_text = "Thank you for your time! You had an average reaction time of " + str(disp_rt) + " ms and an accuracy of " + str(disp_accuracy) + "%."
    # store start times for calc_end_stat
    calc_end_stat.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    calc_end_stat.tStart = globalClock.getTime(format='float')
    calc_end_stat.status = STARTED
    thisExp.addData('calc_end_stat.started', calc_end_stat.tStart)
    calc_end_stat.maxDuration = None
    # keep track of which components have finished
    calc_end_statComponents = calc_end_stat.components
    for thisComponent in calc_end_stat.components:
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
    
    # --- Run Routine "calc_end_stat" ---
    calc_end_stat.forceEnded = routineForceEnded = not continueRoutine
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
            calc_end_stat.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in calc_end_stat.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "calc_end_stat" ---
    for thisComponent in calc_end_stat.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for calc_end_stat
    calc_end_stat.tStop = globalClock.getTime(format='float')
    calc_end_stat.tStopRefresh = tThisFlipGlobal
    thisExp.addData('calc_end_stat.stopped', calc_end_stat.tStop)
    thisExp.nextEntry()
    # the Routine "calc_end_stat" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "end" ---
    # create an object to store info about Routine end
    end = data.Routine(
        name='end',
        components=[end_text_block, mouse_end],
    )
    end.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    end_text_block.setText(end_text)
    # setup some python lists for storing info about the mouse_end
    mouse_end.x = []
    mouse_end.y = []
    mouse_end.leftButton = []
    mouse_end.midButton = []
    mouse_end.rightButton = []
    mouse_end.time = []
    gotValidClick = False  # until a click is received
    # store start times for end
    end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    end.tStart = globalClock.getTime(format='float')
    end.status = STARTED
    thisExp.addData('end.started', end.tStart)
    end.maxDuration = None
    # keep track of which components have finished
    endComponents = end.components
    for thisComponent in end.components:
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
    
    # --- Run Routine "end" ---
    end.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *end_text_block* updates
        
        # if end_text_block is starting this frame...
        if end_text_block.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            end_text_block.frameNStart = frameN  # exact frame index
            end_text_block.tStart = t  # local t and not account for scr refresh
            end_text_block.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end_text_block, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_text_block.started')
            # update status
            end_text_block.status = STARTED
            end_text_block.setAutoDraw(True)
        
        # if end_text_block is active this frame...
        if end_text_block.status == STARTED:
            # update params
            pass
        # *mouse_end* updates
        
        # if mouse_end is starting this frame...
        if mouse_end.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_end.frameNStart = frameN  # exact frame index
            mouse_end.tStart = t  # local t and not account for scr refresh
            mouse_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_end, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_end.started', t)
            # update status
            mouse_end.status = STARTED
            mouse_end.mouseClock.reset()
            prevButtonState = mouse_end.getPressed()  # if button is down already this ISN'T a new click
        if mouse_end.status == STARTED:  # only update if started and not finished!
            buttons = mouse_end.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    pass
                    x, y = mouse_end.getPos()
                    mouse_end.x.append(x)
                    mouse_end.y.append(y)
                    buttons = mouse_end.getPressed()
                    mouse_end.leftButton.append(buttons[0])
                    mouse_end.midButton.append(buttons[1])
                    mouse_end.rightButton.append(buttons[2])
                    mouse_end.time.append(mouse_end.mouseClock.getTime())
                    
                    continueRoutine = False  # end routine on response
        
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
            end.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in end.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "end" ---
    for thisComponent in end.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for end
    end.tStop = globalClock.getTime(format='float')
    end.tStopRefresh = tThisFlipGlobal
    thisExp.addData('end.stopped', end.tStop)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('mouse_end.x', mouse_end.x)
    thisExp.addData('mouse_end.y', mouse_end.y)
    thisExp.addData('mouse_end.leftButton', mouse_end.leftButton)
    thisExp.addData('mouse_end.midButton', mouse_end.midButton)
    thisExp.addData('mouse_end.rightButton', mouse_end.rightButton)
    thisExp.addData('mouse_end.time', mouse_end.time)
    thisExp.nextEntry()
    # the Routine "end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
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
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
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
    expInfo = showExpInfoDlg(expInfo=expInfo)
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
