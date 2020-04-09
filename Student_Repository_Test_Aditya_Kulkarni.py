import unittest

from Student_Repository_Aditya_Kulkarni import University


class MyTestCase(unittest.TestCase):
    def test_University(self):
        stevens: University = University("C:\\Users\\rajek\\PycharmProjects\\Student_Repository")
        self.assertEqual(stevens._students["10115"].info(), ['10115', 'Wyatt, X', 'SFEN',
                                                             ['SSW 567', 'SSW 564', 'SSW 687', 'CS 545'],
                                                             ['SSW 540', 'SSW 555'], [], 3.81])
        self.assertEqual(stevens._students["11399"].info(),
                         ["11399", "Cordova, I", "SYEN", ['SSW 540'], ['SYS 671', 'SYS 612', 'SYS 800'], [], 3.0])
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
        self.assertEqual(stevens._majors["SFEN"]._required, ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'])
        self.assertNotEqual(stevens._majors["SFEN"]._required, ['SSW 564', 'SSW 555', 'SSW 567'])
        self.assertEqual(stevens._majors["SFEN"]._electives, ['CS 501', 'CS 513', 'CS 545'])
        self.assertNotEqual(stevens._majors["SFEN"]._electives, ['CS 501', 'CS 545'])
        self.assertEqual(stevens._majors["SYEN"]._required, ['SYS 671', 'SYS 612', 'SYS 800'])
        self.assertNotEqual(stevens._majors["SYEN"]._required, ['SSW 810', 'SSW 565', 'SSW 540'])
        self.assertEqual(stevens._majors["SYEN"]._electives, ['SSW 810', 'SSW 565', 'SSW 540'])
        self.assertNotEqual(stevens._majors["SYEN"]._electives, ['SSW 810', 'SSW 540'])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
