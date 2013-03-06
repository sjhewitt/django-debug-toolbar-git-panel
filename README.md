===========================
Git Log Debug Toolbar Panel
===========================

The Git Log Debug Toolbar Panel is an add-on for Django Debug Toolbar for 
listing the recent commits to the project.


Installation
============

1. Install and configure [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar>).

2. Add ``'debug_toolbar_git_panel.panel.RecentCommitsDebugPanel'`` to your ``DEBUG_TOOLBAR_PANELS``.


Configuration
=============

- ``GIT_COMMIT_COUNT`` lets you set the number of commits to show in the panel (defaults to 20.)

- ``GIT_COMMIT_URL`` (optional) lets you specify the link to the base url to link to the commit
  
  e.g. ``https://github.com/sjhewitt/django-debug-toolbar-git-panel/commit/`` for this project.
