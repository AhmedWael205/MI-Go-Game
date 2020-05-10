Prerequisites:
Python 3.5 – 3.6
Pip install tensorflow==1.15
Pip install keras
Pip install zmq
Pip install websockets
Pip install asyncio
Pip install json

We also added a requirments.txt file in order to avoid any other version mismatch  

Start up instructions: 
1 - In Console:   python GUI.py
2- run “GUI_exe\GO Game GG.exe”   // GUI
3- 
if Mode = AI vs AI
a-	Run server: yarn start
b-	Choose icon on the right from OUR GUI
c-	In the console select whether you want to enter client name and URL or use default ones
d-	Finally accept request at the server and start the game
if Mode = AI vs Human
a-	Choose icon on the left from OUR GUI
b-  Choose the human (your) player color
a-	In the console select whether you want to enter a move log json file or not
d-  Finally start playing from the GUI
  
N.B:
The agent is currently configured to be as fast as possible while being reasonably smart, however it can be modified to be smarter but much slower by:
In game.py line 37, the agent is initialized as follows  
self.Agent = AIplayer(.h5FileName)
 
However, changing it to
self.Agent = AIplayer(h5FileName, MCTS=True, mctSims=n)

will make it smart but slower as long as  600 <= n <= 1600, noting that a single simulations takes 0.06 seconds, we recommend leaving it to the default setting in order not to exceed the 15 minutes time limit while being reasonably intelligent. Any value for n outside the range will be either slower than acceptable or worse than the default setting.










