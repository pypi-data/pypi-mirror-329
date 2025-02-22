"""
A package to handle the depth processing-related calculations in both Pytorch and Numpy.
"""

from ._align_depth import align_shift_scale
from ._camera import CameraIntrinsics
from ._coord_sys import CoordSys, get_coord_sys_conv_mat
from ._datasets import Dataset, Nyuv2Dataset, Sample, SimplifiedHypersimDataset
from ._depth_clip import DepthClip
from ._depth_map_dilation import fast_dilate_depth_map
from ._losses import dx_loss, mse_log_loss, mse_loss
from ._point_cloud import (
    PointSubsamplingConf,
    depth_2_point_cloud,
    depths_2_matplotlib_fig,
    depths_2_plotly_fig,
)

__all__ = [
    "CameraIntrinsics",
    "CoordSys",
    "get_coord_sys_conv_mat",
    "depth_2_point_cloud",
    "depths_2_plotly_fig",
    "depths_2_matplotlib_fig",
    "mse_log_loss",
    "mse_loss",
    "dx_loss",
    "DepthClip",
    "Dataset",
    "Nyuv2Dataset",
    "SimplifiedHypersimDataset",
    "Sample",
    "fast_dilate_depth_map",
    "PointSubsamplingConf",
    "align_shift_scale",
]

__version__ = "0.2.1"
