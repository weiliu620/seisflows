import unittest

import os
import struct
from tempfile import NamedTemporaryFile

import seisflows.tools.io as tools


class TestBinaryReader(unittest.TestCase):
    def setUp(self):
        # Create a temporary binary file. Make sure it is not deleted upon
        # closing.
        self.tmp_file = NamedTemporaryFile(mode='wb', delete=False)

    def tearDown(self):
        os.remove(self.tmp_file.name)

    def test_read_native_chars(self):
        # Write some binary values
        value = 'abcdef'
        self.tmp_file.file.write(bytearray(value))
        self.tmp_file.close()

        # Read the values back
        reader = tools.BinaryReader(self.tmp_file.name, endian='=')
        r = reader.read('c', len(value), 0)
        self.assertEqual(r, list(value))

    def test_scan(self):
        # Write some binary values
        fmts = [
            ['int32', 1, 0, 'Int32Bits'],
            ['int16', 1, 4, 'Int16Bits'],
            ['char', 1, 6, 'Character']]
        values = (42, 33, 'a')
        endian = '='  # native
        s = struct.Struct(endian + 'i h c')
        self.tmp_file.write(s.pack(*values))
        self.tmp_file.close()

        # Read the values back
        reader = tools.BinaryReader(self.tmp_file.name, endian='=')
        r = reader.scan(fmts)
        self.assertEqual(r['Int32Bits'], 42)
        self.assertEqual(r['Int16Bits'], 33)
        self.assertEqual(r['Character'], 'a')
