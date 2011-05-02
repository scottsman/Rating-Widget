from PyQt4 import QtCore, QtGui

class RatingWidget(QtGui.QWidget):
    """
    """
    
    def __init__(self, parent=None):
        """
        """
        QtGui.QWidget.__init__(self, parent)

        #temp color
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 0, 0))
        self.setPalette(palette)

        star_path = '/home/scottsman/Downloads/rating/rating.png'
        oneStar = StarLabel(star_path, 1, self)
        twoStar = StarLabel(star_path, 2, self)
        threeStar = StarLabel(star_path, 3, self)
        fourStar = StarLabel(star_path, 4, self)
        fiveStar = StarLabel(star_path, 5, self)
        self.stars = [oneStar, twoStar, threeStar, fourStar, fiveStar]

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(oneStar)
        hbox.addWidget(twoStar)
        hbox.addWidget(threeStar)
        hbox.addWidget(fourStar)
        hbox.addWidget(fiveStar)
        hbox.setSpacing(0)

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
            for star in self.stars:
                if star.value <= star_label.value:
                    star.active = True
                    star.visible = True
                    star.setImage(True)
                else:
                    star.active = False
                    star.visible = False
                    star.setImage(False)
        else:
            self.setActiveStarsVisible()

    def setStarsVisible(self, star_label, visible):
        if visible:
            for star in self.stars:
                if star.value <= star_label.value:
                    star.visible = True
                    star.setImage(True)
                else:
                    star.visible = False
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
        QtGui.QLabel.__init__(self, parent)

        self.image_path = image_path
        self.parent = parent
        self.active = False
        self.visible = False
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
        if event.type() == QtCore.QEvent.Enter:# and self.active == False:
            self.parent.setStarsVisible(self, True)
        elif event.type() == QtCore.QEvent.Leave:# and self.active == False:
            self.parent.setStarsVisible(self, False)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:# and self.active == False:
            self.parent.setStarsActive(self, True)
        '''
        elif event.type() == QtCore.QEvent.MouseButtonRelease and self.active == True:
            self.parent.setStarsActive(self, False)
        '''
        return False
