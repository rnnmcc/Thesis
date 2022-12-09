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

from icon4py.atm_dyn_iconam.mo_solve_nonhydro_stencil_12 import (
    mo_solve_nonhydro_stencil_12,
)
from icon4py.common.dimension import CellDim, KDim
from icon4py.testutils.simple_mesh import SimpleMesh
from icon4py.testutils.utils import random_field, zero_field


def mo_solve_nonhydro_stencil_12_numpy(
    z_theta_v_pr_ic: np.array,
    d2dexdz2_fac1_mc: np.array,
    d2dexdz2_fac2_mc: np.array,
    z_rth_pr_2: np.array,
) -> np.array:
    z_theta_v_pr_ic_offset_1 = np.roll(z_theta_v_pr_ic, shift=-1, axis=1)
    z_dexner_dz_c_2 = -0.5 * (
        (z_theta_v_pr_ic - z_theta_v_pr_ic_offset_1) * d2dexdz2_fac1_mc
        + z_rth_pr_2 * d2dexdz2_fac2_mc
    )
    return z_dexner_dz_c_2


def test_mo_solve_nonhydro_stencil_12():
    mesh = SimpleMesh()

    z_theta_v_pr_ic = random_field(mesh, CellDim, KDim)
    d2dexdz2_fac1_mc = random_field(mesh, CellDim, KDim)
    z_rth_pr_2 = random_field(mesh, CellDim, KDim)
    d2dexdz2_fac2_mc = random_field(mesh, CellDim, KDim)

    z_dexner_dz_c_2 = zero_field(mesh, CellDim, KDim)

    z_dexner_dz_c_2_ref = mo_solve_nonhydro_stencil_12_numpy(
        np.asarray(z_theta_v_pr_ic),
        np.asarray(d2dexdz2_fac1_mc),
        np.asarray(d2dexdz2_fac2_mc),
        np.asarray(z_rth_pr_2),
    )

    mo_solve_nonhydro_stencil_12(
        z_theta_v_pr_ic,
        d2dexdz2_fac1_mc,
        d2dexdz2_fac2_mc,
        z_rth_pr_2,
        z_dexner_dz_c_2,
        offset_provider={"Koff": KDim},
    )

    assert np.allclose(
        # work around problem with field[:,:-1], i.e. without the `np.asarray`
        np.asarray(z_dexner_dz_c_2)[:, :-1],
        np.asarray(z_dexner_dz_c_2_ref)[:, :-1],
    )