#!/bin/bash
#; Time-stamp: <2013-01-13 17:38:48 leo>

# Run this (simple) script to install meuporg.

BASE_DIR="/home/"$USER"/.meuporg"
if [[ ! -e $BASE_DIR ]]
then
    mkdir $BASE_DIR
    echo $BASE_DIR" directory created."
else
    echo $BASE_DIR" already exists."
fi
cp -R templates $BASE_DIR 
cp python/* $BASE_DIR/
chmod +x $BASE_DIR/__main__.py
echo 'To run meuporg, use the command "python '$BASE_DIR'"'
echo 'You might want to add the following line to you .bashrc file:'
echo ''
echo 'alias meuporg="python '$BASE_DIR'"'
echo ''
if [[ -e ~/.emacs.d ]]
then
    cp emacs-mode/meuporg.el ~/.emacs.d/
    echo 'EMACS:'
    echo '  meuporg.el put in .emacs.d'
    echo '  To enable meuporg-mode, add the following to your .emacs:'
    echo '    (load "meuporg.el")'
else
    echo "No .emacs.d folder: I won't install the minor-mode then."
fi
echo '[DONE]'
