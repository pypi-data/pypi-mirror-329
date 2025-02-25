import datetime
from decimal import Decimal
from pathlib import Path

from configcalc import read_config_file


def test_read_config_file_float():
    read_content = read_config_file(Path(r"tests/assets/test.toml"), parse_float=float)
    should_read = {
        "title": "TOML Example",
        "owner": {
            "info": {
                "name": "Tom Preston-Werner",
                "dob": datetime.datetime(
                    1979, 5, 27, 7, 32, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=57600))
                ),
                "nb_of_days_per_month": 30,
                "nb_of_months": 3,
                "nb_of_days": "=nb_of_months * nb_of_days_per_month",
                "calculated_value": "= nb_of_days^3 * database.nb_of_ports + 2 / database.data[1][0]^2 * 2.32e-3 * _input_parts - cos(2*nb_of_days)",
            },
            "database": {
                "enabled": True,
                "nb_of_ports": 3,
                "ports": [8000, 8001, 8002],
                "data": [["delta", "phi"], [3.14]],
                "temp_targets": {"cpu": 79.5, "case": 72.0},
            },
        },
        "servers": {
            "alpha": {
                "ip": "10.0.0.1",
                "role": "frontend",
                "test_list_of_dict": [{"a": "a_val", "b": "b_val"}, {"c": "c_val"}],
            },
            "beta": {
                "role": "backend",
                "test": {"ip": "10.0.0.2", "role": "backend_test"},
                "prod": {"ip": "10.0.0.3", "role": "backend_prod"},
            },
        },
    }

    assert read_content == should_read


def test_read_config_file_decimal():
    read_content = read_config_file(Path(r"tests/assets/test.toml"), parse_float=Decimal)
    should_read = {
        "title": "TOML Example",
        "owner": {
            "info": {
                "name": "Tom Preston-Werner",
                "dob": datetime.datetime(
                    1979, 5, 27, 7, 32, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=57600))
                ),
                "nb_of_days_per_month": 30,
                "nb_of_months": 3,
                "nb_of_days": "=nb_of_months * nb_of_days_per_month",
                "calculated_value": "= nb_of_days^3 * database.nb_of_ports + 2 / database.data[1][0]^2 * 2.32e-3 * _input_parts - cos(2*nb_of_days)",
            },
            "database": {
                "enabled": True,
                "nb_of_ports": 3,
                "ports": [8000, 8001, 8002],
                "data": [["delta", "phi"], [Decimal("3.14")]],
                "temp_targets": {"cpu": Decimal("79.5"), "case": Decimal("72.0")},
            },
        },
        "servers": {
            "alpha": {
                "ip": "10.0.0.1",
                "role": "frontend",
                "test_list_of_dict": [{"a": "a_val", "b": "b_val"}, {"c": "c_val"}],
            },
            "beta": {
                "role": "backend",
                "test": {"ip": "10.0.0.2", "role": "backend_test"},
                "prod": {"ip": "10.0.0.3", "role": "backend_prod"},
            },
        },
    }

    assert read_content == should_read
