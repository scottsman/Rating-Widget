import os

from PyQt4 import QtCore, QtGui


class RatingWidget(QtGui.QWidget):
    """ A QWidget that enables a user to choose a rating.
    """

    def __init__(self, parent=None, icon_path=None, num_icons=5):
        """Constructor

        Kwargs:
            parent (QtCore.QObject): Parent of the RatingWigdet.
            icon_path (str): The location of the icon used to represent one value of a
                rating.
            num_icons (int): The number of icons the RatingWidget will display.
        """
        super(RatingWidget, self).__init__(parent)

        # Defaults
        self.value = 0
        self.max_value = num_icons

        # Fallback for the icon_path.
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
        """ Display any icons that are active.
        """
        for icon in self.icons:
            if icon.active:
                icon.setImage(True)
            else:
                icon.setImage(False)

    def setIconsActive(self, icon_label, active):
        """ Update the icons active state.

        All icons less and equal to the value of the icon_label have their active status
        set to True. Everything higher than the icon_label have their active
        status set to False.
        eg. If icon_label 3 is passed in, then 1, 2 and 3 are active
           and 4 and 5 are innactive. 

        If active is False then all icons visibility is reset according to their
        active status.

        Args:
            icons_label (IconLabel): The icon to update to.
        """
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
        """ Update the icons visibility
        """
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
        # Holds the state determining if the Icon is being used.
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

