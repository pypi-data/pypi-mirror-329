# PyLiveServer

1.[description](#description) 2.[dependencies](#dependencies) 3.[how to use](#use)

## description

This is a small script written in python aimed at those who use nvim, helix or the zed code editor on Linux OS.
This will allow you to serve files in the web development process and see the changes in your preferred browser in real time. This file includes the languages ​​commonly used in web development (html, css, js, json, images extensions).

## dependencies

Linux systems already have python3 installed by default.
You just need to use the venv module to create a virtual environment, activate it and install pyliveserver.

## use example

open a terminal in the root directory of your project.

1.[create and activate the virtual environment]

```
python3 -m venv venv
#activate virtual environment
source venv/bin/activate
# you should see (venv) in your terminal
```

2.[install pyliveserver]

```
pip install pyliveserver
#now you can use pyliveserver
pyls
```

3.[try it]

This should open filedialog in the home folder of your system. Select the folder you want to serve and your browser will open. Now you can edit and see the changes in real time!

4.[deactivate virtual environment]

```
#terminal
deactivate
```

don`t forget to add venv in your .gitignore file before commiting!
