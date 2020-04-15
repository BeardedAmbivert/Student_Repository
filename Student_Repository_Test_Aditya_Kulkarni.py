import unittest

from Student_Repository_Aditya_Kulkarni import University


class MyTestCase(unittest.TestCase):
    def test_University(self):
        stevens: University = University("C:\\Users\\rajek\\PycharmProjects\\Student_Repository")
        self.assertEqual(stevens._students["10115"].info(), ['10115', 'Bezos, J', 'SFEN', ['SSW 810', 'CS 546'],
                                                             ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 2.0])
        self.assertEqual(stevens._students["10103"].info(), ['10103', 'Jobs, S', 'SFEN', ['SSW 810', 'CS 501'],
                                                             ['SSW 540', 'SSW 555'], [], 3.38])
        self.assertNotEqual(stevens._students["10115"].info(), ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567']))
        self.assertNotEqual(stevens._students["10103"].info(), ('11399', 'Cordova, I', ['CS 540']))

        self.assertEqual(stevens._instructors["98762"].info(), ([['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                                                                 ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                                                                 ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]))
        self.assertEqual(stevens._instructors["98763"].info(), ([['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                                                                 ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1]]))
        self.assertNotEqual(stevens._instructors["98762"].info(), ([['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                                                                    ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                                                                    ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2]]))
        self.assertNotEqual(stevens._instructors["98763"].info(), ([['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4]]))
        self.assertEqual(stevens._majors["SFEN"]._required, ['SSW 540', 'SSW 810', 'SSW 555'])
        self.assertNotEqual(stevens._majors["SFEN"]._required, ['SSW 564', 'SSW 555', 'SSW 567'])
        self.assertEqual(stevens._majors["SFEN"]._electives, ['CS 501', 'CS 546'])
        self.assertNotEqual(stevens._majors["SFEN"]._electives, ['CS 501', 'CS 545'])
        self.assertEqual(stevens._majors["CS"]._required, ['CS 570', 'CS 546'])
        self.assertNotEqual(stevens._majors["CS"]._required, ['CS 810', 'CS 540'])
        self.assertEqual(stevens._majors["CS"]._electives, ['SSW 810', 'SSW 565'])
        self.assertNotEqual(stevens._majors["CS"]._electives, ['SSW 810', 'SSW 540'])
        self.assertEqual(list(stevens._student_grades_table_db_test("student_repo.sqlite")),
                         [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                          ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                          ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                          ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                          ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                          ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                          ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                          ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                          ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')])
        self.assertNotEqual(list(stevens._student_grades_table_db_test("student_repo.sqlite")),
                            [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                             ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                             ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                             ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
