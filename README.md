#How-to-build

wget http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip

unzip stanford-ner-2015-12-09.zip

export STANFORDTOOLSDIR=$HOME

export CLASSPATH=$STANFORDTOOLSDIR/stanford-ner-2015-12-09/stanford-ner.jar

export STANFORD_MODELS=$STANFORDTOOLSDIR/stanford-ner-2015-12-09/classifiers

wget http://nlp.stanford.edu/software/stanford-parser-full-2015-12-09.zip

unzip stanford-parser-full-2015-12-09.zip

export STANFORDTOOLSDIR=$HOME

export CLASSPATH=$STANFORDTOOLSDIR/stanford-parser-full-2015-12-09/stanford-parser.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar
