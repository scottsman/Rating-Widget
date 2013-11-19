import os

from PyQt4 import QtCore, QtGui


class RatingWidget(QtGui.QWidget):
    """
    """

    def __init__(self, parent=None, icon_path=None, num_icons=5):
        """
        """
        super(RatingWidget, self).__init__(parent)

        self.value = 0
        self.max_value = num_icons

        if not icon_path:
            icon_path = os.path.join(os.path.dirname(__file__), 'rating.png')

        # Dynamically create QWidget layout
        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(0)

        # Add icons to the layout
        self.icons = []
        for icon_value in range(1, num_icons + 1):
            icon_label = IconLabel(icon_path, icon_value, parent=self)

            self.icons.append(icon_label)
            hbox.addWidget(icon_label)


        self.setLayout(hbox)

        self.installEventFilter(self)

    def setActiveIconsVisible(self):
        for icon in self.icons:
            if icon.active:
                icon.setImage(True)
            else:
                icon.setImage(False)

    def setIconsActive(self, icon_label, active):
        if active:
            self.value = icon_label.value
            for icon in self.icons:
                if icon.value <= icon_label.value:
                    icon.active = True
                    icon.setImage(True)
                else:
                    icon.active = False
                    icon.setImage(False)
        else:
            self.setActiveIconsVisible()

    def setIconsVisible(self, icon_label, visible):
        if visible:
            for icon in self.icons:
                if icon.value <= icon_label.value:
                    icon.setImage(True)
                else:
                    icon.setImage(False)
        else:
            self.setActiveIconsVisible()

    def eventFilter(self, obj, event):
        """
        """
        if event.type() == QtCore.QEvent.Leave:
            self.setActiveIconsVisible()
        return False


class IconLabel(QtGui.QLabel):
    """
    """
    def __init__(self, image_path, value, parent=None):
        """
            Args:
                value (int): value of the icon
        """
        super(IconLabel, self).__init__(parent)

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
            self.parent.setIconsVisible(self, True)
        elif event.type() == QtCore.QEvent.Leave:
            self.parent.setIconsVisible(self, False)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.parent.setIconsActive(self, True)
        return False

