# TextAnalyzer

This projects is dedicated to an University Assignment related with Natural Language Processing. This implemenation covers topics like:

* **Tokenization** and **Morfological Analisys** in the first module (called morfo) using freeling with python. 
* The second module (textparser) covers **Syntactic Analisys**, it deals with the generation of syntactic trees using probabilistic models (Stanford and Bikel). 

More information, please check the wiki of this project.

## Deployment

This projects was designed into a container:

The first module **Tokenization** and **Morfological Analisys** depends on freeling and python 2.7. You can find those package installed on this [docker image](https://drive.google.com/file/d/0ByEHTU9ch3ZwcmJlQW5qdGkyT0E/view?usp=sharing)

The second module **Syntatic Analisys** depends on:

- Dan Bikel’s Parsing Engine: dbparser.tar.gz

- Penn Treebank based Trainning set: wsj-02-21.mrg.tar.gz

- Evaluate the accurancy of the model: parseval.tar.gz

- Test set: 00-raw.tar.gz

Those files can be found [this](https://drive.google.com/drive/folders/0ByEHTU9ch3ZwSkhqNl95SUxiZ2M?usp=sharing). Other needed files are:

- Stanford Statistical Parser: [stanford-parser-full-2015-12-09.zip](http://nlp.stanford.edu/software/stanford-parser-full-2015-12-09.zip)

- Stanford Postagger: [stanford-postagger-2015-12-09.zip](http://nlp.stanford.edu/software/stanford-postagger-2015-12-09.zip)



### Run graphical applications into a contaner

To run the **Syntactic Analisys** module the container needs to be able to "show" or "create" grafical UIS. This allow the app to create the parse tree images generated with nltk.

```{r, engine='bash', count_lines}
apt-get install python-tk
apt-get update
apt-get install xvfb
apt-get install imagemagick
```
Then you need to run the following command every time that the container starts.

```{r, engine='bash', count_lines}
Xvfb :1 -screen 0 1024x768x16 &> xvfb.log  &
DISPLAY=:1.0
export DISPLAY
```

http://www.howtogeek.com/109369/how-to-quickly-resize-convert-modify-images-from-the-linux-terminal/
https://linuxmeerkat.wordpress.com/2014/10/17/running-a-gui-application-in-a-docker-container/


HTML ImageViwer
http://ignitersworld.com/lab/imageViewer.html
http://dimsemenov.com/plugins/magnific-popup/


### Installing Java for nltk Stanford Pos tagger and parser in the container

```{r, engine='bash', count_lines}
echo deb http://http.debian.net/debian jessie-backports main >> /etc/apt/sources.list
apt-get update && apt-get install openjdk-8-jdk
update-alternatives --config java
```
<!--- 
jar tvf stanford-parser-3.3.1-models.jar
Extract models 
jar xf stanford-parser-3.6.0-models.jar edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz
--->
# References

[1] http://ignitersworld.com/lab/imageViewer.html
[2] http://www.howtogeek.com/109369/how-to-quickly-resize-convert-modify-images-from-the-linux-terminal/
[3] https://linuxmeerkat.wordpress.com/2014/10/17/running-a-gui-application-in-a-docker-container/
[4] http://stackoverflow.com/questions/23429117/saving-nltk-drawn-parse-tree-to-image-file
[5] https://docs.oracle.com/javase/tutorial/deployment/jar/unpack.html
[6] http://stackoverflow.com/questions/35130798/install-java-8-in-debian-jessie
