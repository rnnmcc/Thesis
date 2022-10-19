# ICON4Py - ICON inspired code in Python and GT4Py
#
# Copyright (c) 2022, ETH Zurich and MeteoSwiss
# All rights reserved.
#
# This file is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later
# version. See the LICENSE.txt file at the top-level directory of this
# distribution for a copy of the license or check <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import numpy as np

from icon4py.atm_dyn_iconam.mo_velocity_advection_stencil_16 import (
    mo_velocity_advection_stencil_16,
)
from icon4py.common.dimension import CellDim, KDim
from icon4py.testutils.simple_mesh import SimpleMesh
from icon4py.testutils.utils import random_field


def mo_velocity_advection_stencil_16_numpy(
    z_w_con_c: np.array,
    w: np.array,
    coeff1_dwdz: np.array,
    coeff2_dwdz: np.array,
) -> np.array:
    w_offset1 = np.roll(w, shift=1, axis=1)
    w_offset2 = np.roll(w, shift=-1, axis=1)
    ddt_w_adv = -z_w_con_c * (
        w_offset1 * coeff1_dwdz
        - w_offset2 * coeff2_dwdz
        + w * (coeff2_dwdz - coeff1_dwdz)
    )
    return ddt_w_adv


def test_mo_velocity_advection_stencil_16():
    mesh = SimpleMesh()

    z_w_con_c = random_field(mesh, CellDim, KDim)
    w = random_field(mesh, CellDim, KDim)
    coeff1_dwdz = random_field(mesh, CellDim, KDim)
    coeff2_dwdz = random_field(mesh, CellDim, KDim)
    ddt_w_adv = random_field(mesh, CellDim, KDim)

    ddt_w_adv_ref = mo_velocity_advection_stencil_16_numpy(
        np.asarray(z_w_con_c),
        np.asarray(w),
        np.asarray(coeff1_dwdz),
        np.asarray(coeff2_dwdz),
    )
    mo_velocity_advection_stencil_16(
        z_w_con_c,
        w,
        coeff1_dwdz,
        coeff2_dwdz,
        ddt_w_adv,
        offset_provider={"Koff": KDim},
    )
    assert np.allclose(ddt_w_adv_ref[:, :-1], ddt_w_adv[:, :-1])