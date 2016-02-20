from sequence import *
import unittest

class test_sequence(unittest.TestCase):
    def test_sequence_equal(self):
        """
        Test that sequence comparison is working as we intend.
        """
        x1 = []
        x2 = []
        for i in range(1, 100):
            x = sequence_generate_entry()
            x1.append(x)
            x2.append(Sequence_Entry(x.color_abbrev))

        self.assertEqual(x1, x2)
        self.assertTrue(sequence_equal(x1, x2))

        self.assertFalse(sequence_equal(x1, x2[0:len(x2)/2]))
        self.assertFalse(sequence_equal(x1[0:len(x1)/2], x2))

        self.assertEqual(sequence_common(x1, x2[0:len(x2)/2]), len(x2)/2)
        self.assertEqual(sequence_common(x1[0:len(x1)/2], x2), len(x1)/2)


    def test_sequence_creation(self):
        for i in range(1, 100):
            x = sequence_generate_entry()
            y = sequence_generate_entry()        
        self.assertNotEqual(x, y)


if __name__ == '__main__':
    unittest.main()
