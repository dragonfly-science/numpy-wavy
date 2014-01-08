import os
import unittest
import numpy as np
from cStringIO import StringIO

from wavy import get_audio, slice_wave

class TestThreeSeconds(unittest.TestCase):
    def setUp(self):
        self.audio, self.framerate = get_audio('test/three-second.wav')

    def test_framerate(self):
        self.assertEqual(self.framerate, 8000)

    def test_threeseconds(self):
        self.assertEqual(len(self.audio), 24000)

    def test_array(self):
        self.assertEqual(type(self.audio), np.ndarray)

class TestFramerate(unittest.TestCase):
    def test_halfsampling(self):
        audio, framerate = get_audio('test/three-second.wav', max_framerate=4000)
        self.assertEqual(len(audio), 12000)
        self.assertEqual(framerate, 4000)
    
    def test_subsampling(self):
        audio, framerate = get_audio('test/three-second.wav', max_framerate=6000)
        self.assertEqual(len(audio), 12000)
        self.assertEqual(framerate, 4000)
    
    def test_third_sampling(self):
        audio, framerate = get_audio('test/three-second.wav', max_framerate=3000)
        self.assertEqual(len(audio), 8000)
        self.assertEqual(framerate, 8000/3.0)
    
    def test_no_upsampling(self):
        audio, framerate = get_audio('test/three-second.wav', max_framerate=10000)
        self.assertEqual(len(audio), 24000)
        self.assertEqual(framerate, 8000)
    
    def test_keep_framerate(self):
        audio, framerate = get_audio('test/three-second.wav', max_framerate=8000)
        self.assertEqual(len(audio), 24000)
        self.assertEqual(framerate, 8000)

class TestOffset(unittest.TestCase):
    def setUp(self):
        self.audio, self.framerate = get_audio('test/three-second.wav')
    
    def test_offset(self):
        audio2, framerate2 = get_audio('test/three-second.wav', offset=1)
        self.assertEqual(len(audio2), 16000)
        self.assertEqual(audio2[0], self.audio[8000])

    def test_offset_duration(self):
        audio1, framerate1 = get_audio('test/three-second.wav', offset=1, duration=1)
        self.assertEqual(len(audio1), 8000)
        self.assertEqual(audio1[0], self.audio[8000])

    def test_duration(self):
        audio0, framerate0 = get_audio('test/three-second.wav', duration=0.5)
        self.assertEqual(len(audio0), 4000)
        self.assertEqual(audio0[0], self.audio[0])

class TestSlice(unittest.TestCase):
    def setUp(self):
        self.one_second = StringIO()
        slice_wave('test/three-second.wav', self.one_second, offset=1, duration=1)
        self.low_framerate = StringIO()
        slice_wave('test/three-second.wav', self.low_framerate, max_framerate=4000)
    
    def test_slice_length(self):
        self.one_second.seek(0)
        audio1, framerate1 = get_audio(self.one_second)
        self.assertEqual(len(audio1), 8000)
        self.assertEqual(framerate1, 8000)

    def test_slice(self):
        self.one_second.seek(0)
        audio3, framerate3 = get_audio('test/three-second.wav')
        audio1, framerate1 = get_audio(self.one_second)
        self.assertEqual(audio3[8000], audio1[0])

    def test_low_framerate(self):
        self.low_framerate.seek(0)
        audio, framerate = get_audio(self.low_framerate)
        self.assertEqual(len(audio), 12000)
        self.assertEqual(framerate, 4000)
    
    def test_subsampling(self):
        self.low_framerate.seek(0)
        audio, framerate = get_audio(self.low_framerate)
        audio3, framerate3 = get_audio('test/three-second.wav')
        self.assertEqual(audio[2000], audio3[4000])

