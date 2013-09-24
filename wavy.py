"Functions for reading wave files into numpy"""
import wave
import numpy as np

_formats = {1: "<%dB", 2:"<%dh", 4:"<%dl"}
_zeroline = {1: 128, 2: 0 , 4: 0}

def _get_frames(in_file, offset=0, duration=0):
    """Return a section of a wavefile as a string of bytes"""
    wav = wave.open(in_file)
    params = wav.getparams()
    nchannels = params[0]
    framerate = params[2]
    wav.setpos(int(offset*framerate*nchannels))
    if not duration:
        duration = duration - offset
    return wav.readframes(int(duration*framerate*nchannels)), params

def get_audio(in_file, offset=0, duration=0):
    """Return the audio from a wavefile as an array"""
    frames, params = _get_frames(in_file=in_file, offset=offset, duration=duration)
    audio = np.array(struct.unpack_from (_formats[params[1]] % (len(frames)/params[1],), frames)) - 
        _zeroline[params[1]]
    if params[0] > 1:
        audio.reshape((-1, params[0]))
    return audio

def slice_wave(in_file, out_file, offset=0, duration=0):
    """Write a section of a wavefile to a new file"""
    wav = wave.open(out_file, 'wb')
    frames, params = get_frames(in_file, offset, duration)
    wav.setparams(params)
    wav.writeframes(frames)
    wav.close()

