# Amarium

[![status-badge](https://ci.codeberg.org/api/badges/cap_jmk/amarium/status.svg)](https://ci.codeberg.org/cap_jmk/amarium)
[![Downloads](https://static.pepy.tech/personalized-badge/amarium?period=total&units=international_system&left_color=orange&right_color=blue&left_text=Downloads)](https://pepy.tech/project/amarium)
[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C-blue)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![PyPI - Version](https://img.shields.io/pypi/v/amarium.svg)](https://pypi.org/project/amarium)
[![Documentation Status](https://readthedocs.org/projects/amarium/badge/?version=latest)](https://amarium.readthedocs.io/en/latest/?badge=latest)

**Table of Content**

<!-- TOC -->

- [Amarium](#amarium)
  - [1. Why](#1-why)
  - [2. What](#2-what)
  - [3. Usage](#3-usage)
  - [4. Dev Notes](#4-dev-notes)

<!-- /TOC -->

## 1. Why

We found ourselves constantly writing files of some sort, always having to face the same problems and writing the same code to solve these problems. So we decided at some point to seperate the most common function as package out.

## 2. What

Small package with a collection of functions frequently used in handling the filesystem.

This package is really for perfectionists. It is one of the few occasions this bad habit makes sense. `These functions have to be rock-solid!` They are tested, and tested to the bone  - verified over many projects, and evaluated with engineered automated testing. Why?

`Because these functions have to be reliable`

How can you satisfy your craving for perfection with this package? Read the `Dev` section.

## 3. Usage

Please refer to the `tests/` directory for examples of the functions and their usage

## 4. Dev Notes

To develop here, we want you to understand that this package is only about creating code of the highest quality.  

Take the download numbers as a reminder for your responsibility.

For example, in a very early stage we changed the naming in the package and lost users (naturally). Thus here, `no mistakes` are allowed. When we say `no mistakes`, we mean absolutetly `zero`, `nada`.

Of course, we know it is impossible. To somewhat come close to it, we do:

- No `PEP` violations and checking with linting
- Automated testing aiming for 100% coverage
- Usage of CI on the repo and locally!
- Writing documentation
- Writing typed code

Thus, we encourage to use out new package `lia` frequently.
Install lia via

```bash
pip install spawn-lia
```

`Lia` then helps you to keep your code nice with

```bash
lia heal package_name/
```

Everytime you write a new function, you should check it locally using `Lia`, to ensure you are not diverging from the quality constraints. Again, we remind you:

`If you are not having any sense for perfection, this is not a place for you to develop!`

