# scippycrm
scippyCRM is a B2B Customer Relationship Management application built with Flask. I will add more and more functionality to it. Contributions from others are welcome as well.

# Technology stack
- Python 3
- Flask
- MongoDB

# Installation
To run this locally you must have MongoDB and Python3.6 (and git, obviously)  installed, and if you have, you can clone this repository via:

```
$ git clone https://github.com/realScipio/scippycrm.git
```

# Features
### v0.0.1:
- login via `admin:admin`
- logout
- display an overview of current "Organisations"
- add a new "Organisation"
- update/change "Organisation" fields

# Roadmap
Some of the planned roadmap milestones include:
- architecture-wise, I will modularize the (future) application components with Flask Blueprints;
- add functionality for multiple System Users
- add functionality for "Employees / Contactpersons", that work for a given "Organisation"
- add functionality for "Contact history" for a given "Organisation" & "Employee"
- add functionality for "Task management" (what to do when for who), integrated with "Contact history"
- add a generic Overview Pager, to "visually step through / browse" large chunks of Overview data
- add Read/Write View functionality for Form Blocks
- add custom-built Responsive Design View @media queries, for system users using the application via mobile / on the road
- add pre-defined Data Filters
- add support for Overview Field Ordering (asc / desc)
- add various Data Import / Export functionality via the GUI (DB dumps, CSV exports, etc.)
- add "Sales Opportunity Tracker"
- add "Document Generator", e.g. to semi-automatically compose Sales Offers and Mailings & export via PDF
- add Visual Graphs to the "Dashboard"
- add "Visual Field Generator", to add and manage Data Components via the GUI instead of programmatically
- etc.!
