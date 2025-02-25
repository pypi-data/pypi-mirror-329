# What am I doing?

A simple, performance-oriented, activity tracker that flexibly connects multiple to-do lists with multiple time trackers and displays your current task and time spent in the status bar.


## Features

- Unlimited flexible combinations of to-do lists and time tracking systems  
- Flexibly nested lists  
- Inactivity detection that automatically pauses time tracking 
- Pomodoro timer  
- Task prioritization
- Time targets: set a minimum or maximum time for any task or list of tasks and get reminded to follow though 
- Randomness interrupt bell (optional) to keep you on track with tracking your time
- Fast, keyboard-driven, interface 
- Offline to-do list cache 
- Tested on Ubuntu and Linux Mint with Xorg and Wayland

### Currently Supported Todo Lists

- Simple text or markdown file with indentation based sub-lists
- Any to-do list that supports [CalDav todos](https://en.wikipedia.org/wiki/CalDAV) 
- [todotxt format](http://todotxt.org/)
- [TaskWarrior](https://taskwarrior.org/)
- [Vikunja](https://www.vikunja.io)
- [Photosynthesis Timetracker](https://github.com/Photosynthesis/Timetracker/)  

### Currently Supported Time Trackers

- CSV file  
- [AcivityWatch](https://www.activitywatch.net)      
- [Photosynthesis Timetracker](https://github.com/Photosynthesis/Timetracker/)  
- [TimeWarrior](https://timewarrior.net)



<!-- ## Installation pipx 
If you don't have pipx install 
```
sudo apt install pipx
pipx ensurepath
``` -->


## Installation

- Install following dependencies:
```
sudo apt install gir1.2-appindicator3-0.1 meson libdbus-glib-1-dev patchelf python3.12-venv
```

- Clone this repo into some out-of-the-way directory (referred to as `YOUR_INSTALL_PATH`) 
- Change to `YOUR_INSTALL_PATH` directory with `cd /path/to/where/you/cloned/what-am-i-doing`
- Set up a python [venv](https://docs.python.org/3/tutorial/venv.html)
```        
python3 -m venv .venv/what-am-i-doing  
source .venv/what-am-i-doing/bin/activate 
```
- Install required python modules: `pip install -r requirements.txt`
- Run `python3 main.py` and check for errors    
- Open settings and add your to-do list and time tracker details
- Add the following to your startup applications (if using venv) `bash -c "source .venv/what-am-i-doing/bin/activate; python3 /YOUR_INSTALL_PATH/src/what-am-doing/main.py"` (if not using venv simply use `python3 main.py`)

## Keybindings

To set up a keybinding to open your tasks on Ubuntu or Linux Mint, open **Setting > Keyboard > Keyboard Shortcuts > Custom Shortcuts**, set the **command** to `/YOUR_INSTALL_PATH/src/what-am-doing/signal.sh`, and pick whatever key combo you'd like.

### Task Window Keybindings


- `f11` Toggle fullscreen
- `Esc` Close task window
- `Enter` Start top task (or make a new task if no results)
- `Ctrl + P` **Pause** current task
- `Ctrl + D` Pause current task and mark it **Done**
- `Ctrl + X` Cancel current task
- `Ctrl + N` **New** task
- `Ctrl + R` **Refresh** todolists


<!-- ## Contributing
Package it for your operating system.
Write a connector for your favorite to-do list or time tracker -->
