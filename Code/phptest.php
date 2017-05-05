{ <?php
session_start();
require_once "/srv/www/lib/pChart/class/pDraw.class.php";
require_once "/srv/www/lib/pChart/class/pImage.class.php";
require_once "/srv/www/lib/pChart/class/pData.class.php";

$myDataset = array(0, 1, 1, 2, 3, 5 ,8, 13);

$myData = new pData();
$myData->addPoints($myDataSet);

$myImage = new pImage(500,300, $myData);
$myImage->setFontProperties(array(
	"FontSize => 15));

$myImage->setGraphArea(25,25,475,275);
$myImage->drawScale();
$myImage->drawBarChart();

header();
$myImage->Render(null);
?> }