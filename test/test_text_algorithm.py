# coding=utf-8
"""Algorithm Test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = '(C) 2021 by Enrico Ferreguti'
__date__ = '30/11/2021'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import unittest
import os
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsProject,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFile,
                       QgsProcessing,
                       QgsProcessingContext,
                       QgsProcessingFeedback,
                       QgsVectorLayer,
                       QgsProcessingAlgorithm)
from qgis.gui import QgsMapCanvas
from qgis.PyQt.QtCore import (QDateTime, QDate, QTime)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QWidget
from ..odt_report_alg import OdtGeneratorAlgorithm
from ..hypertext_report_alg import HypertextGeneratorAlgorithm
from .utilities import get_qgis_app
from .qgis_interface import QgisInterface

import processing

QGISAPP, CANVAS, IFACE, PARENT = get_qgis_app()

templates_path = os.path.join(
    os.path.dirname(__file__),
    'templates')


class TextAlgorithmTest(unittest.TestCase):
    """Test odt algorithm construction."""

    def init__(self, *args, **kwargs):
        super(TextAlgorithmTest, self).__init__(*args, **kwargs)
        self.project = QgsProject(PARENT)
        self.canvas = CANVAS
        CANVAS.setProject(self.project)
        self.loadedProject = self.project.read(os.path.join(templates_path,"sample_prj.qgs"))
        self.vector_driver = self.project.mapLayersByName("testdata")[0]

    def setup(self):
        self.project = QgsProject(PARENT)
        self.canvas = CANVAS
        CANVAS.setProject(self.project)
        self.loadedProject = self.project.read(os.path.join(templates_path,"sample_prj.qgs"))
        self.vector_driver = self.project.mapLayersByName("testdata")[0]

    def testSetupHypertextAlg(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test alg setup
        """
        alg = HypertextGeneratorAlgorithm()
        alg.setInterface(IFACE)
        alg.initAlgorithm()
        self.assertEqual(alg.name(), 'hypertext_report')
        self.assertEqual(alg.displayName(), 'Hypertext report generator')
        #self.assertIn('test_algorithm_1.rsx', 'test_algorithm_1.rsx')

        # test that inputs were created correctly
        template_param = alg.parameterDefinition('TEMPLATE')
        self.assertEqual(template_param.type(), 'file')
        vector_param = alg.parameterDefinition('VECTOR_LAYER')
        self.assertEqual(vector_param.type(), 'vector')
        limit_param = alg.parameterDefinition('LIMIT')
        self.assertEqual(limit_param.type(), 'number')
        embed_param = alg.parameterDefinition('EMBED_IMAGES')
        self.assertEqual(embed_param.type(), 'boolean')
        vector_output = alg.outputDefinition('OUTPUT')
        self.assertEqual(vector_output.type(), 'outputFile')

    def testcheckprojectLoaded(self): 
        self.assertEqual(self.project.count(), 5)

    def testRunTxtProjectAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_project.md"),
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")

    def testRunTxtThemesAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_themes.md"),
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")

    def testRunTxtBookmarksAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_bookmarks.md"),
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")

    def testRunTxtLayoutAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_layout.md"),
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")

    def testRunTxtAtlasAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_atlas.md"),
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")

    def testRunTxtLayersAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_layers.md"),
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")

    def testRunTxtFeaturesAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_feats.md"),
            "VECTOR_LAYER": self.vector_driver,
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")

    def testRunTxtFeaturesWithPicsAlg(self): 
        params = {
            "TEMPLATE": os.path.join(templates_path, "tab_feats_pics.md"),
            "VECTOR_LAYER": self.vector_driver,
            "OUTPUT": "/tmp/test.odt"
        }
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md.zip")
        params["EMBED_IMAGES"] = True
        result = processing.run('report_wizard:hypertext_report', params)
        self.assertEqual(result["OUTPUT"], "/tmp/test.md")


if __name__ == "__main__":
    suite = unittest.makeSuite(TextAlgorithmTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
