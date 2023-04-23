# LostArk-Chaos-Dungeons
An unfinished, proof of concept set of scripts to automate the infinite farming of Chaos Dungeons in Lost Ark. Similar to other Lost Ark scripts I have seen, utilizes OpenCV and PyAutoGUI to be minimally invasive. 

Run `./runner.py` and press the key 0 to start/stop the script. 

These scripts are mainly available just to showcase an interesting way to automate an otherwise tedious task that would not be worth doing manually.

## \*\*Disclaimer\*\*
This project is a proof of concept and is (and will remain) unfinished! I have provided the files here purely for educational purposes, so **I am NOT responsible for what happens to your account for using this code**. Also, I have not tested this code since `May 23, 2022`, so take the usability of this code with a grain of salt.

## Background
Chaos Dungeons are a kind of dungeon in the game [Lost Ark](https://www.playlostark.com/en-us) that reward the player with materials they can use to enhance character equipment. These dungeons can be ran infinitely, but most rewards are only dropped for the first 2 clears. Clears beyond that provide little, but not insignificant amounts of materials as monster drops. This project is meant to handle the farming of these infinite runs.

## Features
Supports:
- Auto-repairing of armor before starting a run
- Auto-entering a run
- Clearing Room 1
- Clearing Room 2 (Inconsistent)
- Recovery/Restarting a run if failed

Currently only supports clearing the first two rooms, of which the second room is not cleared consistently (but does not affect the ability to start new runs). The third room is a lot more complicated to clear as it requires locating and attacking specific structures to spawn enemies.

## Method
The project is split mainly into two parts - Interaction with the game, and detection of the game world using the minimap.

### 1) Game interaction (in `interactions.py`)
Handles clicking of GUIs, attacking, and movement. This is where the gameplay part of clearing a room is contained - Using your skill rotation to buff/heal/defend and damage enemies. Normally the dungeons are not much of a threat when manually clearing, but automated clearing of rooms does require some form of kiting to preserve HP and not lose the fight, so rudimentary kiting is implemented. Uses PyAutoGUI to simulate clicks/keypresses.

### 2) World detection (in `map_finder.py`)
Perhaps the more interesting and complicated part of the project, handles identifying objects on the map using OpenCV's template matching to define player behavior. Uses enemy/elite/boss pixel colors and their general shape on the map to extrapolate the direction in which to move the player. Also matches against the portal icon on the map to correctly move the player to the next room. Template/image matching is imprecise compared to being able to directly capture/hook into the game, but that is obviously not allowed.

`utils.py` provides the libraries and some general useful functions that the other files need.

`runner.py` is the main script to run.

## Setup
All necessary libraries should be noted in `requirements.txt`. You should probably create a Python [virtual environment](https://docs.python.org/3/tutorial/venv.html) to install these libraries into. Run `pip install -r requirements.txt` to get all the required dependencies.