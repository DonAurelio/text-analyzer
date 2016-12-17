# TextAnalyzer

This projects is dedicated to an University Assignment related with Natural Language Processing. This implemenation covers topics like:

* **Tokenization** and **Morfological Analisys** in the first module (called morfo) using freeling with python. 
* The second module (textparser) covers **Syntactic Analisys**, it deals with the generation of syntactic trees using probabilistic models (Standfor and Bikel). Synactics trees are computational data structures that allows determine the structure of a given non-structured text.

More information, please check the wiki of this project.


http://ignitersworld.com/lab/imageViewer.html
http://www.howtogeek.com/109369/how-to-quickly-resize-convert-modify-images-from-the-linux-terminal/
https://linuxmeerkat.wordpress.com/2014/10/17/running-a-gui-application-in-a-docker-container/
http://stackoverflow.com/questions/23429117/saving-nltk-drawn-parse-tree-to-image-file

# Dan Bikel’s Parsing Engine
dbparser.tar.gz

# Penn Treebank based Trainning set 
wsj-02-21.mrg.tar.gz

# Evaluate the accurancy of the model 
parseval.tar.gz

# Test set
00-raw.tar.gz

# Run graphical applications into a contaner

* install the python-tk

* apt-get update

* apt-get install xvfb

* Xvfb :1 -screen 0 1024x768x16 &> xvfb.log  &

* ps aux | grep X

* DISPLAY=:1.0

* export DISPLAY

* apt-get install imagemagick

http://www.howtogeek.com/109369/how-to-quickly-resize-convert-modify-images-from-the-linux-terminal/
https://linuxmeerkat.wordpress.com/2014/10/17/running-a-gui-application-in-a-docker-container/


HTML ImageViwer
http://ignitersworld.com/lab/imageViewer.html


# Install java for nltk stanfor postagger and parser into a container

Ref:(http://stackoverflow.com/questions/35130798/install-java-8-in-debian-jessie)

echo deb http://http.debian.net/debian jessie-backports main >> /etc/apt/sources.list

apt-get update && apt-get install openjdk-8-jdk

update-alternatives --config java


jar tvf stanford-parser-3.3.1-models.jar
Extract models 
https://docs.oracle.com/javase/tutorial/deployment/jar/unpack.html

jar xf stanford-parser-3.6.0-models.jar edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz
