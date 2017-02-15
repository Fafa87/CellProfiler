import StringIO
import base64
import unittest
import zlib

import centrosome.filter
import centrosome.otsu
import centrosome.threshold
import numpy

import cellprofiler.image
import cellprofiler.measurement
import cellprofiler.module
import cellprofiler.modules.applythreshold
import cellprofiler.modules.identify
import cellprofiler.object
import cellprofiler.pipeline
import cellprofiler.preferences
import cellprofiler.thresholding
import cellprofiler.workspace

cellprofiler.preferences.set_headless()


INPUT_IMAGE_NAME = 'inputimage'
OUTPUT_IMAGE_NAME = 'outputimage'


class TestApplyThreshold(unittest.TestCase):
    def make_workspace(self, image, mask=None):
        '''Make a workspace for testing ApplyThreshold'''
        module = cellprofiler.modules.applythreshold.ApplyThreshold()
        module.image_name.value = INPUT_IMAGE_NAME
        module.thresholded_image_name.value = OUTPUT_IMAGE_NAME
        pipeline = cellprofiler.pipeline.Pipeline()
        object_set = cellprofiler.object.ObjectSet()
        image_set_list = cellprofiler.image.ImageSetList()
        image_set = image_set_list.get_image_set(0)
        workspace = cellprofiler.workspace.Workspace(pipeline,
                                                     module,
                                                     image_set,
                                                     object_set,
                                                     cellprofiler.measurement.Measurements(),
                                                     image_set_list)
        image_set.add(INPUT_IMAGE_NAME,
                      cellprofiler.image.Image(image) if mask is None
                      else cellprofiler.image.Image(image, mask))
        return workspace, module

    def test_01_00_write_a_test_for_the_new_variable_revision_please(self):
        self.assertEqual(cellprofiler.modules.applythreshold.ApplyThreshold.variable_revision_number, 8)

    def test_01_01_load_matlab(self):
        '''Load a matlab pipeline containing ApplyThreshold'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUX'
                'AuSk0sSU1RyM+zUggpTVXwKs1TMDBSMDSzMjK2MjRWMDIwsFQgGTAw'
                'evryMzAwPGZkYKiYczfM1/+Qg4Csl6NJm4K6r8WXF65TKg5KS/ioBC'
                'o4ePjs0SnRnD0l7zI/0z+m+knu/f90yhc67FYK2MfnY6y4eW7l52+l'
                'N8w4GVqLGyx++xpMT0gy1O/7Mec47xuLIxfeSJwoeLm23jhfsXvBtr'
                '5oj/KNvMaz103v1cvtO3NzbfiqXVbrFuyznxl59O32janhuy87vS/r'
                '5dl4T0FeosnMd/Vjxo2cpnuq+ONj5n5d2nfB/OQfdbvrikovDpR6/r'
                '5WWcf47OcnprtB+/5Mee5rU5I3r23FY43aJyVVMur7mdQVH3zYkSX4'
                'dqLn2dfvw66cbqyS9DoaVSn7L90pXs68Wmxb9Z7PMe21n6czfRVKKX'
                '79cn9HfacWW6nIdb6D9npArX2yLj13P3GsPXw48bc7k8XEwn+GX9tt'
                'H7bevf533k+b9Qd2C3yo8OGZytPxSilWsXbJWb/zBr9Fnm932n5ZUz'
                'poeXBivM01HZNN1h7H7eaU/nRhrgisSF4lE8S/cX9hN9PXysyfv8+s'
                'P77ts5kc19lF6yTl8i9WF/Ut33Dx8DO9Qpe63c8qdX7Ef/j/p+Pz7p'
                'd39gQsmVbLfsrKwpOx/bjr5Svuk/uFV62u/2//UfSPatlSfzPr9qIN'
                'kftnyOzzS7te/Uzr8Gs7xTufd8ZNst/q+7meke/SzmsA0OAP3A==')
        #
        # ApplyThreshold:
        # image_name = OrigBlue
        # thresholded_image_name = ThreshBlue
        # low_threshold = .1
        # high_threshold = .9
        # grayscale
        #
        fd = StringIO.StringIO(zlib.decompress(base64.b64decode(data)))
        pipeline = cellprofiler.pipeline.Pipeline()
        pipeline.load(fd)
        self.assertEqual(len(pipeline.modules()), 2)
        module = pipeline.modules()[1]
        self.assertTrue(isinstance(module, cellprofiler.modules.applythreshold.ApplyThreshold))
        self.assertEqual(module.image_name.value, "OrigBlue")
        self.assertEqual(module.thresholded_image_name.value, "ThreshBlue")
        self.assertEqual(module.threshold_scope.value, cellprofiler.modules.identify.TS_GLOBAL)
        self.assertEqual(module.global_operation.value, cellprofiler.modules.identify.TM_MANUAL)
        self.assertAlmostEqual(module.manual_threshold.value, .1)
        self.assertEqual(module.threshold_smoothing_scale, 0)

    def test_01_02_load_v2(self):
        '''Load a variable_revision_number = 2 pipeline'''
        data = ('eJztWOFP2kAUPxCNzGRzH8z8eB9lE9J2uihZVIRlYwMkylyM0e2AQ7'
                'pde6S9qmwx8eP+lP0Z+5P2J+wOW4ETaSkj7gMlTXmv7/feu1/fu16v'
                'mKkUMrtwPaXAYqaSbOgEwzJBrEEtIw1NtgqzFkYM1yE107DiYPjeMa'
                'GiQfVVWl1La2tQU5RNEO6I5IuP+aW8DMAcv87zM+remnXlSM8p5APM'
                'mG6e2bMgBpZd/W9+HiJLR1WCDxFxsN0N4enzZoNW2q3bW0VadwguIa'
                'PXmB8lx6hiy95reED3dlm/xORA/46lIXhm+/hct3VqunjXv6y9jUuZ'
                'FFfwABe6PEQkHgQvSz16Yf8OdO1jA3h72mO/6Mq6WdfP9bqDCNQNdH'
                'abhfCn+Pib6fM3A3KlTAe344NblPIQZwVfsuSbS1Rj0ECs1gziJy75'
                'EXKlaWG7KTIJPo5In58IeBmQz2XQH1/Iu7qJrDZcqRJU+waRWYcXTZ'
                '3hhPC34eNvVvIn5Hyh8LEYcBzRPnwUlOjD4Px4eyaNU8g53EAOYTAv'
                'ihDmdAvXGLXaoepQSSl3cHMSzjs8XNy9TpIvOc8j3m1hcOqA8U0yns'
                'enX/3Og/7nKuRsE5kmJlqQfl6Q8ELeY7YD3xJaRaSjH2deGn3c66Hm'
                'DxWEn485151jVXX/uPeD5BHr8xfjdWnicfK/9sF9kPIX8unKdvm1WD'
                'DgrdSLxGchfcKE7NOLreNMsnyS8DRZShzD3DpWkpsnP9RV7erG+IBP'
                'ljfKROhxcw5VgWv64Dak/IUscjjCyHITW7tKJIWqSE3WdHWaq8uhdl'
                'czzvMZo6/Ucea5HZ+4g96v2TajLYJso8fPpOZZuS61CccL0j+jxLv2'
                'ifcQ/TNK/g/ZP6Pk+Ss+2jp5Uv3ySOJDyJ1F9ZlFndbk4w9aV3fjQ7'
                '7Ux61/1T9T3BQ3xU37eIqbXB0M+h6i1a/8y7j7Qvkf857W7xQ3DCeU'
                '963X5P0VYf8FDK+356C/3oRc40vklkXF/rWVMjqbrHaKUFS/2eVMFf'
                'jffM+GZ5D1ribF0e6Lg1ot0madnUhK6qmMECueOJi/+IB4vTxE+W/p'
                'yXDeZb67z+HPdph40ejdeAs+uJjLnMD9BKM955Uh9t7Ywtr/BcBDTrI=')
        #
        # image_name = DNA
        # thresholded_image_name = ThreshDNA
        # Binary image
        # Otsu global thresholding
        # lower & upper bounds = 0, 1
        # Threshold correction factor = 1
        fd = StringIO.StringIO(zlib.decompress(base64.b64decode(data)))
        pipeline = cellprofiler.pipeline.Pipeline()
        pipeline.load(fd)
        self.assertEqual(len(pipeline.modules()), 2)
        module = pipeline.modules()[1]
        self.assertTrue(isinstance(module, cellprofiler.modules.applythreshold.ApplyThreshold))
        self.assertEqual(module.image_name.value, "DNA")
        self.assertEqual(module.thresholded_image_name.value, "ThreshDNA")
        self.assertEqual(module.threshold_scope.value, cellprofiler.modules.identify.TS_GLOBAL)
        self.assertEqual(module.global_operation.value, centrosome.threshold.TM_OTSU)
        self.assertEqual(module.threshold_range.min, 0)
        self.assertEqual(module.threshold_range.max, 1)
        self.assertEqual(module.threshold_correction_factor.value, 1)

    def test_01_03_load_v3(self):
        #
        # image_name = DNA
        # thresholded_image_name = ThreshBlue
        # Binary image
        # Otsu global thresholding / 3 classes / entropy / background
        #
        data = ('eJztWG9PEzEY78ZQkKhIYuRlX27KltspCSwG2BiR6TYWmCghqN2uY6'
                'ddu9z1gGlIfOnH8iP5EWzHHbeVwY2DaUjWpbk9T5/f86+99rmWstVi'
                'NgcXUxosZavJhkkwrBDEG8xqZSDlC3DdwohjAzKagSVG4VuHQm0Jpv'
                'WMvpjR0lDXtGUQrkUKpUfiEX8KwD3xnBI96g5NunSkp0t6B3Nu0kN7'
                'EsTAvMv/LfouskxUI3gXEQfbvgmPX6ANVu20z4dKzHAILqNWr7BoZa'
                'dVw5a91fCA7nDFPMFkx/yOlRA8sW18ZNomoy7e1a9yz+0yrtiVefg4'
                '7echouRB5mWuhy/lN4EvHxuQtyc98rMubVLDPDINBxFottDhuRdSnx'
                'agb6JP3wTIl7Nd3FoAblbxQ/YqPuHJjRNU57CFeL05jJ4Hih5JV5sW'
                'tps5MenDxxHp0xMBL4fM5zzoty/pnEmR1YHxGkH1bxBRAx43TY4TUt'
                '9SgL5JRZ+kC8Xi+9KQcUT78FFQZv8HF5S3Z0qcks7jBnIIhwW5CGHe'
                'tHCdM6sTah1qKe0C7p6C85qHm3afo8yX6ueeeNvC4NID4hulPS+fQe'
                't3CvTPq6TXm4hSTPRh3ucZBS/pLW478A1hNUS6/JvsS9ePezHU/pEG'
                '4fdjketuW0i7f9zxYfyI9emLiXVJ8U3W188A3DvFf0l/iq9WXsuCAa'
                '+kXiQ+S+oDJmSbHa/sZ5OVg4THWWfEadGVfS25fPAjvaCfngnviM3y'
                'jJkIHbfIYVrimgG4JcV/SUsf9jCyXMdenSaSkiUKHd50ebrLy6OOz7'
                'mt+bnOPrUWYO+hEp+k5fmIYZ0g2+6e9TexH7Qf3FfsS3qDcou1L+7r'
                'txn3oLogJ47jQ4s51PD1bE5dr776l/52izHpcHv09gfVY759KEpE3L'
                '6t83SMG+PGuPF7PMaNbh0MqqNZ7av4ovIPlLsU713BSeZl9YT63Sjl'
                'v4Cr5/E56J9HSddF6dy2mLyXs1Kt7uWRnSIMGWe3N6mi+FvoucgZpg'
                '7WFTv6ZXZQu006vHvDwoiRykqy6pGD8zc9wF5vHqLi93ju6ryr+fbn'
                '4c9qGHvRiYv2ZgJwMTdzEvcLXG+e41fIe7GFlf8LJ2oenw==')
        fd = StringIO.StringIO(zlib.decompress(base64.b64decode(data)))
        pipeline = cellprofiler.pipeline.Pipeline()
        pipeline.load(fd)
        self.assertEqual(len(pipeline.modules()), 2)
        module = pipeline.modules()[1]
        self.assertTrue(isinstance(module, cellprofiler.modules.applythreshold.ApplyThreshold))
        self.assertEqual(module.image_name.value, "DNA")
        self.assertEqual(module.thresholded_image_name.value, "ThreshBlue")
        self.assertEqual(module.threshold_scope.value, cellprofiler.modules.identify.TS_GLOBAL)
        self.assertEqual(module.global_operation.value, centrosome.threshold.TM_OTSU)
        self.assertEqual(module.threshold_range.min, 0)
        self.assertEqual(module.threshold_range.max, 1)
        self.assertEqual(module.threshold_correction_factor.value, 1)
        self.assertEqual(module.two_class_otsu.value, cellprofiler.modules.identify.O_THREE_CLASS)
        self.assertEqual(module.assign_middle_to_foreground.value, cellprofiler.modules.identify.O_BACKGROUND)

    def test_01_07_load_v7(self):
        data = r"""CellProfiler Pipeline: http://www.cellprofiler.org
        Version:3
        DateRevision:20130226215424
        ModuleCount:5
        HasImagePlaneDetails:False

        Images:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:1|show_window:False|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True]
            :
            Filter based on rules:No
            Filter:or (file does contain "")

        Metadata:[module_num:2|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True]
            Extract metadata?:Yes
            Extraction method count:1
            Extraction method:Manual
            Source:From file name
            Regular expression:Channel(?P<Wavelength>\x5B12\x5D)-\x5B0-9\x5D{2}-(?P<WellRow>\x5BA-Z\x5D)-(?P<WellColumn>\x5B0-9\x5D{2}).tif
            Regular expression:(?P<Date>\x5B0-9\x5D{4}_\x5B0-9\x5D{2}_\x5B0-9\x5D{2})$
            Filter images:All images
            :or (file does contain "")
            Metadata file location\x3A:
            Match file and image metadata:\x5B\x5D
            Case insensitive matching:No

        NamesAndTypes:[module_num:3|svn_version:\'Unknown\'|variable_revision_number:1|show_window:False|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True]
            Assignment method:Assign images matching rules
            Load as:Grayscale image
            Image name:DNA
            :\x5B\x5D
            Assign channels by:Order
            Assignments count:2
            Match this rule:or (metadata does Wavelength "1")
            Image name:GFP
            Objects name:Cell
            Load as:Grayscale image
            Match this rule:or (metadata does Wavelength "2")
            Image name:DNA
            Objects name:Nucleus
            Load as:Grayscale image

        Groups:[module_num:4|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True]
            Do you want to group your images?:No
            grouping metadata count:1
            Metadata category:None

        ApplyThreshold:[module_num:5|svn_version:\'Unknown\'|variable_revision_number:7|show_window:True|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True]
            Select the input image:RainbowPony
            Name the output image:GrayscalePony
            Select the output image type:Grayscale
            Set pixels below or above the threshold to zero?:Below threshold
            Subtract the threshold value from the remaining pixel intensities?:Yes
            Number of pixels by which to expand the thresholding around those excluded bright pixels:2.0
            Threshold setting version:1
            Threshold strategy:Adaptive
            Threshold method:MCT
            Smoothing for threshold:Automatic
            Threshold smoothing scale:1.5
            Threshold correction factor:1.1
            Lower and upper bounds on threshold:0.07,0.99
            Approximate fraction of image covered by objects?:0.02
            Manual threshold:0.1
            Select the measurement to threshold with:Pony_Perimeter
            Select binary image:Pony_yes_or_no
            Masking objects:PonyMask
            Two-class or three-class thresholding?:Two classes
            Minimize the weighted variance or the entropy?:Weighted variance
            Assign pixels in the middle intensity class to the foreground or the background?:Foreground
            Method to calculate adaptive window size:Image size
            Size of adaptive window:13
"""
        fd = StringIO.StringIO(data)
        pipeline = cellprofiler.pipeline.Pipeline()
        pipeline.loadtxt(fd)
        module = pipeline.modules()[-1]
        self.assertTrue(isinstance(module, cellprofiler.modules.applythreshold.ApplyThreshold))
        self.assertEqual(module.image_name, "RainbowPony")
        self.assertEqual(module.thresholded_image_name, "GrayscalePony")
        self.assertEqual(module.threshold_scope, cellprofiler.modules.identify.TS_GLOBAL)
        self.assertEqual(module.global_operation.value, cellprofiler.modules.identify.TM_MXE)
        self.assertEqual(module.threshold_smoothing_scale, 1.3488)
        self.assertEqual(module.threshold_correction_factor, 1.1)
        self.assertEqual(module.threshold_range.min, .07)
        self.assertEqual(module.threshold_range.max, .99)
        self.assertEqual(module.manual_threshold, 0.1)
        self.assertEqual(module.thresholding_measurement, "Pony_Perimeter")
        self.assertEqual(module.two_class_otsu, cellprofiler.modules.identify.O_TWO_CLASS)
        self.assertEqual(module.assign_middle_to_foreground, cellprofiler.modules.identify.O_FOREGROUND)
        self.assertEqual(module.adaptive_window_size, 13)

    def test_01_08_load_v8(self):
        data = r"""CellProfiler Pipeline: http://www.cellprofiler.org
Version:3
DateRevision:300
GitHash:
ModuleCount:5
HasImagePlaneDetails:False

Images:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'To begin creating your project, use the Images module to compile a list of files and/or folders that you want to analyze. You can also specify a set of rules to include only the desired files in your selected folders.\'\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    :
    Filter images?:Images only
    Select the rule criteria:and (extension does isimage) (directory doesnot containregexp "\x5B\\\\\\\\\\\\\\\\/\x5D\\\\\\\\.")

Metadata:[module_num:2|svn_version:\'Unknown\'|variable_revision_number:4|show_window:False|notes:\x5B\'The Metadata module optionally allows you to extract information describing your images (i.e, metadata) which will be stored along with your measurements. This information can be contained in the file name and/or location, or in an external file.\'\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    Extract metadata?:No
    Metadata data type:Text
    Metadata types:{}
    Extraction method count:1
    Metadata extraction method:Extract from file/folder names
    Metadata source:File name
    Regular expression:^(?P<Plate>.*)_(?P<Well>\x5BA-P\x5D\x5B0-9\x5D{2})_s(?P<Site>\x5B0-9\x5D)_w(?P<ChannelNumber>\x5B0-9\x5D)
    Regular expression:(?P<Date>\x5B0-9\x5D{4}_\x5B0-9\x5D{2}_\x5B0-9\x5D{2})$
    Extract metadata from:All images
    Select the filtering criteria:and (file does contain "")
    Metadata file location:
    Match file and image metadata:\x5B\x5D
    Use case insensitive matching?:No

NamesAndTypes:[module_num:3|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\'The NamesAndTypes module allows you to assign a meaningful name to each image by which other modules will refer to it.\'\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    Assign a name to:All images
    Select the image type:Grayscale image
    Name to assign these images:DNA
    Match metadata:\x5B\x5D
    Image set matching method:Order
    Set intensity range from:Image metadata
    Assignments count:1
    Single images count:0
    Maximum intensity:255.0
    Volumetric:No
    x:1.0
    y:1.0
    z:1.0
    Select the rule criteria:and (file does contain "")
    Name to assign these images:DNA
    Name to assign these objects:Cell
    Select the image type:Grayscale image
    Set intensity range from:Image metadata
    Retain outlines of loaded objects?:No
    Name the outline image:LoadedOutlines
    Maximum intensity:255.0

Groups:[module_num:4|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'The Groups module optionally allows you to split your list of images into image subsets (groups) which will be processed independently of each other. Examples of groupings include screening batches, microtiter plates, time-lapse movies, etc.\'\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    Do you want to group your images?:No
    grouping metadata count:1
    Metadata category:None

ApplyThreshold:[module_num:5|svn_version:\'Unknown\'|variable_revision_number:8|show_window:True|notes:\x5B\x5D|batch_state:array(\x5B\x5D, dtype=uint8)|enabled:True|wants_pause:False]
    Select the input image:DNA
    Name the output image:ThreshBlue
    Threshold setting version:3
    Threshold strategy:Global
    Thresholding method:MCT
    Threshold smoothing scale:0
    Threshold correction factor:1.0
    Lower and upper bounds on threshold:0.0,1.0
    Manual threshold:0.0
    Select the measurement to threshold with:None
    Two-class or three-class thresholding?:Two classes
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Size of adaptive window:50
    Use default parameters?:Default
    Lower outlier fraction:0.05
    Upper outlier fraction:0.05
    Averaging method:Mean
    Variance method:Standard deviation
    # of deviations:2.0
        """

        fd = StringIO.StringIO(data)
        pipeline = cellprofiler.pipeline.Pipeline()
        pipeline.loadtxt(fd)
        module = pipeline.modules()[-1]
        self.assertTrue(isinstance(module, cellprofiler.modules.applythreshold.ApplyThreshold))
        self.assertEqual(module.image_name, "DNA")
        self.assertEqual(module.thresholded_image_name, "ThreshBlue")
        self.assertEqual(module.threshold_scope, cellprofiler.modules.identify.TS_GLOBAL)
        self.assertEqual(module.global_operation.value, cellprofiler.modules.identify.TM_MXE)
        self.assertEqual(module.threshold_smoothing_scale, 0)
        self.assertEqual(module.threshold_correction_factor, 1.0)
        self.assertEqual(module.threshold_range.min, 0.0)
        self.assertEqual(module.threshold_range.max, 1.0)
        self.assertEqual(module.manual_threshold, 0.0)
        self.assertEqual(module.thresholding_measurement, "None")
        self.assertEqual(module.two_class_otsu, cellprofiler.modules.identify.O_TWO_CLASS)
        self.assertEqual(module.assign_middle_to_foreground, cellprofiler.modules.identify.O_FOREGROUND)
        self.assertEqual(module.adaptive_window_size, 50)

    def test_04_01_binary_manual(self):
        '''Test a binary threshold with manual threshold value'''
        numpy.random.seed(0)
        image = numpy.random.uniform(size=(20, 20))
        expected = image > .5
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = cellprofiler.modules.identify.TM_MANUAL
        module.manual_threshold.value = .5
        module.run(workspace)
        output = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(numpy.all(output.pixel_data == expected))

    def test_04_02_binary_global(self):
        '''Test a binary threshold with Otsu global method'''
        numpy.random.seed(0)
        image = numpy.random.uniform(size=(20, 20))
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = centrosome.threshold.TM_OTSU
        module.run(workspace)
        threshold = cellprofiler.thresholding.otsu(cellprofiler.image.Image(image))
        expected = image > threshold
        output = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(numpy.all(output.pixel_data == expected))

    def test_04_03_binary_correction(self):
        '''Test a binary threshold with a correction factor'''
        numpy.random.seed(0)
        image = numpy.random.uniform(size=(20, 20))
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = centrosome.threshold.TM_OTSU
        module.threshold_correction_factor.value = .5
        module.run(workspace)
        threshold = cellprofiler.thresholding.otsu(cellprofiler.image.Image(image)) * 0.5
        expected = image > threshold
        output = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(numpy.all(output.pixel_data == expected))

    def test_04_04_low_bounds(self):
        '''Test a binary threshold with a low bound'''

        numpy.random.seed(0)
        image = numpy.random.uniform(size=(20, 20))
        image[(image > .4) & (image < .6)] = .5
        expected = image > .7
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = centrosome.threshold.TM_OTSU
        module.threshold_range.min = .7
        module.run(workspace)
        output = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(numpy.all(output.pixel_data == expected))

    def test_04_05_high_bounds(self):
        '''Test a binary threshold with a high bound'''

        numpy.random.seed(0)
        image = numpy.random.uniform(size=(40, 40))
        expected = image > .1
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = centrosome.threshold.TM_OTSU
        module.threshold_range.max = .1
        module.run(workspace)
        output = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(numpy.all(output.pixel_data == expected))

    def test_04_07_threshold_from_measurement(self):
        '''Test a binary threshold from previous measurements'''
        numpy.random.seed(0)
        image = numpy.random.uniform(size=(20, 20))
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = cellprofiler.modules.identify.TM_MANUAL
        module.manual_threshold.value = .5
        module.run(workspace)

        module2 = cellprofiler.modules.applythreshold.ApplyThreshold()
        module2.image_name.value = OUTPUT_IMAGE_NAME
        module2.thresholded_image_name.value = OUTPUT_IMAGE_NAME + 'new'
        module2.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module2.global_operation.value = cellprofiler.modules.identify.TM_MEASUREMENT
        module2.thresholding_measurement.value = 'Threshold_FinalThreshold_' + OUTPUT_IMAGE_NAME
        module2.run(workspace)

    def test_05_01_otsu_wv(self):
        '''Test the weighted variance version of Otsu'''
        numpy.random.seed(0)
        image = numpy.hstack((numpy.random.exponential(1.5, size=600),
                              numpy.random.poisson(15, size=300)))
        image.shape = (30, 30)
        image = centrosome.filter.stretch(image)
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = centrosome.threshold.TM_OTSU
        module.two_class_otsu.value = cellprofiler.modules.identify.O_TWO_CLASS
        module.run(workspace)
        threshold, _ = module.get_otsu_threshold(cellprofiler.image.Image(image))
        expected = image > threshold
        output = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(numpy.all(output.pixel_data == expected))

    def test_05_03_otsu3_wv_low(self):
        '''Test the three-class otsu, weighted variance middle = background'''
        numpy.random.seed(0)
        image = numpy.hstack((numpy.random.exponential(1.5, size=300),
                              numpy.random.poisson(15, size=300),
                              numpy.random.poisson(30, size=300))).astype(numpy.float32)
        image.shape = (30, 30)
        image = centrosome.filter.stretch(image)
        _, threshold = cellprofiler.thresholding.otsu3(cellprofiler.image.Image(image))
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = centrosome.threshold.TM_OTSU
        module.two_class_otsu.value = cellprofiler.modules.identify.O_THREE_CLASS
        module.assign_middle_to_foreground.value = cellprofiler.modules.identify.O_BACKGROUND
        module.run(workspace)
        m = workspace.measurements
        m_threshold = m[cellprofiler.measurement.IMAGE, cellprofiler.modules.identify.FF_ORIG_THRESHOLD % module.get_measurement_objects_name()]
        self.assertAlmostEqual(m_threshold, threshold)

    def test_05_04_otsu3_foreground(self):
        '''Test the three-class otsu, assign middle to foreground'''
        numpy.random.seed(0)
        image = numpy.hstack((numpy.random.exponential(1.5, size=300),
                              numpy.random.poisson(15, size=300),
                              numpy.random.poisson(30, size=300)))
        image.shape = (30, 30)
        image = centrosome.filter.stretch(image)
        threshold, _ = cellprofiler.thresholding.otsu3(cellprofiler.image.Image(image))
        workspace, module = self.make_workspace(image)
        module.threshold_scope.value = cellprofiler.modules.identify.TS_GLOBAL
        module.global_operation.value = centrosome.threshold.TM_OTSU
        module.two_class_otsu.value = cellprofiler.modules.identify.O_THREE_CLASS
        module.assign_middle_to_foreground.value = cellprofiler.modules.identify.O_FOREGROUND
        module.run(workspace)
        m = workspace.measurements
        m_threshold = m[cellprofiler.measurement.IMAGE, cellprofiler.modules.identify.FF_ORIG_THRESHOLD % module.get_measurement_objects_name()]
        self.assertAlmostEqual(m_threshold, threshold)

    def test_volume(self):
        numpy.random.seed(73)

        data = numpy.random.rand(64, 256, 256)

        image = cellprofiler.image.Image(data, dimensions=3)

        image_set_list = cellprofiler.image.ImageSetList()

        image_set = image_set_list.get_image_set(0)

        image_set.add(INPUT_IMAGE_NAME, image)

        module = cellprofiler.modules.applythreshold.ApplyThreshold()

        module.image_name.value = INPUT_IMAGE_NAME

        module.thresholded_image_name.value = OUTPUT_IMAGE_NAME

        workspace = cellprofiler.workspace.Workspace(
            cellprofiler.pipeline.Pipeline(),
            module,
            image_set,
            cellprofiler.object.ObjectSet(),
            cellprofiler.measurement.Measurements(),
            image_set_list
        )

        module.run(workspace)

        output_image = image_set.get_image(OUTPUT_IMAGE_NAME)

        assert output_image.dimensions == 3
