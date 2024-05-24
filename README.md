blurhash-python
===============

This is an encoder for the BlurHash algorithm. To find out more about BlurHash, see https://github.com/woltapp/blurhash.

Installation
------------
Install blurhash with pip
```
$ pip install blurhash-python
```
or pipenv
```
$ pipenv install blurhash-python
```

Usage
-----
Create blurhash from image file
```python
import blurhash

with open('image.jpg', 'rb') as image_file:
    hash = blurhash.encode(image_file, x_components=4, y_components=3)
```
Alternatively, scale the image to produce a faster hash, and create a blurhash from the in-memory image directly
```python
import blurhash
from PIL import Image

with Image.open('image.jpg') as image:
  image.thumbnail(( 100, 100 ))
  hash = blurhash.encode(image, x_components=4, y_components=3)
```
You can also pass file name as parameter to the function
```python
import blurhash

hash = blurhash.encode('image.jpg', x_components=4, y_components=3)
```
`y_components` and `x_components` parameters adjust the amount of
vertical and horizontal AC components in hashed image. Both parameters must
be `>= 1` and `<= 9`.

Development
-----------
Install development requirements and package in editable mode
```
$ pipenv install --dev
```

Tests
-----
Run test suite with `pytest` in virtual environment
```
$ pytest
```
Use `tox` to run test suite against all supported python versions
```
$ tox
```

Local Build
-----------

Build source distribution and wheels into `dist/` directory.
```
$ python -m build
```