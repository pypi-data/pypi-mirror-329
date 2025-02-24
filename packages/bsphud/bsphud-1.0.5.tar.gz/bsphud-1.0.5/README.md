# BSPHUD

Desktop switcher popup for [bspwm](https://github.com/baskerville/bspwm).

- PyPI: <https://pypi.org/project/bsphud/>
- GitHub: <https://github.com/maybeetree/bsphud>

![BSPHUD screenshot](img/bsphud-scrot.png)

BSPHUD is a window that pops up in the middle of your screen
and gives an overview of the desktops on the currently focused monitor.
Each desktop is represented by a black box.
If the box is filled,
there are windows on that desktop.
The box with a ring around it is the currently focused desktop.

The idea is that you bind BSPHUD to the modifier key
(not a combination; the modifier key itself)
that you normally use for window management hotkeys,
so that BSPHUD pops up right before you're about to switch
to a different desktop,
send a window to a different monitor,
etc.

## Installation

You can install through pip, Python's package manager:

```
pip install bsphud
```

And then launch BSPHUD like so:

```
bsphud
```

or

```
python -m bsphud
```


Or you can simply copy [src/bsphud/bsphud.py](src/bsphud/bsphud.py)
to a safe location and run it with Python:

```
python bsphud.py
```

Or you can even just run it directly:

```
./bsphud.py
```

BSPHUD has no dependencies except for Python and Tkinter.
Tkinter is usually included with Python,
but sometimes it's not,
for example on minimal systems or if you compiled Python
yourself and didn't explicitly enable Tkinter.

If you're on Alpine linux, tkinter can be installed with
`apk add python3-tkinter`.

## Configuration

BSPHUD will pop up when you send it SIGUSR1
and close when you send it SIGUSR2.
Sending SIGUSR1 when the window is already open
will cause BSPHUD to refresh the state of the desktop.
BSPHUD writes its pid to `/tmp/bsphud.pid`.

Below is an example configuration with
[sxhkd](https://github.com/baskerville/sxhkd):

```sxhkdrc

# Show BSPHUD when left super is held down
Super_L + any
	kill -10 $(cat /tmp/bsphud.pid)

# Hide BSPHUD when left super is released
@Super_L + any
	kill -12 $(cat /tmp/bsphud.pid)

# If you have something like this
# (a shortcut to reload sxhkd),
# it is wise to add a delay before sending the signal,
# to prevent sxhkd from locking up
super + @Escape
	sleep 1; pkill -USR1 -x sxhkd ; notify-send sxhkd reloaded

# Any shortcuts that change 
# desktops/windows need to also send SIGUSR1
# in order to keep the BSPHUD display
# up to date with the state of the window manager

# super + <number> to switch to that desktop
# and super + shift + <number> to move window to that desktop
super + {_,shift + }{1-9,0}
	bspc {desktop -f,node -d} 'focused:^{1-9,10}' --follow; kill -10 $(cat /tmp/bsphud.pid)

# super + comma and super + period to cycle monitors
super + {_,shift} + {comma,period}
	bspc {monitor -f, node -m} {prev,next} --follow; kill -10 $(cat /tmp/bsphud.pid)

```

## Misc notes

- there needs to be a rule that tells bspwm to not manage
the BSPHUD window.
BSPHUD creates this rule automatically.
Since the window is unmanaged, the border
is actually drawn by BSPHUD itself,
not by bspwm.
BSPHUD queries your preferred border width and color
using `bspc config`.

- If you plan to run multiple instances of BSPHUD
(e.g. multiuser system),
it is wise to change the location of the PID file.
For example:
```
python -m bsphud --pidfile /var/run/user/$(id -u)/bsphud.pid
```

- bug: If you send a SIGUSR signal to BSPHUD immediately after
launching it, it might crash.
Working on it!

- BSPHUD is inspired by the venerable [XFCE](https://xfce.org/)
desktop envrionment,
which has a comparable feature built-in.

