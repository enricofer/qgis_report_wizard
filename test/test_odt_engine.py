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
                       QgsProject,)
from .utilities import get_qgis_app
from ..report_engines import odt_renderer

QGISAPP, CANVAS, IFACE, PARENT = get_qgis_app()

templates_path = os.path.join(
    os.path.dirname(__file__),
    'templates')


class OdtEngineTest(unittest.TestCase):
    """Test odt algorithm construction."""

    def setUp(self):
        self.target = "/tmp/OUTPUT.odt"
        if os.path.exists(self.target):
            os.remove(self.target)
        self.loadedProject = QgsProject.instance().read(os.path.join(templates_path,"sample_prj.qgs"))
        self.vector_driver = QgsProject.instance().mapLayersByName("testdata")[0]

    def testLoadProjectOdtEngine(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test loading project
        """
        self.assertTrue(self.loadedProject)

    def testSetupOdtEngine(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test setup odt engine
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        self.assertEqual(len(engine.environment), 4)
        self.assertEqual(len(engine.environment["features"]), 6)

    def testTxtEngineProjectTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render project template
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_project.odt")
        output, result = engine.render(template,self.target)
        print (result)
        self.assertEqual(output, self.target)

    def testTxtEngineLayersTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render layers template
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_layers.odt")
        output, result = engine.render(template,self.target)
        self.assertEqual(output, self.target)

    def testTxtEngineFeaturesTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render features template
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_feats.odt")
        output, result = engine.render(template,self.target)
        self.assertEqual(output, self.target)

    def testTxtEngineFeaturesPicsTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render features template with pictures
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_feats_pics.odt")
        output, result = engine.render(template,self.target)
        print (result)
        self.assertEqual(output, self.target)

    def testTxtEngineLayoutsTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render layouts template
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_layout.odt")
        output, result = engine.render(template,self.target)
        self.assertEqual(output, self.target)

    def testTxtEngineThemesTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render themes template
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_themes.odt")
        output, result = engine.render(template,self.target)
        self.assertEqual(output, self.target)

    def testTxtEngineVariablesTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render Variables template
        """
        engine = odt_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_variables.odt")
        output, result = engine.render(template,self.target)
        self.assertEqual(output, self.target)


if __name__ == "__main__":
    suite = unittest.makeSuite(OdtEngineTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
