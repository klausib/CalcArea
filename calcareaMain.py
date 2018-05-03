# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
from qgis.gui import *
from qgis.core import *


import resources, math, copy

from mainWindow import *




class calcareaMain( QtGui.QWidget): # Inherits QWidget to install an Event filter
    def __init__(self,iface):

        QtGui.QWidget.__init__(self)

        #----------------------------------------------------------------------
        #instance variables

        #Reference to the QGIS Interface
        self.iface = iface
        self.mc = self.iface.mapCanvas()    #Map Canvas variable

        self.layer = QgsVectorLayer()

        self.maptool = QgsMapTool(self.mc)     #force a variable type
        self.grafArea = QgsDistanceArea()
        self.DialogDock = QtGui.QDockWidget()
        self.Dialog = QtGui.QDialog()
##        self.cpoint = QgsPoint()
##        self.cpointF = QtCore.QPointF()
        self.cpoint_list = []
        self.end = False


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

        #self.Dialog.installEventFilter(self)
        self.DialogDock.installEventFilter(self)




        # emits a map tool change event
        QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *, QgsMapTool *)"), self.digklick)

        # emits a layer change event
        QtCore.QObject.connect(self.iface, QtCore.SIGNAL("currentLayerChanged (QgsMapLayer *)"), self.switch_layer)


        # if an edit session already has been started
        if self.mc.mapTool().isEditTool():
            self.digklick(self.mc.mapTool().isEditTool(), None)

        self.switch_layer(self.mc.currentLayer())

        # fetch events before mapCanvas gets them!
        self.iface.mapCanvas().viewport().installEventFilter( self)


    # if the plugin leaves QGIS
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

        self.Dialog.lblQuadratmeter.setText(str(round(self.grafArea.measureArea(feat),2)) + ' m²'.decode('utf8'))
        self.Dialog.lblHektar.setText(str(round(self.grafArea.measureArea(feat)/10000,2)) + ' ha'.decode('utf8'))
        self.Dialog.lblQuadratkilometer.setText(str(round(self.grafArea.measureArea(feat)/1000000,2)) + ' km²'.decode('utf8'))

##        if len(self.cpoint_list) > 4:  # an area consists of at least three points
##                        file = open("D:/daten.txt","w+")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
##                        #file.write('Dynamisch ' + str(feat.geometry().asWkt()))
##                        file.write('Dynamisch ' + str(feat.geometry().area()) + ' ' + str(feat.exportToWkt()))
##                        file.write("\n")
##                        file.write('Punktliste ' + str(self.cpoint_list))
##                        file.write("\n")
##                        #file.write("Hallo")
##                        file.close()


        self.Dialog.lblMeter.setText(str(round(self.grafArea.measurePerimeter(feat),2)) + ' m'.decode('utf8'))
        self.Dialog.lblKilometer.setText(str(round(self.grafArea.measurePerimeter(feat)/1000,2)) + ' km'.decode('utf8'))

##        if poly != None:
##            self.Dialog.lblQuadratmeter.setText(str(round(self.grafArea.computePolygonFlatArea(poly),2)) + ' m²'.decode('utf8'))
##            #self.Dialog.lblHektar.setText(str(feat.length()))
##            self.Dialog.lblHektar.setText(str(round(self.grafArea.computePolygonFlatArea(poly)/10000,2)) + ' ha'.decode('utf8'))
##            self.Dialog.lblQuadratkilometer.setText(str(round(self.grafArea.computePolygonFlatArea(poly)/1000000,2)) + ' km²'.decode('utf8'))
##            #QtGui.QMessageBox.critical(None, QtCore.QCoreApplication.translate("calcareaMain","Wrong Units!"),str(self.grafArea.computePolygonFlatArea(poly)))




    #slot for the 'geometryChanged' layer signal
    def seppl(self,id,feat):
        self.area(feat)
        self.cpoint_list = []    #then empty the list!


    #slot for the 'featureAdded' layer signal
    def kasperl(self,id):
        seli = QgsFeatureRequest(id)
        feat = QgsFeature()
        iti = self.layer.getFeatures(seli)
        iti.nextFeature(feat)
        self.area(feat.geometry())
##        file = open("D:/daten.txt","a")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
##        file.write('Feature Added ' + str(feat.geometry().area()) + ' ' + str(feat.geometry().exportToWkt()))
##        #file.write(str(self.cpoint_list))
##        #
##        file.close()
        self.cpoint_list = []    #then empty the list!



    # slot for the 'currentLayerChanged' signal emitted by the QGIS iface
    def switch_layer(self,layer):


        # to prevent an error when closing QGIS
        # while the plugin is still active
        if layer == None:
            return

        # polygon layer with read/write access
        if layer.type() == 0 and layer.geometryType() == 2 and not layer.isReadOnly():
            self.layer = layer
            self.Dialog.lblLayer_area.setText('Layer: ' + self.layer.name())
            self.Dialog.lblLayer_perimeter.setText('Layer: ' + self.layer.name())
            #self.Dialog.repaint()

            QtCore.QObject.connect(self.layer, QtCore.SIGNAL('geometryChanged (QgsFeatureId, QgsGeometry &)'), self.seppl)  #geht erst ab 1.9
            QtCore.QObject.connect(self.layer, QtCore.SIGNAL('featureAdded (QgsFeatureId)'), self.kasperl)





        else:   # wrong layer type
            self.layer = None
            self.Dialog.lblLayer_area.setText('Layer: ')
            self.Dialog.lblLayer_perimeter.setText('Layer: ')
            #self.Dialog.repaint()



    # slot for the map tool change event of the map canvas
    def digklick(self,Aktion,Aktion_neu):

        Aktion = self.mc.mapTool()
        self.maptool = Aktion

        # If the tool is without a name attribute
        if Aktion.action() == None :
            self.Aufzeichnen = False
            self.Dialog.lblQuadratmeter.setText('')
            self.Dialog.lblHektar.setText('')
            self.Dialog.lblQuadratkilometer.setText('')
            self.Dialog.lblMeter.setText('')
            self.Dialog.lblKilometer.setText('')
            QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL('xyCoordinates ( const QgsPoint &) '), self.temp_vertex)
            #self.Dialog.repaint()

        elif Aktion.action().objectName().find('AddFeature') > -1 :   # edit tool AddFeature

            QtCore.QObject.connect(self.mc, QtCore.SIGNAL('xyCoordinates ( const QgsPoint &) '), self.temp_vertex)

        elif Aktion.action().objectName().find('NodeTool') > -1 :   # edit tool NodeTool

            QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL('xyCoordinates ( const QgsPoint &) '), self.temp_vertex)


        else:   # some other tool is selected
            self.Aufzeichnen = False
            self.Dialog.lblQuadratmeter.setText('')
            self.Dialog.lblHektar.setText('')
            self.Dialog.lblQuadratkilometer.setText('')
            self.Dialog.lblMeter.setText('')
            self.Dialog.lblKilometer.setText('')
            QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL('xyCoordinates ( const QgsPoint &) '), self.temp_vertex)
            #self.Dialog.repaint()



    # slot for the xyCoordinates signal of the map canvas
    def temp_vertex(self,point):

##        self.cpoint.setX(point.x())
##        self.cpoint.setY(point.y())
        b = []
        b = self.cpoint_list[:]
        b.append(point) # add the coordinate of the current mouse position


        if len(b) > 2:  # an area consists of at least three points
             self.area(QgsGeometry().fromPolygon([b]))



    # event filter
    def eventFilter(self,affe,event):

        if not event == None:


            if event.type() == QtCore.QEvent.Close: # close event

                QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *,QgsMapTool *)"), self.digklick)
                QtCore.QObject.disconnect(self.iface, QtCore.SIGNAL("currentLayerChanged (QgsMapLayer *)"), self.switch_layer)
                QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL('xyCoordinates ( const QgsPoint &) '), self.temp_vertex)

                if not self.layer == None:
                    QtCore.QObject.disconnect(self.layer, QtCore.SIGNAL('geometryChanged (QgsFeatureId, QgsGeometry &)'), self.seppl)  #geht erst ab 1.9
                    QtCore.QObject.disconnect(self.layer, QtCore.SIGNAL('featureAdded (QgsFeatureId)'), self.kasperl)




                #self.Dialog.removeEventFilter(self)
                self.DialogDock.removeEventFilter(self)

                # delete the Widgets!
                self.Dialog = None  # delete
                self.iface.mainWindow().removeDockWidget(self.DialogDock)   #first remove
                self.DialogDock = None  #then delete

                return True

            elif event.type() == QtCore.QEvent.MouseButtonPress: # mouse press event during edit session

                transi = self.mc.getCoordinateTransform()
                X_ = event.posF().x()
                Y_ = event.posF().y()
                if event.button() == QtCore.Qt.LeftButton:
                    self.cpoint_list.append(QgsPoint(transi.toMapCoordinatesF(X_,Y_)))
                    return True    #do not block the event
                elif event.button() == QtCore.Qt.RightButton:
                    self.cpoint_list= []
                    return True
            else:   # everything else
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


