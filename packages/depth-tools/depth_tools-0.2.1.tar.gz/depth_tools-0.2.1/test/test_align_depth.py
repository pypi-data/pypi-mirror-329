import math

import npy_unittest
import numpy as np
import torch

import depth_tools
import depth_tools.pt


class TestAlignDepth(npy_unittest.NpyTestCase):
    def setUp(self):
        self.rng = np.random.default_rng(30)

        self.gt_map = self.rng.uniform(0.1, 25, (1, 120, 160))
        self.pred_map = self.gt_map * 2 + 10
        self.mask = self.rng.uniform(0, 1, self.gt_map.shape) > 0.5

        self.pred_map[~self.mask] = 0
        self.gt_map[~self.mask] = 0

        self.expected_shift = -5
        self.expected_scale = 0.5

    def test_align_shift_scale__happy_path__no_control_mask(self):
        with self.assertNoLogs():
            aligned_map, actual_shift, actual_scale = depth_tools.align_shift_scale(
                mask=self.mask,
                control_mask=None,
                gt_map=self.gt_map,
                pred_map=self.pred_map,
                verify_args=True,
            )

        self.assertAllclose(aligned_map, self.gt_map, atol=1e-4)
        self.assertAlmostEqual(actual_shift, self.expected_shift)
        self.assertAlmostEqual(actual_scale, self.expected_scale)

    def test_align_shift_scale__happy_path__no_control_mask_pt(self):
        with self.assertNoLogs():
            with torch.no_grad():
                aligned_map, actual_shift, actual_scale = (
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
                )
        aligned_map = aligned_map.numpy()
        actual_shift = actual_shift.item()
        actual_scale = actual_scale.item()

        self.assertAllclose(aligned_map, self.gt_map, atol=1e-4)
        self.assertAlmostEqual(actual_shift, self.expected_shift)
        self.assertAlmostEqual(actual_scale, self.expected_scale)

    def test_align_shift_scale__happy_path__control_mask(self):
        control_mask = (
            self.rng.uniform(0, 1, size=self.pred_map.shape) > 0.5
        ) & self.mask

        self.pred_map[(~control_mask) & self.mask] = 50000

        with self.assertNoLogs():
            aligned_map, actual_shift, actual_scale = depth_tools.align_shift_scale(
                mask=self.mask,
                control_mask=control_mask,
                gt_map=self.gt_map,
                pred_map=self.pred_map,
                verify_args=True,
            )

        self.assertAllclose(
            aligned_map[control_mask & self.mask],
            self.gt_map[control_mask & self.mask],
            atol=1e-4,
        )
        self.assertAlmostEqual(actual_shift, self.expected_shift)
        self.assertAlmostEqual(actual_scale, self.expected_scale)

    def test_align_shift_scale__happy_path__control_mask_pt(self):
        control_mask = (
            self.rng.uniform(0, 1, size=self.pred_map.shape) > 0.5
        ) & self.mask

        self.pred_map[(~control_mask) & self.mask] = 50000

        with self.assertNoLogs():
            with torch.no_grad():
                aligned_map, actual_shift, actual_scale = (
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=torch.from_numpy(control_mask),
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
                )
        aligned_map = aligned_map.numpy()
        actual_shift = actual_shift.item()
        actual_scale = actual_scale.item()

        self.assertAllclose(
            aligned_map[control_mask & self.mask],
            self.gt_map[control_mask & self.mask],
            atol=1e-4,
        )
        self.assertAlmostEqual(actual_shift, self.expected_shift)
        self.assertAlmostEqual(actual_scale, self.expected_scale)

    def test_align_shift_scale__invalid_shape(self):
        with self.subTest("invalid_pred_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask,
                        control_mask=None,
                        gt_map=self.gt_map,
                        pred_map=self.pred_map.flatten(),
                        verify_args=True,
                    )
        with self.subTest("invalid_gt_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask,
                        control_mask=None,
                        gt_map=self.gt_map.flatten(),
                        pred_map=self.pred_map,
                        verify_args=True,
                    )
        with self.subTest("invalid_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask.flatten(),
                        control_mask=None,
                        gt_map=self.gt_map,
                        pred_map=self.pred_map,
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask,
                        control_mask=self.mask.flatten(),
                        gt_map=self.gt_map,
                        pred_map=self.pred_map,
                        verify_args=True,
                    )

    def test_align_shift_scale__invalid_shape_pt(self):
        with self.subTest("invalid_pred_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map.flatten()),
                        verify_args=True,
                    )
        with self.subTest("invalid_gt_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map.flatten()),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask.flatten()),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=torch.from_numpy(self.mask.flatten()),
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )

    def test_align_shift_scale__invalid_dtype(self):
        with self.subTest("invalid_pred_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask,
                        control_mask=None,
                        gt_map=self.gt_map,
                        pred_map=self.pred_map.astype(np.complex128),
                        verify_args=True,
                    )
        with self.subTest("invalid_gt_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask,
                        control_mask=None,
                        gt_map=self.gt_map.astype(np.complex128),
                        pred_map=self.pred_map,
                        verify_args=True,
                    )
        with self.subTest("invalid_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask.astype(np.complex128),
                        control_mask=None,
                        gt_map=self.gt_map,
                        pred_map=self.pred_map,
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.align_shift_scale(
                        mask=self.mask,
                        control_mask=self.mask.astype(np.complex128),
                        gt_map=self.gt_map,
                        pred_map=self.pred_map,
                        verify_args=True,
                    )

    def test_align_shift_scale__invalid_dtype_pt(self):
        with self.subTest("invalid_pred_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map.astype(np.complex128)),
                        verify_args=True,
                    )
        with self.subTest("invalid_gt_map"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map.astype(np.complex128)),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask.astype(np.complex128)),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=torch.from_numpy(self.mask.astype(np.complex128)),
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )

    def test_align_shift_scale__inconsistent_shape(self):
        with self.subTest("invalid_gt_map_width"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.double_width(self.gt_map)),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_gt_map_height"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.double_height(self.gt_map)),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_mask_width"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.double_width(self.mask)),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_mask_height"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.double_height(self.mask)),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask_width"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=torch.from_numpy(self.double_width(self.mask)),
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask_height"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=torch.from_numpy(self.double_height(self.mask)),
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )

    def test_align_shift_scale__inconsistent_shape_pt(self):
        with self.subTest("invalid_gt_map_width"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.double_width(self.gt_map)),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_gt_map_height"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.double_height(self.gt_map)),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_mask_width"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.double_width(self.mask)),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_mask_height"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.double_height(self.mask)),
                        control_mask=None,
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask_width"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=torch.from_numpy(self.double_width(self.mask)),
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )
        with self.subTest("invalid_control_mask_height"):
            with self.assertNoLogs():
                with self.assertRaises(ValueError):
                    depth_tools.pt.align_shift_scale(
                        mask=torch.from_numpy(self.mask),
                        control_mask=torch.from_numpy(self.double_height(self.mask)),
                        gt_map=torch.from_numpy(self.gt_map),
                        pred_map=torch.from_numpy(self.pred_map),
                        verify_args=True,
                    )

    def test_align_shift_scale__inconsistent_dtype(self):
        with self.assertNoLogs():
            with self.assertRaises(ValueError):
                depth_tools.align_shift_scale(
                    control_mask=None,
                    gt_map=self.gt_map.astype(np.float64),
                    pred_map=self.pred_map.astype(np.float32),
                    mask=self.mask,
                    verify_args=True,
                )

    def test_align_shift_scale__inconsistent_dtype_pt(self):
        with self.assertNoLogs():
            with self.assertRaises(ValueError):
                depth_tools.pt.align_shift_scale(
                    control_mask=None,
                    gt_map=torch.from_numpy(self.gt_map.astype(np.float64)),
                    pred_map=torch.from_numpy(self.pred_map.astype(np.float32)),
                    mask=torch.from_numpy(self.mask),
                    verify_args=True,
                )

    def test_algin_shift_scale__no_pixel_selected(self):
        with self.assertLogs(level="WARNING"):
            aligned_depth, shift, scale = depth_tools.align_shift_scale(
                control_mask=np.full(self.gt_map.shape, False),
                gt_map=self.gt_map,
                pred_map=self.pred_map,
                mask=self.mask,
                verify_args=True,
            )

        expected_aligned_depth = np.full(
            aligned_depth.shape, np.nan, aligned_depth.dtype
        )

        self.assertArrayEqual(aligned_depth, expected_aligned_depth)
        self.assertTrue(math.isnan(shift))
        self.assertTrue(math.isnan(scale))

    def test_algin_shift_scale__no_pixel_selected_pt(self):
        with self.assertLogs(level="WARNING"):
            with torch.no_grad():
                aligned_depth, shift, scale = depth_tools.pt.align_shift_scale(
                    control_mask=torch.from_numpy(np.full(self.gt_map.shape, False)),
                    gt_map=torch.from_numpy(self.gt_map),
                    pred_map=torch.from_numpy(self.pred_map),
                    mask=torch.from_numpy(self.mask),
                    verify_args=True,
                )
        aligned_depth = aligned_depth.numpy()
        shift = shift.item()
        scale = scale.item()

        expected_aligned_depth = np.full(
            aligned_depth.shape, np.nan, aligned_depth.dtype
        )

        self.assertArrayEqual(aligned_depth, expected_aligned_depth)
        self.assertTrue(math.isnan(shift))
        self.assertTrue(math.isnan(scale))

    def double_width(self, im: np.ndarray) -> np.ndarray:
        return np.concatenate([im, im], axis=-1)

    def double_height(self, im: np.ndarray) -> np.ndarray:
        return np.concatenate([im, im], axis=-2)
