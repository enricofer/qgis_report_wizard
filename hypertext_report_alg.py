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

__author__ = 'enrico ferreguti'
__date__ = '2021-15-12'
__copyright__ = '(C) 2021 by enrico ferreguti'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import (
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterBoolean,
)

import os

from .report_engines import hypertext_renderer

class HypertextGeneratorAlgorithm(QgsProcessingAlgorithm):

    TEMPLATE = "TEMPLATE"
    VECTOR_LAYER = "VECTOR_LAYER"
    LIMIT = "LIMIT"
    OUTPUT = "OUTPUT"
    EMBED_IMAGES = "EMBED_IMAGES"
    SAVE_TO_FOLDER = "SAVE_TO_FOLDER"

    def init__(self, *args,**kwargs):
        print (kwargs)
        self.iface = kwargs.pop("iface")
        super(HypertextGeneratorAlgorithm, self).__init__(*args,**kwargs)
    
    def setInterface(self, iface):
        self.iface = iface

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(self.TEMPLATE, 'Text template (html, xml, markdown, txt)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer(self.VECTOR_LAYER, 'Vector Layer that drive feature rendering', types=[QgsProcessing.TypeVectorAnyGeometry], optional=True))
        self.addParameter(QgsProcessingParameterNumber(self.LIMIT, 'Limit features rendering amount', defaultValue=100)) 
        self.addParameter(QgsProcessingParameterBoolean(self.EMBED_IMAGES, 'Base64 Encode and Embed images in text document', defaultValue=False))
        self.addParameter(QgsProcessingParameterBoolean(self.SAVE_TO_FOLDER, 'Save text and images to folder', defaultValue=False))
        self.addParameter(QgsProcessingParameterFileDestination(self.OUTPUT, 'Rendered output text file'))

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        template = self.parameterAsFile(parameters, self.TEMPLATE, context)
        vector_layer = self.parameterAsVectorLayer(parameters, self.VECTOR_LAYER, context)
        feature_limit = self.parameterAsInt(parameters, self.LIMIT, context)
        target = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        embed_images = self.parameterAsBoolean(parameters, self.EMBED_IMAGES, context)
        save_to_folder = self.parameterAsBoolean(parameters, self.SAVE_TO_FOLDER, context)

        if save_to_folder and parameters[self.OUTPUT] == 'TEMPORARY_OUTPUT':
            save_to_folder = False
            feedback.reportError('With "Save text and images to folder" option, output folder have to be specified\n')
        
        if embed_images and save_to_folder:
            feedback.reportError('"Save text and images to folder" option has priority on "Embed images in text document" option\n')
            embed_images = False

        template_path,template_ext = os.path.splitext(template)

        if not target.endswith(template_ext):
            targetpath,extension = os.path.splitext(target)
            target = targetpath + template_ext

        iface = self.provider().iface
        engine = hypertext_renderer(iface, vector_layer, feature_limit)
        output_file, result = engine.render(template, target, embed_images,save_to_folder)

        return {
            "OUTPUT": output_file,
            "TRACE": result
        }

    def name(self):
        return 'hypertext_report'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return 'Hypertext report generator'

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return 'report wizard'

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'report_wizard'

    def createInstance(self):
        return HypertextGeneratorAlgorithm()
