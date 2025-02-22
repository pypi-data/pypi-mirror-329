import depth_tools
import depth_tools.pt
import numpy as np
import torch

from .testutil import TestBase


class TestLosses(TestBase):
    def setUp(self):
        self.gt = np.array(
            [
                [
                    [
                        [1.0, 1.0],
                        [2.0, 2.0],
                        [3.0, 1.0],
                    ]
                ],
                [
                    [
                        [1.0, 1.0],
                        [1.0, 1.0],
                        [2.0, 1.0],
                    ]
                ],
                [
                    [
                        [1.0, 3.0],
                        [1.0, 2.0],
                        [3.0, 1.0],
                    ]
                ],
                [
                    [
                        [2.0, 1.0],
                        [1.0, 1.0],
                        [2.0, 3.0],
                    ]
                ],
            ],
            dtype=np.float32,
        )

        self.pred = np.array(
            [
                [
                    [
                        [1.0, 1.0],
                        [2.0, 2.0],
                        [2.0, 1.0],
                    ]
                ],
                [
                    [
                        [3.0, 1.0],
                        [3.0, 1.0],
                        [2.0, 1.0],
                    ]
                ],
                [
                    [
                        [2.0, 3.0],
                        [3.0, 2.0],
                        [2.0, 1.0],
                    ]
                ],
                [
                    [
                        [1.0, 1.0],
                        [2.0, 1.0],
                        [3.0, 3.0],
                    ]
                ],
            ],
            dtype=np.float32,
        )

        self.mask = np.array(
            [
                [
                    [
                        [True, False],
                        [False, True],
                        [True, True],
                    ]
                ],
                [
                    [
                        [True, True],
                        [False, True],
                        [True, False],
                    ]
                ],
                [
                    [
                        [True, False],
                        [True, True],
                        [False, False],
                    ]
                ],
                [
                    [
                        [False, False],
                        [False, False],
                        [True, True],
                    ]
                ],
            ]
        )

        self.expected_mse_losses = np.array(
            [1 / 4, 4 / 4, 5 / 3, 1 / 2], dtype=np.float32
        )
        self.expected_mse_log_losses = np.array(
            [0.16440196 / 4, 1.206949 / 4, (0.480453 + 1.206949) / 3, 0.16440196 / 2],
            dtype=np.float32,
        )

        self.expected_d001_losses = np.array(
            [3 / 4, 3 / 4, 1 / 3, 1 / 2], dtype=np.float32
        )  # d_(0.01)
        self.expected_d100_losses = np.array([1, 1, 1, 1], dtype=np.float32)  # d_100

    def test_dx_loss__np__happy_path(self) -> None:
        actual_d001_losses = depth_tools.dx_loss(
            pred=self.pred, gt=self.gt, mask=self.mask, x=0.01
        )
        actual_d100_losses = depth_tools.dx_loss(
            pred=self.pred, gt=self.gt, mask=self.mask, x=100
        )
        self.assertAllclose(actual_d001_losses, self.expected_d001_losses)
        self.assertAllclose(actual_d100_losses, self.expected_d100_losses)

    def test_dx_loss__pt__happy_path(self) -> None:
        with torch.no_grad():
            actual_d001_losses = depth_tools.pt.dx_loss(
                pred=torch.from_numpy(self.pred),
                gt=torch.from_numpy(self.gt),
                mask=torch.from_numpy(self.mask),
                x=0.01,
            ).numpy()
            actual_d100_losses = depth_tools.pt.dx_loss(
                pred=torch.from_numpy(self.pred),
                gt=torch.from_numpy(self.gt),
                mask=torch.from_numpy(self.mask),
                x=100,
            ).numpy()

        self.assertAllclose(actual_d001_losses, self.expected_d001_losses)
        self.assertAllclose(actual_d100_losses, self.expected_d100_losses)

    def test_dx_loss__np__invalid_arrays(self):
        def fn(pred, gt, mask):
            depth_tools.dx_loss(pred=pred, gt=gt, mask=mask, verify_args=True, x=0.7)

        self.probe_invalid_inputs([self.pred, self.gt, self.mask], fn)

    def test_dx_loss__pt__invalid_arrays(self):
        def fn(pred, gt, mask):
            depth_tools.pt.dx_loss(
                pred=torch.from_numpy(pred),
                gt=torch.from_numpy(gt),
                mask=torch.from_numpy(mask),
                verify_args=True,
                x=0.7,
            )

        self.probe_invalid_inputs([self.pred, self.gt, self.mask], fn)

    def test_mse_loss__np__happy_path(self):
        actual_mse_losses = depth_tools.mse_loss(
            pred=self.pred, gt=self.gt, mask=self.mask
        )
        self.assertAllclose(actual_mse_losses, self.expected_mse_losses)

    def test_mse_loss__pt__happy_path(self):
        with torch.no_grad():
            actual_mse_losses = depth_tools.pt.mse_loss(
                pred=torch.from_numpy(self.pred),
                gt=torch.from_numpy(self.gt),
                mask=torch.from_numpy(self.mask),
            ).numpy()
        self.assertAllclose(actual_mse_losses, self.expected_mse_losses)

    def test_mse_loss__np__invalid_arrays(self):
        def fn(pred, gt, mask):
            depth_tools.mse_loss(pred=pred, gt=gt, mask=mask, verify_args=True)

        self.probe_invalid_inputs([self.pred, self.gt, self.mask], fn)

    def test_mse_loss__pt__invalid_arrays(self):
        def fn(pred, gt, mask):
            with torch.no_grad():
                depth_tools.pt.mse_loss(
                    pred=torch.from_numpy(pred),
                    gt=torch.from_numpy(gt),
                    mask=torch.from_numpy(mask),
                    verify_args=True,
                )

        self.probe_invalid_inputs([self.pred, self.gt, self.mask], fn)

    def test_mse_log_loss__np__happy_path(self):
        actual_mse_log_losses = depth_tools.mse_log_loss(
            pred=self.pred, gt=self.gt, mask=self.mask
        )
        self.assertAllclose(actual_mse_log_losses, self.expected_mse_log_losses)

    def test_mse_log_loss__pt__happy_path(self):
        with torch.no_grad():
            actual_mse_log_losses = depth_tools.pt.mse_log_loss(
                pred=torch.from_numpy(self.pred),
                gt=torch.from_numpy(self.gt),
                mask=torch.from_numpy(self.mask),
            ).numpy()
        self.assertAllclose(actual_mse_log_losses, self.expected_mse_log_losses)

    def test_mse_log_loss__np__invalid_arrays(self):
        def fn(pred, gt, mask):
            depth_tools.mse_log_loss(pred=pred, gt=gt, mask=mask, verify_args=True)

        self.probe_invalid_inputs([self.pred, self.gt, self.mask], fn)

    def test_mse_log_loss__pt__invalid_arrays(self):
        def fn(pred, gt, mask):
            with torch.no_grad():
                depth_tools.pt.mse_log_loss(
                    pred=torch.from_numpy(pred),
                    gt=torch.from_numpy(gt),
                    mask=torch.from_numpy(mask),
                    verify_args=True,
                )

        self.probe_invalid_inputs([self.pred, self.gt, self.mask], fn)
