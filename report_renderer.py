# -*- coding: utf-8 -*-
"""
/***************************************************************************
 reportWizard
                                 A QGIS plugin
 Quick  markdown and html reports generation 
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-21
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Enrico Ferreguti
        email                : enricofer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from typing import OrderedDict
from qgis.PyQt.QtCore import QSize, Qt, QByteArray, QBuffer, QIODevice
from qgis.PyQt.QtGui import QImage

from qgis.gui import QgsMapCanvas
from qgis.core import (
    QgsWkbTypes,
    QgsMapLayerType,
    QgsApplication,
    QgsMapRendererParallelJob,
    QgsExpressionContextUtils,
    QgsProject,
    QgsMapLayer,
    QgsRectangle,
    QgsRectangle,
)

import tempfile
import os

class abstact_report_engine:

    def isVector(self,layer):
        return layer["obj"].type() == QgsMapLayerType.VectorLayer

    def isRaster(self,layer):
        return layer["obj"].type() == QgsMapLayerType.RasterLayer

    def __init__(self,iface,vector_layer_driver=None, feature_limit=100):
        self.iface = iface
        self.environment = {}

        self.environment["globals"] = {
            "image": "canvas:"+iface.mapCanvas().theme(),
            "project": QgsProject.instance(),
            "mapCanvas": iface.mapCanvas(),
            "extent": iface.mapCanvas().extent(),
            "vector_driver":vector_layer_driver,
            "box": [
                iface.mapCanvas().extent().xMinimum(),
                iface.mapCanvas().extent().yMinimum(),
                iface.mapCanvas().extent().xMaximum(),
                iface.mapCanvas().extent().yMaximum()
            ],
            "vars":{}
        }

        for k in list(QgsExpressionContextUtils.projectScope(QgsProject.instance()).variableNames())+list(QgsExpressionContextUtils.globalScope().variableNames()):
            if k in ('layers','user_account_name'):
                continue
            var_value = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable(k)
            self.environment["globals"]["vars"][str(k)] =  var_value if isinstance(var_value, str) else str(var_value).replace("\\","/")
        print(self.environment["globals"]["vars"])
        self.environment["globals"]["themes"] = list(QgsProject.instance().mapThemeCollection().mapThemes())

        self.environment["globals"]["bookmarks"] = []
        for bookmark in list(QgsProject.instance().bookmarkManager().bookmarks())+list(QgsApplication.instance().bookmarkManager().bookmarks()):
            bk_def = {
                "name": bookmark.name(),
                "id": bookmark.id(),
                "extent": bookmark.extent(),
                "box": [
                    bookmark.extent().xMinimum(),
                    bookmark.extent().yMinimum(),
                    bookmark.extent().xMaximum(),
                    bookmark.extent().yMaximum()
                ]
            }
            self.environment["globals"]["bookmarks"].append(bk_def)
        
        self.environment["layers"] = []
        for layername,layer in QgsProject.instance().mapLayers().items():

            if  layer.type() == QgsMapLayerType.VectorLayer:
                type = "vector"
            elif layer.type() == QgsMapLayerType.RasterLayer:
                type = "raster"
            elif layer.type() == QgsMapLayerType.PluginLayer:
                type = "plugin"
            elif layer.type() == QgsMapLayerType.MeshLayer:
                type = "mesh"
            else:
                type = "unknown"

            fields = []
            geometryType = ""
            if type == 'vector':
                if  layer.geometryType() ==  QgsWkbTypes.PointGeometry:
                    geometryType = "point"
                elif layer.geometryType() == QgsWkbTypes.LineGeometry:
                    geometryType = "linestring"
                elif layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                    geometryType = "polygon"
                elif layer.geometryType() == QgsWkbTypes.UnknownGeometry:
                    geometryType = "unknown"
                elif layer.geometryType() == QgsWkbTypes.NullGeometry:
                    geometryType = "nullgeometry"
                for field in layer.fields().toList():
                    fields.append(field.name())

            self.environment["layers"].append ({
                "obj":layer,
                "type": 'layer',
                "layerType": type,
                "geometryType": geometryType,
                "name": layer.name(),
                "image": "layer:%s" % layer.id(),
                "id": layername,
                "source": layer.publicSource(),
                "extent": layer.extent(),
                "box": [
                    layer.extent().xMinimum(),
                    layer.extent().yMinimum(),
                    layer.extent().xMaximum(),
                    layer.extent().yMaximum()
                ],
                "fields": fields
            })
            
        self.environment["layouts"] = []
        for layout in QgsProject.instance().layoutManager().printLayouts():
            layout_def = {
                "obj": layout,
                "type": 'layout',
                "name": layout.name(),
                "image": "layout:%s" % layout.name(),
                "atlas": layout.atlas().coverageLayer().id()  if layout.atlas().enabled() else None
            }
            self.environment["layouts"].append (layout_def)

        self.environment["features"] = []

        if vector_layer_driver and vector_layer_driver.type() == QgsMapLayerType.VectorLayer :
            feats = vector_layer_driver.selectedFeatures()
            if not feats:
                feats = vector_layer_driver.getFeatures()
            count = 0
            for feat in feats: #Iterator?
                f_dict = {
                    "id": feat.id(),
                    "type": 'feature',
                    "obj": feat,
                    "geom": feat.geometry(),
                    "image": "feature:%s" % (vector_layer_driver.id())
                }
                attributes = {}
                for field in vector_layer_driver.fields().toList():
                    attributes[field.name()] = feat[field.name()]
                f_dict["attributes"] = attributes
                self.environment["features"].append(f_dict)
                count += 1
                if count > feature_limit:
                    break
        else:
            self.environment["features"] = []
        
        self.exporter = canvas_image_exporter(iface.mapCanvas())


    def canvas_image(self,box=None,width=150,height=150,theme=None):
        if isinstance(box, QgsRectangle):
            bb = box
        elif isinstance(box, QgsGeometry):
            bb = box.boundingBox()
        else:
            bb = self.iface.mapCanvas().extent()
        img = self.exporter.image_shot(bb,width,height,theme)
        return img


    def canvas_base64_image(self,box=None,xsize=150,ysize=150,theme=None):
        if isinstance(box, QgsRectangle):
            bb = box
        elif isinstance(box, QgsGeometry):
            bb = box.boundingBox()
        else:
            bb = self.iface.mapCanvas().extent()
        base64_img = self.exporter.base64_shot(bb,xsize,ysize,theme)
        #print (str(base64_img))
        return base64_img     


class canvas_image_exporter:

    def __init__(self, main_canvas):
        self.main_canvas = main_canvas
        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.setLayers(self.main_canvas.mapSettings().layers())
        self.canvas.refresh()
        self.canvas.update()
        self.settings = self.main_canvas.mapSettings()

    def image_shot(self, extent, xsize, ysize,theme):
        #self.canvas.resize(xsize,ysize) #QSize(xsize,ysize)
        if theme:
            if isinstance(theme, str):
                self.canvas.setTheme(theme)
            elif issubclass(type(theme),QgsMapLayer):
                self.canvas.setLayers([theme])
            else:
                self.canvas.setLayers(self.main_canvas.layers())
        
        self.canvas.setExtent(extent)
        self.canvas.refresh()
        self.canvas.update()
        print ("export settings2:", extent,"xsize:", extent.xMaximum() - extent.xMinimum(),xsize,"ysize:", extent.yMaximum() - extent.yMinimum(),ysize )
        mapSettings = self.canvas.mapSettings()
        mapSettings.setOutputSize( QSize(xsize,ysize ) )
        job = QgsMapRendererParallelJob(mapSettings)
        job.start()
        job.waitForFinished()
        image = job.renderedImage()
        return image

    def base64_shot(self, extent, xsize, ysize, theme):
        image = self.image_shot(extent,xsize,ysize,theme)
        return self.img2base64(image)
    
    def img2base64(self, image):
        if not isinstance(image, QImage):
            image = QImage(image)
        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, 'PNG')
        base64_data = ba.toBase64().data()

        return "data:image/png;base64," + str(base64_data, 'UTF-8')