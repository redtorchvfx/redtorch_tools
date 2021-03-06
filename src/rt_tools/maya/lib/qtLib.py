"""
qtLib.py

Author: Ehsan Hassani Moghaddam

"""

# python modules
import os
import sys
import subprocess
import traceback
import functools
import weakref

# Maya modules
import maya.cmds as mc
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets

# rt_tools modules
from . import fileLib
from . import decoratorLib

reload(fileLib)
reload(decoratorLib)

# CONSTANTS
GREY = (93, 93, 93)
SILVER = (150, 150, 150)
YELLOW = (200, 200, 130)
GREEN = (40, 220, 40)
RED = (220, 40, 40)

SILVER_LIGHT = (180, 180, 180)

GREY_DARK = (60, 60, 60)

GREEN_PASTAL = (100, 160, 100)
YELLOW_PASTAL = (210, 150, 90)
RED_PASTAL = (220, 100, 100)

GREEN_PALE = (130, 160, 130)
PURPLE_PALE = (180, 150, 180)
ORANGE_PALE = (200, 130, 80)

dirname = __file__.split('rt_tools')[0]
ICON_DIR = os.path.abspath(os.path.join(dirname, 'rt_tools', 'icon'))
SETTINGS_PATH = os.path.join(os.getenv("HOME"), 'testUI.uiconfig')


def setFGBGColor(widget, color, bgColor):
    widget.setStyleSheet("color: rgb{}; background-color: rgb{};".format(color, bgColor))


def setBGColor(widget, color, affectChildren=True):
    if affectChildren:
        widget.setStyleSheet("background-color: rgb{};".format(color))
    else:
        objName = widget.objectName()
        # widget.setObjectName('tempWidgetName')
        widget.setStyleSheet('#{}{{ background-color: rgb{}; }}'.format(objName, color))


def setColor(widget, color, affectChildren=True):
    if affectChildren:
        widget.setStyleSheet("color: rgb{};".format(color))
    else:
        objName = widget.objectName()
        widget.setStyleSheet('#{}{{ color: rgb{}; }}'.format(objName, color))


def resetColor(button):
    button.setStyleSheet("background-color: rgb{};".format(GREY))


def getMayaWindow():
    for obj in QtWidgets.QApplication.topLevelWidgets():
        try:
            if obj.objectName() == 'MayaWindow':
                return obj
        except:
            continue
    raise RuntimeError('Could not find MayaWindow instance')


def createGroupBox(parentLayout, label='newGroup', margins=6, spacing=4,
                   maxHeight=None, maxWidth=None, ignoreSizePolicy=False,
                   checkable=False, checked=False, mode='h'):
    if mode == 'h':
        bg_lay = QtWidgets.QHBoxLayout()
    else:
        bg_lay = QtWidgets.QVBoxLayout()

    gb = QtWidgets.QGroupBox(label)
    gb.setCheckable(checkable)
    gb.setChecked(checked)

    if maxHeight:
        gb.setMaximumHeight(maxHeight)

    if maxWidth:
        gb.setMaximumWidth(maxWidth)

    gb.setStyleSheet("QGroupBox { font: bold;\
                                  border: 1px solid rgb(40, 40, 40); \
                                  margin-top: 0.5em;\
                                  border-radius: 3px;}\
                      QGroupBox::title { top: -8px;\
                                         color: rgb(150, 150, 150);\
                                         padding: 0 5px 0 5px;\
                                         left: 10px;}")

    gb.setLayout(bg_lay)
    parentLayout.addWidget(gb)

    bg_lay.layout().setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
    bg_lay.setContentsMargins(margins, margins, margins, margins)
    bg_lay.setSpacing(spacing)

    if ignoreSizePolicy:
        gb.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

    return gb, bg_lay


def createVFrame(parent, margins=1, spacing=1):
    f = QtWidgets.QFrame()
    f.setFrameStyle(QtWidgets.QFrame.StyledPanel)
    parent.addWidget(f)

    vb = QtWidgets.QVBoxLayout()
    vb.setContentsMargins(margins, margins, margins, margins)
    vb.setSpacing(spacing)
    f.setLayout(vb)
    vb.layout().setAlignment(QtCore.Qt.AlignTop)
    return vb


def createHLayout(parent, maxHeight=None, maxWidth=None, margins=1, spacing=3):
    wid = QtWidgets.QWidget()
    parent.layout().addWidget(wid)

    if maxHeight:
        wid.setMaximumHeight(maxHeight)

    if maxWidth:
        wid.setMaximumWidth(maxWidth)

    lay = QtWidgets.QHBoxLayout()
    wid.setLayout(lay)
    lay.layout().setContentsMargins(margins, margins, margins, margins)
    lay.layout().setSpacing(spacing)
    lay.layout().setAlignment(QtCore.Qt.AlignTop)
    return lay


def createVLayout(parent, maxHeight=None, maxWidth=None, margins=4, spacing=4):
    wid = QtWidgets.QWidget()
    parent.layout().addWidget(wid)

    if maxHeight:
        wid.setMaximumHeight(maxHeight)

    if maxWidth:
        wid.setMaximumWidth(maxWidth)

    lay = QtWidgets.QVBoxLayout()
    parent.addLayout(lay)
    lay.layout().setContentsMargins(margins, margins, margins, margins)
    lay.layout().setSpacing(spacing)
    lay.layout().setAlignment(QtCore.Qt.AlignTop)
    return lay


def createComboBox(label, labelWidthMin=40, labelWidthMax=200, maxHeight=100, parent=None):
    if parent:
        wid = None
        lay = createHLayout(parent)
        lay.layout().setContentsMargins(1, 1, 1, 1)
        lay.layout().setSpacing(1)
    else:
        wid = QtWidgets.QWidget()
        lay = QtWidgets.QHBoxLayout()
        wid.setLayout(lay)
    lay.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    # lay.setAlignment(QtCore.Qt.AlignTop)
    lb = QtWidgets.QLabel(label)
    lb.setMinimumWidth(labelWidthMin)
    lb.setMaximumWidth(labelWidthMax)
    lb.setMaximumHeight(maxHeight)
    cb = QtWidgets.QComboBox()
    cb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
    lay.addWidget(lb)
    lay.addWidget(cb)
    cb.setMaximumHeight(maxHeight)
    return wid, lb, cb


def createCheckBox(label, labelWidthMin=40, labelWidthMax=200, parent=None):
    if parent:
        wid = None
        lay = createHLayout(parent)
        lay.layout().setContentsMargins(1, 1, 1, 1)
        lay.layout().setSpacing(1)
    else:
        wid = QtWidgets.QWidget()
        lay = QtWidgets.QHBoxLayout()
        wid.setLayout(lay)
    lay.setAlignment(QtCore.Qt.AlignLeft)
    lb = QtWidgets.QLabel(label)
    lb.setMinimumWidth(labelWidthMin)
    lb.setMaximumWidth(labelWidthMax)
    cb = QtWidgets.QCheckBox()
    cb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
    lay.addWidget(lb)
    lay.addWidget(cb)
    return wid, lb, cb


def createSpinBox(label, labelWidthMin=40, labelWidthMax=200, parent=None):
    if parent:
        wid = None
        lay = createHLayout(parent)
        lay.layout().setContentsMargins(1, 1, 1, 1)
        lay.layout().setSpacing(1)
    else:
        wid = QtWidgets.QWidget()
        lay = QtWidgets.QHBoxLayout()
        wid.setLayout(lay)
    lay.setAlignment(QtCore.Qt.AlignLeft)
    lb = QtWidgets.QLabel(label)
    lb.setMinimumWidth(labelWidthMin)
    lb.setMaximumWidth(labelWidthMax)
    cb = QtWidgets.QSpinBox()
    cb.setMaximum(99999)
    cb.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    lay.addWidget(lb)
    lay.addWidget(cb)
    return wid, lb, cb


def createLineEdit(label, labelWidthMin=40, labelWidthMax=200, parent=None):
    if parent:
        wid = None
        lay = createHLayout(parent)
        lay.layout().setContentsMargins(1, 1, 1, 1)
        lay.layout().setSpacing(1)
    else:
        wid = QtWidgets.QWidget()
        lay = QtWidgets.QHBoxLayout()
        wid.setLayout(lay)
    lay.setAlignment(QtCore.Qt.AlignLeft)
    lb = QtWidgets.QLabel(label)
    lb.setMinimumWidth(labelWidthMin)
    lb.setMaximumWidth(labelWidthMax)
    cb = QtWidgets.QLineEdit()
    cb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
    lay.addWidget(lb)
    lay.addWidget(cb)
    return wid, lb, cb


def createSeparator(parent):
    lay = QtWidgets.QHBoxLayout()
    parent.addLayout(lay)
    separator = QtWidgets.QFrame()
    separator.setFrameStyle(QtWidgets.QFrame.HLine)
    lay.addWidget(separator)


def createTreeWidget(parent=None, selectionMode='single', selectFocused=True):
    tw = QtWidgets.QTreeWidget()
    if parent:
        parent.layout().addWidget(tw)
    tw.setAlternatingRowColors(True)
    if selectionMode == 'single':
        tw.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    elif selectionMode == 'multi':
        tw.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    else:
        tw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    tw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
    tw.setIndentation(20)
    tw.setRootIsDecorated(True)
    tw.setAnimated(True)
    tw.header().setVisible(False)
    if selectFocused:
        tw.currentItemChanged.connect(doSelectFocused)
    return tw


def doSelectFocused(item):
    if not item:
        return
    tw = item.treeWidget()
    tw.setCurrentItem(item)


def addItemToTreeWidget(treeWidget, itemName, insert=False):
    # # font
    # nodeFont = QtGui.QFont()
    # nodeFont.setPointSize(8)

    # check if already added to tree
    alreadyExists = getItemInTree(treeWidget, itemName)
    if alreadyExists:
        treeWidget.setCurrentItem(alreadyExists)
        return alreadyExists

    # add item
    node_item = QtWidgets.QTreeWidgetItem()
    node_item.setText(0, itemName)
    # node_item.setFont(0, nodeFont)
    node_item.setFlags(node_item.flags())  # | QtCore.Qt.ItemIsUserCheckable)

    if insert:
        treeWidget.insertTopLevelItem(0, node_item)
    else:
        treeWidget.addTopLevelItem(node_item)

    return node_item


def clearLayout(lay):
    for i in reversed(range(lay.count())):
        lay.itemAt(i).widget().setParent(None)


def filterTW(tw, le):
    """
    Hides items in a QTreeWidget that don't match the text in the QLineEdit
    :param tw: QTreeWidget we want to filter the items for
    :param le: QLineEdit that holds the filter string
    :return: n/a
    """
    filter_text = le.text().lower()

    numItems = tw.topLevelItemCount()
    for i in range(numItems):
        item = tw.topLevelItem(i)

        # show items if no text is given
        if not filter_text:
            item.setHidden(False)
            continue

        # for j in filter_text:
        #     # hide item if given text is not found in it
        #     if j not in item.text(0).lower():
        #         item.setHidden(True)
        #         break
        #     # show item if given text is found in it
        #     else:
        #         item.setHidden(False)

        # hide item if given text is not found in it
        if filter_text.lower() not in item.text(0).lower():
            item.setHidden(True)
        # show item if given text is found in it
        else:
            item.setHidden(False)


def getSelectedItemAsText(tw):
    """
    return the text of currently selected item in given QTreeWidget
    :param tw: QTreeWidget we want to get the selected item for
    :return: text of currently selected item
    :rtype: string
    """
    item = getSelectedItem(tw)
    if item:
        return item.text(0)


def getSelectedItem(tw):
    items = tw.selectedItems()
    if items:
        return items[-1]


def getItemInTree(tw, text):
    numItems = tw.topLevelItemCount()
    for i in range(numItems):
        item = tw.topLevelItem(i)
        if item.text(0) == text:
            return item


def selectItemByText(tw, text, parentText=None):
    """
    given a QTreeWidget and a text, select the item with that text if exists
    :param tw: QTreeWidget to look for given text
    :param text: text to lookup in the given QTreeWidget
    :param parentText: if item is a child of another item, this is the text for parent
    :return: n/a
    """
    numItems = tw.topLevelItemCount()
    item_found = False

    for i in range(numItems):
        item = tw.topLevelItem(i)
        # item is a top level item
        if not parentText:
            if text == item.text(0):
                tw.setCurrentItem(item)
                item_found = True
                break

        # item is a child of a top level item
        else:
            if parentText == item.text(0):
                child_count = item.childCount()
                for j in range(child_count):
                    child_item = item.child(j)
                    if text == child_item.text(0):
                        tw.setCurrentItem(child_item)
                        item_found = True
                        break

    if not item_found:
        tw.clearSelection()


def printMessage(infoLE, message, mode='info'):
    infoLE.setText(message)
    if mode == 'error':
        color = RED_PASTAL
    elif mode == 'warning':
        color = YELLOW_PASTAL
    else:
        color = GREEN_PASTAL
    infoLE.setStyleSheet('color: rgb{}'.format(color))
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    del exc_info


def createColorGuide(layout, text, color, parent):
    """
    Create a colored box with a text in the UI
    :param text: text that comes after box
    :param color: color of box
    :param parent: parent widget that box and text will be added to
    :return: n/a
    """
    grey_btn = QtWidgets.QLabel()
    grey_btn.setFixedSize(12, 12)
    setBGColor(grey_btn, color)
    grey_lb = QtWidgets.QLabel(text)
    layout.layout().addWidget(grey_btn)
    layout.layout().addWidget(grey_lb)


class UI(QtWidgets.QDialog):
    def __init__(self, title='test UI', parent=getMayaWindow()):

        # create window
        super(UI, self).__init__(parent=parent)
        self.setWindowTitle(title)
        self.resize(350, 340)

        # main path
        self.objPath = ''
        self.QCData = self.getShowsAndAssets()

        # main layout
        mainWidget = QtWidgets.QVBoxLayout()
        self.setLayout(mainWidget)
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        QCs_w = QtWidgets.QWidget()
        mainWidget.addWidget(QCs_w)
        self.QCs_lay = QtWidgets.QVBoxLayout(QCs_w)
        self.populateMainTab()

        # restore UI settings
        self.restoreUI()

    def populateMainTab(self):
        """
        populate the main tab of UI
        :return:
        """
        # ======================================================================
        # QCs frame
        qc_gb, qc_frame = createGroupBox(self.QCs_lay, 'Available Rig QCs')

        qc_vl = createVLayout(qc_frame)
        qc_hl = createHLayout(qc_vl)

        show_vl = createVLayout(qc_hl)
        self.shows_filter_le = QtWidgets.QLineEdit()
        self.shows_filter_le.setPlaceholderText('filter')
        show_vl.layout().addWidget(self.shows_filter_le)
        self.shows_tw = createTreeWidget(show_vl)

        assetNames_vl = createVLayout(qc_hl)
        self.assetNames_filter_le = QtWidgets.QLineEdit()
        self.assetNames_filter_le.setPlaceholderText('filter')
        assetNames_vl.layout().addWidget(self.assetNames_filter_le)
        self.assetNames_tw = createTreeWidget(assetNames_vl)

        # populate shows tab
        self.populateShowsTW()

        # Connect signals.
        self.shows_tw.itemSelectionChanged.connect(self.handleNewShowSelected)
        self.shows_filter_le.textChanged.connect(self.filterShows)
        self.assetNames_filter_le.textChanged.connect(self.filterAssetNames)
        self.assetNames_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.assetNames_tw.customContextMenuRequested.connect(self.rightClickMenu)
        self.assetNames_tw.itemDoubleClicked.connect(self.openLatestInRV)

        # ======================================================================
        # colors meaning frame
        color_gb, color_frame = createGroupBox(self.QCs_lay, 'Color Guide')

        color_vl = self.createVLayout(color_frame)
        self.createColorGuide(text=' No QC Found', color=GREY, parent=color_vl)
        self.createColorGuide(text=' QC Found (not submitted to SG)', color=YELLOW, parent=color_vl)
        self.createColorGuide(text=' QC Found (submitted to SG)', color=GREEN_PASTAL, parent=color_vl)
        self.createColorGuide(text=' QC Found (submitted to SG, but out-dated, newer rig available)',
                              color=RED_PASTAL, parent=color_vl)

    def rightClickMenu(self, event):
        """
        add right-click menu to assetNames
        :return: n/a
        """
        menu = QtWidgets.QMenu(self.assetNames_tw)
        menu.addAction('Open Directoy', self.openDirectoy)
        menu.addAction('Copy RV Command', self.copyRVCommand)
        menu.exec_(self.assetNames_tw.mapToGlobal(event))

    def openDirectoy(self):
        """
        Opens directory of rig QC images for selected asset in file explorer
        :return: n/a
        """
        # get selected show and asset
        show = getSelectedItemAsText(self.shows_tw)
        assetName = getSelectedItemAsText(self.assetNames_tw)
        if not (show and assetName):
            return

        # find the latest QC
        imageDir = self.getLatestQC()

        # if there's no QC, return the rig image directory
        if not imageDir:
            imageDir = '/jobs/{}/assets/{}/PRODUCTS/images/rig/'.format(show, assetName)
            # create rig image directory if doesn't exist
            if not os.path.lexists(imageDir):
                os.makedirs(imageDir)

        # open directory
        subprocess.Popen(['xdg-open', os.path.abspath(imageDir)])

    def filterAssetNames(self):
        filterTW(self.assetNames_tw, self.assetNames_filter_le)

    def filterShows(self):
        filterTW(self.shows_tw, self.shows_filter_le)

    def populateShowsTW(self):
        """
        find all shows in /jobs and add them to shows list
        :return: n/a
        """
        self.shows_tw.clear()
        shows = self.QCData.keys()
        for show in sorted(shows):
            self.addItemToTreeWidget(self.shows_tw, show)
        # select current show
        show = os.getenv('M_JOB')
        selectItemByText(self.shows_tw, show)
        self.handleNewShowSelected()

    def handleNewShowSelected(self):
        """
        populates asset section if a new show is selected
        :return: n/a
        """
        # get selected show
        items = self.shows_tw.selectedItems()
        if not items:
            return
        show = items[-1].text(0)

        # populate assets list
        self.assetNames_tw.clear()
        assetNames = self.QCData[show]
        if not assetNames:
            return

        tt = 'Double click to open latest QC in RV\n'
        tt += 'Right click for more options'

        # show the assets with playblasts in PRODUCT
        for assetName in sorted(assetNames):
            # no QC found
            color = GREY

            # add item with correct color
            item = self.addItemToTreeWidget(self.assetNames_tw, assetName)
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(*color)))
            item.setToolTip(0, tt)

    def closeEvent(self, event):
        """
        Save UI current size and position
        :return: n/a
        """
        # settings path
        settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat)
        # window size and position
        settings.setValue("geometry", self.saveGeometry())

    def restoreUI(self):
        """
        Restore UI size and position that if was last used
        :return: n/a
        """
        if os.path.exists(SETTINGS_PATH):
            settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat)
            # window size and position
            self.restoreGeometry(settings.value("geometry"))


class Button(QtWidgets.QPushButton):
    def __init__(self, title='', parent=None, **kwargs):
        super(Button, self).__init__(title, parent=parent)

        # inputs
        command = kwargs.get('command', 'print(\"No command defined!\")')
        annotation = kwargs.get('annotation', None)
        self.title = title
        self.iconPath = kwargs.get('iconPath', None)
        self.btnSize = kwargs.get('btnSize', 32)
        self.transparent = kwargs.get('transparent', True)
        self.rightClickData = kwargs.get('rightClickData', {})
        self.isMenuButton = kwargs.get('isMenuButton', False)

        # annotation
        if annotation:
            self.setToolTip(annotation)
        else:
            self.setToolTip(title)

        # icon
        self.addIcon()

        # add right click menu
        if self.rightClickData:
            self.addMenuAction()

        # disable right-click
        else:
            self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

        # command
        self.clicked.connect(lambda: run_command(command))

    def paintEvent(self, event):
        QtWidgets.QPushButton.paintEvent(self, event)
        if self.rightClickData and not self.isMenuButton:
            self.drawCornerTriangle()

    def leaveEvent(self, event):
        """
        workaround for the bug when button is right-clicked it stays highlighted
        """
        QtWidgets.QPushButton.leaveEvent(self, event)
        self.repaint()

    def addMenuAction(self):
        # action menu policy
        if self.isMenuButton:
            menu = QtWidgets.QMenu(self)
            self.setMenu(menu)
        else:
            menu = self
            self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        # add right-click options
        for button_title, command in self.rightClickData.items():
            action = QtWidgets.QAction(self)
            action.setText(button_title)
            action.triggered.connect(functools.partial(run_command, command))
            menu.addAction(action)

    def addIcon(self):
        if self.iconPath and os.path.lexists(self.iconPath) and os.path.isfile(self.iconPath):

            # create convas and add image to it
            btn_pixmap = QtGui.QIcon(self.iconPath)

            # add transparency and round shapes to button
            if self.transparent:
                styleSheet = '''
                QPushButton {
                    background-color: rgba(0, 0, 0, 0);
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 50);
                }
                '''
                self.setStyleSheet(styleSheet)

            # set size
            if self.btnSize:
                self.setMinimumSize(self.btnSize, self.btnSize)
                self.setMaximumSize(self.btnSize, self.btnSize)
                self.setIconSize(QtCore.QSize(self.btnSize, self.btnSize))

            # set convas as button icon
            self.setText('')
            self.setIcon(btn_pixmap)

    def drawCornerTriangle(self):
        width = self.width()
        height = self.height()
        triangleSize = self.btnSize * 0.15
        offset = 2

        painter = QtGui.QPainter(self)
        path = QtGui.QPainterPath()

        path.moveTo(width - offset, height - offset)
        path.lineTo(width - offset, height - offset - triangleSize)
        path.lineTo(width - offset - triangleSize, height - offset)
        path.lineTo(width - offset, height - offset)
        painter.fillPath(path, QtGui.QBrush(QtGui.QColor(200, 200, 200)))

        # painter.drawText(0, 0, self.width(), self.height(), QtCore.Qt.AlignCenter, self.title)

        painter.end()


def launch():
    global testUI_obj
    if 'testUI_obj' in globals():
        testUI_obj.close()
        testUI_obj.deleteLater()
        del globals()['testUI_obj']
    testUI_obj = UI()
    testUI_obj.show()


def confirmDialog(parent, title='Confirm', msg='Are you sure you?'):
    reply = QtWidgets.QMessageBox.question(parent,
                                           title,
                                           msg,
                                           QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.No)

    if reply == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        # super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()


class Bubble(QtWidgets.QLabel):
    def __init__(self, text):
        super(Bubble, self).__init__(text)
        self.word = text
        self.setContentsMargins(5, 5, 5, 5)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.drawRoundedRect(
            0, 0, self.width() - 1, self.height() - 1, 5, 5)
        super(Bubble, self).paintEvent(event)


def fillWidgetsWithBtns(widget, btnNames, btnSize=None):
    widget.setMinimumWidth(10)
    layout = FlowLayout(widget)

    for btnName in btnNames:
        btn = QtWidgets.QPushButton(btnName)
        if btnSize:
            btn.setMinimumSize(btnSize, btnSize)
            btn.setMaximumSize(btnSize, btnSize)
        else:
            btn.setFixedWidth(btn.sizeHint().width())
        layout.addWidget(btn)


def btnsFromJson(layout, config, btnSize=None):
    categoriesAndBtns_data = fileLib.loadJson(config)

    # add an extra widget and layout so we can minimize empty spaces
    ww = QtWidgets.QWidget()
    layout.addWidget(ww)
    vl = QtWidgets.QVBoxLayout()
    ww.setLayout(vl)
    ww.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
    vl.setContentsMargins(0, 0, 0, 0)
    vl.setSpacing(5)

    for cat, btns_data in categoriesAndBtns_data.items():
        # group by category
        gb, lay = createGroupBox(
            parentLayout=vl,
            label=cat
        )

        w = QtWidgets.QWidget()
        lay.addWidget(w)

        w.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        w.setMinimumWidth(10)
        flowLayout = FlowLayout(w, margin=4, hspacing=8, vspacing=8)

        for btnName, btn_data in btns_data.items():
            # button
            commandString = btn_data.get('command', 'print("No command defined")')

            annotationString = btn_data.get('annotation', '')

            iconPath = btn_data.get('icon', '')
            if not os.path.lexists(iconPath):
                iconName = os.path.basename(iconPath)
                iconPath = os.path.join(ICON_DIR, iconName)

            rightClickData = btn_data.get('right_click_commands', {})

            btn = Button(
                title=btnName,
                iconPath=iconPath,
                btnSize=btnSize,
                annotation=annotationString,
                command=commandString,
                rightClickData=rightClickData
            )
            flowLayout.addWidget(btn)


def twFilterField(parent=None, tw=None):
    filter_le = QtWidgets.QLineEdit()
    if parent:
        parent.layout().addWidget(filter_le)
    filter_le.setPlaceholderText('filter')
    filter_le.textChanged.connect(lambda: filterTW(tw=tw, le=filter_le))
    return filter_le


def createBrowseField(parent, label='Path:', txt='Browse For Something ...',
                      labelWidth=90, icon='browse.png', iconLabel=None):
    address_vl = createHLayout(parent, maxHeight=30)
    lb = QtWidgets.QLabel(label)
    lb.setMinimumSize(labelWidth, 20)
    lb.setMaximumSize(labelWidth, 20)
    address_vl.layout().addWidget(lb)
    address_le = QtWidgets.QLineEdit()
    address_le.setPlaceholderText(txt)
    address_vl.layout().addWidget(address_le)
    dirBrowse_btn = QtWidgets.QPushButton()
    if icon:
        icn = QtGui.QIcon(os.path.join(ICON_DIR, icon))
        dirBrowse_btn.setIcon(icn)
    if iconLabel:
        dirBrowse_btn.setText(iconLabel)
    dirBrowse_btn.setMinimumSize(25, 25)
    dirBrowse_btn.setMaximumSize(25, 25)
    address_vl.layout().addWidget(dirBrowse_btn)
    return address_le, dirBrowse_btn


def getSaveFileName(dialog, le, defaultFolder, txt='Select file', ext='json'):
    defaultFolder_from_ui = le.text()
    if defaultFolder_from_ui:
        defaultFolder = defaultFolder_from_ui
    f, filter = QtWidgets.QFileDialog.getSaveFileName(dialog,
                                                      txt,
                                                      defaultFolder,
                                                      "{0} Files (*.{0})".format(ext),
                                                      "",
                                                      QtWidgets.QFileDialog.Options())
    if f:
        le.setText(f)


def getOpenFileName(dialog, le, defaultFolder, txt='Select file', ext='json'):
    defaultFolder_from_ui = le.text()
    if defaultFolder_from_ui:
        defaultFolder = defaultFolder_from_ui
    f, filter = QtWidgets.QFileDialog.getOpenFileName(dialog,
                                                      txt,
                                                      defaultFolder,
                                                      "{0} Files (*.{0})".format(ext),
                                                      "",
                                                      QtWidgets.QFileDialog.Options())
    if f:
        le.setText(f)


def setOpenFileName(dialog, le, defaultFolder):
    defaultFolder_from_ui = le.text()
    if defaultFolder_from_ui:
        defaultFolder = defaultFolder_from_ui
    f, filter = QtWidgets.QFileDialog.getOpenFileName(dialog,
                                                      "Select file",
                                                      defaultFolder,
                                                      "All Files (*);;Text Files (*.json)",
                                                      "",
                                                      QtWidgets.QFileDialog.Options())
    if f:
        le.setText(f)


def getExistingDir(dialog, le, defaultFolder):
    defaultFolder_from_ui = le.text()
    if defaultFolder_from_ui:
        defaultFolder = defaultFolder_from_ui
    folder = QtWidgets.QFileDialog.getExistingDirectory(dialog,
                                                        "Select Folder",
                                                        defaultFolder,
                                                        QtWidgets.QFileDialog.ShowDirsOnly)
    if folder:
        le.setText(folder)


def dictToTreeWidget(tw, data):
    tw.clear()
    for cat, btns_data in data.items():

        # add categories
        cat_item = addItemToTreeWidget(tw, cat)
        cat_item.setFlags(cat_item.flags() | QtCore.Qt.ItemIsEditable)
        cat_item.setExpanded(True)

        # add buttons
        for btn, btn_data in btns_data.items():
            btn_item = QtWidgets.QTreeWidgetItem()
            btn_item.setFlags(cat_item.flags() | QtCore.Qt.ItemIsEditable)
            btn_item.setText(0, btn)
            cat_item.addChild(btn_item)
            right_click_data = btn_data.get('right_click_commands', {})

            # add right_click buttons
            for rc_btn, rc_btn_data in right_click_data.items():
                rc_btn_item = QtWidgets.QTreeWidgetItem()
                rc_btn_item.setFlags(cat_item.flags() | QtCore.Qt.ItemIsEditable)
                rc_btn_item.setText(0, rc_btn)
                btn_item.addChild(rc_btn_item)


def dock_window(dialog_class):
    """
    Author: Lior ben horin
    From: https://gist.github.com/liorbenhorin/.../Simple_MayaDockingClass.py
    :param dialog_class:
    :return:
    """
    try:
        # mc.workspaceControl(dialog_class.CONTROL_NAME, e=True, close=True)
        mc.deleteUI(dialog_class.CONTROL_NAME)
    except:
        pass

    # building the workspace control with maya.cmds
    main_control = mc.workspaceControl(
        dialog_class.CONTROL_NAME,
        tabToControl=["AttributeEditor", -1],
        initialWidth=300,
        minimumWidth=dialog_class.minimumWidth,
        widthProperty='free',
        label=dialog_class.DOCK_LABEL_NAME
    )

    # now lets get a C++ pointer to it using OpenMaya
    control_widget = omui.MQtUtil.findControl(dialog_class.CONTROL_NAME)

    # convert the C++ pointer to Qt object we can use
    control_wrap = wrapInstance(long(control_widget), QtWidgets.QWidget)

    # control_wrap is the widget of the docking window and now we can start working with it:
    control_wrap.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    win = dialog_class(control_wrap)

    # after maya is ready we should restore the window since it may not be visible
    def launch_dock_ui():
        mc.workspaceControl(main_control, e=True, rs=True)
        mc.workspaceControl(main_control, e=True, label=dialog_class.DOCK_LABEL_NAME)
    mc.evalDeferred(launch_dock_ui)

    # will return the class of the dock content.
    return win.run()


class DockingUI(QtWidgets.QWidget):
    """
    usage:
    my_dock = dock_window(DockingUI)
    """
    instances = list()
    CONTROL_NAME = 'my_workspcae_control'
    DOCK_LABEL_NAME = 'my workspcae control'
    minimumWidth = 50

    def __init__(self, parent=None):
        super(DockingUI, self).__init__(parent)

        # let's keep track of our docks so we only have one at a time.
        DockingUI.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))

        self.window_name = self.CONTROL_NAME
        self.ui = parent
        self.main_layout = parent.layout()
        self.main_layout.setContentsMargins(2, 2, 2, 2)

        # here we can start coding our UI
        self.my_label = QtWidgets.QLabel('hello world!')
        self.main_layout.addWidget(self.my_label)

    @staticmethod
    def delete_instances():
        for ins in DockingUI.instances:
            try:
                print ('Delete {}'.format(ins))
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass

            DockingUI.instances.remove(ins)
            del ins

    def run(self):
        return self


@decoratorLib.repeatable_cmd
@decoratorLib.undoChunk
def run_command(commandString):
    exec (commandString, globals(), globals())
