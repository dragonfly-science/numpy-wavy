import os
import unittest
import numpy as np

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
        slice_wave('test/three-second.wav', 'test/one-second.wav', offset=1, duration=1)
    
    def test_slice_length(self):
        audio1, framerate1 = get_audio('test/one-second.wav')
        self.assertEqual(len(audio1), 8000)
        self.assertEqual(framerate1, 8000)

    def test_slice(self):
        audio3, framerate3 = get_audio('test/three-second.wav')
        audio1, framerate1 = get_audio('test/one-second.wav')
        self.assertEqual(audio3[8000], audio1[0])

    def tearDown(self):
        os.remove('test/one-second.wav')
