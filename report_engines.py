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

from qgis.PyQt.QtCore import QSize

from PyQt5.Qsci import QsciScintilla, QsciLexerHTML, QsciLexerMarkdown

from qgis.gui import QgsMapCanvas
from qgis.core import (
    QgsWkbTypes,
    QgsMapLayerType,
    QgsPointXY,
    QgsExpressionContextUtils,
    QgsProject,
    QgsRectangle,
    QgsLayoutExporter,
)

import tempfile
import os

from secretary import Renderer    
from .report_renderer import abstact_report_engine      
                
class odt_renderer(abstact_report_engine):

    def render(self,template,target):
        engine = Renderer()
        engine.environment.filters['isVector'] = self.isVector
        engine.environment.filters['isRaster'] = self.isRaster
        
        @engine.media_loader
        def qgis_images_loader(value,dpi=200,box=None,center=None,atlas=None,theme=None,scale_denominator=None,around_border=0.1,mimetype="image/png",filter=None,**kwargs):

            if center and not scale_denominator:
                raise ("Can't specify center without scale_denominator parameter")   

            def getFrame(reference_frame):
                centerxy = center
                bb = box
                print ("getFrame", bb, centerxy, scale_denominator, theme )
                if scale_denominator:
                    if not centerxy:
                        if bb:
                            centerxy = bb.center()
                        else:
                            centerxy = reference_frame.center()
                    else:
                        if isinstance(centerxy,str):
                            coords = centerxy.split(",")
                            centerxy = QgsPointXY(coords[0],coords[1])
                        elif not isinstance(centerxy,QgsPointXY):
                            raise ("Malformed center parameter")
                    
                    semiScaledXSize = meterxsize*scale_denominator/2
                    semiScaledYSize = meterysize*scale_denominator/2
                    return QgsRectangle(centerxy.x()-semiScaledXSize, centerxy.y()-semiScaledYSize, centerxy.x()+semiScaledXSize, centerxy.y()+semiScaledYSize)
                else:
                    if not bb:
                        bb = reference_frame

                    if around_border:
                        if xsize >= ysize:
                            dim = bb.xMaximum() - bb.xMinimum()
                        else:
                            dim = bb.yMaximum() - bb.yMinimum()
                        dim = dim*around_border
                        bb.grow(dim)
                    return bb



            if atlas:
                image_metadata = ["atlas",atlas]
            else:
                image_metadata = value["image"].split(":")
            print ("image metadata",image_metadata, kwargs.keys())
            if not 'svg:width' in kwargs['frame_attrs']:
                print ("NO svg:width!")
                return

            units = kwargs['frame_attrs']['svg:width'][-2:]
            if units == "cm":
                m_conversion_factor = 0.01
                reverse_factor = 2.54
            elif units == "in":
                m_conversion_factor = 0.01
                reverse_factor = 1
            elif units == "mm":
                m_conversion_factor = 0.001
                reverse_factor = 25.4
            
            xsize = float(kwargs['frame_attrs']['svg:width'][:-2])
            ysize = float(kwargs['frame_attrs']['svg:height'][:-2])

            meterxsize = xsize*m_conversion_factor
            meterysize = ysize*m_conversion_factor

            width = int(xsize/reverse_factor*dpi)
            height = int(ysize/reverse_factor*dpi)
            aspect_ratio = width/height

            img_temppath = tempfile.NamedTemporaryFile(suffix=".png",delete=False).name
            
            if image_metadata[0] == 'canvas':
                print ("CANVAAS", theme)
                view_box = getFrame(self.iface.mapCanvas().extent())
                img = self.canvas_image(box=view_box,width=width,height=height,theme=theme)
                img.save(img_temppath)

            elif image_metadata[0] == 'feature':
                layer = QgsProject.instance().mapLayer(image_metadata[1])
                feature = layer.getFeature(value['id'])
                QgsExpressionContextUtils.setLayerVariable(layer,"atlas_featureid", feature.id())
                QgsExpressionContextUtils.setLayerVariable(layer,"atlas_feature", feature)
                if layer.geometryType() == QgsWkbTypes.PointGeometry:
                    p = feature.geometry().boundingBox().center()
                    halfwidth = self.iface.mapCanvas().extent().width()/8
                    halfheight = halfwidth = self.iface.mapCanvas().extent().height()/4
                    pointFeatbox = QgsRectangle(p.x()-halfwidth,p.y()-halfheight,p.x()+halfwidth,p.y()+halfheight)
                    view_box = getFrame(pointFeatbox)
                else:
                    view_box = getFrame(feature.geometry().boundingBox())
                print ("GEOM BOX", feature.geometry().boundingBox().width() )
                img = self.canvas_image(box=view_box,width=width,height=height,theme=theme)
                img.save(img_temppath)
                
            elif image_metadata[0] == 'layer':
                layer = QgsProject.instance().mapLayer(image_metadata[1])
                view_box = getFrame(layer.extent())
                img = self.canvas_image(box=view_box,width=width,height=height,theme=layer)
                img.save(img_temppath)
                
            elif image_metadata[0] in ('layout', 'atlas'):
                #https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/pyqgis-101-exporting-layouts/
                manager = QgsProject.instance().layoutManager()
                layout = manager.layoutByName(image_metadata[1])
                if image_metadata[0] == 'atlas': # is atlas
                    layout.atlas().seekTo(value['id'])
                    print ("SEEKto", value['id'])
                    layout.atlas().refreshCurrentFeature()
                exporter = QgsLayoutExporter(layout)
                print ("UNITS",layout.pageCollection().page(0).pageSize() )
                aspect_ratio = layout.pageCollection().page(0).pageSize().width()/layout.pageCollection().page(0).pageSize().height()
                settings = exporter.ImageExportSettings()
                print (settings.imageSize)
                if width > height:
                    height = width*aspect_ratio
                else:
                    width = height*aspect_ratio
                settings.imageSize = QSize(width ,height)
                settings.dpi = dpi
                settings.cropToContents = False
                #settings.pages = [0]
                print ( xsize, ysize, settings.imageSize, settings.dpi)
                res = exporter.exportToImage(img_temppath, settings)
                print ("LAYOUT EXPORT RESULT",res, exporter.errorFile())
            else:
                raise Exception("Can't export image. Item must be feature, layer or layout.")
                
            print (img_temppath)
            return (open(img_temppath, 'rb'), mimetype)
                
        result = engine.render(template, **self.environment )

        with open(target, 'wb') as output:
            output.write(result)
            output.flush()
        
        return True