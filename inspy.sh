#!/bin/bash
echo "Checking For Root User...."
sleep 1
if [[ $(id -u) -ne 0 ]] ; then 
   echo "You are Not Root! Please Run as Root" ; exit 1 ; 
else echo "Checking For Requirement Packages.." ; 
fi

clear
cat<< EOF

                              ░▀█▀░█▀█░█▀▀░█▀█░█░█
                              ░░█░░█░█░▀▀█░█▀▀░░█░
                              ░▀▀▀░▀░▀░▀▀▀░▀░░░░▀░
                                                                                                                
 ---------ＡＮ  ＡＤＶＡＮＣＥ  ＤＡＲＫＷＥＢ  ＯＳＩＮＴ  ＴＯＯＬ----------
                               
                           MADE BY: INDIAN CYBER ARMY               
           YOUTUBE CHANNEL: https://www.youtube.com/@indiancyberarmy5 
--------------------------------------------------------------------------------     
         
EOF
read -p " Do you want to start tor service
a) yes
b) no (Default is b)  " ab
case $ab in
    b) echo redirecting to a next configuration ...;;
    a) echo starting tor service ...;
    service tor start 

sleep 2

esac
clear
cat<< EOF

                              ░▀█▀░█▀█░█▀▀░█▀█░█░█
                              ░░█░░█░█░▀▀█░█▀▀░░█░
                              ░▀▀▀░▀░▀░▀▀▀░▀░░░░▀░
                                                                                                                
 ---------ＡＮ  ＡＤＶＡＮＣＥ  ＤＡＲＫＷＥＢ  ＯＳＩＮＴ  ＴＯＯＬ----------
 
 
EOF
read -p "a) Scrape images
b) Crawl website 
(Enter a or b)  :" ab
case $ab in
    a) echo Scraping images... ;;
    b) echo Crawling Website of .onion... ;
    sleep 1
    bash src/src.sh
    
esac
python3 src/imscr.py

clear
cat<< EOF

                              ░▀█▀░█▀█░█▀▀░█▀█░█░█
                              ░░█░░█░█░▀▀█░█▀▀░░█░
                              ░▀▀▀░▀░▀░▀▀▀░▀░░░░▀░
                                                                                                                
 ---------ＡＮ  ＡＤＶＡＮＣＥ  ＤＡＲＫＷＥＢ  ＯＳＩＮＴ  ＴＯＯＬ----------
 
 
EOF

read -p "Do you want to craete a powershell backdoor using villain
y) Yes I Want
n) No Not Needed
[choose any option y or n (Default is y)] :" yn
case $yn in
    y) echo Starting Villain ...;;
    n) echo Exiting directly ...;
    exit 1

esac
python3 bkdr/Villain.py