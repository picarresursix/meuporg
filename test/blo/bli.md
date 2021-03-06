<!-- Time-stamp: <2013-01-01 00:34:18 leo> -->


REGULUS
=======


Regulus is the name of the system I use to store all the miscellaneous
customization, bash-functions and configuration of my system.  The aim
is to have a proper version control of all of my configuration files
as well as doing some tidying.

I had the idea when I saw the
[sputnik project](https://github.com/sputnik/) started by dell.

The files in this directory are the ones I actually use, i.e. for
instance my `.emacs` file is just a symbolic link to the one at
`~/regulus/emacs/dot_emacs`.


Files currently protected by Regulus
====================================

Bash
----

The configuration of my bash prompt, and the miscellaneous custom
functions I use:

* To have a nice prompt displaying some characteristics of my last
commit if I am in a git repository.
* Easily make scripts executables and copy them somewhere in my $PATH.
* My .bashrc


Emacs configuration
-------------------

My .emacs file and .emacs.d directory. Custom shortcuts, and some
custom functions.


Yell
----

Functions to warn me when a function's execution is finished via a
notification and a sound. Useful when launching time consuming
computations/simulations.


Roadmap
-------

### Description ###

A roadmap is made of some statistics, a todo list and an idea list. It
is generated by a bash script (provided here) from small `items` left
in the text files in a directory and relies *heavily* on emacs'
org-mode.

A roadmap is used to describe the content of a directory *and its
subdirectories*. We say that the roadmap "rules" this part of the
directory tree.


### Example ###

For instance, suppose you have a file `bar` with the following content
in a directory `foo`:

    Some code
    Some more code
    // !TODO! Fix this part: it needs to be better
    Yet another part of your code
    // !IDEA! Using this function might be better
    
The items enclosed between exclamation marks should have a different colour.
Now, use `cd` to go in `foo` and run the following commands:

    roadmap -n # this one creates an empty roadmap
    roadmap -u # update it

Go back to `bar` and hit `C-d h`: it will take you to the newly
created file which contains a list of TODO items and one of IDEA
items. In each list, the description of each item is given and is a
link to the exact place in the code where it is. Here, that would be:

    ROADMAP

    * Configuration...
    * Items
    ** [/] TODO list
      1. [ ] Fix this part: it needs to be better (foo/bar:3)
    ** [/] IDEA list
      1. [ ] Using this function might be better (foo/bar:5)
    * Statistics...
      
Thus, if you visit the link on `Fix this part`, you will end up with
your cursor at the beginning of line 3 in the file `foo/bar`.

An actual example is given by this screen cap:
![A screen cap of a roadmap.org file](https://github.com/picarresursix/regulus/blob/master/screen.png "A screen cap of a roadmap")


### Bash ###

Nothing beats what is diplayed if we call the roadmap.sh script
without any arguments:

    -$ ./roadmap.sh
    Usage: roadmap -OPTION

    OPTION has to be one of the following:
        -n: creates an empty roadmap.org file in the current directory.
        -u: updates the roadmap.org file in the current directory.
        -h: displays the path to the roadmap ruling this directory tree.


### Emacs ###

To go along with this script, I wrote a small minor-mode for emacs. It
provides highlighting of the items as well as the following
shortcuts. Note that I am using
[ergoEmacs](http://ergoemacs.org/emacs/ergonomic_emacs_keybinding.html),
a mode to have ergonomic shortcuts so my "C-d" is free. It is easy to
modify by editing the `roadmap.el` file.

  * `C-d r` When the current buffer is a roadmap, updates it.
  * `C-d h` Opens the roadmap ruling the current file (if any).
  * `C-d i t` Inserts a TODO item.
  * `C-d i i` Inserts an IDEA item.
  * `C-d n` Goes to the next item in the same file
  * `C-d p` Goes to the previousitem in the same file  


### Installation ###

You can look at the literate source code of both the bash script and
the emacs minor-mode in the roadmap-implementation.org file. However,
all you need is to put the roadmap.sh script in your path and load
roadmap.el in emacs, for instance by adding the following in your
.emacs:

    (load-file "path/to/roadmap.el")
    
You should be good to go after that. Have fun!


Modifying/Hacking
=================

As you might guess since I put this project on github, feel free (and
further, encouraged) to use it! I would also love to hear your
comments: you can contact me via github or at `leoperrin
[at/arobase] picarresursix.fr`.
