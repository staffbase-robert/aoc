import unittest
from day9 import move_tail, move

class Test_move_tain(unittest.TestCase):

    def test_easy(self):
        self.assertEqual((0,1), move_tail((0,2), (0,0)))
        self.assertEqual((1,0), move_tail((2,0), (0,0)))

    def test_move_diag(self):
        self.assertEqual((1,1), move_tail((1,2), (0,0)))
        self.assertEqual((-1,-1), move_tail((-1,-2), (0,0)))
        self.assertEqual((1,-1), move_tail((1,-2), (0,0)))
        self.assertEqual((-1,-1), move_tail((-2,-1), (0,0)))

    def test_no_move(self):
        self.assertEqual((1,1), move_tail((0,0), (1,1)))
        self.assertEqual((0,0), move_tail((-1,-1), (0,0)))
        self.assertEqual((0,0), move_tail((-1,1), (0,0)))
        self.assertEqual((0,0), move_tail((1,-1), (0,0)))
        self.assertEqual((0,0), move_tail((1,1), (0,0)))

    def test_multiple(self):
        H = (0,0)
        T = H
        H_want = [
            (0,0), (1,0), (2,0), (3,0), (4,0),
            (4,-1), (4,-2), (4,-3), (4,-4),
            (3,-4), (2,-4), (1,-4), 
            (1,-3),
            (2,-3), (3,-3), (4,-3), (5,-3),
            (5,-2),
            (4,-2), (3,-2), (2,-2), (1,-2), (0,-2),
            (1,-2), (2,-2)
        ]
        T_want = [
            (0,0), (0,0), (1,0), (2,0), (3,0),
            (3, 0), (4,-1), (4,-2), (4,-3),
            (4,-3), (3,-5), (2,-5),
            (2,-5),
            # (2,-3), (3,-3), (4,-3), (5,-3),
            # (5,-2),
            # (4,-2), (3,-2), (2,-2), (1,-2), (0,-2),
            # (1,-2), (2,-2)
        ]

        i = 0
        for inst in [
            "R", "R", "R", "R", 
            "U", "U", "U", "U",
            "L", "L", "L",
            "D",
            "R", "R", "R", "R",
            "D",
            "L", "L", "L", "L", "L",
            "R", "R"
        ]:
            self.assertEqual(H_want[i], H)
            if len(T) >= i:
                self.assertEqual(T_want[i], T)
            i+=1
            H = move(H, inst[0])
            T = move_tail(H, T)
        self.assertEqual((2, -2), H)
        self.assertEqual((1, -2), T)

if __name__ == '__main__':
    unittest.main()
