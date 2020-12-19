# README

Python cli tool for task specific browser window and tab url management and automation.

## Objective
The creation of a python cli skeleton to automate the manual digital task setup and tear process for common enterprise systems gui-based admnistrative actions and workflows with out of the box compatibility with windows os for v1 native features without the added abstractions of pki, apis, idps, and anything / everything related to authentication and authorization. 😇

## Workflow Requirements
- command for three different business processes
- each process will open to specific urls for browser-based gui administration work
- flags to open additional urls as different 'options/ subtasks' of the parent class of processes
- kill / reset state, e.g. close all newly opened windows and tabs upon task completion

## Basic Requirements / Consideratons
- basic config must support custom browser preferences, e.g. open wwww.super-fake-url.com and www.super-fake-url/admin/users as two new tabs in primary chrome and www.another-fake-url.com and another-fake-url.com/something in a NEW Firefox window as new tabs
- cross-platform support for standardized-issue enterprise Windows 10 laptops
- Chrome / Firefox
- scope of poc does not include workflow complexities as a result of an external adpi, idp, or anything related authentication / authorization / sessions.
- compiled as binary for local system installation

## Nice-to-have
- optional global hotkey mapping as an event action trigger for state reset
- tested on Windows VM

## Testing


## Dependencies
To avoid the complexities of seamless cross-platform installation and interoperability with python programs running on Windows 10 third-party packages will not be used in v1


