import pytest
from config.settings import Config, DevelopmentConfig, ProductionConfig, TestingConfig, get_config

def test_config_defaults():
    defaults = Config.get_timer_defaults()
    assert defaults['work_duration'] == 1500
    assert defaults['break_duration'] == 300
    assert defaults['long_break_duration'] == 900
    assert defaults['sessions_until_long_break'] == 4


def test_development_config():
    dev = DevelopmentConfig()
    assert dev.DEBUG is True
    assert dev.SECRET_KEY is not None


def test_production_config():
    prod = ProductionConfig()
    assert prod.DEBUG is False
    assert prod.SECRET_KEY is not None


def test_testing_config():
    test = TestingConfig()
    assert test.TESTING is True
    assert test.DEBUG is True
    assert test.DEFAULT_WORK_DURATION == 10
    assert test.DEFAULT_BREAK_DURATION == 5
    assert test.DEFAULT_LONG_BREAK_DURATION == 15


def test_get_config():
    assert get_config('development') == DevelopmentConfig
    assert get_config('production') == ProductionConfig
    assert get_config('testing') == TestingConfig
    assert get_config('unknown') == DevelopmentConfig
