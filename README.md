# player-simulator

Platform allowing easy analysis of DeepMind's algorithm **DQN** learning to play Mario Bros.
Application provides neural network design tool and statistical tools for analysis.

## 1. Installation (Ubuntu)
Mario gameplay is emulated using FCEUX.
```
# First, install python dependencies and fceux emulator package:
sudo apt-get install python-pip python-dev python-tk build-essential git fceux
# Checkout this repository:
git pull https://github.com/kelsohmm/player-simulator.git
cd player-simulator
# Install required packages:
pip install -r requirements.txt
# Run application:
python gui_main.py
```

## 2. Creating new session
![Image](https://i.imgur.com/cTsw38P.png)
First, select an empty directory for you new session in the popup window.
Next, choose your neural network architecture and hiperparameters.  
**Choose wisely - you can't change them later!**

## 3. Session control window
![Image](https://i.imgur.com/KZpBFi0.png)

The session control window is divided into 3 sections

**a) Left section**  
Allows for controlling algorithm runtime parameters and starting/stoping the learning session.
Running the simulation will also open fceux emulator window

---

**b) Center section**  
Displays overall statistics and charts for all played games.
![Image](https://i.imgur.com/i0hLcG0.png)

**c) Right section**  
Display statistics and charts for one selected game from history. Allows also for watching the game replay.
![Image](https://i.imgur.com/r3TWnwZ.png)
![Image](https://i.imgur.com/GyueMWM.png)
