import os
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

    def _setup_icons_active(self, rating_widget, limit):
        """Helper to set a certain number of icons active but not visible.

        Args:
            rating_widget (QWidget): The rating widget being tested.
            limit (int): The amount of icons to set active.
        """
        # Set icons below the limit to active
        for count, icon in enumerate(rating_widget.icons):
            if count < limit:
                icon.active = True
            else:
                icon.active = False

        # Assert that all icons are not visible for the sake of the test.
        for icon in rating_widget.icons:
            self.assertFalse(icon.visible)

    def test_active_icons_visible(self):
        """Assert that set_active_icons_visible correctly sets the visibility
        for active icons.
        """
        rating_widget = ratingWidget.RatingWidget(num_icons=5)

        limit = 3

        self._setup_icons_active(rating_widget, limit)

        # Set all active icons visible.
        rating_widget.set_active_icons_visible()

        # Assert all active icons are now visible.
        for count, icon in enumerate(rating_widget.icons):
            self.assertEqual(icon.visible, bool(count < limit))

    def test_set_icons_active(self):
        """Assert that set_icons_active correctly sets icons active up to
        a specified icon.
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

    def test_set_icons_visible(self):
        """Assert that set_icons_visible correctly sets visibility up to
        a specified icon.
        """
        rating_widget = ratingWidget.RatingWidget(num_icons=5)

        # Assert all icons are initially not visible.
        # Could be it's own test, but helps assert there is a change in visibility state.
        for icon in rating_widget.icons:
            self.assertFalse(icon.visible)

        test_icon = rating_widget.icons[2]
        rating_widget.set_icons_visible(test_icon)

        # Assert all icons with a value less than or equal to the chosen icon,
        # are visible.
        for icon in rating_widget.icons:
            self.assertEqual(icon.visible, (icon.value <= test_icon.value))

    def test_eventFilter(self):
        """Assert that the mouse leaving the widget triggers the icons
        to be set to their default state.
        """
        rating_widget = ratingWidget.RatingWidget(num_icons=5)

        limit = 3

        self._setup_icons_active(rating_widget, limit)

        # Trigger the event filter
        rating_widget.eventFilter(rating_widget, QtCore.QEvent(QtCore.QEvent.Leave))

        # Assert all active icons are now visible.
        for count, icon in enumerate(rating_widget.icons):
            self.assertEqual(icon.visible, bool(count < limit))

    def test_max_value(self):
        """Assert that the max_value is set correctly when setting the number
        of icons for the rating widget.
        """
        max_value = 10

        rating_widget = ratingWidget.RatingWidget(num_icons=max_value)

        self.assertEqual(rating_widget.max_value, max_value)

    def test_value(self):
        """Assert that the value of the rating_widget is updated and retreivable.
        """
        rating_widget = ratingWidget.RatingWidget(num_icons=5)
        self.assertEqual(rating_widget.value, 0)

        test_icon = rating_widget.icons[2]
        rating_widget.set_icons_active(test_icon)
        self.assertEqual(rating_widget.value, test_icon.value)

        test_icon = rating_widget.icons[4]
        rating_widget.set_icons_active(test_icon)
        self.assertEqual(rating_widget.value, test_icon.value)


class TestIconLabel(unittest.TestCase):

    _icon_path = os.path.join(os.path.dirname(__file__), '..', 'media', 'rating.png')

    def setUp(self):
        """Create a QApplication.
        """
        self.app = QtGui.QApplication(sys.argv)
        QtGui.qApp = self.app
        self.icon_label = ratingWidget.IconLabel(self._icon_path, 1)

    def tearDown(self):
        """Remove the QApplication
        """
        self.icon_label = None
        QtGui.qApp = None
        self.app = None

    def test_init(self):
        self.assertFalse(self.icon_label.active)
        self.assertFalse(self.icon_label.visible)
        self.assertEqual(self.icon_label.value, 1)

    def test_set_get_active(self):
        self.icon_label.active = True
        self.assertTrue(self.icon_label.active)

    def test_set_get_visible(self):
        self.icon_label.visible = True
        self.assertTrue(self.icon_label.visible)

    def test_set_image_not_set(self):
        self.assertFalse(self.icon_label.visible)

    def test_set_image_false(self):
        self.icon_label.set_image(False)
        self.assertFalse(self.icon_label.visible)

    def test_set_image_true(self):
        self.icon_label.set_image(True)
        self.assertTrue(self.icon_label.visible)

    # Signal testing
    def assert_icon_emitted(self, icon_emitted):
        self.assertEqual(icon_emitted, self.icon_label)

    def test_eventFilter_enter(self):
        self.icon_label.mouse_enter_icon.connect(self.assert_icon_emitted)
        self.icon_label.eventFilter(self.icon_label, QtCore.QEvent(QtCore.QEvent.Enter))

    def test_eventFilter_leave(self):
        self.icon_label.mouse_leave_icon.connect(self.assert_icon_emitted)
        self.icon_label.eventFilter(self.icon_label, QtCore.QEvent(QtCore.QEvent.Leave))

    def test_eventFilter_mouseRelease(self):
        self.icon_label.mouse_release_icon.connect(self.assert_icon_emitted)
        QTest.mouseRelease(self.icon_label, QtCore.Qt.LeftButton)



if __name__ == "__main__":
    unittest.main()
