# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
from qgis.gui import *
from qgis.core import *


import resources

from mainWindow import *




class calcareaMain( QtGui.QWidget): #Inherits QWidget to install an Event filter
    def __init__(self,iface):

        QtGui.QWidget.__init__(self)

        #----------------------------------------------------------------------
        #instance variables

        #Reference to the QGIS Interface
        self.iface = iface
        self.mc = self.iface.mapCanvas()    #Map Canvas variable

        self.layer = QgsVectorLayer()
        self.Aufzeichnen = False
        self.maptool = QgsMapTool(self.mc)     #force a variable type
        self.grafArea = QgsDistanceArea()
        self.DialogDock = QtGui.QDockWidget()
        self.Dialog = QtGui.QDialog()
        self.tmpNitem = None


        #----------------------------------------------------------------------


    #initialize the connection to the QGIS GUI - the plugin starts from there
    def initGui(self):

        self.actionCalcArea = QtGui.QAction( QtGui.QIcon(":/plugins/CalcArea/CalcArea.png"),  QtCore.QCoreApplication.translate("calcareaMain", "Calculate the Area while editing. Best with Plugin Improved Polygon Capturing."),  self.iface.mainWindow() )
        QtCore.QObject.connect(self.actionCalcArea, QtCore.SIGNAL("triggered()"), self.showMainWindow)

        self.iface.addToolBarIcon( self.actionCalcArea )
        self.iface.addPluginToVectorMenu(QtCore.QCoreApplication.translate("calcareaMain",  "Calculate area while editing"),  self.actionCalcArea)


    # the dock widget is created
    def showMainWindow(self):


        if not self.mc.mapUnits() == 0: # squaremeter!
            QtGui.QMessageBox.critical(None, QtCore.QCoreApplication.translate("calcareaMain","Wrong Units!"),QtCore.QCoreApplication.translate("calcareaMain",'The Plugin needs metrical Units!'))
            return

        if self.iface.mainWindow().findChild(QtGui.QDockWidget,'CalcArea DialogDock') == None:

            self.Dialog = CalcAreaDialog()
            self.DialogDock = QtGui.QDockWidget('Calc Area', self.iface.mainWindow())
            self.DialogDock.setWidget(self.Dialog)

            self.DialogDock.setObjectName('CalcArea DialogDock')
            self.Dialog.setObjectName('CalcArea Dialog')

        else:
            return

        self.iface.mainWindow().addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.DialogDock)
        self.DialogDock.show()
        self.Dialog.installEventFilter(self)
        self.DialogDock.installEventFilter(self)


        # emits a map tool change event
        QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.digklick)


        # emits a layer change event
        QtCore.QObject.connect(self.iface, QtCore.SIGNAL("currentLayerChanged (QgsMapLayer *)"), self.switch_layer)




        # if an edit session already has been started
        if self.mc.mapTool().isEditTool():
            self.digklick(self.mc.mapTool().isEditTool())

        self.switch_layer(self.mc.currentLayer())

    # if the plugin has to leave QGIS
    def unload(self):

        #first delete the Widgets!
        self.Dialog = None
        self.iface.mainWindow().removeDockWidget(self.DialogDock)
        self.DialogDock = None

        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&CalcArea", self.actionCalcArea)
        self.iface.removeToolBarIcon(self.actionCalcArea)


    #calculate the feature area/perimeter and
    #update the fields of the dialog widget
    def area(self,feat):

        self.Dialog.lblQuadratmeter.setText(str(round(self.grafArea.measure(feat),2)) + ' m²'.decode('utf8'))
        self.Dialog.lblHektar.setText(str(round(self.grafArea.measure(feat)/10000,2)) + ' ha'.decode('utf8'))
        self.Dialog.lblQuadratkilometer.setText(str(round(self.grafArea.measure(feat)/1000000,2)) + ' km²'.decode('utf8'))

        self.Dialog.lblMeter.setText(str(round(self.grafArea.measurePerimeter(feat),2)) + ' m'.decode('utf8'))
        self.Dialog.lblKilometer.setText(str(round(self.grafArea.measurePerimeter(feat)/1000,2)) + ' km'.decode('utf8'))


    #slot for the 'geometryChanged' layer signal
    def seppl(self,id,feat):
        self.area(feat)

    #slot for the 'featureAdded' layer signal
    def kasperl(self,id):
        seli = QgsFeatureRequest(id)
        feat = QgsFeature()
        iti = self.layer.getFeatures(seli)
        iti.nextFeature(feat)
        self.area(feat.geometry())


    # slot for the 'currentLayerChanged' signal emitted by the QGIS iface
    def switch_layer(self,layer):


        # to prevent an error on closing QGIS
        # while the plugin is still active
        if layer == None:
            return

        # polygon layer with read/write access -> our possible object
        if layer.type() == 0 and layer.geometryType() == 2 and not layer.isReadOnly():
            self.layer = layer
            self.Dialog.lblLayer_area.setText('Layer: ' + self.layer.name())
            self.Dialog.lblLayer_perimeter.setText('Layer: ' + self.layer.name())
            #self.Dialog.repaint()

            QtCore.QObject.connect(self.layer, QtCore.SIGNAL('geometryChanged (QgsFeatureId, QgsGeometry &)'), self.seppl)  #geht erst ab 1.9
            QtCore.QObject.connect(self.layer, QtCore.SIGNAL('featureAdded (QgsFeatureId)'), self.kasperl)
            QtCore.QObject.connect(self.mc, QtCore.SIGNAL('xyCoordinates ( const QgsPoint &) '), self.temp_vertex)



        else:   # wrong layer -> no possible object
            self.layer = None
            self.Dialog.lblLayer_area.setText('Layer: ')
            self.Dialog.lblLayer_perimeter.setText('Layer: ')
            #self.Dialog.repaint()


    # slot for the map tool change event of the map canvas
    def digklick(self,Aktion):

        Aktion = self.mc.mapTool()

        if str(Aktion).find('QgsMapToolCapturePolygon') > -1:   # Plugin 'Improved Polygon Capturing' is selected. It offers more
            self.Aufzeichnen = True                             # possibilities: the area of a polygon can be calculated
            self.maptool = Aktion                               # quasi in real time!
            #self.switch_layer(self.mc.currentLayer())
        elif Aktion.isEditTool() and Aktion.action().objectName().find('NodeTool') < 0 :    # An edit tool is selected and it's not
            self.Aufzeichnen = False                                                        # the Node Tool
            self.maptool = Aktion
            #self.switch_layer(self.mc.currentLayer())

        elif Aktion.action().objectName().find('NodeTool') > -1 :   # An edit tool is selected and it's
            self.Aufzeichnen = False                                # the Node Tool
            self.maptool = Aktion

        else:   # some other tool is selected
            self.Aufzeichnen = False
            self.Dialog.lblQuadratmeter.setText('')
            self.Dialog.lblHektar.setText('')
            self.Dialog.lblQuadratkilometer.setText('')
            #self.Dialog.repaint()


    # slot for the xyCoordinates signal of the map canvas
    def temp_vertex(self,point):

        #do only process if the 'Improved Polygon Capturing' is selected!
        if self.Aufzeichnen:
            a = self.maptool.captureList[:] # a method of the 'Improved Polygon Capturing' returns a list the already set vertices
            a.append(point) # add the coordinate of the current mouse position

            if len(a) > 2:  # an area consists of at least three points


                # calculate the area/perimeter and update the fields of the dialog widget
                self.area(QgsGeometry().fromPolygon([a]))



    # an event filter - but only for the close event
    def eventFilter(self,affe,event):

        if not event == None:

            if event.type() == QtCore.QEvent.Close: # close event

                QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.digklick)
                QtCore.QObject.disconnect(self.iface, QtCore.SIGNAL("currentLayerChanged (QgsMapLayer *)"), self.switch_layer)
                QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL('xyCoordinates ( const QgsPoint &) '), self.temp_vertex)

                if not self.layer == None:
                    QtCore.QObject.disconnect(self.layer, QtCore.SIGNAL('geometryChanged (QgsFeatureId, QgsGeometry &)'), self.seppl)  #geht erst ab 1.9
                    QtCore.QObject.disconnect(self.layer, QtCore.SIGNAL('featureAdded (QgsFeatureId)'), self.kasperl)



                self.Dialog.removeEventFilter(self)
                self.DialogDock.removeEventFilter(self)

                # delete the Widgets!
                self.Dialog = None  # delete
                self.iface.mainWindow().removeDockWidget(self.DialogDock)   #first remove
                self.DialogDock = None  #then delete

                return True

            else:   # everything but the close event
                return False



# Dialog Widget Class
# inherits the QT Designer window definition
# and the QDialog definition
class CalcAreaDialog(QtGui.QDialog,Ui_frmMainWindow):
    def __init__(self):

        #QtGui.QDialog.__init__(self,parent) #parent keeps the dialog in front of the parent window (without locking it).
        QtGui.QDialog.__init__(self)
        Ui_frmMainWindow.__init__(self)

        self.setupUi(self)  #creates the GUI specified with QT Designer

