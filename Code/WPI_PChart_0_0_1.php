<?php

/* Include all the classes 
include("/srv/www/lib/pChart2.1.4/class/pData.class.php");
include("/srv/www/lib/pChart2.1.4/class/pDraw.class.php");
include("/srv/www/lib/pChart2.1.4/class/pImage.class.php");
*/
require_once "/srv/www/lib/pChart/class/pDraw.class.php";
require_once "/srv/www/lib/pChart/class/pImage.class.php";
require_once "/srv/www/lib/pChart/class/pData.class.php";

$myData = new pData(); /* Create your dataset object */

$db = mysql_connect("localhost", "root", ""); //location of server, db username, db pass
mysql_select_db("piplanter", $db);

$Requete = "SELECT * FROM `DailyTable04_26_2017__10_50_52PM`"; //table name
$Result = mysql_query($Requete, $db);

/*This fetches the data from the mysql database, and adds it to pchart as points*/
while($row = mysql_fetch_array($Result))
{
	$Time = $row["Time"];
	$myData->addPoints($Time,"Time");

	$mst1_V = $row["mst1_V"];
	$myData->addPoints($mst1_V,"mst1_V");
	$mst2_V = $row["mst2_V"];
	$myData->addPoints($mst2_V,"mst2_V");
	$mst3_V = $row["mst3_V"];
	$myData->addPoints($mst3_V,"mst3_V");
	$mst4_V = $row["mst4_V"];
	$myData->addPoints($mst4_V,"mst4_V");

	$ldr1_V = $row["ldr1_V"];
	$myData->addPoints($ldr1_V,"ldr1_V");

	$tmp1_F = $row["tmp1_F"];

	$myData->addPoints($tmp1_F,"tmp1_F");
}

$myData-> setSerieOnAxis("tmp1_F", 0); //assigns the data to the frist axis
$myData-> setAxisName(0, "Degrees F"); //adds the label to the first axis

$myData-> setSerieOnAxis("ldr1_V", 1);
$myData-> setAxisName(1, "LDR");

$myData-> setSerieOnAxis("mst1_V", 2);
$myData-> setSerieWeight("mst1_V",2);
$myData-> setSerieOnAxis("mst2_V", 2);
$myData-> setSerieOnAxis("mst3_V", 2);
$myData-> setSerieOnAxis("mst4_V", 2);
$myData-> setAxisName(2, "Relative Moisture");

$myData->setAbscissa("Time"); //sets the time data set as the x axis label

$myData-> setSerieWeight("mst1_V",1); //draws the line tickness
$myData->setPalette("mst1_V",array("R"=>58,"G"=>95,"B"=>205,"Alpha"=>80)); //sets the line color
$myData-> setSerieWeight("mst2_V",1);
$myData->setPalette("mst2_V",array("R"=>39,"G"=>64,"B"=>139,"Alpha"=>80));
$myData-> setSerieWeight("mst3_V",1);
$myData->setPalette("mst3_V",array("R"=>0,"G"=>34,"B"=>102,"Alpha"=>80));
$myData-> setSerieWeight("mst4_V",1);
$myData->setPalette("mst4_V",array("R"=>67,"G"=>110,"B"=>238,"Alpha"=>80));

$myData-> setSerieWeight("ldr1_V",2);
$myData-> setSerieTicks("ldr1_V", 4);

$myData-> setSerieWeight("tmp1_F",2);
$myData-> setSerieTicks("tmp1_F", 4);

$myPicture = new pImage(2000,500,$myData); /* Create a pChart object and associate your dataset */
$myPicture->setFontProperties(array("FontName"=>"/srv/www/lib/pChart/fonts/pf_arma_five.ttf","FontSize"=>6)); /* Choose a nice font */
$myPicture->setGraphArea(130,40,1900,300); /* Define the boundaries of the graph area */
$myPicture->drawScale(array("LabelRotation"=>320)); /* Draw the scale, keep everything automatic */

$Settings = array("R"=>250, "G"=>250, "B"=>250, "Dash"=>1, "DashR"=>0, "DashG"=>0, "DashB"=>0);

/*The combination makes a cool looking graph*/
$myPicture->drawPlotChart();
$myPicture->drawLineChart();
$myPicture->drawLegend(30,320); //adds the legend

//$date-> date("d-M-Y:H:i:s");

//$myPicture->autoOutput(); /* Build the PNG file and send it to the web browser */

$myPicture->render("/var/www/html/piplanter/renders/".date("d-M-Y_H:i:s").".png");
?>