import unittest

import numpy as np
import numpy.testing

import depth_tools

from .testutil import TestBase


class TestCamera(TestBase):
    def setUp(self):
        self.cam = depth_tools.CameraIntrinsics(c_x=2, c_y=3, f_x=4, f_y=5)

    def test_get_intrinsic_mat(self):
        mat = self.cam.get_intrinsic_mat()

        self.assertIssubdtype(mat.dtype, np.float32)

        self.assertEqual(mat.shape, (3, 3))

        self.assertAlmostEqual(mat[0, 0], self.cam.f_x)
        self.assertAlmostEqual(mat[0, 1], 0)
        self.assertAlmostEqual(mat[0, 2], self.cam.c_x)
        self.assertAlmostEqual(mat[1, 0], 0)
        self.assertAlmostEqual(mat[1, 1], self.cam.f_y)
        self.assertAlmostEqual(mat[1, 2], self.cam.c_y)
        self.assertAlmostEqual(mat[2, 0], 0)
        self.assertAlmostEqual(mat[2, 1], 0)
        self.assertAlmostEqual(mat[2, 2], 1)

    def test_get_intrinsic_mat_inv(self):
        mat = self.cam.get_intrinsic_mat()
        mat_inv = self.cam.get_intrinsic_mat_inv()

        expected_prod = np.eye(3, dtype=np.float32)

        self.assertAllclose(mat @ mat_inv, expected_prod)
