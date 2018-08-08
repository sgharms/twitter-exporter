#!/usr/bin/env python3

import argparse
import sys,os,json,re
import curses
import pdb

parser = argparse.ArgumentParser(description='Provide a top-level directory')
parser.add_argument("dir", help="Top-level directoy to begin search")
args = parser.parse_args()

path = args.dir

file_list = []

def find_files(n):
    for (dirpath, dirnames, filenames) in os.walk(n, topdown=True):
        prefix = "  " * dirpath.count('/')
        if len(dirnames) > 0:
            sorted_dirnames = sorted(dirnames)
            [find_files(d) for d in sorted_dirnames]
        for file in filenames:
            file_list.append("{}/{}".format(dirpath, file))


find_files(path)
file_list.sort()

counter = 0
def draw_menu(stdscr):
    global counter
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_WHITE)
    title =""

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # tindr style. not that i ever knew. right, keep; left, pass
        color_flag = 0
        last_action = ""
        if k == curses.KEY_RIGHT:
           fn = file_list[counter]
           os.remove(fn)
           fh = open("deletables.txt", "a+")
           fh.write(title["id_str"] + "\n")
           fh.close()
           counter += 1
           color_flag = 2
           last_action = "DELETED {}!".format(fn)
        elif k == curses.KEY_LEFT:
           fh = open("deletables.txt", "a+")
           fh.write(title["id_str"] + "\n")
           fh.close()
           counter += 1
           color_flag = 4
           last_action = "Preserved!"

        stdscr.attron(curses.color_pair(color_flag))
        stdscr.attron(curses.A_BOLD)
        last_pos = (width - 1) if len(last_action) == 0 else ( width - len(last_action) - 1 )
        stdscr.addstr(0,  last_pos, last_action)


        # Declaration of strings
        statusbarstr = "Press \'q\' to exit | [{} of {}]".format(counter + 1, len(file_list))
        jsonstr = open(file_list[counter], "r").read()
        title = json.loads(jsonstr)

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(1))

        # Rendering title
        flag = 0
        for cnt, line in enumerate(json.dumps(title, indent=2, sort_keys=True).split("\n")):
            matchObj = re.match("(.*\"(full_text|created_at)\":\s+\")(.*)\"", line)
            if matchObj:
                if flag == 0:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.attroff(curses.A_BOLD)
                    stdscr.addstr(height // 2 + 2, 0, matchObj.group(3)[0:width - 1])
                    flag += 1
                else:
                    stdscr.attron(curses.color_pair(4))
                    stdscr.attron(curses.A_BOLD)
                    stdscr.addstr(height // 2 -2, 0, matchObj.group(3)[0:width - 1].strip())

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(1))
        stdscr.attroff(curses.A_BOLD)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))

        # Menu
        right_cmd =  "<RIGHT> to delete "
        left_cmd =  "<LEFT> to preserve "

        stdscr.attron(curses.A_BOLD)
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(height-2, width - len(right_cmd) - len(left_cmd), right_cmd)
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(height-2, 0, left_cmd)


        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
