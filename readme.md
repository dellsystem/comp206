IMPORTANT NOTES
===============
The state of the repository as it was at the end of assignment 4 is saved under the tag **v1.0.0**. There should be no need to revert to it, though. To get your site ready for assignment 5:

1.  Create a new directory in your public_html/ folder called 206-ass5 or something like that.
2.  Remove or rename the .git directory in your old comp206/ (or whatever) directory, so you don't do stuff in this directory by accident (the old sites need to stay the same until the TAs finish grading them).
3.  `cd` into the new directory and run `git init`. Then run `git remote add origin git@github.com:dellsystem/comp206.git`, then pull with `git pull origin master`.
4.  **If you haven't done so already, add the URL of your ass5 directory to near the bottom of game.py. This is in bold because it is important.**

To do
-----

*   Make the rooms link to different sites (~wliu65/206-5/show.py for the moon, ~hbrund/whatever/show.py for dune etc)
*   Fix up items (Chantal?), price ranges, and amounts on each planet (edit inventory#.csv
*   Don't let the user enter points or prices that are not integers. In other words, validate hidden input fields. Also make sure that prices are at least 0, if we're too lazy to make them in the entered range. It doesn't really matter, but it's good to know how to do this anyway. Plus being unsecure just sucks in general.

Things to pay attention to
--------------------------

*   Atomicity (doing well with that)
*   Sanitising and validating data (LOL)
*   Code reuse (we have a working template engine so good enough) 
*   The model-view-controller concept - .html files will handle all the templating crap (i.e. all the html output - views), the controller will handle all the actions (mostly form submission), and I guess the inventory.csv file will be the essence of the model

Random crap we don't really need but it's here anyways so whatever
------------------------------------------------------------------

Images:

*   http://sos.noaa.gov/images/Solar_System/moon.jpg
*   http://www.spacewallpapers.net/wallpapers/displayimage.php?pid=322&fullsize=1
*   http://dl.dropbox.com/u/18272581/206%20mockup/backgrounds/gallery_948_62_214391.jpg (MAYBE) (GET SOURCE)
*   http://content.wallpapers-room.com/resolutions/1600x1200/S/Wallpapers-room_com___Sunrise_in_Space_by_gucken_1600x1200.jpg (ALSO MAYBE)
*   http://dl.dropbox.com/u/18272581/206%20mockup/backgrounds/quantum_space_617.jpg
