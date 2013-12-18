import sys

import unittest
import ratingWidget

from PyQt4 import QtGui, QtCore
from PyQt4.QtTest import QTest

class TestRatingWidget(unittest.TestCase):

    def setUp(self):
        """Create a QApplication.
        """
        self.app = QtGui.QApplication(sys.argv)
        QtGui.qApp = self.app

    def tearDown(self):
        """Remove the QApplication
        """
        QtGui.qApp = None
        self.app = None

    def test_num_icons(self):
        """Assert the correct number of icons is created.
        """
        rating_widget = ratingWidget.RatingWidget(num_icons=3)
        self.assertTrue(len(rating_widget.icons) == 3)

    def test_set_icons_active(self):
        """Assert that set_icons_active correctly sets icons active
        """
        rating_widget = ratingWidget.RatingWidget(num_icons=5)

        # Assert all icons are initially false.
        # Could be it's own test, but helps assert there is a change in active state.
        for icon in rating_widget.icons:
            self.assertFalse(icon.active)

        test_icon = rating_widget.icons[2]
        rating_widget.set_icons_active(test_icon)

        # Assert all icons with a value less than or equal to the chosen icon,
        # are active.
        for icon in rating_widget.icons:
            self.assertEqual(icon.active, (icon.value <= test_icon.value))

    def test_active_icons_visible(self):
        """Assert that set_active_icons_visible correctly sets the visibility
        for active icons.
        """
        rating_widget = ratingWidget.RatingWidget(num_icons=5)

        limit = 3

        # Set icons below the limit to active
        for count, icon in enumerate(rating_widget.icons):
            if count < limit:
                icon.active = True
            else:
                icon.active = False

        # Assert that all icons are not visible for the sake of the test.
        for icon in rating_widget.icons:
            self.assertFalse(icon.visible)

        # Set all active icons visible.
        rating_widget.set_active_icons_visible()

        # Assert all active icons are now visible.
        for count, icon in enumerate(rating_widget.icons):
            self.assertEqual(icon.visible, bool(count < limit))


class TestIconLabel(unittest.TestCase):

    def test_num_icons(self):
        pass

if __name__ == "__main__":
    unittest.main()
