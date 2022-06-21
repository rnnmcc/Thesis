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

from icon4py.atm_dyn_iconam.mo_solve_nonhydro_stencil_03 import (
    mo_solve_nonhydro_stencil_03,
)
from icon4py.common.dimension import CellDim, KDim
from icon4py.testutils.simple_mesh import SimpleMesh
from icon4py.testutils.utils import random_field


def mo_solve_nonhydro_stencil_03_numpy(
    z_exner_ex_pr: np.array,
):
    z_exner_ex_pr = np.zeros_like(z_exner_ex_pr)
    return z_exner_ex_pr


def test_mo_solve_nonhydro_stencil_03():
    mesh = SimpleMesh()
    z_exner_ex_pr = random_field(mesh, CellDim, KDim)

    ref = mo_solve_nonhydro_stencil_03_numpy(
        np.asarray(z_exner_ex_pr),
    )

    mo_solve_nonhydro_stencil_03(
        z_exner_ex_pr,
        offset_provider={},
    )
    assert np.allclose(z_exner_ex_pr, ref)