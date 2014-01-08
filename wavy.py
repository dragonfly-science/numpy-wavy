"Functions for reading wave files into numpy"""
import wave
import struct
import math
from contextlib import closing

import numpy as np

_formats = {1: "<%dB", 2:"<%dh", 4:"<%dl"}
_zeroline = {1: 128, 2: 0 , 4: 0}

def _get_frames(in_file, offset=0, duration=0):
    """Return a section of a wavefile as a string of bytes"""
    with closing(wave.open(in_file)) as wav:
        params = wav.getparams()
        nchannels = params[0]
        framerate = params[2]
        nframes = params[3]
        wav.setpos(int(offset*framerate*nchannels))
        if not duration:
            duration = nframes/float(framerate*nchannels) - offset
        return wav.readframes(int(duration*framerate*nchannels)), params

def get_audio(in_file, offset=0, duration=0, max_framerate=None):
    """Return the audio from a wavefile as an array"""
    frames, params = _get_frames(in_file=in_file, offset=offset, duration=duration)
    nchannels = params[0]
    sampwidth = params[1]
    framerate = params[2]
    audio = np.array(struct.unpack_from (_formats[sampwidth] % (len(frames)/sampwidth,), frames)) - \
        _zeroline[sampwidth]
    if nchannels > 1:
        audio.reshape((-1, nchannels))
    if max_framerate:
        subsampling = int(math.ceil(framerate/float(max_framerate)))
        if subsampling  > 1:
            audio = audio[::int(subsampling),]
            framerate = framerate/float(subsampling)
    return audio, framerate

def slice_wave(in_file, out_file, offset=0, duration=0, max_framerate=None):
    """Write a section of a wavefile to a new file"""
    with closing(wave.open(in_file)) as win:
        params = win.getparams()
    wav = wave.open(out_file, 'wb')
    try:
        if not max_framerate:
            frames, params = _get_frames(in_file, offset, duration)
        else:
            audio, framerate = get_audio(in_file, offset=offset, duration=duration, max_framerate=max_framerate)
            params = list(params)
            if len(audio.shape) == 1:
                params[0] = 1
            else:
                params[0] = audio.shape[1]
            params[2] = framerate
            audio = audio.flatten() + _zeroline[params[1]]
            frames = struct.pack(_formats[params[1]] % (len(audio),), *audio)
        wav.setparams(params)
        wav.writeframes(frames)
    finally:
        try:
            wav.close()
        except:
            pass




