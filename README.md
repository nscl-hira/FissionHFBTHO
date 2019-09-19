# FissionHFBTHO

Directory for getting started with fission calculations in HFBTHOv3. 

## Installing

### Getting Cygwin
First, you need to be able to ssh into the HPCC, this means having access to some sort of Un\*x style terminal. If you want to see visualisations from the python scripts you also need to be X11 forwarding enabled. My favorite method of doing this is Cygwin. There are instuctions for downloading and installing it [here](https://cs.hofstra.edu/docs/pages/guides/cygwin_installation.html). There listed required files should be enough to get started with.

### Connecting to the HPCC
After you have Cygwin installed, you can ssh into the hpcc. First make sure that Xming is running, this is your local X11 server that is needed to open graphical windows over SSH.

To connect, run the command
```
ssh -XY nedID@hpcc.msu.edu
```
You should be prompted for your HPCC password and brought to the gateway. From here you can ssh into other development nodes. If you need to test if X11 forwarding is working run `xclock`. This should pop up a simple clock. ICER maintains some of their own documentation for connecting [here](https://wiki.hpcc.msu.edu/display/ITH/Connect+to+HPC+System).

You should also set up ssh keys between the HPCC, your desktop, and the NSCL's fishtank so you're not constantly prompted for a password. You should also consider adding ssh keys to your github account, instructions [here.](https://help.github.com/en/articles/connecting-to-github-with-ssh) There is some documentation on how to do that for the [HPCC here](https://wiki.hpcc.msu.edu/display/ITH/SSH+Key-Based+Authentication) and the [NSCL here](https://wikihost.nscl.msu.edu/gradwiki/doku.php?id=computers:remotes_services)

### Getting this rep
Once on the HPCC, checkout this repo into your home directory using the commands
```
cd ~/
git clone git@github.com:nscl-hira/FissionHFBTHO.git
```
If you don't have ssh keys in github you'll have to replace that last command with 
```
https://github.com/nscl-hira/FissionHFBTHO.git
```

If you `ls` in your home directory, you should see a new folder names `FissionHFBTHO`

## Linux
The most important linux command is `man`. For nearly any command you can type `man command` and get the manual page wich has all of the information on what the command does. Going through a linux quickstart guide or something is probably beneficial. 

## Loading the enviroment
Before doing anything with the code, make sure the enviroment variables are set correctly. From within the folder, this is done with the command
```
source ~/bin/env.sh
```
This also loads all of the required modules to run HFBTHO as complied in my (Adam's) directory.

## Basics of git
Git is a a version control system. Basically, it allows you to save a record of the changes to a directory or code base, and allows you to revert to old versions as needed. It is also useful for tracking changes made by multiple people and merging everything together. GitHub has a page that describes some of the philisophy around git and diestributed version control systems [here](https://guides.github.com/introduction/git-handbook/).

#### Basic git commands

* See the changes made since the last commit
```
git status
```
* Add the changes made to some file `dir/test.py` to the next commit
```
git add dir/test.py
```
* Add all of the changes since the last commit to the next commit
```
git add .
```
* Create a new commit
```
git commit -m "This is the message for this commit"
```
* Push the status of your local repository to the remote repository (what is on github)
```
git push
```
* Pull any changes from the remote repository
```
git pull
```

## Setting up a python enviroment
Setting up the ability to plot stuff on the HPCC is a pain. The easiest way to just build a local installation of Conda, a package/enviroment manager for python. There are installation instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#). You will need to either use `wget` or `curl` to download the file to the HPCC, or download it locally and `scp` it over. The first option (`wget`) is probably the easiest.

## Basics of HTBTHO

## Basics of submitting jobs via SLURM

## Running a theory calculation

