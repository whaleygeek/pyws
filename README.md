pyws
====

Python worksheets for a programming workshop, first run on 12/02/2014 in Essex

1. what is a computer
2. simple turtle commands (twurtle)
3. interactive python turtle
4. stored program python turtle
5. building in minecraft using python


To get these resources for the first time:

git clone https://github.com/whaleygeek.pyws
./install


To update to the latest version:

git pull https://github.com/whaleygeek/pyws


Most of these resources have come from other workshops and activities,
and I have pulled them together into this single package as they can either
be used individiually, or together as a longer workshop.

1. "What is a computer" is a printed worksheet form of an exercise I have
run in many schools - ask the children "how many computers are in your house".

2. The "twurtle" is a tweeting turtle, without the tweeter. I ran this as
an activity in a school in Essex in 2013. The worksheet in docs is self
explanatory.

3. "Interactive python" - get the children to progress from the twurtle into
real python and draw simple shapes, and introduce loops (which are intentionally
not included in twurtle)

4. "Stored program python turtle" - use IDLE to save programs to a file and
build up bigger programs and re-run them several times, to show the benefits
of the stored program concept.

5. "Building with minecraft" - this only runs on the Raspberry Pi. The worksheet
is self explanatory. There is also a copy of my BMP image builder that if you
run it as: python build_mc rpi_logo.bmp   it builds a huge raspberry pi.
Also gui.py in this folder is a simple example of a tkinter program that you
press a button and it does something in minecraft. You can run this tkinter
program on a Mac or PC or another Raspberry Pi and connect over the network
to remotely control someone else's minecraft game.



It's likely that most or all of the code currently only works with python 2
on the Raspberry Pi, I haven't completely made it python3 clean yet.

The minecraft examples will only work on the Raspberry Pi, but all other
examples *should* work fine on PC or Mac or Linux.

David Whale
@whaleygeek
11/02/2014


