=====
Usage
=====

These scripts should be available as terminal commands without the .py extension.

--------------
capture_osc.py
--------------
usage: replay_osc.py [-h] [-f FILENAME] [-a ADDRESS] [-p PORT] [-l] [-d] [-t]

Replay OSC data stream from file. Close to save: Ctrl-C or Cmd-C

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Name of file to replay.
  -a ADDRESS, --address ADDRESS
                        OSC address to replay to.
  -p PORT, --port PORT  OSC port to listen on.
  -l, --loop            Replay over and over.
  -d, --debug           Print values being replayed.
  -t, --time-bundle     Sends using timestamped bundle format.


-------------
replay_osc.py
-------------
usage: replay_osc.py [-h] [-f FILENAME] [-a ADDRESS] [-p PORT] [-l] [-d] [-t]

Replay OSC data stream from file. Close stream with Ctrl-C or Cmd-C

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Name of file to replay.
  -a ADDRESS, --address ADDRESS
                        OSC address to replay to.
  -p PORT, --port PORT  OSC port to listen on.
  -l, --loop            Replay over and over.
  -d, --debug           Print values being replayed.
  -t, --time-bundle     Sends using timestamped bundle format.


--------------
osc_to_csv.py
--------------
usage: osc_to_csv.py [-h] FILENAME [-f FOLDER]

Convert an osc file to multiple csv files.
File names for csv are the path names.
The first column is the corresponding timestamp.

With liblo installed, osc files can be captured with :code:`oscdump [PORT] > [filename]`

arguements:
  FILEPATH              osc file path

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder   folder to save all csv into
