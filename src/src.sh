#!/bin/bash

clear
cat<< EOF

                              ░▀█▀░█▀█░█▀▀░█▀█░█░█
                              ░░█░░█░█░▀▀█░█▀▀░░█░
                              ░▀▀▀░▀░▀░▀▀▀░▀░░░░▀░
                                                                                                                
 ---------ＡＮ  ＡＤＶＡＮＣＥ  ＤＡＲＫＷＥＢ  ＯＳＩＮＴ  ＴＯＯＬ----------
 
EOF

read -p " Enter the Link :" web
read -p "Do you want to crawl deeper
y) Yes I Want
n) No Thanks
(Enter y or n) :" yn

case $yn in
    y) echo Crawling Deeper ...;;
    n) echo Crawling ...;
    python3 src/tor-crawl/main.py -u $web

esac

read -p "In Depth 1 or 2 ( If you gets error for your network speed then run on 1):" n
python3 src/tor-crawl/main.py -u $web --depth $n

read -p "Do you want to srape images from the website
a) Yes I Want
b) Not Yet, Just Exit
(Select a or b) :" ab

case $ab in
    a) echo Ok Redirecting ...;;
    b) echo Exiting ...;
    exit 1


esac