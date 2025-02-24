from copy import deepcopy
import types

import numpy as np
import opytional as opyt
import pytest

from downstream.dstream import steady_algo, stretched_algo, tilted_algo
from downstream.dsurf import Surface


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32])
def test_Surface(algo: types.ModuleType, S: int) -> None:
    surface = Surface(algo, S)
    assert surface.T == 0
    assert [*surface] == [None] * surface.S
    assert [*surface.lookup()] == [None] * surface.S

    for T in range(100):
        site = surface.ingest_one(T)
        if site is not None:
            assert surface[site] == T
        assert [*surface] == [*surface.lookup()]
        assert [*zip(surface.lookup(), surface)] == [
            *surface.lookup_zip_items()
        ]


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32, np.empty(32, dtype=np.uint32)])
@pytest.mark.parametrize("step_size", [1, 5, 25, 50])
def test_Surface_ingest_many(
    algo: types.ModuleType, S: int, step_size: int
) -> None:
    single_surface = Surface(algo, S)
    multi_surface = Surface(algo, S)
    num_iterations = min(
        (
            opyt.apply_if_or_value(
                algo.get_ingest_capacity(single_surface.S),
                lambda x: x // step_size // 2,
                100,
            ),
            100,
        )
    )
    for T in range(num_iterations):
        for i in range(step_size):
            single_surface.ingest_one(T * step_size + i)
        multi_surface.ingest_many(step_size, lambda x: x)
        assert single_surface == multi_surface


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32, np.empty(32, dtype=np.uint32)])
def test_Surface_ingest_none(algo: types.ModuleType, S: int):
    surf = Surface(algo, S)
    for T in range(100):
        surf.ingest_one(T)
        new_surf = deepcopy(surf)
        new_surf.ingest_many(0, lambda _: None)
        assert new_surf == surf


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32, np.empty(32, dtype=np.uint32)])
def test_ingest_cap(algo: types.ModuleType, S: int):
    surf = Surface(algo, S)
    cap = algo.get_ingest_capacity(surf.S)
    if cap is None:
        return
    with pytest.raises(AssertionError):
        Surface(algo, S).ingest_many(cap + 1, lambda _: 1)
    surf.ingest_many(cap, lambda _: 1)
    with pytest.raises(AssertionError):
        surf.ingest_one(1)


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [32, np.empty(32, dtype=np.uint32)])
@pytest.mark.parametrize("step_size", [1, 5, 25, 50])
def test_ingest_items_relative_times(
    algo: types.ModuleType, S: int, step_size: int
):
    surf_absolute = Surface(algo, S)
    surf_relative = Surface(algo, S)
    for T in range(100):
        surf_absolute.ingest_many(step_size, lambda x: x)
        surf_relative.ingest_many(
            step_size, lambda x: T * step_size + x, use_relative_time=True
        )
        assert surf_absolute == surf_relative
