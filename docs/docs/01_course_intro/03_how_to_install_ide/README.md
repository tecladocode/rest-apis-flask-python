---
title: How to install an IDE
description: What IDE should you use? How do you install it? Let me show you in this quick guide.
---

# How to install an IDE

An IDE is an Integrated Development Environment. If you've got experience coding, I'm sure you've used an IDE at some point or another.

IDEs are text editors that let you modify your code. However, as the name says, they do a bit more than just that.

Often we can use IDEs to run our code, connect to databases, use a debugger, or a whole host of other things!

Throughout this course I use Visual Studio Code. It's a very powerful IDE that you can get for free at https://code.visualstudio.com/. If you get VS Code, I've got a blog post on how to set it up for Python development: https://blog.tecladocode.com/how-to-set-up-visual-studio-code-for-python-development/

## Opening Projects

Whenever you work using an IDE, you should open separate projects in separate windows:

- 👍 When you start a section of the course, make a folder for that section and open it with VSCode. Now VSCode treats that as a "project" folder.
- 👎 Make a folder for the entire course and open it with VSCode. Inside it, make a folder for each section. VSCode will treat the top-level course folder as the "project", and your experience will be a bit more difficult.

I've noticed some students like opening their "projects" folder with the IDE, so that they can work on all their projects in one window. This is likely to cause problems due to how Python looks for code files to use and import (more on that when you get to the "Imports" section of the Python Refresher!).

So don't be afraid to have many different project folders, each one with their own virtual environment and dependencies. That's normal and will make it much easier to work with!