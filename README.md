![Build Status](https://travis-ci.org/dragonfly-science/numpy-wavy.png)

numpy-wavy
==========

A python module for importing wave (`*.wav`) files into numpy. 

Contains a single module `wavy` providing the functions `get_audio` and `slice_wave`.

To read in a wavefile:

```py
from wavy import get_audio
audio = get_audio('soundfile.wav')
```

To read in the third second of the file:
```py
from wavy import get_audio
audio = get_audio('soundfile.wav', offset=2, duration=1)
```

To save the third second of the file to a new file:
```py
from wavy import slice_wave
slice_wav('soundfile.wav', 'second.wav', offset=2, duration=1)
```
To down sample an audio file, specify the `max_framerate` argument in either
`get_audio` or `slice_wave`. The audio will be
subsampled so that  the resulting framerate is less than or equal to `max_framerate`.
For example, to ensure that the framerate is less than or equal to 4k:
```py
from wavy import slice_wave
slice_wav('soundfile.wav', 'subsampled.wav', max_framerate=4000)
```



This was developed for a specific project, and is put here in
case other people find it useful. It hasn't been tested on a wide variety
of files. If you find that it doesn't work as expected, carry
out the usual pull request business.

Licence
=======

    Copyright (C) 2013  Dragonfly Science

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
