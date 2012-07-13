# Beat Bricks

A LEGO Step Sequencer made at [ADVANCE HACKATHON][1]. There's a [video][2].

 [1]: http://hackathon.advance-conference.com/
 [2]: https://vimeo.com/45026119


## Disclaimer

This is a hackathon project. It was made during a weekend and a few evenings the week after.
It's basically a proof of concept, so please don't expect it to be easy to set up or even
ready for production use. You'll probably have to tweak the code a little to adapt it to the
camera you're using and the lighting conditions. Even if you know what you're doing, it takes
some time to get it running. I still think that you can have some fun playing with it, like I
had creating it.


## How It Works

In a video image of the LEGO plate, every potential brick position is evaluated for its color.
Depending on the detected color, a note in the step sequencer pattern is added or removed. These
changes to the step sequencer pattern are published as OSC messages. The actual sequencer is a
separate process that listens to these OSC messages, recreates the pattern from them and sends
out MIDI notes for the pattern at 120 bpm.

In case you're wondering: I took the detour through OSC and a separate process for latency
reasons. In the separate process the MIDI messages can be triggered with much lower latency than
in a "green" Python thread.


## What You Need

<!-- Hardware -->

* A 32x32 pin LEGO plate
* Some 2x2 LEGO bricks
* A webcam (I used a Logitech C270)
* Adhesive tape, preferrably double-faced
* Some basic hacking skills

<!-- MIDI Stuff -->

* A MIDI loopback device (IAC, MIDI Yoke etc.)
* A MIDI-based sound generator (Ableton Live, pure data, Rosegarden etc.)

<!-- Software -->

* Python
* OpenCV Python module
* pyliblo
* pyPortMidi


## How To Set It Up

1. Tape the webcam to a wall cupboard in your kitchen.
2. Tape the LEGO plate to the countertop below the webcam.
3. Make sure that the plate is well-lit (bright, from above, without shadows).
4. Connect the webcam to your laptop.
5. Run `python initializer.py` to mark the position of the LEGO plate in the webcam image:
   In the window that appears, click the four corners of the plate counterclockwise.
   Start with the corner that is on the lower left when you're standing in front of it.
   That's not necessarily the lower left corner in the image, since it might be rotated.
   After the fourth click, the program should end and create a file called `rect.json`.
6. Run `python step.py`. This is the actual sequencer that listens to the OSC messages and
   sends out MIDI notes.
7. Run `python lego.py` in a separate terminal. This is the program that detects bricks in
   the camera image and creates an OSC message for every change. In the window that opens,
   you should see a square picture of the LEGO plate.


## Troubleshooting

* Instead of running `python step.py` you can run `oscdump 8765` (it comes with pyliblo) at
  first. If you don't see it printing messages like `/pattern/set 1 4` when putting a brick
  on the plate, the brick detection in `lego.py` isn't working correctly. If you see these
  messages, but don't hear any sound, there's a problem with you MIDI setup and sound device.
