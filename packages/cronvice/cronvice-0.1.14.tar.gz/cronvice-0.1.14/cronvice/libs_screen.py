#!/usr/bin/env python3

from fire import Fire
from console import fg, bg
import shutil
import os
import datetime as dt
import shlex
import subprocess as sp


#=========================================================================
#
#-------------------------------------------------------------------------
#

def is_session_desktop():
    if os.environ.get('SSH_TTY'):
        return False #"SSH Terminal Session"
    elif os.environ.get('DISPLAY'):
        return True#"Desktop Session"
    else:
        return False#"Unknown Session"

#=========================================================================
#
#-------------------------------------------------------------------------
#

def enter_screen(scrname):
    """
    it enters when run from here
    """
    sessions = list_screen_sessions()
    print(sessions)
    print(scrname)
    if is_in_screen(scrname, sessions):
        CMD = f"screen -x {scrname}"
        if is_session_desktop():
            args = shlex.split(f"xterm -e bash -c '{CMD}'")
            process = sp.Popen(args,  stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            process.poll()
        else:
            args = shlex.split(f"bash -c '{CMD}'")
            res = sp.call(args)

#=========================================================================
#
#-------------------------------------------------------------------------
#

def stop_screen(scrname):
    """
    it enters when run from here
    """
    sessions = list_screen_sessions()
    #print(sessions)
    #print("-", scrname, "-")
    if is_in_screen(scrname, sessions):
        CMD = f"screen -X -S {scrname} quit"
        if is_session_desktop():
            args = shlex.split(f"xterm -e bash -c '{CMD}'")
            process = sp.Popen(args,  stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            process.poll()
        else:
            args = shlex.split(f"bash -c '{CMD}'")
            res = sp.call(args)
    else:
        print("X.. no such screen:", scrname)



#=========================================================================
#
#-------------------------------------------------------------------------
#

def list_screen_sessions():
    """
    return the existing screen sessions
    """
    try:
        result = sp.run(['screen', '-ls'], capture_output=True, text=True, check=True)
        #print(result.stdout)
        return result.stdout.strip().split('\n')[1:-1]
    except sp.CalledProcessError as e:
        #print(f"x... screen ls - error occurred: {e}")
        return None




#=========================================================================
#
#-------------------------------------------------------------------------
#

def is_in_screen(TAG, sessions):
    """
    if tag in screen list => True
    """
    if sessions is None:return False
    for i in sessions:
        #print(i, TAG, i.find(TAG) )
        if i.find(TAG) > 0:
            return True
    return False

#=========================================================================
#
#-------------------------------------------------------------------------
#


def del_job_anycommand( cron, tag):
    """
    older
    """
    ACT = False
    RMTG = f"screen -dmS {tag} " #SPACE IMPORTANT
    for job in cron:
        if job.command.find(RMTG) > 0:
            print(f"i... removing /{RMTG}/ ")#... {job}")
            cron.remove(job)
            ACT = True
    if ACT:
        cron.write()

if __name__ == "__main__":
    Fire({"e": enter_screen
        }
         )
