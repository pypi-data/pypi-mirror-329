# -*- coding: utf-8 -*-
# Copyright (c) 2022-2023 Salvador E. Tropea
# Copyright (c) 2022-2023 Instituto Nacional de Tecnologïa Industrial
# License: Apache 2.0
# Project: KiAuto (formerly kicad-automation-scripts)
"""
Tests for 'pcbnew_do export_vrml'

For debug information use:
pytest-3 --log-cli-level debug

"""
import os
import sys
# Look for the 'utils' module from where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))
prev_dir = os.path.dirname(script_dir)
sys.path.insert(0, prev_dir)
# Utils import
from utils import context
sys.path.insert(0, os.path.dirname(prev_dir))

PROG = 'pcbnew_do'


def test_export_vrml_1(test_dir):
    """ Generate a GenCAD file with no special options test """
    ctx = context.TestContext(test_dir, 'export_vrml_1', 'good-project')
    cmd = [PROG, '-vv', 'export_vrml', '--output_name', 'good.wrl']
    ctx.run(cmd)
    ctx.expect_out_file('good.wrl')
    ctx.clean_up()


def test_export_vrml_2(test_dir):
    """ Generate a GenCAD file 3D models separated """
    ctx = context.TestContext(test_dir, 'export_vrml_2', 'good-project')
    cmd = [PROG, '-vv', 'export_vrml', '--dir_models', '3DModels', '--output_name', 'good.wrl']
    ctx.run(cmd)
    vrml_file = ctx.expect_out_file('good.wrl')
    with open(vrml_file, 'rt') as f:
        vrml = f.read()
    models = ['B02B-JWPF-SK-R.wrl', 'C_0402_1005Metric.wrl', 'R_0402_1005Metric.wrl']
    for m in models:
        m_f = os.path.join('3DModels', m)
        ctx.expect_out_file(m_f)
        assert 'url "{}"'.format(m_f) in vrml
    ctx.clean_up()


def test_export_vrml_3(test_dir):
    """ Generate a GenCAD file with some options """
    ctx = context.TestContext(test_dir, 'export_vrml_3', 'good-project')
    cmd = [PROG, '-vv', 'export_vrml', '-x', '1', '-y', '1', '-u', 'inches', '-U', 'inches', '--dir_models', '3DModels',
           '--output_name', 'good.wrl']
    ctx.run(cmd)
    ctx.expect_out_file('good.wrl')
    ctx.clean_up()
