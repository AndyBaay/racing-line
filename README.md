## Setting up env
- Make sure you are in the root directory of this repo (i.e. /racing-line )
  - Running `pwd` should show a path ending in /racing-line
- Run `python3 -m venv venv`
- Run `source venv/bin/activate` to activate the virtual env
- Run `pip install -r requirements.txt`

That should setup your python environment. Confirm it is working by running `python racingline/main.py`

## Using the track editor

From the root directory run:
```bash
python racingline/editor.py
```
This will bring up a pygame window where you can draw points to create a track.

Draw the outer track boundary first, by clicking and adding points until you get back to the orignal point.

Once you complete a boundry it will turn a different color to confirm it. Then you can draw the innner line.

Once both lines are drawn click the save button. It will save the track definition to a an arbitrary json file and 
provide the name in the console.

## Sources

- https://dspace.mit.edu/bitstream/handle/1721.1/64669/706825301-MIT.pdf
- https://math.stackexchange.com/questions/289575/car-racing-how-to-calculate-the-radius-of-the-racing-line-through-a-turn-of-var
