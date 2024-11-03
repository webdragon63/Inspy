#!/bin/bash

clear
VERMILION='\033[0;31m'
WHITE='\033[0;37m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'

echo -e "${VERMILION}                              ░▀█▀░█▀█░█▀▀░█▀█░█░█"
echo -e "${WHITE}                              ░░█░░█░█░▀▀█░█▀▀░░█░"
echo -e "${GREEN}                              ░▀▀▀░▀░▀░▀▀▀░▀░░░░▀░"
                                                                                                                
echo -e "${BLUE} ---------ＡＮ  ＡＤＶＡＮＣＥ  ＤＡＲＫＷＥＢ  ＯＳＩＮＴ  ＴＯＯＬ----------"
                               
echo -e "${WHITE}                           MADE BY: INDIAN CYBER ARMY "              
echo -e "${CYAN}           YOUTUBE CHANNEL: https://www.youtube.com/@indiancyberarmy5" 
echo -e "${CYAN}--------------------------------------------------------------------------------" 
echo -e "${BLUE}"

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

read -p "Do you want to scrape images from the website
a) Yes I Want
b) Not Yet, Just Exit
(Select a or b) :" ab

case $ab in
    a) echo Ok Redirecting ...;;
    b) echo Exiting ...;
    exit 1


esac
