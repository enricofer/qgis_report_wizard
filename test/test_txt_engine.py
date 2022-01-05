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
from ..report_engines import hypertext_renderer

import processing

QGISAPP, CANVAS, IFACE, PARENT = get_qgis_app()

templates_path = os.path.join(
    os.path.dirname(__file__),
    'templates')


class TextEngineTest(unittest.TestCase):
    """Test odt algorithm construction."""

    def init__(self, *args, **kwargs):
        super(TextEngineTest, self).__init__(*args, **kwargs)
        self.target_md = "/tmp/OUTPUT.md"
        self.target_zip = self.target_md+".zip"
        if os.path.exists(self.target):
            os.remove(self.target)
        if os.path.exists(self.target_zip):
            os.remove(self.target_zip)
        self.project = QgsProject(PARENT)
        CANVAS.setProject(self.project)
        self.loadedProject = self.project.read(os.path.join(templates_path,"sample_prj.qgs"))
        self.vector_driver = self.project.mapLayersByName("testdata")[0]

    def __setup(self):
        self.target_md = "/tmp/OUTPUT.md"
        self.target_zip = self.target_md+".zip"
        if os.path.exists(self.target):
            os.remove(self.target)
        if os.path.exists(self.target_zip):
            os.remove(self.target_zip)
        self.project = QgsProject(PARENT)
        CANVAS.setProject(self.project)
        self.loadedProject = self.project.read(os.path.join(templates_path,"sample_prj.qgs"))
        self.vector_driver = self.project.mapLayersByName("testdata")[0]

    def testSetupTxtEngine(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test engine setup
        """
        engine = hypertext_renderer(IFACE, self.vector_driver, 100)
        self.assertEqual(len(engine.environment), 4)
        self.assertEqual(len(engine.environment["features"]), 6)

    def testTxtEngineProjectTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test engine setup
        """
        engine = hypertext_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_project.md")
        result = engine.render(template,self.target,embed_images=False)
        self.assertEqual(result, self.target_zip)


if __name__ == "__main__":
    suite = unittest.makeSuite(TextEngineTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
