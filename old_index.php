<?php
// SO I DON'T HAVE TO COPY AND PASTE HTML OKAY
// Just for now
$mode = $_GET['mode'];

switch ($mode) {
    case 'login':
        break;
    case 'credits':
        break; // ugh PHP
    case 'room1':
        $title = 'the moon';
        break;
    case 'room2':
        $title = 'arrakis';
        break;
    case 'room3':
        $title = 'the orion nebula';
        break;
    case 'room4':
        $title = 'shatner space station';
        break;
    case 'room5':
        $title = 'Memento Mori';
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
    <meta name="author" content="Clarence, Chantal, Eleyine, Harry, and Wendy">

    <!-- Mobile viewport optimized: j.mp/bplateviewport -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="includes/reset.css" type="text/css" />
    <link rel="stylesheet" href="includes/style.css" type="text/css" />
    <script src="includes/modernizr-1.7.min.js"></script>
</head>

<!-- body IDs are used for specific background images -->
<body class="room" id="<?php echo $mode; ?>">
    <div id="wrap">
    	  <header id="header" class="pulsed">
          <h1><a href="index.php"><img src="images/title.png" alt="Spacetraders" title="Spacetraders" /></a></h1>
          <nav id="menu">
            <ul>
                <li><a href="index.php">Home</a></li>
                <li><a href="index.php?mode=login">Login</a></li>
                <li><a href="index.php?mode=credits" target="_blank"><!-- not exactly good practice but WHATEVER don't judge me -->Credits</a></li>
            </ul>
            <div id="clock">
              <applet code="dclock.class" Width=300 Height=30>
                <param name=bgcolor value="000000">
                <param name=seconds value="yes">
                <param name=24hour value="yes">
                <param name=background value="panel.gif">
                <param name=digits value="bit.gif">
              </applet>
            </div>
          </nav>
        </header>
        <div id="content">
        <div id="page" class="pulsed opacity-80">
        <div class="page-header"><?php echo $title; ?></div>
        <div class="page-body"><?php
        switch ($mode) {
            case 'login':
                include('login.html');
                break;
            case 'credits':
                include('credits.html');
                break;
            case 'room1':
                include('room1.html');
                $menu = true;
                $left_url = 'http://www.cs.mcgill.ca/~llehne/room-page/room-page.html';
                $right_url = 'http://www.cs.mcgill.ca/~hbrund/comp206/index.php?mode=room2';
                // I know redundancy but WHATEVER
                break;
            case 'room2':
                include('room2.html');
                $menu = true;
                $left_url = 'http://www.cs.mcgill.ca/~wliu65/206/index.php?mode=room1';
                $right_url = 'http://www.cs.mcgill.ca/~csuder/comp206/index.php?mode=room3';
                break;
            case 'room3':
                include('room3.html');
                $menu = true;
                $left_url = 'http://www.cs.mcgill.ca/~hbrund/comp206/index.php?mode=room2';
                $right_url = 'http://www.cs.mcgill.ca/~cleung24/comp206/index.php?mode=room4';
                break;
            case 'room4':
                include('room4.html');
                $menu = true;
                $left_url = 'http://www.cs.mcgill.ca/~csuder/comp206/index.php?mode=room3';
                $right_url = 'http://www.cs.mcgill.ca/~ezarou/index.php?mode=room5';
                break;
            case 'room5':
                include('room5.html');
                $menu = true;
                $left_url = 'http://www.cs.mcgill.ca/~cleung24/comp206/index.php?mode=room4';
                $right_url = 'http://cs.mcgill.ca/~ztrifi/myPage.html';
                break;
            default:
                include('home.html');
                break;
        } ?>
        </div>
        </div>
        </div>
    </div>
    <?php 
        // As you can tell by this PHP magic, menu only shows up for rooms
        if ( isset($menu) ) { ?>
        <footer id="footer" class="pulsed opacity-80">
            <nav id="rooms">
              <ul class="map-thing">
              <?php
              // terrible but fuck it, it's PHP what can I do
              $images = array("moon_thumb", "dune_thumb", "orion_thumb", "sss_thumb", "memento_thumb");
              $names = array("The Moon", "Arrakis", "Orion", "SSS", "MM");
	      $devs = array("~wliu65/206/", "~hbrund/comp206/", "~csuder/comp206/", "~cleung24/comp206/", "~ezarou/");
              echo '<li class="go-button"><a class="awesome blue large" href="' . $left_url . '">&laquo; Go left</a></li>';
               // Looool loop, good on you, I was too lazy to do that 
              foreach( $images as $key => $image) {
                  $name = $names[$key];
		  $dev = $devs[$key];
                  $number = $key+1;
                  $current_class = ($mode == "room".$number ? "current" : "");
                  echo '<li class="'.$current_class.'">
                          <a class="image_link" href="http://www.cs.mcgill.ca/'.$dev.'index.php?mode=room'.$number.'">
                            <img src="images/'.$image.'.jpg" />
                          </a>
                          <a class="text_link awesome black" href="index.php?mode=room'.$number.'">
                            '.$name.'
                          </a>
                        </li>';
              }

              echo '<li class="go-button"><a class="awesome blue large" href="' . $right_url . '">Go right &raquo;</a><a class="awesome blue large" href="index.php">Logout</a></li>';
              ?>
              </ul>
            </nav>
        </footer>
    <?php } ?>
</body>
</html>
