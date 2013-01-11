## Meuporg is an Efficient and Unified Project ORGanization tool

Meuporg is a system I developed to automatically keep a centralised track of the things I have to do in each of my pojects.

It is a set of tools to update automatically a text file depending on the content of the directory it is in intended to be used to manage one person  projects. Meuporg is free software (BSD licence): basically, you are free to use/redistribute/do anything you want with it as long you give me credit for designing it.


## Ideas and principles behind Meuporg

### Problem addressed

We all have many projects we work on. In my case, I write a master thesis, I implement an open-source program, I write a math book, I manage a blog, I take care of my computer, etc. Nothing very impressive but all these tasks require me to organize myself ("no shit Sherlock"? Well, some people don't). Furthermore, I don't work on all of them at the same time: it is fairly common for one of these projects to be on stand by for weeks, months even. They can also be big: while they of course remain manageable by a single person, I need a way to keep track of what is left to do, what possible improvements could be, etc. in order to be efficient right away when catching up.

I used org-mode from the start when working but I found that keeping separated TODO-lists with vague indications as for where the modifications had to be done was pretty cumbersome. I thought it would be awesome to be able to leave a small description of what was left to do in a file at the point where it was to be done and then to have a list of these items built automatically with links pointing to the exact place in the code were the modification has to be done. I also wanted it to be very easy to use (remember it is intended to fight cumbersomeness). Meuporg was born.


The first version of this system was called roadmap and relied on bash instead of python. It used to be part of my [regulus](https://github.com/picarresursix/regulus/) system.


The name of this program comes from a nice joke by @tishrtman. A French joke I'm afraid; "meuporg" being an attempt at transcripting the awful pronunciation a French journalist used for the "MMORPG" acronym. _sigh_...



### Principle

The idea of meuporg is for you to have a file (refered to in what follows as your _main file_) where you put all the notes, to-do lists, ideas, links, etc. that are relevant for a given project and to have a script updating the said file using the content of the directory it is in.

Meuporg relies on *items*. Items are small text snippets you can leave anywhere in any text file in your working directory that will be collected by the script, sorted, prettily formatted and inserted in your main file. We will dive into more details later; let us look an example now.

First, you need a file called `meup.org` (if you use org-mode) or `meuporg.md` (if you use markdown). It contains some configuration so the simplest is to get the correct template and copy it in your directory. Now suppose you have the following files in the same directory: `readme.md`, `awesomeprog.c`, `lib/awesomelib.c`, `lib/awesomelib.h` and a `doc` folder containing automatically generated documentation (so you don't want to touch it). Suppose also that these files have some data already.


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
    // !IDEA! Perhaps we could heuristic H here?
    return AWESOME_NESS;
}
```

`readme.md`:
```markdown
AWESOME PROGRAM
===============

This program is awesome.

<!-- !TODO! Write a description for my program.
-->
<!-- !IDEA! Perhaps I should give an example of usage?
-->

By the way, see this guy's website !FIXLINK!: he also does awesome things!
```

We also have the following `meuporg.md` file:

```markdown
AWESOME
=======

## Configuration

include:
exclude: .*doc.*

## Notes
When writing `awesome`, I could use the `cool` framework, see [here](http://cool.org).

## Items
```

Now run `meuporg -u` in the same directory. The `meuporg.md` will be updated to become:

```markdown
AWESOME
=======

## Configuration

include:
exclude: .*doc.*

## Notes
When writing `awesome`, I could use the `cool` framework, see [here](http://cool.org).

## Items
## FIXLINK
   1. [link](./readme.md:11)
## IDEA
   1. [Perhaps we could heuristic H here?](./lib/awesomelib.c:62)
   2. [Perhaps I should give an example of usage? -->](./readme.md:7)
## TODO
   1. [Write main function.](./awesome.c:100)
   2. [Write a detailed description of awesomeness.](./lib/awesomelib.h:50)
   3. [Write a description for my program. -->](./readme.md:6)
```


But wait, there is more! Suppose we want to sort the items, for instance that we want those concerning the awesome library to be separated from the others. It is very simple, just modify `meuporg.md` like this:

```markdown
AWESOME
=======

## Configuration

include:
exclude: .*doc.*

## Notes
When writing `awesome`, I could use the `cool` framework, see [here](http://cool.org).

## awesomelib
### Items
## Items
```

And run `meuporg.py -u`. You will obtain this:

```markdown
AWESOME
=======

## Configuration

include:
exclude: .*doc.*

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
    1. [Perhaps we could heuristic H here?](./lib/awesomelib.c:62)
### TODO
    2. [Write a detailed description of awesomeness.](./lib/awesomelib.h:50)
```

Neat right?

What happened? When `meuporg` parses the main file, it looks for headings. If it finds an "Items" heading, it updates it. To do so, it runs as usual but includes only the files whose relative path matches the pattern `.*last_heading.*`. Here, `last_heading="awesomelib"`. Logical, isn't it? Furthermore, all the items matching this pattern will not be written in any other "Items" node. So if you add a node "Items" in the end, like here, it will "garbage collect" all not printed items.


## Supported format

Right now, only org-mode and markdown are supported. To be completly honest, I don't really see what other relevant formats could be...


## Emacs

If you use emacs's org-mode, be sure to check the content of the `emacs` folder: it contains the `meuporg` minor-mode. Just copy-paste the `meuporg.el` file somewhere in your `.emacs.d` and add the following to your `.emacs`.

```elisp
(load-file "path/to/meuporg.el")
```

It will automatically set up everything. In particular, the mode will activate itself when a file is in a directory ruled by a meup.org file. It provides many useful keybindings to insert items, jump to the previous/next item in a file, update the main file, etc.
