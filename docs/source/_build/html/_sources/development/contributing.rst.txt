.. _contributing:

***********************
Contributing to pyufunc
***********************

.. contents:: Table of contents:
   :local:


All contributions, bug reports, bug fixes, documentation improvements,
enhancements, and ideas are welcome.

.. _contributing.bug_reports:

Bug reports and enhancement requests
====================================

Bug reports and enhancement requests are an important part of making pyufunc more stable and
are curated though Github issues. When reporting an issue or request, please select the `appropriate
category and fill out the issue form fully <https://github.com/xyluo25/pyufunc/issues/new/choose>`_
to ensure others and the core development team can fully understand the scope of the issue.

The issue will then show up to the pyufunc community and be open to comments/ideas from others.

Finding an issue to contribute to
=================================

If you are brand new to pyufunc or open-source development, we recommend searching
the `GitHub "issues" tab <https://github.com/xyluo25/pyufunc/issues>`_
to find issues that interest you.

Once you've found an interesting issue, it's a good idea to assign the issue to yourself,
so nobody else duplicates the work on it. On the Github issue, a comment with the exact
text ``take`` to automatically assign you the issue
(this will take seconds and may require refreshing the page to see it).

If for whatever reason you are not able to continue working with the issue, please
unassign it, so other people know it's available again. You can check the list of
assigned issues, since people may not be working in them anymore. If you want to work on one
that is assigned, feel free to kindly ask the current assignee if you can take it
(please allow at least a week of inactivity before considering work in the issue discontinued).

.. _contributing.github:

Submitting a pull request
=========================

.. _contributing.version_control:

Version control, Git, and GitHub
--------------------------------

pyufunc is hosted on `GitHub <https://www.github.com/xyluo25/pyufunc>`_, and to
contribute, you will need to sign up for a `free GitHub account
<https://github.com/signup/free>`_.

If you are new to Git, you can reference some of these resources for learning Git. Feel free to reach out
to the community for help if needed:

* `Git documentation <https://git-scm.com/doc>`_.
* `Numpy's Git resources <https://numpy.org/doc/stable/dev/gitwash/git_resources.html>`_ tutorial.

Also, the project follows a forking workflow further described on this page whereby
contributors fork the repository, make changes and then create a pull request.
So please be sure to read and follow all the instructions in this guide.

If you are new to contributing to projects through forking on GitHub,
take a look at the `GitHub documentation for contributing to projects <https://docs.github.com/en/get-started/quickstart/contributing-to-projects>`_.
GitHub provides a quick tutorial using a test repository that may help you become more familiar
with forking a repository, cloning a fork, creating a feature branch, pushing changes and
making pull requests.

Below are some useful resources for learning more about forking and pull requests on GitHub:

* the `GitHub documentation for forking a repo <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_.
* the `GitHub documentation for collaborating with pull requests <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests>`_.
* the `GitHub documentation for working with forks <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks>`_.

Getting started with Git
------------------------

`GitHub has instructions <https://docs.github.com/en/get-started/quickstart/set-up-git>`__ for installing git,
setting up your SSH key, and configuring git.  All these steps need to be completed before
you can work seamlessly between your local repository and GitHub.

.. _contributing.forking:

Create a fork of pyufunc
------------------------

You will need your own copy of pyufunc (aka fork) to work on the code. Go to the `pyufunc project
page <https://github.com/xyluo25/pyufunc>`_ and hit the ``Fork`` button. Please uncheck the box to copy only the main branch before selecting ``Create Fork``.
You will want to clone your fork to your machine
