#
# Copyright © 2024 Intel Corporation
# SPDX-License-Identifier: Apache 2.0
#

from intel_npu_acceleration_library.backend.factory import NNFactory
import numpy as np


class QLinear(NNFactory):
    """Quantized Linear class, computing a matrix matrix multiplication with weights prefetching."""

    def __init__(
        self,
        inC: int,
        outC: int,
        batch: int,
        profile: bool = False,
        device: str = "NPU",
        dtype: np.dtype = np.int8,
        asym: bool = False
    ):
        """Initialize the QLinear class.

        Args:
            inC (int): input channels
            outC (int): output channels
            batch (int): batch
            profile (bool): Enable/Disable profiling. Defaults to False.
            device (str): Target device, default to "NPU".
            dtype (np.dtype): weights datatype. Defaults to np.int8.

        """
        super().__init__(profile, device)
        self.inC, self.outC = inC, outC
        self.batch = batch
        self.asym = asym

        input = self.parameter((self.batch, self.inC))
        _ = self.linear(input, outC, inC, bias=False, wt_dtype=dtype, asym=asym)
        self.compile()

    def run(
        self, X: np.ndarray, W: np.ndarray, scale: np.ndarray, zero: np.ndarray=None, op_id: str=None
    ) -> np.ndarray:
        """Run the layer:  $X * (W * S)^T$ .

        Args:
            X (np.ndarray): activation
            W (np.ndarray): quantized weights
            scale (np.ndarray): quantization scale
            op_id (str): operation id

        Raises:
            RuntimeError: Input, weights or scale shape mismatch

        Returns:
            np.ndarray: result
        """
        if not (X.shape[0] == self.batch and X.shape[1] == self.inC):
            raise RuntimeError(
                f"Input shape {X.shape} different from expected one {(self.batch, self.inC)}"
            )
        if not (X.shape[0] == self.batch and X.shape[1] == self.inC):
            raise RuntimeError(
                f"Weight shape {W.shape} different from expected one {(self.outC, self.inC)}"
            )
        if not (X.shape[0] == self.batch and X.shape[1] == self.inC):
            raise RuntimeError(
                f"Scale shape {W.shape} different from expected one {(self.outC, 1)}"
            )
        if not self.asym:
            return super().run(X, (W, scale), op_id=op_id)
        else:
            return super().run(X, (W, scale, zero), op_id=op_id)
