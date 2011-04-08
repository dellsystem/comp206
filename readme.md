IMPORTANT NOTES
===============
The state of the repository as it was at the end of assignment 4 is saved under the tag **v1.0.0**. There should be no need to revert to it, though. To get your site ready for assignment 5:

1.  Create a new directory in your public_html/ folder called 206-ass5 or something like that.
2.  Remove or rename the .git directory in your old comp206/ (or whatever) directory, so you don't do stuff in this directory by accident (the old sites need to stay the same until the TAs finish grading them).
3.  `cd` into the new directory and run `git init`. Then run `git remote add origin git@github.com:dellsystem/comp206.git`, then pull with `git pull origin master`.
4.  **If you haven't done so already, add the URL of your ass5 directory to near the bottom of game.py. This is in bold because it is important.**

To do
-----

*   All 5 inventory input fields should show up regardless of whether or not there is an item to fill them with
*   If points = 0, user can't do anything, even sell items ? Look into that
*   Pass on Space Junk items to other rooms unchanged (i.e. make them keep their original names)
*   Make the rooms link to different sites (~wliu65/206-5/show.py for the moon, ~hbrund/whatever/show.py for dune etc)
*  <del> Fix up items (Chantal?), price ranges, and amounts on each planet (edit inventory#.csv </del>
*   <del>Don't let the user enter points or prices that are not integers. In other words, validate hidden input fields. Also make sure that prices are at least 0, if we're too lazy to make them in the entered range. It doesn't really matter, but it's good to know how to do this anyway. Plus being unsecure just sucks in general.</del> **Validation mostly done (see if you can break it; if you can, the code is near the top of game.py, fix it plz)**

Things to pay attention to
--------------------------

*   Atomicity (doing well with that)
*   Sanitising and validating data (getting there)
*   Code reuse (we have a working template engine so good enough) 
*   The model-view-controller concept 
