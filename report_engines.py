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

from zipfile import ZipFile,ZIP_DEFLATED

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from jinja2 import evalcontextfilter, Markup, escape, meta

from .ext_libs.secretary import Renderer    
from .report_renderer import abstact_report_engine   

def layout_export(value,image_metadata,img_path,img_size,as_is=None):
    #https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/pyqgis-101-exporting-layouts/
    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(image_metadata[1])
    if image_metadata[0] == 'atlas': # is atlas
        layout.atlas().seekTo(value['id'])
        layout.atlas().refreshCurrentFeature()
    exporter = QgsLayoutExporter(layout)
    aspect_ratio = layout.pageCollection().page(0).pageSize().width()/layout.pageCollection().page(0).pageSize().height()
    settings = exporter.ImageExportSettings()
    if not as_is:
        if img_size["width"] > img_size["height"]:
            img_size["height"] = img_size["width"]*aspect_ratio
        else:
            img_size["width"] = img_size["height"]*aspect_ratio
    settings.imageSize = QSize(img_size["width"] ,img_size["height"])
    settings.dpi = img_size["dpi"]
    settings.cropToContents = False
    #settings.pages = [0]
    res = exporter.exportToImage(img_path, settings)
    if res:
        return img_path
    else:
        return None

class markdown_renderer(abstact_report_engine):

    def export_image(self,box,width,height,theme,img_path,around_border):
        if around_border:
            if width >= height:
                dim = box.xMaximum() - box.xMinimum()
            else:
                dim = box.yMaximum() - box.yMinimum()
            dim = dim*around_border
            box.grow(dim)
        if img_path:
            img = self.canvas_image(box,width,height,theme)
            img.save(img_path)
            path, img_name = os.path.split(img_path)
            return img_name
        else:
            return self.canvas_base64_image(box,width,height,theme)

    def image_render(self, value,width=300,height=300,dpi=200,box=None,center=None,atlas=None,theme=None,around_border=0.1,mimetype="image/png",filter=None,**kwargs):

        if atlas:
            image_metadata = ["atlas",atlas]
        else:
            image_metadata = value["image"].split(":")

        img_temppath = tempfile.NamedTemporaryFile(suffix=".png",delete=False,dir=self.tempdir).name

        if image_metadata[0] == 'canvas':
            view_box = self.iface.mapCanvas().extent()
            if self.as_single_file:
                img_temppath = None
            return self.export_image(view_box, width, height, theme, img_temppath, around_border)

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
                view_box = pointFeatbox
            else:
                view_box = feature.geometry().boundingBox()
            if self.as_single_file:
                img_temppath = None
            return self.export_image(view_box, width, height, theme, img_temppath, around_border)
            
        elif image_metadata[0] == 'layer':
            layer = QgsProject.instance().mapLayer(image_metadata[1])
            view_box = layer.extent()
            return self.export_image(view_box, width, height, theme or layer, img_temppath if not self.as_single_file else None, around_border)
            
        elif image_metadata[0] in ('layout', 'atlas'):
            size = {
                "width":width,
                "height":height,
                "dpi":dpi
            }
            res = layout_export(value,image_metadata,img_temppath,size,as_is=False)
            if res:
                if self.as_single_file:
                    return self.exporter.img2base64(res)
                else:
                    path, img_name = os.path.split(res)
                    return img_name 
            else:
                self.report_exception ("md image export: Can't export layout.")

        else:
            self.report_exception ("md image export: Can't export image. Item must be globals, feature, layer or layout.",item=value)

    def render(self,template,target,embed_images=False):
        template_path,template_filename = os.path.split(template)
        env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=select_autoescape(['html', 'xml']),
        )
        self.as_single_file = embed_images
        self.tempdir = tempfile.mkdtemp(suffix=None, prefix=None, dir=None)
        env.filters["image"] = self.image_render
        env.filters['isVector'] = self.isVector
        env.filters['isRaster'] = self.isRaster
        template_obj = env.get_template(template_filename)
        result = template_obj.render(**self.environment )
        if self.as_single_file:
            output = open(target, 'w')
            output.write(result)
        else:
            target_path,target_filename = os.path.split(target)
            output = open(os.path.join(self.tempdir,target_filename), 'w')
            output.write(result)
            target = target+".zip"
            md_files = os.listdir(self.tempdir)
            zip = ZipFile(target, "w", ZIP_DEFLATED)
            for f in md_files:
                zip.write(os.path.join(self.tempdir,f),f)

            # fix for Linux zip files read in Windows
            for filename in zip.filelist:
                filename.create_system = 0

            zip.close()

        return target
                
class odt_renderer(abstact_report_engine):

    def render(self,template,target):
        engine = Renderer()
        engine.environment.filters['isVector'] = self.isVector
        engine.environment.filters['isRaster'] = self.isRaster
        
        @engine.media_loader
        def qgis_images_loader(value,dpi=200,box=None,center=None,atlas=None,theme=None,scale_denominator=None,around_border=0.1,mimetype="image/png",filter=None,**kwargs): 

            xsize = float(kwargs['frame_attrs']['svg:width'][:-2])
            ysize = float(kwargs['frame_attrs']['svg:height'][:-2])
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

            meterxsize = xsize*m_conversion_factor
            meterysize = ysize*m_conversion_factor

            width = int(xsize/reverse_factor*dpi)
            height = int(ysize/reverse_factor*dpi)
            aspect_ratio = width/height

            img_temppath = tempfile.NamedTemporaryFile(suffix=".png",delete=False).name

            if self.isurl(value):
                img = self.url_image(value,width,height)
                img.save(img_temppath)
            
            elif isinstance(value,dict) and "image" in value.keys():

                if center and not scale_denominator:
                    self.report_exception ("odt image export: Can't specify center without scale_denominator parameter")

                def getFrame(reference_frame):
                    centerxy = center
                    bb = box
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
                                self.report_exception ("odt image export: Malformed center parameter",center=type(centerxy))
                        
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
                if not 'svg:width' in kwargs['frame_attrs']:
                    self.report_exception ("odt image export: Malformed svg image parameters",swg_attrs=str(kwargs['frame_attrs']))

                meterxsize = xsize*m_conversion_factor
                meterysize = ysize*m_conversion_factor
                
                if image_metadata[0] == 'canvas':
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
                    img = self.canvas_image(box=view_box,width=width,height=height,theme=theme)
                    img.save(img_temppath)
                    
                elif image_metadata[0] == 'layer':
                    layer = QgsProject.instance().mapLayer(image_metadata[1])
                    view_box = getFrame(layer.extent())
                    img = self.canvas_image(box=view_box,width=width,height=height,theme=layer)
                    img.save(img_temppath)
                    
                elif image_metadata[0] in ('layout', 'atlas'):
                    size = {
                        "width":width,
                        "height":height,
                        "dpi":dpi
                    }
                    res = layout_export(value,image_metadata,img_temppath,size,as_is=False)
                else:
                    self.report_exception ("odt image export: Can't export image. Item must be globals, feature, layer or layout.",item=value)
            else:
                self.report_exception("Can't generate image from object", obj=value)
                
            return (open(img_temppath, 'rb'), mimetype)
                
        result = engine.render(template, **self.environment )

        with open(target, 'wb') as output:
            output.write(result)
            output.flush()
        
        return True
