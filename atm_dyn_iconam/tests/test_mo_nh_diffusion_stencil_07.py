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

from icon4py.atm_dyn_iconam.mo_nh_diffusion_stencil_07 import (
    mo_nh_diffusion_stencil_07,
)
from icon4py.common.dimension import C2E2CODim, CellDim, KDim
from icon4py.testutils.simple_mesh import SimpleMesh
from icon4py.testutils.utils import random_field, zero_field


def mo_nh_diffusion_stencil_07_numpy(
    c2e2cO: np.array, w: np.array, geofac_n2s: np.array
) -> np.array:
    geofac_n2s = np.expand_dims(geofac_n2s, axis=-1)
    z_nabla2_c = np.sum(w[c2e2cO] * geofac_n2s, axis=1)
    return z_nabla2_c


def test_mo_nh_diffusion_stencil_07():
    mesh = SimpleMesh()

    w = random_field(mesh, CellDim, KDim)
    geofac_n2s = random_field(mesh, CellDim, C2E2CODim)
    z_nabla2_c = zero_field(mesh, CellDim, KDim)

    ref = mo_nh_diffusion_stencil_07_numpy(
        mesh.c2e2cO, np.asarray(w), np.asarray(geofac_n2s)
    )
    mo_nh_diffusion_stencil_07(
        w,
        geofac_n2s,
        z_nabla2_c,
        offset_provider={"C2E2CO": mesh.get_c2e2cO_offset_provider()},
    )
    assert np.allclose(z_nabla2_c, ref)