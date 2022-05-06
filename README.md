# RelativityApp

## Overview

Young lawyers and paralegals become excellent at changing filenames. Tab, highlight, delete, tab, highlight, delete. At the speed of light, they move through the files in File Explorer, changing what could be hundreds of documents and billing the client a few Jacksons for it. 

This was a surprisingly common state of being in U.S. law firms thanks to the dominance of Relativity, a database storing documents collected during a stage of litigation called Discovery, when parties must exchange data relevant to the case. Litigation lawyers export files from Relativity all the time and for some odd reason (one of the many mysteries of the legal industry), all exported files had numerical prefixes to their names. So, for example, say I wanted to export the files "helloworld.docx" and "thisisappt.xlsx". When downloaded, they would be name "01_helloworld.docx" and "02_thisisappt.xlsx". Since exports can involve hundreds if not thousands of documents, you can imagine why this might drive someone insane.

RelativityApp solves this issue. It accomplishes one simple task: remove those godforsaken prefixes. Nothing more, nothing less, but great for that reason. 

It's written in Python. To make it more accessible, I made a user interface using Tkinter and made it into an executable program via PyInstaller (.exe not available on GitHub).