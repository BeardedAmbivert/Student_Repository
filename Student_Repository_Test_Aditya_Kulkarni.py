import unittest

from Project.HW09_Aditya_Kulkarni import University


class MyTestCase(unittest.TestCase):
    def test_University(self):
        stevens: University = University("C:\\Users\\rajek\\PycharmProjects\\untitled\\Project")
        self.assertEqual(stevens._students["10115"].info(), ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567',
                                                                                   'SSW 687']))
        self.assertEqual(stevens._students["11399"].info(), ('11399', 'Cordova, I', ['SSW 540']))
        self.assertNotEqual(stevens._students["10115"].info(), ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567']))
        self.assertNotEqual(stevens._students["11399"].info(), ('11399', 'Cordova, I', ['CS 540']))

        self.assertEqual(stevens._instructors["98760"].info(), ([['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]))
        self.assertEqual(stevens._instructors["98765"].info(), ([['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                                                                 ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]]))
        self.assertNotEqual(stevens._instructors["98760"].info(), ([['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                                                                 ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2]]))
        self.assertNotEqual(stevens._instructors["98765"].info(), ([['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4]]))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
