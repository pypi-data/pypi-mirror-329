import numpy as np


def dx_loss(
    *,
    pred: np.ndarray,
    gt: np.ndarray,
    mask: np.ndarray,
    x: float,
    verify_args: bool = False,
) -> np.ndarray:
    """
    Calculate the non-differentiable $\\delta_x$ loss. Unlike the similar Pytorch function, this function does not do any aggregation.

    This function expects the arguments to have the same shape, so broadcast is not necessary.

    This function does not do any additional reductions.

    Parameters
    ----------
    pred
        The predicted values. Format: ``Ims_Scalar`` or ``Im_Scalar``
    gt
        The ground truth values. Format: ``Ims_Scalars`` or ``Im_Scalar``
    mask
        The masks that select the relevant pixels. Format: ``Ims_Mask`` or ``Ims_FloatMask``
    x
        The ``x`` parameter of the loss.
    verify_args
        If this is true, then the function verifies the arguments and raises errors if the shapes or data types are incorrect. Otherwise the possible errors are treated as implementation detail.

    Return
    ------
    v
        The final losses. Format: ``Scalars``
    """
    if verify_args:
        _verify_loss_args(gt=gt, pred=pred, mask=mask)

    deltas = np.zeros_like(pred)
    deltas[mask] = np.maximum(pred[mask] / gt[mask], gt[mask] / pred[mask])

    loss_vals: np.ndarray = deltas < (1.25**x)
    loss_vals[~mask] = False

    loss_vals = np.sum(loss_vals, axis=(-2, -1)) / np.sum(mask, axis=(-2, -1))
    loss_vals = np.squeeze(loss_vals, axis=-1)
    return loss_vals


def mse_loss(
    *,
    pred: np.ndarray,
    gt: np.ndarray,
    mask: np.ndarray,
    verify_args: bool = False,
) -> np.ndarray:
    """
    Calculate the masked MSE loss. Unlike the similar Pytorch function, this function does not do any aggregation.

    This function expects the arguments to have the same shape, so broadcast is not necessary.

    This function does not do any additional reductions.

    Parameters
    ----------
    pred
        The predicted values. Format: ``Ims_Scalar`` or ``Im_Scalar``
    gt
        The ground truth values. Format: ``Ims_Scalars`` or ``Im_Scalar``
    mask
        The masks that select the relevant pixels. Format: ``Ims_Mask`` or ``Ims_FloatMask``
    verify_args
        If this is true, then the function verifies the arguments and raises errors if the shapes or data types are incorrect. Otherwise the possible errors are treated as implementation detail.

    Return
    ------
    v
        The final losses. Format: ``Scalars``
    """
    if verify_args:
        _verify_loss_args(gt=gt, pred=pred, mask=mask)

    x = (pred - gt) ** 2
    x = x * mask
    x = np.sum(x, axis=(-2, -1)) / np.sum(mask, axis=(-2, -1))
    x = np.squeeze(x, axis=-1)
    return x


def mse_log_loss(
    pred: np.ndarray, gt: np.ndarray, mask: np.ndarray, verify_args: bool = True
) -> np.ndarray:
    """
    Calculate the masked MSE loss. Unlike the similar Pytorch function, this function does not do any aggregation.

    This function expects the arguments to have the same shape, so broadcast is not necessary.

    This function does not do any additional reductions.

    Parameters
    ----------
    pred
        The predicted values. Format: ``Ims_Scalar`` or ``Im_Scalar``
    gt
        The ground truth values. Format: ``Ims_Scalars`` or ``Im_Scalar``
    mask
        The masks that select the relevant pixels. Format: ``Ims_Mask`` or ``Ims_FloatMask``
    verify_args
        If this is true, then the function verifies the arguments and raises errors if the shapes or data types are incorrect. Otherwise the possible errors are treated as implementation detail.

    Return
    ------
    v
        The final losses. Format: ``Scalars_Float``
    """
    if verify_args:
        _verify_loss_args(gt=gt, pred=pred, mask=mask)
    x = (np.log(pred) - np.log(gt)) ** 2
    x = x * mask
    x = np.sum(x, axis=(-2, -1)) / np.sum(mask, axis=(-2, -1))
    x = np.squeeze(x, axis=-1)
    return x


def _verify_loss_args(pred: np.ndarray, gt: np.ndarray, mask: np.ndarray) -> None:
    """
    Throws `ValueError` if the loss arguments do not have the proper format.

    Parameters
    ----------
    pred
        The predicted values. Format: ``Ims_Scalar`` or ``Im_Scalar``
    gt
        The ground truth values. Format: ``Ims_Scalars`` or ``Im_Scalar``
    mask
        The masks that select the relevant pixels. Format: ``Ims_Mask`` or ``Ims_FloatMask``
    """
    if pred.shape != gt.shape:
        raise ValueError(
            f"The shape of the ground truths ({gt.shape}) is not equal the shape of the predictions ({pred.shape})."
        )
    if mask.shape != pred.shape:
        raise ValueError(
            f"The shape of the mask ({mask.shape}) is not equal the shape of the predictions ({pred.shape})."
        )

    if len(pred.shape) not in [3, 4]:
        raise ValueError("The predictions should be 3-or 4 dimensional.")

    if not np.issubdtype(pred.dtype, np.floating):
        raise ValueError(
            f"The prediction tensor does not contain floating point data. Dtype: {pred.dtype}"
        )
    if not np.issubdtype(gt.dtype, np.floating):
        raise ValueError(
            f"The ground truth tensor does not contain floating point data. Dtype: {gt.dtype}"
        )
    if not (
        np.issubdtype(mask.dtype, np.floating) or np.issubdtype(mask.dtype, np.bool_)
    ):
        raise ValueError(
            f"The mask tensor contains neither floating point, nor boolean data. Dtype: {mask.dtype}"
        )
