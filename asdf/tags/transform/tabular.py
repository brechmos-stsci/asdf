# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function

import numpy as np
from numpy.testing import assert_array_equal
from ... import yamlutil

from .basic import TransformType

__all__ = ['TabularType']


class TabularType(TransformType):
    import astropy
    name = "transform/tabular"
    types = [astropy.modeling.models.Tabular2D,
             astropy.modeling.models.Tabular1D
             ]

    @classmethod
    def from_tree_transform(cls, node, ctx):
        from astropy import modeling
        lookup_table = node.pop("lookup_table")
        dim = lookup_table.ndim
        name = node.get('name', None)
        fill_value = node.pop("fill_value", None)
        points = np.asarray(node['points'])
        if dim == 1:
            model = modeling.models.Tabular1D(points=points, lookup_table=lookup_table,
                                              method=node['method'], bounds_error=node['bounds_error'],
                                              fill_value=fill_value, name=name)
        elif dim == 2:
            model = modeling.models.Tabular2D(points=points, lookup_table=lookup_table,
                                              method=node['method'], bounds_error=node['bounds_error'],
                                              fill_value=fill_value, name=name)
        else:
            tabular_class = modeling.models.tabular_model(dim, name)

            model = tabular_class(points=points, lookup_table=lookup_table,
                                  method=node['method'], bounds_error=node['bounds_error'],
                                  fill_value=fill_value, name=name)

        return model

    @classmethod
    def to_tree_transform(cls, model, ctx):
        node = {}
        node["fill_value"] = model.fill_value
        node["lookup_table"] = model.lookup_table
        node["points"] = model.points
        node["method"] = str(model.method)
        node["bounds_error"] = model.bounds_error
        node["name"] = model.name
        return yamlutil.custom_tree_to_tagged_tree(node, ctx)

    @classmethod
    def assert_equal(cls, a, b):
        assert_array_equal(a.lookup_table, b.lookup_table)
        assert_array_equal(a.points, b.points)
        assert (a.method == b.method)
        if a.fill_value is None:
            assert b.fill_value is None
        elif np.isnan(a.fill_value):
            assert np.isnan(b.fill_value)
        else:
            assert(a.fill_value == b.fill_value)
        assert(a.bounds_error == b.bounds_error)
