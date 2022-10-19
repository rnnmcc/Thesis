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

from functional.ffront.decorator import field_operator, program
from functional.ffront.fbuiltins import Field, neighbor_sum

from icon4py.common.dimension import C2E2CO, C2E2CODim, CellDim, KDim


@field_operator
def _mo_nh_diffusion_stencil_09(
    area: Field[[CellDim], float],
    z_nabla2_c: Field[[CellDim, KDim], float],
    geofac_n2s: Field[[CellDim, C2E2CODim], float],
    w: Field[[CellDim, KDim], float],
    diff_multfac_w: float,
) -> Field[[CellDim, KDim], float]:
    w = w - diff_multfac_w * area * area * neighbor_sum(
        z_nabla2_c(C2E2CO) * geofac_n2s, axis=C2E2CODim
    )
    return w


@program
def mo_nh_diffusion_stencil_09(
    area: Field[[CellDim], float],
    z_nabla2_c: Field[[CellDim, KDim], float],
    geofac_n2s: Field[[CellDim, C2E2CODim], float],
    w: Field[[CellDim, KDim], float],
    diff_multfac_w: float,
):
    _mo_nh_diffusion_stencil_09(area, z_nabla2_c, geofac_n2s, w, diff_multfac_w, out=w)