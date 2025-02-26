# Angets (Ankha's Gets): Functions for user input.

Ever get tired of fine-tuning user input?
\
Well, this is the package for you!
\
At least it is for me since I made the whole thing in the first place...

## Prerequisites

Python 3.11.x or newer.

## Installation

`pip install angets`

## Usage

Import Module.

```python
import angets
```

Basic usage, One attempt with a prompt to the user.

```python
input0 = angets.get_non_empty_string('Give me a response! ')
```

To get inputs with a bit more control.
> Remember to set `verbose` to True as no warning will be conveyed to the user otherwise.

```python
input1 = angets.get_constrained_float(
    within=(6, 9),
    interval='[]',
    prompt='Now give me a number within said range!',
    warning="Oops! Not within the bounds I'm afraid...",
    verbose=True,
    attempts=10
)
```

That is the gist of the main features.
\
It should be a useful utility tool to mitigate against invalid user inputs.

## <img src="/assets/images/troll_face.png" alt="Troll Face" style="height: 24px; width: 24px;" /> Problem?

Actually, I don't expect anyone else other than me to use this package.
\
But if you find it useful enough to want to contribute, be my guest!

## Changes

Created:

- 19 February 2025.

Revised:

- 21 February 2025.
  1. Fixed the installation command.
  2. Added a new image.