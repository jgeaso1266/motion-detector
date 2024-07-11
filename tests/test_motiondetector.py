from src.motion_detector import MotionDetector
from tests.fakecam import FakeCamera
from PIL import Image
from unittest.mock import MagicMock, patch
from viam.components.camera import Camera
from viam.services.vision import CaptureAllResult, Classification, Detection
from typing import List

import pytest
import cv2
import numpy as np

class TestMotionDetector:

    def getMD(self):
        md = MotionDetector("test")
        md.sensitivity = 0.9
        md.min_box_size = 1000
        md.cam_name = "test"
        md.camera = FakeCamera("test")
        return md

    def test_blah(self):
        x = "blah"
        assert "h" in x

    def test_classifications(self):
        img1 = Image.open("tests/img1.jpg")
        img2 = Image.open("tests/img2.jpg")
        gray1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(np.array(img2), cv2.COLOR_BGR2GRAY)

        md = self.getMD()
        classifications = md.classification_from_gray_imgs(gray1, gray2)
        assert len(classifications) == 1
        assert classifications[0]["class_name"] == "motion"
        

    def test_detections(self):
        img1 = Image.open("tests/img1.jpg")
        img2 = Image.open("tests/img2.jpg")
        gray1 = cv2.cvtColor(np.array(img1), cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(np.array(img2), cv2.COLOR_BGR2GRAY)

        md = self.getMD()
        detections = md.detections_from_gray_imgs(gray1, gray2)
        assert len(detections) > 0
        assert detections[0]["class_name"] == "motion"


    @pytest.mark.asyncio
    async def test_properties(self):
        md = self.getMD()
        props = await md.get_properties()
        assert props.classifications_supported == True
        assert props.detections_supported == True
        assert props.object_point_clouds_supported == False

    
    @pytest.mark.asyncio
    async def test_captureall(self):
        md = self.getMD()
        out = await md.capture_all_from_camera("test",return_image=True, 
                                                return_classifications=True,
                                                return_detections=True,
                                                return_object_point_clouds=True)
        assert isinstance(out, CaptureAllResult)
        print(out)
        assert out.image is not None 
        assert out.classifications is not None 
        assert len(out.classifications) == 1
        assert out.classifications[0]["class_name"] == "motion"
        assert out.detections is not None 
        assert out.detections[0]["class_name"] == "motion"
        assert out.objects is None 



