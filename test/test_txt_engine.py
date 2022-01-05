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
from ..report_engines import hypertext_renderer

QGISAPP, CANVAS, IFACE, PARENT = get_qgis_app()

templates_path = os.path.join(
    os.path.dirname(__file__),
    'templates')


class TextEngineTest(unittest.TestCase):
    """Test odt algorithm construction."""

    def setUp(self):
        self.target_md = "/tmp/OUTPUT.md"
        self.target_zip = self.target_md+".zip"
        if os.path.exists(self.target_md):
            os.remove(self.target_md)
        if os.path.exists(self.target_zip):
            os.remove(self.target_zip)
        #project = QgsProject(PARENT)
        #CANVAS.setProject(project)
        self.loadedProject = QgsProject.instance().read(os.path.join(templates_path,"sample_prj.qgs"))
        self.vector_driver = QgsProject.instance().mapLayersByName("testdata")[0]

    def testLoadProjectTxtEngine(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test loading project
        """
        self.assertTrue(self.loadedProject)

    def testSetupTxtEngine(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test setup text engine
        """
        engine = hypertext_renderer(IFACE, self.vector_driver, 100)
        print (engine.environment)
        self.assertEqual(len(engine.environment), 4)
        self.assertEqual(len(engine.environment["features"]), 6)

    def testTxtEngineProjectTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render project template
        """
        engine = hypertext_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_project.md")
        result = engine.render(template,self.target_md,embed_images=False)
        self.assertEqual(result, self.target_zip)

    def testTxtEngineLayersTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render layers template
        """
        engine = hypertext_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_layers.md")
        result = engine.render(template,self.target_md,embed_images=False)
        self.assertEqual(result, self.target_zip)

    def testTxtEngineFeaturesTemplate(self):  # pylint: disable=too-many-locals,too-many-statements
        """
        Test render features template
        """
        engine = hypertext_renderer(IFACE, self.vector_driver, 100)
        template = os.path.join(templates_path,"tab_feats.md")
        result = engine.render(template,self.target_md,embed_images=False)
        self.assertEqual(result, self.target_zip)


if __name__ == "__main__":
    suite = unittest.makeSuite(TextEngineTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
