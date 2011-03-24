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
<html>
<head>
    <title><?php echo $title; ?></title>
    <link rel="stylesheet" href="includes/style.css" type="text/css" />
</head>

<!-- body IDs are used for specific background images -->
<body id="<?php echo $mode; ?>">
    <div id="wrap">
        <div id="header" class="opacity-80">
        <a href="index.php"><img src="title.png" alt="Spacetraders" title="Spacetraders" /></a>
        <ul id="menu">
            <li><a href="index.php">Home</a></li>
            <li><a href="index.php?mode=login">Login</a></li>
            <li><a href="index.php?mode=credits">Credits</a></li>
        </ul>
         </div>
        <div id="content" class="opacity-80">
        <div class="page-header"><?php echo $title; ?></div>
        <div class="page-body"><?php
        switch ($mode) {
            case 'login':
                echo '<p>For now, just enter username: <code>demo</code> and password: <code>demo</code> to access the room shit</p>';
                echo '<div class="center"><form method="post" action="">
                <p><label for="username">Username</label> &nbsp;<input type="text" name="username" id="username" /></p><p><label for="password">Password</label> &nbsp;<input type="password" name="password" id="password" /></p><input type="submit" name="submit" value="Submit" /></div>
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
        <?php 
        // As you can tell by this PHP magic, menu only shows up for rooms
        if ( isset($menu) ) { ?>
        <div id="footer" class="opacity-80">
        <ul class="map-thing">
        <?php
        // terrible but fuck it, it's PHP what can I do
        $room1_class = ($mode == 'room1') ? 'opaque' : 'transparent';
        $room2_class = ($mode == 'room2') ? 'opaque' : 'transparent';
        $room3_class = ($mode == 'room3') ? 'opaque' : 'transparent';
        $room4_class = ($mode == 'room4') ? 'opaque' : 'transparent';
        $room5_class = ($mode == 'room5') ? 'opaque' : 'transparent';

        echo '<li class="go-button"><a href="">Go left</a></li>';
        echo '<li class="' . $room1_class . '"><a href="index.php?mode=room1"><img src="images/moon_thumb.jpg" /></a></li>';
        echo '<li class="' . $room2_class . '"><a href="index.php?mode=room2"><img src="images/dune_thumb.jpg" /></a></li>';
        echo '<li class="' . $room3_class . '"><a href="index.php?mode=room3"><img src="images/orion_thumb.jpg" /></a></li>';
        echo '<li class="' . $room4_class . '"><a href="index.php?mode=room4"><img src="images/iss_thumb.jpg" /></a></li>';
        echo '<li class="' . $room5_class . '"><a href="index.php?mode=room5"><img src="images/sunrise_thumb.jpg" /></a></li>';
        echo '<li class="go-buttom"><a href="">Go right</a></li>';
        ?>
        </ul>
        <br clear="all" />
        <ul class="map-thing">
        <li>&nbsp;</li>
        <li><a href="index.php?mode=room1">The moon</a></li>
        <li><a href="index.php?mode=room2">Dune</a></li>
        <li><a href="index.php?mode=room3">Orion</a></li>
        <li><a href="index.php?mode=room4">ISS</a></li>
        <li><a href="index.php?mode=room5">Eleyine</a></li>
        <li><a href="index.php">Logout</a></li>
        </ul>
        </div>
        <?php } ?>
    </div>
</body>
</html>
