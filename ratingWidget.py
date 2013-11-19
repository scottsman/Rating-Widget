import os

from PyQt4 import QtCore, QtGui


class RatingWidget(QtGui.QWidget):
    """
    """

    def __init__(self, parent=None, star_path=None, num_stars=5):
        """
        """
        super(RatingWidget, self).__init__(parent)

        self.value = 0
        self.max_value = num_stars

        if not star_path:
            star_path = os.path.join(os.path.dirname(__file__), 'rating.png')

        # Dynamically create QWidget layout
        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(0)

        # Add stars to the layout
        self.stars = []
        for star_value in range(1, num_stars + 1):
            star_label = StarLabel(star_path, star_value, parent=self)

            self.stars.append(star_label)
            hbox.addWidget(star_label)


        self.setLayout(hbox)

        self.installEventFilter(self)

    def setActiveStarsVisible(self):
        for star in self.stars:
            if star.active:
                star.setImage(True)
            else:
                star.setImage(False)

    def setStarsActive(self, star_label, active):
        if active:
            self.value = star_label.value
            for star in self.stars:
                if star.value <= star_label.value:
                    star.active = True
                    star.setImage(True)
                else:
                    star.active = False
                    star.setImage(False)
        else:
            self.setActiveStarsVisible()

    def setStarsVisible(self, star_label, visible):
        if visible:
            for star in self.stars:
                if star.value <= star_label.value:
                    star.setImage(True)
                else:
                    star.setImage(False)
        else:
            self.setActiveStarsVisible()

    def eventFilter(self, obj, event):
        """
        """
        if event.type() == QtCore.QEvent.Leave:
            self.setActiveStarsVisible()
        return False


class StarLabel(QtGui.QLabel):
    """
    """
    def __init__(self, image_path, value, parent=None):
        """
            Args:
                value (int): value of the star
        """
        super(StarLabel, self).__init__(parent)

        self.image_path = image_path
        self.parent = parent
        self.active = False
        self.value = value

        self.setMouseTracking(True)

        self.installEventFilter(self)

    def setImage(self, value):
        """
        """
        if value:
            self.setPixmap(QtGui.QPixmap(self.image_path))
        else:
            self.setPixmap(QtGui.QPixmap(None))

    def eventFilter(self, obj, event):
        """
        """
        if event.type() == QtCore.QEvent.Enter:
            self.parent.setStarsVisible(self, True)
        elif event.type() == QtCore.QEvent.Leave:
            self.parent.setStarsVisible(self, False)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.parent.setStarsActive(self, True)
        return False

