#!/bin/bash
#; Time-stamp: <2013-01-26 13:55:06 leo>

# Run this (simple) script to install meuporg.


# If XDG_CONFIG_HOME is set, we put meuporg's directory in. Otherwise,
# we put it in ~/.config or, if does not exist, in ~/
if [[ $XDG_CONFIG_HOME != "" ]];
then
    BASE_DIR=$XDG_CONFIG_HOME/.meuporg
elif [[ -e $HOME/.config ]];
then
    BASE_DIR=$HOME/.config/meuporg
else
    BASE_DIR=$HOME/.meuporg
fi

# Creating the directory if it does not exist
if [[ ! -e $BASE_DIR ]]
then
    mkdir $BASE_DIR
    echo $BASE_DIR" directory created."
else
    echo $BASE_DIR" already exists."
fi

# Copying useful data in it.
cp -R templates $BASE_DIR 
cp -R python/* $BASE_DIR/
chmod +x $BASE_DIR/__main__.py

# giving some useful info
echo 'To run meuporg, use the command "python '$BASE_DIR'"'
echo 'You might want to add the following line to you .bashrc file:'
echo ''
echo 'alias meuporg="python2.7 '$BASE_DIR'"'
echo ''

# Telling about the emacs minor-mode
if [[ -e ~/.emacs.d ]]
then
    cp emacs-mode/meuporg.el ~/.emacs.d/
    echo 'EMACS:'
    echo '  meuporg.el put in .emacs.d'
    echo '  To enable meuporg-mode, add the following to your .emacs:'
    echo '    (load "~/.emacs.d/meuporg.el")'
else
    echo "No .emacs.d folder: I won't install the minor-mode then."
fi
echo '[DONE]'
