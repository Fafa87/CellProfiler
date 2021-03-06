'''test_measuretexture - test the MeasureTexture module
'''

import base64
import unittest
import zlib
from StringIO import StringIO

import cellprofiler.image as cpi
import cellprofiler.measurement as cpmeas
import cellprofiler.modules.measuretexture as M
import cellprofiler.object as cpo
import cellprofiler.pipeline as cpp
import cellprofiler.workspace as cpw
import numpy as np

INPUT_IMAGE_NAME = 'Cytoplasm'
INPUT_OBJECTS_NAME = 'inputobjects'


class TestMeasureTexture(unittest.TestCase):
    def make_workspace(self, image, labels, convert=True, mask=None):
        '''Make a workspace for testing MeasureTexture'''
        module = M.MeasureTexture()
        module.image_groups[0].image_name.value = INPUT_IMAGE_NAME
        module.object_groups[0].object_name.value = INPUT_OBJECTS_NAME
        pipeline = cpp.Pipeline()
        object_set = cpo.ObjectSet()
        image_set_list = cpi.ImageSetList()
        image_set = image_set_list.get_image_set(0)
        workspace = cpw.Workspace(pipeline,
                                  module,
                                  image_set,
                                  object_set,
                                  cpmeas.Measurements(),
                                  image_set_list)
        image_set.add(INPUT_IMAGE_NAME, cpi.Image(image, convert=convert,
                                                  mask=mask))
        objects = cpo.Objects()
        objects.segmented = labels
        object_set.add_objects(objects, INPUT_OBJECTS_NAME)
        return workspace, module

    def test_01_03_load_v2(self):
        data = """CellProfiler Pipeline: http://www.cellprofiler.org
Version:1
SVNRevision:10865

MeasureTexture:[module_num:1|svn_version:\'1\'|variable_revision_number:2|show_window:True|notes:\x5B\x5D]
    Hidden:2
    Hidden:2
    Hidden:2
    Select an image to measure:rawDNA
    Select an image to measure:rawGFP
    Select objects to measure:Cells
    Select objects to measure:Nuclei
    Texture scale to measure:3
    Texture scale to measure:5
    Measure Gabor features?:Yes
    Number of angles to compute for Gabor:6

MeasureTexture:[module_num:2|svn_version:\'1\'|variable_revision_number:2|show_window:True|notes:\x5B\x5D]
    Hidden:2
    Hidden:2
    Hidden:2
    Select an image to measure:rawDNA
    Select an image to measure:rawGFP
    Select objects to measure:Cells
    Select objects to measure:Nuclei
    Texture scale to measure:3
    Texture scale to measure:5
    Measure Gabor features?:No
    Number of angles to compute for Gabor:6
"""
        pipeline = cpp.Pipeline()

        def callback(caller, event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))

        pipeline.add_listener(callback)
        pipeline.load(StringIO(data))
        self.assertEqual(len(pipeline.modules()), 2)
        for i, wants_gabor in enumerate((True, False)):
            module = pipeline.modules()[i]
            self.assertTrue(isinstance(module, M.MeasureTexture))
            self.assertEqual(len(module.image_groups), 2)
            self.assertEqual(module.image_groups[0].image_name, "rawDNA")
            self.assertEqual(module.image_groups[1].image_name, "rawGFP")
            self.assertEqual(len(module.object_groups), 2)
            self.assertEqual(module.object_groups[0].object_name, "Cells")
            self.assertEqual(module.object_groups[1].object_name, "Nuclei")
            self.assertEqual(len(module.scale_groups), 2)
            self.assertEqual(module.scale_groups[0].scale, 3)
            self.assertEqual(len(module.scale_groups[0].angles.get_selections()), 1)
            self.assertEqual(module.scale_groups[0].angles.get_selections()[0], M.H_HORIZONTAL)
            self.assertEqual(module.scale_groups[1].scale, 5)
            self.assertEqual(len(module.scale_groups[1].angles.get_selections()), 1)
            self.assertEqual(module.scale_groups[1].angles.get_selections()[0], M.H_HORIZONTAL)
            self.assertEqual(module.wants_gabor, wants_gabor)
            self.assertEqual(module.gabor_angles, 6)

    def test_01_03_load_v3(self):
        data = """CellProfiler Pipeline: http://www.cellprofiler.org
Version:1
SVNRevision:10865

MeasureTexture:[module_num:1|svn_version:\'1\'|variable_revision_number:3|show_window:True|notes:\x5B\x5D]
    Hidden:2
    Hidden:2
    Hidden:2
    Select an image to measure:rawDNA
    Select an image to measure:rawGFP
    Select objects to measure:Cells
    Select objects to measure:Nuclei
    Texture scale to measure:3
    Angles to measure:Horizontal,Vertical
    Texture scale to measure:5
    Angles to measure:Diagonal,Anti-diagonal
    Measure Gabor features?:Yes
    Number of angles to compute for Gabor:6

MeasureTexture:[module_num:2|svn_version:\'1\'|variable_revision_number:3|show_window:True|notes:\x5B\x5D]
    Hidden:2
    Hidden:2
    Hidden:2
    Select an image to measure:rawDNA
    Select an image to measure:rawGFP
    Select objects to measure:Cells
    Select objects to measure:Nuclei
    Texture scale to measure:3
    Angles to measure:Horizontal,Vertical
    Texture scale to measure:5
    Angles to measure:Diagonal,Anti-diagonal
    Measure Gabor features?:No
    Number of angles to compute for Gabor:6
"""
        pipeline = cpp.Pipeline()

        def callback(caller, event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))

        pipeline.add_listener(callback)
        pipeline.load(StringIO(data))
        self.assertEqual(len(pipeline.modules()), 2)
        for i, wants_gabor in enumerate((True, False)):
            module = pipeline.modules()[i]
            self.assertTrue(isinstance(module, M.MeasureTexture))
            self.assertEqual(len(module.image_groups), 2)
            self.assertEqual(module.image_groups[0].image_name, "rawDNA")
            self.assertEqual(module.image_groups[1].image_name, "rawGFP")
            self.assertEqual(len(module.object_groups), 2)
            self.assertEqual(module.object_groups[0].object_name, "Cells")
            self.assertEqual(module.object_groups[1].object_name, "Nuclei")
            self.assertEqual(len(module.scale_groups), 2)
            self.assertEqual(module.scale_groups[0].scale, 3)
            angles = module.scale_groups[0].angles.get_selections()
            self.assertEqual(len(angles), 2)
            self.assertTrue(M.H_HORIZONTAL in angles)
            self.assertTrue(M.H_VERTICAL in angles)

            angles = module.scale_groups[1].angles.get_selections()
            self.assertEqual(len(angles), 2)
            self.assertTrue(M.H_DIAGONAL in angles)
            self.assertTrue(M.H_ANTIDIAGONAL in angles)

            self.assertEqual(module.scale_groups[1].scale, 5)
            self.assertEqual(module.wants_gabor, wants_gabor)
            self.assertEqual(module.gabor_angles, 6)
            self.assertEqual(module.images_or_objects, M.IO_BOTH)

    def test_01_04_load_v4(self):
        data = """CellProfiler Pipeline: http://www.cellprofiler.org
Version:3
DateRevision:20141017202435
GitHash:b261e94
ModuleCount:3
HasImagePlaneDetails:False

MeasureTexture:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:4|show_window:True|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    Hidden:2
    Hidden:2
    Hidden:2
    Select an image to measure:rawDNA
    Select an image to measure:rawGFP
    Select objects to measure:Cells
    Select objects to measure:Nuclei
    Texture scale to measure:3
    Angles to measure:Horizontal,Vertical
    Texture scale to measure:5
    Angles to measure:Diagonal,Anti-diagonal
    Measure Gabor features?:Yes
    Number of angles to compute for Gabor:6
    Measure images or objects?:Images

MeasureTexture:[module_num:2|svn_version:\'Unknown\'|variable_revision_number:4|show_window:True|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    Hidden:2
    Hidden:2
    Hidden:2
    Select an image to measure:rawDNA
    Select an image to measure:rawGFP
    Select objects to measure:Cells
    Select objects to measure:Nuclei
    Texture scale to measure:3
    Angles to measure:Horizontal,Vertical
    Texture scale to measure:5
    Angles to measure:Diagonal,Anti-diagonal
    Measure Gabor features?:No
    Number of angles to compute for Gabor:6
    Measure images or objects?:Objects

MeasureTexture:[module_num:3|svn_version:\'Unknown\'|variable_revision_number:4|show_window:True|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    Hidden:2
    Hidden:2
    Hidden:2
    Select an image to measure:rawDNA
    Select an image to measure:rawGFP
    Select objects to measure:Cells
    Select objects to measure:Nuclei
    Texture scale to measure:3
    Angles to measure:Horizontal,Vertical
    Texture scale to measure:5
    Angles to measure:Diagonal,Anti-diagonal
    Measure Gabor features?:No
    Number of angles to compute for Gabor:6
    Measure images or objects?:Both
"""
        pipeline = cpp.Pipeline()

        def callback(caller, event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))

        pipeline.add_listener(callback)
        pipeline.load(StringIO(data))
        self.assertEqual(len(pipeline.modules()), 3)
        for i, (wants_gabor, io_choice) in enumerate(
                ((True, M.IO_IMAGES),
                 (False, M.IO_OBJECTS),
                 (False, M.IO_BOTH))):
            module = pipeline.modules()[i]
            self.assertTrue(isinstance(module, M.MeasureTexture))
            self.assertEqual(len(module.image_groups), 2)
            self.assertEqual(module.image_groups[0].image_name, "rawDNA")
            self.assertEqual(module.image_groups[1].image_name, "rawGFP")
            self.assertEqual(len(module.object_groups), 2)
            self.assertEqual(module.object_groups[0].object_name, "Cells")
            self.assertEqual(module.object_groups[1].object_name, "Nuclei")
            self.assertEqual(len(module.scale_groups), 2)
            self.assertEqual(module.scale_groups[0].scale, 3)
            angles = module.scale_groups[0].angles.get_selections()
            self.assertEqual(len(angles), 2)
            self.assertTrue(M.H_HORIZONTAL in angles)
            self.assertTrue(M.H_VERTICAL in angles)

            angles = module.scale_groups[1].angles.get_selections()
            self.assertEqual(len(angles), 2)
            self.assertTrue(M.H_DIAGONAL in angles)
            self.assertTrue(M.H_ANTIDIAGONAL in angles)

            self.assertEqual(module.scale_groups[1].scale, 5)
            self.assertEqual(module.wants_gabor, wants_gabor)
            self.assertEqual(module.gabor_angles, 6)

    def test_02_02_many_objects(self):
        '''Regression test for IMG-775'''
        np.random.seed(22)
        image = np.random.uniform(size=(100, 100))
        i, j = np.mgrid[0:100, 0:100]
        labels = (i / 10).astype(int) + (j / 10).astype(int) * 10 + 1
        workspace, module = self.make_workspace(image, labels)
        self.assertTrue(isinstance(module, M.MeasureTexture))
        module.scale_groups[0].scale.value = 2
        module.scale_groups[0].angles.value = ",".join(M.H_ALL)
        module.run(workspace)
        m = workspace.measurements
        all_measurements = module.get_measurements(
                workspace.pipeline, INPUT_OBJECTS_NAME, M.TEXTURE)
        all_columns = module.get_measurement_columns(workspace.pipeline)
        self.assertTrue(all([oname in (INPUT_OBJECTS_NAME, cpmeas.IMAGE)
                             for oname, feature, coltype in all_columns]))
        all_column_features = [
            feature for oname, feature, coltype in all_columns
            if oname == INPUT_OBJECTS_NAME]
        self.assertTrue(all([any([oname == cpmeas.IMAGE and feature == afeature
                                  for oname, feature, coltype in all_columns])
                             for afeature in all_column_features]))
        for measurement in M.F_HARALICK:
            self.assertTrue(measurement in all_measurements)
            self.assertTrue(
                    INPUT_IMAGE_NAME in module.get_measurement_images(
                            workspace.pipeline, INPUT_OBJECTS_NAME, M.TEXTURE, measurement))
            all_scales = module.get_measurement_scales(
                    workspace.pipeline, INPUT_OBJECTS_NAME, M.TEXTURE,
                    measurement, INPUT_IMAGE_NAME)
            for angle in M.H_ALL:
                mname = '%s_%s_%s_%d_%s' % (
                    M.TEXTURE, measurement, INPUT_IMAGE_NAME, 2, M.H_TO_A[angle])
                self.assertTrue(mname in all_column_features)
                values = m.get_current_measurement(INPUT_OBJECTS_NAME, mname)
                self.assertTrue(np.all(values != 0))
                self.assertTrue("%d_%s" % (2, M.H_TO_A[angle]) in all_scales)

    def test_03_01_gabor_null(self):
        '''Test for no score on a uniform image'''
        image = np.ones((10, 10)) * .5
        labels = np.ones((10, 10), int)
        workspace, module = self.make_workspace(image, labels)
        module.scale_groups[0].scale.value = 2
        module.run(workspace)
        mname = '%s_%s_%s_%d' % (M.TEXTURE, M.F_GABOR, INPUT_IMAGE_NAME, 2)
        m = workspace.measurements.get_current_measurement(INPUT_OBJECTS_NAME,
                                                           mname)
        self.assertEqual(len(m), 1)
        self.assertAlmostEqual(m[0], 0)

    def test_03_02_gabor_horizontal(self):
        '''Compare the Gabor score on the horizontal with the one on the diagonal'''
        i, j = np.mgrid[0:10, 0:10]
        labels = np.ones((10, 10), int)
        himage = np.cos(np.pi * i) * .5 + .5
        dimage = np.cos(np.pi * (i - j) / np.sqrt(2)) * .5 + .5

        def run_me(image, angles):
            workspace, module = self.make_workspace(image, labels)
            module.scale_groups[0].scale.value = 2
            module.gabor_angles.value = angles
            module.run(workspace)
            mname = '%s_%s_%s_%d' % (M.TEXTURE, M.F_GABOR, INPUT_IMAGE_NAME, 2)
            m = workspace.measurements.get_current_measurement(INPUT_OBJECTS_NAME,
                                                               mname)
            self.assertEqual(len(m), 1)
            return m[0]

        himage_2, himage_4, dimage_2, dimage_4 = [run_me(image, angles)
                                                  for image, angles in
                                                  ((himage, 2), (himage, 4),
                                                   (dimage, 2), (dimage, 4))]
        self.assertAlmostEqual(himage_2, himage_4)
        self.assertAlmostEqual(dimage_2, 0)
        self.assertNotAlmostEqual(dimage_4, 0)

    def test_03_02_01_gabor_off(self):
        '''Make sure we can run MeasureTexture without gabor feature'''
        workspace, module = self.make_workspace(np.zeros((10, 10)),
                                                np.zeros((10, 10), int))
        self.assertTrue(isinstance(module, M.MeasureTexture))
        module.wants_gabor.value = False
        module.run(workspace)
        m = workspace.measurements
        self.assertTrue(isinstance(m, cpmeas.Measurements))
        for object_name in (cpmeas.IMAGE, INPUT_OBJECTS_NAME):
            features = m.get_feature_names(object_name)
            self.assertTrue(all([f.find(M.F_GABOR) == -1 for f in features]))

    # def test_03_03_measurement_columns(self):
    #     '''Check that results of get_measurement_columns match the actual column names output'''
    #     data = 'eJztW91u2zYUph0naFqgSHexBesNd9d2iSA7SZcEQ2vPXjcPsRs0Xn8wbJgi0TEHWjQkKrU39N32GHuEXe4RJtqyJXFyJMuSJ6cSQEiH5seP5/DwHEqyWrXOWe0beCTJsFXr7HcxQfCcKKxLjf4pHFATD/dg3UAKQxqk+ilsUR3+YBFYPoDlw1P55PTgEFZk+QTEOArN1n37tHsMwJZ9vmOXovPTpiMXPIXLF4gxrF+Zm6AEdp36P+3yWjGwcknQa4VYyHQppvVNvUs7o8HspxbVLILaSt/b2D7aVv8SGebL7hTo/HyOh4hc4N+RoMK02St0jU1MdQfv9C/WzngpE3i5HXqfu3YoCHYo2eWhp563/x647UsBdnvgab/jyFjX8DXWLIVA3FeuZqPg/ckh/W34+tsAjXZtjDsOwW0J49ga21klCEfjLfjwBVBxxlsNwe0IvLx00JDtfztUVAb7ClN7SYw/DL8p4LlcR4SYEe0+T/9FcQcRcSUfrgSe7h3KUey9LejJ5Td24DDMHtKc+mX0jWPn5tnZj62IvKJ/v7NXR1y96yNGB0Qx+wvoPW99heGKPlwRtGk0vnm4MH3vCfpy+SUzLfgdoZcKmemblN3C4txnQj9cbqCuYhEGmzzIwQY2kMqoMVrKDxbFlSU58fi4JeCnxxS/7bFbNYQ36jzGyTOyJI+PvbJz4RlX2vEy6flbNF7aupfTjM/z9Et6nhaNH2U5Xnw/WlLvtOYnAHcUR7+nIJrf3wH++eFyvafoOiKVuPG0qTOkm5iNnPoo/dwV+uFyg0KdMmiZyO0nblyKmweT0n9RfjkgDiSpr+gv5Yi4uOtP9Os21VGaeSZoXl7wG03dvv1awk5fxbRT0P5oEX3fhvB9IejL5V+kJ/uPnp9//Yq+fyZ9+Xh8Xafk2U/y/snPf1Q+PF7ADnH3qUH5vvOeQtXeb5nOneAydumF8B8L/FzmdniHFMMxxOGHiWlaVGc91zjjuoYycmuSjGNx8uYbhK96/JnINX8AoKvz/HgR+y2RHyLls7h+E2THF9RAVwa1dG15vcP407q/Cto/xI3raeaDqPf7WdGvGjLOpPJBmnl6nfJB0vl8XeL/qvN+1uJEVtb7qvSTpaP/fZxpP39Jcj+2alxW9lFZm+e0909xcX/turiCgAt637RK+4xfTnEDDaL3E7Se6OVvSGVuR+uyLjzjhljX0CDF/tZlnd12XBWsZp1E7edjs9tt0TercTDXN8fluOzgwvYRnwD/uuIytRjBOvrPRiLN9b0jjIMXN35PRrFOds9a/Lxt+THHZQOXlfiS4/K4m+M+XlwV3Oznef7LcTkux+W424X7u+DixPcbXPa+N+ftf/XwBOWJJ8CfJ7isIkIGBuXfTRlSf/xxjykRqmiTr2ukM/uy6fnQhvMMQniqAk91Hg/WkM5wdzQwbDaL0b7CsCo1ndpzu7Y2reW8vRDeoPfzN/KaSKW6phijGefFtCYKX0Xgq8zj6yPFtAzE0JDZJ6k1ETsT0bWr10+2A/i88120pU8fPrh7k38B4Pcr19/+eR6Hb2OjWLgP/P/zuheCKwG/n4/9Gizm149uaD/VMavt/wXhfSus'
    #     # alternate data: 1 image, 1 object, tex scale=3, gabor angles=6
    #     #        data = 'eJztW91u2zYUph0nW1agSHexFesNd9d2iSA7TZMGQ2vPXjcPsWs0Xrti2DBGomMONGlIVGpv6Hvtco+yy13uESbasiVzciTLP7UzCSCkQ/Hjx3N4eA5lWbVS86z0FTzSdFgrNQ9ahGLYoEi0uNU5hV1uk94+LFsYCWxCzk5hjTP4nUNh/hDmj08LJ6eHBVjQ9ScgwZGp1m67p7+OAdhxzx+6Jevd2vbkTKBI+RwLQdilvQ1y4K5X/6dbXiGLoAuKXyHqYNunGNVXWYs3+93xrRo3HYrrqBNs7B51p3OBLftFawT0bjdID9Nz8htWVBg1e4mviE048/Be/2rtmJcLhVfaofGZb4eMYoecW+4F6mX7b4HfPhditzuB9nueTJhJrojpIApJB12ORyH70yP625robwtU6qUB7iQCt6OMY2dgZ4NiEo83M4HPgLw33mIEbk/hlaWJe+Lg6x4yBOwgYbQXMf4o/LaCl3IZU2rHtPs0/WfFHcbE5SZwOfB4/5Eex967ip5Sfu0GDstuY9Orn0ffJHaunp19X4vJq/r3G3d1JNW73Be8S5HdmUHvaesrCpedwGVBncfjm4aL0veWoq+UXwjbgd9QfoHoWN9511VUfPtUwUu5glvIoQJWZXCDFWJhQ3CrP9f8z4rLa/rC1ueOghsdI9yud17kvCXJK7qmD479vHcRGNesdngcE7fq+VLjoqtzfp75SqrfqudHjRN5fT4/Xda8xpmfmLijefSLinvB/d2eJ5fbiDFMC0nzTZUJzGwi+oFxRPXzkdKPlCscMi6gY2O/n1XN8yjfLUr/Wfn1kDiwSH2T7uPirL84fl3nDC8zv4TNy3P5QMncx6w57HSc0E5h+6BZ9P0hgu9zRV8p/6w9PLj/rPHlS/72qfbFg8F1mdOnP+oHT376vfDuwQx2SLofDcvzzbccGu5+1Pae+OaxSzuC/0Thl7K0wxuMLM8Qj94NTVPjTLR94wzqKqjv1ywyjiXJm68xuWzL3z6u5IM+M6b58YryQ6x8ltRvwuz4nFv40uIOM+fXO4p/Wc9RYfuHpHF9mfmgsGH6FSPGuah8sMw8vUn5YNH5fFPi/6rz/rrFiXVZ76vST9eO3vs4l/27yyL3Y6vGrcs+at3medn7p6S4P+76uIyCC3uvtEr7DF5CSQN14/cTtp74xa/YEH5Hm7IuAuOGhJm4u8T+NmWd3XRcEaxmncTt56bYbV3jQopLcSkuxb2vfcfHYDIuSpk7ghKG/7NRWGZ83lPGIYufj4aj2CS7r1v+u2n5PsWtB25d4kuKS+Nuivv/4orgej9P81+KS3EpLsXdLNzfGR+nvr+QcvC9uGz/S4AnLE88BJN5QsoGprRrcfn9k6V1Bh/p2BrlyBx+JaOduZfVwAczkqcbwVNUeIrTeIiJmSCtftdy2RzBO0gQQ6t6tQ23tjSqlbztCN6w9+/X8trY4MxEVn/MeT6qicNXUPgK0/g6GNmOhQXuCfek1YZicyj6dg36yW4IX3C+s670yb07H1znXwBM+pXvb/88S8K3tZXN3AaT/+O6FYHLgUk/H/g1mM2v71/TfqTjurb/F2wyHOE='
    #     maybe_download_sbs()
    #     cpprefs.set_default_image_directory(
    #         os.path.join(example_images_directory(),"ExampleSBSImages"))
    #     fd = StringIO(zlib.decompress(base64.b64decode(data)))
    #     pipeline = cpp.Pipeline()
    #     pipeline.load(fd)
    #     module = pipeline.modules()[3]
    #     measurements = pipeline.run(image_set_end=1)
    #     for x in module.get_measurement_columns(pipeline):
    #         assert x[1] in measurements.get_feature_names(x[0]), '%s does not match any measurement output by pipeline'%(str(x))
    #     for obname in measurements.get_object_names():
    #         for m in measurements.get_feature_names(obname):
    #             if m.startswith(M.TEXTURE):
    #                 assert (obname, m, 'float') in module.get_measurement_columns(pipeline), 'no entry matching %s in get_measurement_columns.'%((obname, m, 'float'))

    def test_03_04_measurement_columns_with_and_without_gabor(self):
        workspace, module = self.make_workspace(np.zeros((10, 10)),
                                                np.zeros((10, 10), int))
        self.assertTrue(isinstance(module, M.MeasureTexture))
        module.wants_gabor.value = True
        columns = module.get_measurement_columns(None)
        ngabor = len(['x' for c in columns if c[1].find(M.F_GABOR) >= 0])
        self.assertEqual(ngabor, 2)
        module.wants_gabor.value = False
        columns = module.get_measurement_columns(None)
        ngabor = len(['x' for c in columns if c[1].find(M.F_GABOR) >= 0])
        self.assertEqual(ngabor, 0)

    def test_03_05_categories(self):
        workspace, module = self.make_workspace(np.zeros((10, 10)),
                                                np.zeros((10, 10), int))
        self.assertTrue(isinstance(module, M.MeasureTexture))
        for has_category, object_name in ((True, cpmeas.IMAGE),
                                          (True, INPUT_OBJECTS_NAME),
                                          (False, "Foo")):
            categories = module.get_categories(workspace.pipeline, object_name)
            if has_category:
                self.assertEqual(len(categories), 1)
                self.assertEqual(categories[0], M.TEXTURE)
            else:
                self.assertEqual(len(categories), 0)
        module.images_or_objects.value = M.IO_IMAGES
        categories = module.get_categories(workspace.pipeline, cpmeas.IMAGE)
        self.assertEqual(len(categories), 1)
        categories = module.get_categories(
                workspace.pipeline, INPUT_OBJECTS_NAME)
        self.assertEqual(len(categories), 0)
        module.images_or_objects.value = M.IO_OBJECTS
        categories = module.get_categories(workspace.pipeline, cpmeas.IMAGE)
        self.assertEqual(len(categories), 0)
        categories = module.get_categories(
                workspace.pipeline, INPUT_OBJECTS_NAME)
        self.assertEqual(len(categories), 1)

    def test_03_06_measuremements(self):
        workspace, module = self.make_workspace(np.zeros((10, 10)),
                                                np.zeros((10, 10), int))
        self.assertTrue(isinstance(module, M.MeasureTexture))
        for wants_gabor in (False, True):
            module.wants_gabor.value = wants_gabor
            for object_name in (cpmeas.IMAGE, INPUT_OBJECTS_NAME):
                features = module.get_measurements(workspace.pipeline,
                                                   object_name, M.TEXTURE)
                self.assertTrue(all([f in M.F_HARALICK + [M.F_GABOR]
                                     for f in features]))
                self.assertTrue(all([f in features for f in M.F_HARALICK]))
                if wants_gabor:
                    self.assertTrue(M.F_GABOR in features)
                else:
                    self.assertFalse(M.F_GABOR in features)

    def test_04_01_zeros(self):
        '''Make sure the module can run on an empty labels matrix'''
        workspace, module = self.make_workspace(np.zeros((10, 10)),
                                                np.zeros((10, 10), int))
        module.run(workspace)
        m = workspace.measurements
        self.assertTrue(isinstance(m, cpmeas.Measurements))
        for f in m.get_feature_names(INPUT_OBJECTS_NAME):
            if f.startswith(M.TEXTURE):
                values = m.get_current_measurement(INPUT_OBJECTS_NAME, f)
                self.assertEqual(len(values), 0)

    def test_04_02_wrong_size(self):
        '''Regression test for IMG-961: objects & image different size'''
        np.random.seed(42)
        image = np.random.uniform(size=(10, 30))
        labels = np.ones((20, 20), int)
        workspace, module = self.make_workspace(image, labels)
        module.run(workspace)
        m = workspace.measurements
        workspace, module = self.make_workspace(image[:, :20], labels[:10, :])
        module.run(workspace)
        me = workspace.measurements
        for f in m.get_feature_names(INPUT_OBJECTS_NAME):
            if f.startswith(M.TEXTURE):
                values = m.get_current_measurement(INPUT_OBJECTS_NAME, f)
                expected = me.get_current_measurement(INPUT_OBJECTS_NAME, f)
                self.assertEqual(values, expected)

    def test_04_03_mask(self):
        np.random.seed(42)
        image = np.random.uniform(size=(10, 30))
        mask = np.zeros(image.shape, bool)
        mask[:, :20] = True
        labels = np.ones((10, 30), int)
        workspace, module = self.make_workspace(image, labels, mask=mask)
        module.run(workspace)
        m = workspace.measurements
        workspace, module = self.make_workspace(image[:, :20], labels[:, :20])
        module.run(workspace)
        me = workspace.measurements
        for f in m.get_feature_names(INPUT_OBJECTS_NAME):
            if f.startswith(M.TEXTURE):
                values = m.get_current_measurement(INPUT_OBJECTS_NAME, f)
                expected = me.get_current_measurement(INPUT_OBJECTS_NAME, f)
                self.assertEqual(values, expected)

    def test_04_04_no_image_measurements(self):
        image = np.ones((10, 10)) * .5
        labels = np.ones((10, 10), int)
        workspace, module = self.make_workspace(image, labels)
        assert isinstance(module, M.MeasureTexture)
        module.images_or_objects.value = M.IO_OBJECTS
        module.scale_groups[0].scale.value = 2
        module.run(workspace)
        m = workspace.measurements
        self.assertFalse(
                m.has_feature(
                        cpmeas.IMAGE,
                        "Texture_AngularSecondMoment_%s_2_0" % INPUT_IMAGE_NAME))
        self.assertTrue(
                m.has_feature(
                        INPUT_OBJECTS_NAME,
                        "Texture_AngularSecondMoment_%s_2_0" % INPUT_IMAGE_NAME))

    def test_04_05_no_object_measurements(self):
        image = np.ones((10, 10)) * .5
        labels = np.ones((10, 10), int)
        workspace, module = self.make_workspace(image, labels)
        assert isinstance(module, M.MeasureTexture)
        module.images_or_objects.value = M.IO_IMAGES
        module.scale_groups[0].scale.value = 2
        module.run(workspace)
        m = workspace.measurements
        self.assertTrue(
                m.has_feature(
                        cpmeas.IMAGE,
                        "Texture_AngularSecondMoment_%s_2_0" % INPUT_IMAGE_NAME))
        self.assertFalse(
                m.has_feature(
                        INPUT_OBJECTS_NAME,
                        "Texture_AngularSecondMoment_%s_2_0" % INPUT_IMAGE_NAME))
