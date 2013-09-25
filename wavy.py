"Functions for reading wave files into numpy"""
import wave
import numpy as np
import struct

_formats = {1: "<%dB", 2:"<%dh", 4:"<%dl"}
_zeroline = {1: 128, 2: 0 , 4: 0}

def _get_frames(in_file, offset=0, duration=0):
    """Return a section of a wavefile as a string of bytes"""
    wav = wave.open(in_file)
    params = wav.getparams()
    nchannels = params[0]
    framerate = params[2]
    nframes = params[3]
    wav.setpos(int(offset*framerate*nchannels))
    if not duration:
        duration = nframes/float(framerate*nchannels) - offset
    return wav.readframes(int(duration*framerate*nchannels)), params

def get_audio(in_file, offset=0, duration=0):
    """Return the audio from a wavefile as an array"""
    frames, params = _get_frames(in_file=in_file, offset=offset, duration=duration)
    nchannels = params[0]
    sampwidth = params[1]
    framerate = params[2]
    audio = np.array(struct.unpack_from (_formats[sampwidth] % (len(frames)/sampwidth,), frames)) - \
        _zeroline[sampwidth]
    if nchannels > 1:
        audio.reshape((-1, nchannels))
    return audio, framerate

def slice_wave(in_file, out_file, offset=0, duration=0):
    """Write a section of a wavefile to a new file"""
    wav = wave.open(out_file, 'wb')
    try:
        frames, params = _get_frames(in_file, offset, duration)
        wav.setparams(params)
        wav.writeframes(frames)
    finally:
        try:
            wav.close()
        except:
            pass


