IMPORTANT NOTES
===============
The state of the repository as it was at the end of assignment 4 is saved under the tag **v1.0.0**. There should be no need to revert to it, though. To get your site ready for assignment 5:

1.  Create a new directory in your public_html/ folder called 206-ass5 or something like that.
2.  Remove or rename the .git directory in your old comp206/ (or whatever) directory, so you don't do stuff in this directory by accident (the old sites need to stay the same until the TAs finish grading them).
3.  `cd` into the new directory and run `git init`. Then run `git add remote origin git@github.com:dellsystem/comp206.git`, then pull with `git pull origin master`.

Overview of the model
---------------------

Basically how things will work and shit. CURRENTLY IN PROGRESS ... edit this part if anything needs changing

*   The process starts with **login.html**. The user will have to enter the username/password combination specified in **users.csv** (ash/ketchum plz?). The username and password are then sent to the login.cgi file through a post request.  There are two possibilities:
    *   The correct combination is entered. In that case, the login.cgi file will show us the first room page or something? Or a link to it? Not sure.
    *   The combination entered is not correct. **login.cgi** will print out the contents of **login_error.html** (to be created), which will indicate this failure and provide the user with a link back to the welcome page.
*   The room pages are all generated solely by a python script (**show\_activity.py** or something - it makes sense to combine them into one). The python script will ONLY generate a page if 1) it is invoked by **login.cgi** (or something? basically, when the user logs in, we could do this a different way) or 2) it receives post data from another room (either in our game or another group's game). The thing is, how do we know when we receive post data? The default way would be to check for a "submit" (in PHP - isset($_POST['submit'])) but since it isn't specified that the submit buttons have to be named submit in the assignment, we can't really assume that they will be named that. So we could just check that the points field has value, and if it does, then assume that we should be displaying the room page. Some extra notes on this part:
    *   If the value of the points field is NOT an integer, take the value to be 0. 
    *   Any inventory items that were not created by us are shown as "Old space junk", with a corresponding image. Maybe the first 10 characters of the name (with a trailing ellipsis) can be shown in parentheses or something. Of course, they'll keep their original name in the hidden input field, so when we pass them on to other groups they get the original item.
    *   Any inventory items that belong in this game have a corresponding image as well, and possibly a mouse-over description or something (i.e. title text).
*   When a user tries to make a sale or purchase, **show_activity.py** is again invoked (actually, we could split it up into 2 ... it might be more logical, I guess we'll see). That's it for now I don't feel like thinking about this anymore.

Things to pay attention to
--------------------------

*   Atomicity
*   Sanitising and validating data
*   Code reuse (we don't want to have to copy and paste shit, especially HTML)
*   The model-view-controller concept - .html files will handle all the templating crap (i.e. all the html output - views), the controller will handle all the actions (mostly form submission), and I guess the inventory.csv file will be the essence of the model

Random crap we don't really need but it's here anyways so whatever
------------------------------------------------------------------

Images:

*   http://sos.noaa.gov/images/Solar_System/moon.jpg
*   http://www.spacewallpapers.net/wallpapers/displayimage.php?pid=322&fullsize=1
*   http://dl.dropbox.com/u/18272581/206%20mockup/backgrounds/gallery_948_62_214391.jpg (MAYBE) (GET SOURCE)
*   http://content.wallpapers-room.com/resolutions/1600x1200/S/Wallpapers-room_com___Sunrise_in_Space_by_gucken_1600x1200.jpg (ALSO MAYBE)
*   http://dl.dropbox.com/u/18272581/206%20mockup/backgrounds/quantum_space_617.jpg
