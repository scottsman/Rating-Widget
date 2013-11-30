import os

from PyQt4 import QtCore, QtGui


class RatingWidget(QtGui.QWidget):
    """A QWidget that enables a user to choose a rating.
    """

    def __init__(self, parent=None, icon_path=None, num_icons=5):
        """Constructor.

        Kwargs:
            parent (QtCore.QObject): Parent of the RatingWigdet.
            icon_path (str): The location of the icon used to represent one value of a
                rating.
            num_icons (int): The number of icons the RatingWidget will display.
        """
        super(RatingWidget, self).__init__(parent)

        # Set defaults.
        self._value = 0
        self._max_value = num_icons

        # Fallback for the icon_path.
        if not icon_path:
            icon_path = os.path.join(os.path.dirname(__file__), 'rating.png')

        # Dynamically create QWidget layout.
        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(0)

        # Add icons to the layout.
        self.icons = []
        for icon_value in range(1, self._max_value+ 1):
            icon_label = IconLabel(icon_path, icon_value, parent=self)

            self.icons.append(icon_label)
            hbox.addWidget(icon_label)


        # Set the created layout to the widget.
        self.setLayout(hbox)

        self.installEventFilter(self)

    def setActiveIconsVisible(self):
        """Display any icons that are active.
        """
        for icon in self.icons:
            if icon.active:
                icon.setImage(True)
            else:
                icon.setImage(False)

    def setIconsActive(self, icon_label, active):
        """Update the icons active state.

        All icons less and equal to the value of the icon_label have their active status
        set to True. Everything higher than the icon_label have their active
        status set to False.
        eg. If icon_label 3 is passed in, then 1, 2 and 3 are active
           and 4 and 5 are innactive. 

        If active is False then all icons visibility is reset according to their
        active status.

        Args:
            icons_label (IconLabel): The icon to update to.
            active (bool): Control if if the icons active state are set or used.
                TODO. Remove/Rename this. Confusing and it doesn't look like it's being used.
        """
        if active:
            self._value = icon_label.value
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
        """Update the icons visibility.

        Args:
            icons_label (IconLabel): The icon to update to.
            visible (bool): Control if the visibility is set based on the icon_label
                or the active status.
                TODO. Rename this. Confusing.
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
        """Event filter defining custom actions.

        Args:
            obj (QObject): Unused by this derived method.
            event (QEvent): The event that occured.

        Returns:
            (bool) True. So the event can be handled further if required.
        """
        # When the mouse leaves the widget, set the icons visibility to it's value state.
        if event.type() == QtCore.QEvent.Leave:
            self.setActiveIconsVisible()
        else:
            super(RatingWidget, self).eventFilter(obj, event)
        return False

    @property
    def value(self):
        return self._value

    @property
    def max_value(self):
        return self._max_value


class IconLabel(QtGui.QLabel):
    """A Qlabel that to represent an icon in the rating widget.
    """
    def __init__(self, image_path, value, parent=None):
        """Constructor.
        Args:
            image_path (str): Path to the image to use for the icon.
            value (int): value of the icon.
            parent (QObject): Parent object for this class.
        """
        super(IconLabel, self).__init__(parent)

        self.image_path = image_path
        self.parent = parent
        self.active = False
        self.value = value

        # Enable mouse events without buttons being held down.
        self.setMouseTracking(True)

        self.installEventFilter(self)

    def setImage(self, value):
        """Set the image for the label.

        Args:
            value (bool): Flag for whether to use the image_path or no image for
                the in picture in the label.
        """
        if value:
            self.setPixmap(QtGui.QPixmap(self.image_path))
        else:
            # TODO. Could have a empty equivalent of the image_path.
            self.setPixmap(QtGui.QPixmap(None))

    def eventFilter(self, obj, event):
        """Event filter defining custom actions.
        """
        # When the mouse _enters_ the label area, set the icon visible.
        if event.type() == QtCore.QEvent.Enter:
            self.parent.setIconsVisible(self, True)
        # When the mouse _leaves_ the label area, set the icon invisible.
        elif event.type() == QtCore.QEvent.Leave:
            self.parent.setIconsVisible(self, False)
        # When the mouse _clicks_ the label area, set the icon active.
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.parent.setIconsActive(self, True)
        else:
            super(IconLabel, self).eventFilter(obj, event)
        return False
