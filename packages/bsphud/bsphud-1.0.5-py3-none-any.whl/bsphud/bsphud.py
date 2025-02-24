#!/usr/bin/env python

import signal
import os
import argparse
import json
import subprocess
from time import sleep
from pathlib import Path

import tkinter as tk
from tkinter import ttk

__all__ = ["run", "make_pidfile", "BSPHUD"]

class BSPHUD:
    def __init__(self):
        subprocess.check_output([
            'bspc',
            'rule',
            '-r',
            '*:*:BSPHUD',
            ])
        subprocess.check_output([
            'bspc',
            'rule',
            '-a',
            '*:*:BSPHUD',
            'manage=off'
            ])
        
        self.get_border()

        self.root = tk.Tk()
        self.root.title("BSPHUD")
        self.root.configure(background=self.border_color)
        self.hide()
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        self.pad_x = 20
        self.pad_y = 20
        self.box_width = 50
        self.box_height = 50
        self.inner_box_spacing = 10
        self.line_width = 4
        self.box_spacing = 10

        self.desktops = []
        self.focused = -1

    def get_border(self):
        self.border_color = subprocess.check_output([
            'bspc', 'config', 'focused_border_color'
            ]).decode('utf-8').upper().strip()
        self.border_width = int(subprocess.check_output([
            'bspc', 'config', 'border_width']).decode('utf-8'))

    def mainloop(self):
        self.root.mainloop()

    def show(self):
        self.shown = True
        self.root.deiconify()
        self.root.lift()
        self.root.update()

    def hide(self):
        self.shown = False
        self.root.withdraw()
        self.root.update()
        # Sometimes, when the window appears,
        # it causes the focused node to become unfocused.
        # The bellow command fixes it by focusing the focused node.
        subprocess.run([
            'bspc',
            'node',
            '-f',
            'focused'
            ])

    def handler(self, sig, frame):
        if sig== signal.SIGUSR1:
            self.update()
            self.set_size()
            self.draw()
            self.show()

        elif sig == signal.SIGUSR2:
            self.hide()

        else:
            print('huh?')

    def update(self):
        monitor = json.loads(
            subprocess.check_output(
                [
                    'bspc',
                    'query',
                    '-T',
                    '-m',
                    'focused'
                    ]
                ).decode('utf-8')
            )

        focused_desktop_id = monitor['focusedDesktopId']

        self.mon_x = monitor['rectangle']['x']
        self.mon_y = monitor['rectangle']['y']
        self.mon_width = monitor['rectangle']['width']
        self.mon_height = monitor['rectangle']['height']

        self.desktops.clear()

        for i, desktop in enumerate(monitor['desktops']):
            self.desktops.append(
                desktop['root'] is not None
                )
            if desktop['id'] == focused_desktop_id:
                self.focused = i

    def set_size(self):
        win_height = self.pad_y * 2 + self.box_height
        win_width = (
            self.pad_x * 2
            + (self.box_width + self.box_spacing) * len(self.desktops)
            )
        win_x = self.mon_x + (self.mon_width - win_width) // 2
        win_y = self.mon_y + (self.mon_height - win_height) // 2
        self.root.geometry(f"{win_width}x{win_height}+{win_x}+{win_y}")
        self.canvas.config(
            width=win_width,
            height=win_height,
            )

        self.win_width = win_width
        self.win_height = win_height

    def draw(self):
        self.canvas.delete("all")

        for i, desktop in enumerate(self.desktops):
            left = (
                self.pad_x
                + (self.box_width + self.box_spacing) * i
                )

            top = self.pad_y

            self.canvas.create_rectangle(
                (
                    left + self.inner_box_spacing,
                    top + self.inner_box_spacing
                    ),
                (
                    left + self.box_width - self.inner_box_spacing,
                    top + self.box_height - self.inner_box_spacing
                    ),
                fill=[None, 'black'][desktop],
                width=self.line_width,
                )

            if i == self.focused:
                self.canvas.create_rectangle(
                    (
                        left,
                        top
                        ),
                    (
                        left + self.box_width,
                        top + self.box_height
                        ),
                    fill=None,
                    width=self.line_width,
                    )

            self.canvas.create_rectangle(
                (0, 0),
                (self.win_width, self.win_height),
                fill=None,
                width=self.border_width * 4,
                outline=self.border_color,
                )

def make_pidfile(path):
    path.write_text(str(os.getpid()))

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-j',
        '--pidfile',
        type=Path,
        help="PID file location",
        default='/tmp/bsphud.pid'
        )
    args = parser.parse_args()

    make_pidfile(args.pidfile)
    hud = BSPHUD()

    signal.signal(signal.SIGUSR1, hud.handler)
    signal.signal(signal.SIGUSR2, hud.handler)

    while True:
        signal.pause()

if __name__ == '__main__':
    run()



