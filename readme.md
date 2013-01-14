# Meuporg is an Efficient and Unified Project ORGanization tool

Meuporg (*!M!*) allows to automatically keep a centralised track of to-do items and notes associated with a project.

It is a set of tools to update automatically a text file depending on the content of the directory it is in. It is in intended to be used to manage one person  projects. Meuporg is free software (BSD licence): basically, you are free to use/redistribute/do anything you want with it as long you give me credit for designing it.


## Installation

Get the archive containing all the information from one of the links on the side of the page and then uncompress it. If you run some UNIX derivative, `cd` in the newly created directory and run the `install.sh` script.


## Ideas and principles behind Meuporg

### Problem addressed

We all have many projects we work on. Studies, open-source project(s), blogging, taking care of our computer, etc. All these tasks require us to organize ourselves ("no shit Sherlock"? Well, some people don't). Furthermore, we don't work on all of them at the same time: it is fairly common for one of these projects to be on stand by for weeks, months even. They can also be big. Thus, we need a way to keep track of what is left to do, what possible improvements could be, etc. in order to be efficient right away when catching up.

I used org-mode from the start when working on such projects but I found that keeping separated TODO-lists with vague indications as for where the modifications had to be done was pretty cumbersome. I thought it would be awesome to be able to leave a small description of what was left to do in a file at the point where it was to be done and then to have a list of these items built automatically with links pointing to the exact place in the code were the modifications have to be done. I also wanted it to be very easy to use (remember it is intended to fight cumbersomeness). Meuporg was born.



### Principle

The idea of meuporg is for you to have a file (refered to in what follows as your _main file_) where you put all the notes, to-do lists, ideas, links, etc. that are relevant for a given project and to have a script updating the said file using the content of the directory it is in.

Meuporg relies on *items*. Items are small text snippets you can leave anywhere in any text file in your working directory that will be collected by the script, sorted, prettily formatted and inserted in your main file. Inserting an item is dead simple: put "!ITEM! some multi word description" at the beginning of a line and _voilà_: you have an item with _name_`ITEM` and with description `some multi word description`. Let us look at an example.

First, you need a file called `meup.org` (if you use org-mode) or `meuporg.md` (if you use markdown). Run `meuporg -t org` or `meuporg -t md` to create it. Now suppose you have the following files in the same directory: `readme.md`, `awesomeprog.c`, `lib/awesomelib.c`, `lib/awesomelib.h` and a `doc` folder containing automatically generated documentation (so you don't want to touch it). Here is the content of these files.


awesomeprog.c
```c
#include "lib/awesomelib.h"

int main(int argc, char ** argv)
{
    // !TODO! Write main function.
    return 0;
}
```

`lib/awesomelib.h`
```c
// some code

/**
 * Does some awesome stuff.
 *
 * @param input The string describing the awesome thing to do.
 * !TODO! Write a detailed description of awesomeness.
 */
int awesomeness(char * input)
```

`lib/awesomelib.c`
```c
// <some code>

int awesomeness(char * input)
{
    // some code
    // !IDEA! Perhaps we could use heuristic H here? Or perhaps
    // ! heuristic H' would work better?
    return AWESOME_NESS;
}
```

`readme.md`:
```md
AWESOME PROGRAM
===============

This program is awesome.

<!-- !TODO! Write a description for my program.
-->
<!-- !IDEA! Perhaps I should give an example of usage?
-->

By the way, see this guy's website !FIXLINK!: he also does awesome things!
```

We also have the following `meuporg.md` file (we added the `Notes` heading).

```md
AWESOME
=====

 * DESCRIPTION: description
 * AUTHOR: Me
 * Date: 2013-01-13

# Project description
  The following fields are used to configure meuporg. Use space separated python regexp, see [the Python documentation](http://docs.python.org/2/howto/regex.html#matching-characters) for more info.
## Files to include
   INCLUDE:
   EXCLUDE: .\*doc.\*
   INCLUDE_BACKUP_FILES: NO
   INCLUDE_HIDDEN_FILES: NO

# Notes
When writing `awesome`, I could use the `cool` framework, see [here](http://cool.org).

# Items
```

Now run `meuporg -u` (`u` as in "update") in the same directory. The `meuporg.md` will be updated to become:

```md
AWESOME
=======


# Project description
  The following fields are used to configure meuporg. Use space separated python regexp, see [the Python documentation](http://docs.python.org/2/howto/regex.html#matching-characters) for more info.
## Files to include
   INCLUDE:
   EXCLUDE: .\*doc.\*
   INCLUDE_BACKUP_FILES: NO
   INCLUDE_HIDDEN_FILES: NO

# Notes
When writing `awesome`, I could use the `cool` framework, see [here](http://cool.org).

# Items
## FIXLINK
   1. [link](./readme.md:11)
## IDEA
   1. [Perhaps we could heuristic H here? Or perhaps heuristic H' would work better?](./lib/awesomelib.c:62)
   2. [Perhaps I should give an example of usage? -->](./readme.md:7)
## TODO
   1. [Write main function.](./awesome.c:100)
   2. [Write a detailed description of awesomeness.](./lib/awesomelib.h:50)
   3. [Write a description for my program. -->](./readme.md:6)
```

Note that the `FIXLINK` was in the middle of the line and thus considered "in-code": it has no description so "link" is the only thing displayed. For instance, I use many such "FIXREF" items when writing papers using LaTeX.

Also, the `IDEA` item in `awesomelib.c` was written on several lines. As long as new lines following an item start with `!`, they are considered like parts of its description.

But wait, there is more! Suppose we want to sort the items, for instance that we want those concerning the awesome library to be separated from the others. It is very simple, just modify `meuporg.md` like this:

```md
AWESOME
=======

# Configuration
   INCLUDE:
   EXCLUDE: .\*doc.\*
   INCLUDE_BACKUP_FILES: NO
   INCLUDE_HIDDEN_FILES: NO

# Notes
When writing `awesome`, I could use the `cool` framework, see [here](http://cool.org).

# awesomelib
## Items
# Items
```

And run `meuporg.py -u`. You will obtain this:

```md
AWESOME
=======

## Configuration
   INCLUDE:
   EXCLUDE: .\*doc.\*
   INCLUDE_BACKUP_FILES: NO
   INCLUDE_HIDDEN_FILES: NO

## Notes
When writing `awesome`, I could use the `cool` framework, see [here](http://cool.org).

## awesomelib
### Items
#### IDEA
    1. [Perhaps I should give an example of usage? -->](./readme.md:7)
#### TODO
    1. [Write main function.](./awesome.c:100)
    2. [Write a description for my program. -->](./readme.md:6)

## Items
### FIXLINK
    1. [link](./readme.md:11)
### IDEA
    1. [Perhaps we could heuristic H here? Or perhaps heuristic H' would work better?](./lib/awesomelib.c:62)
### TODO
    2. [Write a detailed description of awesomeness.](./lib/awesomelib.h:50)
```

Neat right?

What happened? When `meuporg` parses the main file, it looks for headings. If it finds an "Items" heading, it updates it. To do so, it runs as usual but includes only the files whose relative path contain all the previous headings. Here, the "Items" was in a heading "awesomelib" so only the items in files whose path contains this tring where kept. You can nest these if you prefer!

Furthermore, all the items are written at most one time. So if you add a node "Items" in the end, like here, it will "garbage collect" all not printed items.


## Formats

Right now, only org-mode and markdown are supported. To be completly honest, I don't really see what other relevant formats could be...

Items can contain any letter (upper and lower case, case sensitive), numbers and underscores.


## Emacs

If you use emacs's org-mode, a `meuporg.el` file will be copied in your `.emacs.d` during Installation. It contains the `meuporg` minor-mode. Just add the following to your `.emacs` (as suggested during installation).

```lisp
(load "meuporg.el")
```

It will automatically set up everything. In particular, the mode will activate itself when a file is in a directory ruled by a meup.org file. It provides many useful keybindings to insert items, jump to the previous/next item in a file, update the main file, etc. Here is a list:

  * `C-! r`     Updates the main file of the directory and reverts its buffer (`meuporg-reload`).
  * `C-! h`     Open the main file ruling the current buffer (if any) (`meuporg-open-main`).
  * `C-! n`     Moves the cursor to the next item in the same buffer (if any) (`meuporg-go-to-next-item`).
  * `C-! p`     Moves the cursor to the previous item in the same buffer (if any) (`meuporg-go-to-previous-item`).
  * `C-! i t`   Inserts "!TODO! " (`meuporg-insert-todo`).
  * `C-! i i`   Inserts "!IDEA! " (`meuporg-insert-idea`).
  * `C-! i c`   Inserts "!TO_CHECK! " (`meuporg-insert-tocheck`).
  * `C-! i f`   Inserts "!FIX_REF! " (`meuporg-insert-fixref`).



## Notes

The first version of this system was called roadmap and relied on bash instead of python. It used to be part of my [regulus](https://github.com/picarresursix/regulus/) system.

The name of this program comes from a nice joke by @tshirtman. A French joke I'm afraid; "meuporg" being an attempt at transcripting the awful pronunciation a French journalist used for the "MMORPG" acronym. _sigh_...


## Modifying/Hacking

As you might guess since I put this project on github, feel free (and further, encouraged) to use it! I would also love to hear your comments: you can contact me via github or at `leoperrin [at/arobase] picarresursix.fr`.
