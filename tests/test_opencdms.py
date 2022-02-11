#!/usr/bin/env python

"""Tests for `opencdms_process` package."""

from cmath import nan
from typing import Tuple
from py import process
import py
import pytest

from click.testing import CliRunner

# from opencdms_process import opencdms_process
from opencdms_process import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "opencdms_process.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output

import opencdms_process.process.climatol.windrose_generator
import opencdms_process.process.rinstat.rpy2_experiment

from opencdms_process.process.rinstat import rpy2_experiment
import math

#from opencdms_process.process import date_components

def test_naflex_na_omit_if():
    input_data: Tuple = (1.0, 3.0, nan, nan, 3.0, 2.0, nan, 5.0, 8.0, 7.0)
    actual: Tuple = rpy2_experiment.naflex_na_omit_if(input_data, 0.2)
    # We cannot do `assert actual == input_data` because in Python `nan == nan` returns False!`
    assert len(actual) == len(input_data)
    input_data_non_nan: Tuple = tuple(x for x in input_data if math.isnan(x) == False)
    actual_non_nan: Tuple = tuple(x for x in actual if math.isnan(x) == False)
    assert input_data_non_nan == actual_non_nan
    
    actual: Tuple = rpy2_experiment.naflex_na_omit_if(input_data, 0.3)
    assert len(actual) == len(input_data) - 3
    input_data_non_nan: Tuple = tuple(x for x in input_data if math.isnan(x) == False)
    actual_non_nan: Tuple = tuple(x for x in actual if math.isnan(x) == False)
    assert input_data_non_nan == actual
    
def test_simple_rpy2_example():
    
    assert rpy2_experiment.simple_rpy2_example() == 'a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z'
    
