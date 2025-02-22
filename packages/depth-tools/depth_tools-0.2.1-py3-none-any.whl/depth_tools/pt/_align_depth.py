from collections.abc import Collection
from typing import cast

import torch

from .._logging_internal import LOGGER


def align_shift_scale(
    *,
    pred_map: torch.Tensor,
    gt_map: torch.Tensor,
    mask: torch.Tensor,
    control_mask: torch.Tensor | None = None,
    verify_args: bool = False,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Align the predicted scalar map to a ground truth scalar map with a shift and scale to minimize the MSE loss. This is can be used for disparity maps or depth maps produced by depth estimators that only estimate relative depth or metric depth estimators, when some ground truth depth is available during inference time. Note that some authors apply further pre-processing.

    The function assumes without checking that ``control_mask`` only selects a subset of the pixels of ``mask``, regardless of ``verify_args``.

    This function is only differentiable for the predicted and ground truth scalar maps, it is not differentiable for the masks.

    Parameters
    ----------
    pred_map
        The predicted scalar map. Format: ``Im_Scalar``
    gt_map
        The ground truth scalar map. It should have the same width and height as the predicted scalar map. It should have the same dtype as the predicted map. Format: ``Im_Scalar``
    mask
        The mask that selects the valid pixels. It should have the same width and height as the predicted scalar map. Format: ``Im_Mask``.
    algorithm
        The algorithm to use.
    control_mask
        An optional mask that selects the pixels used to calculate the shift and scale. If not specified, then all valid pixels will be used. If defined, it should have the same width and height as the predicted scalar map. Format: ``Im_Mask``.

    Returns
    -------
    scaled_pred
        The scaled predictions. NaN if no pixel is selected to control the alignment.
    shift
        The shift applied. NaN if no pixel is selected to control the alignment.
    scale
        The scale applied. NaN if no pixel is selected to control the alignment.

    Raises
    ------
    ValueError
        If any of the checked parameter assumptions does not hold and ``verify_args=True``. Otherwise implementation detail.

    Notes
    -----
    This function intentionally implements only the bare bones of prediction alignment. We found that the fine details, not implemented by this function, are highly different between papers. For example, many papers (e.g. MiDAS papers) do the alignment in the disparity space. However, the depth -> disparity conversion is model-dependent.

    Developer notes
    ---------------
    The predicted and ground truth maps should have the same dtype, because `torch.linalg.lstsq` has a similar requirement. Contrary, the similar Numpy function supports different dtypes for the arguments. However, we decided not to support this for Numpy, because this makes the Pytorch and Numpy implementations of these two functions consistent. This decision might be revisited later.
    """
    if control_mask is None:
        control_mask = mask

    if verify_args:
        _verify_align_shift_and_scale_map_args(pred_map, gt_map, mask, control_mask)

    pred_values = pred_map[control_mask]
    gt_values = gt_map[control_mask]

    if len(pred_values) == 0:
        LOGGER.warning(
            f"The prediction aligment failed, because the control mask (or the mask) does not select any pixel. Returning with nan."
        )
        return (
            torch.full(pred_values.shape, torch.nan),
            torch.tensor(torch.nan),
            torch.tensor(torch.nan),
        )

    A = torch.stack([pred_values, torch.ones_like(pred_values)], dim=1)
    b = gt_values

    scale, shift = cast(Collection[torch.Tensor], torch.linalg.lstsq(A, b)[0])

    scaled_pred = pred_map.clone()
    scaled_pred[mask] = pred_map[mask] * scale + shift
    return scaled_pred, shift, scale


def _verify_align_shift_and_scale_map_args(
    pred_map: torch.Tensor,
    gt_map: torch.Tensor,
    mask: torch.Tensor,
    control_mask: torch.Tensor,
) -> None:
    """
    Check if the parameters of `align_shift_scale` are consistent with the assumptions.

    Parameters
    ----------
    pred_map
        The predicted scalar map. Format: ``Im_Scalar``
    gt_map
        The ground truth scalar map. It should have the same width and height as the predicted scalar map. It should have the same dtype as the predicted map. Format: ``Im_Scalar``
    mask
        The mask that selects the valid pixels. It should have the same width and height as the predicted scalar map. Format: ``Im_Mask``.
    algorithm
        The algorithm to use.
    control_mask
        An optional mask that selects the pixels used to calculate the shift and scale. If not specified, then all valid pixels will be used. If defined, it should have the same width and height as the predicted scalar map. Format: ``Im_Mask``.

    Raises
    ------
    ValueError
        If any of the checked parameter assumptions does not hold and ``verify_args=True``. Otherwise implementation detail.
    """

    if (len(pred_map.shape) != 3) or (pred_map.shape[0] != 1):
        raise ValueError(
            f"The array containing the predicted scalar map does not have format `Im_Scalar` its shape does not have format `(1, H, W)`. Shape: {pred_map.shape}"
        )
    if not torch.is_floating_point(pred_map):
        raise ValueError(
            f"The array containing the predicted scalar map does not have format `Im_Scalar` it does not have floating dtype. Dtype: {pred_map.dtype}"
        )
    if (len(gt_map.shape) != 3) or (gt_map.shape[0] != 1):
        raise ValueError(
            f"The array containing the ground truth scalar map does not have format `Im_Scalar` its shape does not have format `(1, H, W)`. Shape: {pred_map.shape}"
        )
    if not torch.is_floating_point(gt_map):
        raise ValueError(
            f"The array containing the ground truth scalar map does not have format `Im_Scalar` it does not have floating dtype. Dtype: {pred_map.dtype}"
        )
    if (len(mask.shape) != 3) or (mask.shape[0] != 1):
        raise ValueError(
            f"The array containing the ground truth mask does not have format `Im_Mask` its shape does not have format `(1, H, W)`. Shape: {pred_map.shape}"
        )
    if mask.dtype != torch.bool:
        raise ValueError(
            f"The array containing the mask does not have format `Im_Mask` it does not have boolean dtype. Dtype: {pred_map.dtype}"
        )
    if (len(control_mask.shape) != 3) or (control_mask.shape[0] != 1):
        raise ValueError(
            f"The array containing the ground truth control mask does not have format `Im_Mask` its shape does not have format `(1, H, W)`. Shape: {pred_map.shape}"
        )
    if control_mask.dtype != torch.bool:
        raise ValueError(
            f"The array containing the control mask does not have format `Im_Mask` it does not have boolean dtype. Dtype: {control_mask.dtype}"
        )
    if pred_map.dtype != gt_map.dtype:
        raise ValueError(
            f"The predicted and ground truth scalar maps should have the same dtype. Dtypes: predicted map: {pred_map.dtype}; ground truth map: {gt_map.dtype}"
        )

    all_other_maps = [gt_map, mask, control_mask]
    all_other_map_names = ["ground truth map", "mask", "control mask"]
    pred_width = pred_map.shape[2]
    pred_height = pred_map.shape[1]

    for other_map, other_map_name in zip(all_other_maps, all_other_map_names):
        if other_map.shape[2] != pred_width:
            raise ValueError(
                f"The width of the predicted scalar map is not equal to the width of the {other_map_name}. Shape of the {other_map_name}: {other_map.shape}; Shape of the predicted map: {pred_map.shape}"
            )
        if other_map.shape[1] != pred_height:
            raise ValueError(
                f"The height of the predicted scalar map is not equal to the width of the {other_map_name}. Shape of the {other_map_name}: {other_map.shape}; Shape of the predicted map: {pred_map.shape}"
            )
