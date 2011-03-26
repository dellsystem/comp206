<?php
// SO I DON'T HAVE TO COPY AND PASTE HTML OKAY
// Just for now
$mode = $_GET['mode'];

// These are all temp hacks to make the creation process easier
// The actual site will not be in PHP, of course ...
if ( isset($_POST['submit']) ) {
    // Checking for username = demo, password = demo
    if ( $_POST['username'] == 'demo' && $_POST['password'] == 'demo' ) {
        $mode = 'room1';
    } else {
        // Go back to the login page
        $mode = 'login';
    }
}

switch ($mode) {
    case 'login':
        break;
    case 'credits':
        break; // ugh PHP
    case 'room1':
        $title = 'the moon';
        break;
    case 'room2':
        $title = 'dune';
        break;
    case 'room3':
        $title = 'the orion nebula';
        break;
    case 'room4':
        $title = 'the international space station (?)';
        break;
    case 'room5':
        $title = 'eleyine\'s room';
        break;
    default:
        $mode = 'welcome';
        break;
}
// make it easier to manage titles and modes
if ( !isset($title) ) {
    $title = $mode;
}
?>

<!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7 ]> <html class="no-js ie6" lang="en"> <![endif]-->
<!--[if IE 7 ]>    <html class="no-js ie7" lang="en"> <![endif]-->
<!--[if IE 8 ]>    <html class="no-js ie8" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8">

    <!-- Always force latest IE rendering engine (even in intranet) & Chrome Frame
         Remove this if you use the .htaccess -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

    <title>SPACE TRADERS: <?php echo $title; ?></title>
    <meta name="description" content="Space Traders! An exciting web based commodity trading game.">
    <meta name="author" content="Eleyine ZAROUR">

    <!-- Mobile viewport optimized: j.mp/bplateviewport -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="includes/reset.css" type="text/css" />
    <link rel="stylesheet" href="includes/style.css" type="text/css" />
    <script src="includes/modernizr-1.7.min.js"></script>
</head>

<!-- body IDs are used for specific background images -->
<body class="room" id="<?php echo $mode; ?>">
    <div id="wrap">
    	  <header id="header">
          <h1><a href="index.php"><img src="title.png" alt="Spacetraders" title="Spacetraders" /></a></h1>
          <nav id="menu">
            <ul>
                <li><a href="index.php">Home</a></li>
                <li><a href="index.php?mode=login">Login</a></li>
                <li><a href="index.php?mode=credits">Credits</a></li>
            </ul>
            <div id="clock">
					<applet CODE="LiteClockApp.class" 
						WIDTH= 100px 
						HEIGHT=70px 
						FORE='105,245,255' > 
							Your browser does not support java.
					</applet>
				</div>
          </nav>
        </header>

        <div id="content">
        <div id="page" class="opacity-80">
        <div class="page-header"><?php echo $title; ?></div>
        <div class="page-body"><?php
        switch ($mode) {
            case 'login':
                echo '<p>For now, just enter username: <code>demo</code> and password: <code>demo</code> to access the room shit</p>';
                echo '<div class="form"><form method="post" action="">';
                echo '<p class="username"><label for="username">Username</label> &nbsp;<input type="text" name="username" id="username" /></p><br />';
                echo '<p class="password"><label for="password">Password</label> &nbsp;<input type="password" name="password" id="password" /></p>';
                echo '<p class="submit"><input type="submit" name="submit" value="SUBMIT" class="awesome blue large" /></p></div>
                </form>';
                break;
            case 'credits':
                echo '<p><strong>Person 1</strong><br />Person 1 will put a brief description of his/her room here, and optionally a link to a personal webpage.</p>';
                echo '<p><strong>Person 2</strong><br />Person 2 will put a brief description of his/her room here, and optionally a link to a personal webpage.</p>';
                echo '<p><strong>Person 3</strong><br />Person 3 will put a brief description of his/her room here, and optionally a link to a personal webpage.</p>';
                echo '<p><strong>Person 4</strong><br />Person 4 will put a brief description of his/her room here, and optionally a link to a personal webpage.</p>';
                echo '<p><strong>Person 5</strong><br />Person 5 will put a brief description of his/her room here, and optionally a link to a personal webpage.</p>';
                break;
            case 'room1':
                echo '<p>So the first place you land upon leaving Earth is the moon. Which makes sense, really, seeing as it\'s closer to Earth than any of the other things.</p>';
                echo '<p>What can you do here, besides marvel at your sudden weight loss? Well, the main attractions on this desolate moonscape are the trading of illicit moon dust and the collecting of green cheese. Luckily for you, you don\'t even have to get your hands dirty if you want to acquire some delicious green cheese - you can buy some from the local traders for almost nothing. Unfortunately, that is also how much green cheese is valued outside of the moon, so don\'t expect to get rich buying and selling this commodity.</p>';
                echo 'Once you get bored of the moon, go ahead and venture to another region. Note that every time you travel, you face the risk of getting hijacked by interstellar pirates, so beware. Maybe you can buy things that lessen your risk of being attacked. Click the "go right" and "go left" icons to follow the recommended path, or venture off on your own by selecting any region (even this one! Go on, try it).';
                $menu = true;
                break;
            case 'room2':
                echo 'The background image is a sand dune because 1) I\'ve never read dune; 2) sand dunes are awesome; and 3) Harry is a nerd. Replace this background image with a more appropriate one as you wish (although I really can\'t think of anything more appropriate than a sand dune).';
                echo '<p>At the moment, it\'s possible to go to a planet/thing without first logging in. That is not good, but it doesn\'t matter, because this PHP-based site is just to show what the site might look like. Ignore any PHP-related bugs, please.</p>';
                $menu = true;
                break;
            case 'room3':
                echo '<p>Welcome to the Orion Nebula! The image you (Chantal) linked in the channel was a bit small, so I found a random image of the orion nebula and put it up for now. Feel free to use whatever image you like though, of course. The Orion nebula is gorgeous so you have a ton of choices.</p>'; 
                $menu = true;
                break;
            case 'room4':
                echo '<p>Background image: some space station picture that Eleyine found. Enjoy the watermark.</p>';
                $menu = true;
                break;
            case 'room5':
                echo '<p>I don\'t know what theme you ended up deciding on, so I just put up the image you linked before because I really liked it.</p>';
                $menu = true;
                break;
            default:
                echo '<p>This will be a short paragraph describing the theme of the site, the game, etc. Basically the user is some sort of space traveler trying to make some extra money through space trade. The user starts on Earth and eventually finds his way into the far reaches of outer space blah blah.</p>';
            echo '<p>(This is just a demo site, using PHP for easier testing/etc, to showcase the template. Check out the login page, the rooms, and the credits page. If everyone is okay with the design I will put up the final version of the template on github and put up instructions on creating your room using the template (so you can modify the background and the content). Should happen by Thursday night.)</p>';
            break;
        }?>
        </div>
        </div>
        </div>
    </div>
    <?php 
        // As you can tell by this PHP magic, menu only shows up for rooms
        if ( isset($menu) ) { ?>
        <footer id="footer" class="opacity-80">
            <nav id="rooms">
              <ul class="map-thing">
              <?php
              // terrible but fuck it, it's PHP what can I do
              $images = array("moon_thumb", "dune_thumb", "orion_thumb", "iss_thumb", "sunrise_thumb");
              $names = array("The Moon", "Dune", "Orion", "ISS", "Eleyine");
              
              echo '<li class="go-button"><a class="awesome blue large" href="">&laquo; Go left</a></li>';
               // Looool loop, good on you, I was too lazy to do that 
              foreach( $images as $key => $image) {
                  $name = $names[$key];
                  $number = $key+1;
                  $current_class = ($mode == "room".$number ? "current" : "");
                  echo '<li class="'.$current_class.'">
                          <a class="image_link" href="index.php?mode=room'.$number.'">
                            <img src="images/'.$image.'.jpg" />
                          </a>
                          <a class="text_link awesome black" href="index.php?mode=room'.$number.'">
                            '.$name.'
                          </a>
                        </li>';
              }

              echo '<li class="go-button"><a class="awesome blue large" href="">Go right &raquo;</a><a class="awesome blue large" href="">Logout</a></li>';
              ?>
              </ul>
            </nav>
        </footer>
    <?php } ?>
</body>
</html>
