import numpy, unittest

from bibliopixel.util import colors, color_list, log
from bibliopixel.util.color_list import ListMath, NumpyMath

COLORS1 = [colors.Red, colors.Green, colors.Blue, colors.White]
COLORS2 = [colors.Black, colors.Blue, colors.Red, colors.Black]
SUM12 = [colors.Red, colors.Cyan, colors.Magenta, colors.White]
WHITES = [colors.White, colors.White, colors.White, colors.White]
BLACKS = [colors.Black, colors.Black, colors.Black, colors.Black]


def make_numpy(cl):
    return numpy.array(cl, dtype='uint8')


class TestBase(unittest.TestCase):
    def assert_list_equal(self, actual, expected):
        x, y = actual, expected
        if hasattr(x, 'shape'):
            equals = numpy.array_equal(x, make_numpy(y))
        else:
            log.printer(type(x), type(y))
            equals = (x == y)
        if not equals:
            log.printer('____')
            log.printer(x)
            log.printer('NOT EQUAL')
            log.printer(y)
            log.printer('____')
        self.assertTrue(equals)


class ColorListTest(TestBase):
    def test_simple(self):
        self.assertIs(numpy, color_list.numpy)

        self.assertFalse(color_list.is_numpy([]))
        self.assertTrue(color_list.is_numpy(make_numpy([])))

        self.assertIs(color_list.Math(False), ListMath)
        self.assertIs(color_list.Math(True), NumpyMath)

    def test_lists(self):
        cl1 = COLORS1[:]
        cl2 = COLORS2[:]
        ListMath.add(cl1, cl2, 0)
        self.assert_list_equal(cl1, COLORS1)
        ListMath.add(cl1, cl2)
        self.assert_list_equal(cl1, SUM12)

    def test_numpy(self):
        cl1 = make_numpy(COLORS1)
        cl2 = make_numpy(COLORS2)
        NumpyMath.add(cl1, cl2, 0)
        self.assert_list_equal(cl1, COLORS1)
        NumpyMath.add(cl1, cl2, 1)
        self.assert_list_equal(cl1, SUM12)

    def test_clear_list(self):
        cl = COLORS1[:]
        ListMath.clear(cl)
        self.assert_list_equal(cl, BLACKS)

    def test_clear_numpy(self):
        cl = make_numpy(COLORS1)
        NumpyMath.clear(cl)
        self.assert_list_equal(cl, BLACKS)
        self.assert_list_equal(cl, BLACKS)

    def test_copy_list(self):
        cl = COLORS1[:]
        ListMath.copy(cl, COLORS2)
        self.assert_list_equal(cl, COLORS2)

    def test_copy_numpy(self):
        cl = make_numpy(COLORS1)
        NumpyMath.copy(cl, make_numpy(COLORS2))
        self.assert_list_equal(cl, COLORS2)


class MixerTest(TestBase):
    def do_test(self, mixer, thirds):
        self.assertEqual(mixer.levels, [0, 0, 0])
        self.assert_list_equal(mixer.color_list, COLORS1)

        mixer.mix()
        self.assert_list_equal(mixer.color_list, COLORS1)

        mixer.clear()
        mixer.mix()

        self.assert_list_equal(mixer.color_list, BLACKS)

        mixer.levels[:] = [1, 0, 0]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, COLORS2)

        mixer.levels[:] = [0, 1, 0]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, WHITES)

        mixer.levels[:] = [0, 0, 1]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, BLACKS)

        mixer.levels[:] = [1 / 3, 1 / 3, 1 / 3]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, thirds)

        mixer.levels[:] = [1, 1, 1]
        mixer.clear()
        mixer.mix(1 / 3)
        self.assert_list_equal(mixer.color_list, thirds)

    def test_lists(self):
        mixer = color_list.Mixer(COLORS1[:], [COLORS2, WHITES, BLACKS])
        self.do_test(mixer,
                     [(85, 85, 85), (85, 85, 170), (170, 85, 85), (85, 85, 85)])

    def test_numpy(self):
        mixer = color_list.Mixer(
            make_numpy(COLORS1), [make_numpy(COLORS2), make_numpy(WHITES), make_numpy(BLACKS)])
        self.do_test(mixer,
                     [(85, 85, 85), (85, 85, 170), (170, 85, 85), (85, 85, 85)])


del TestBase
