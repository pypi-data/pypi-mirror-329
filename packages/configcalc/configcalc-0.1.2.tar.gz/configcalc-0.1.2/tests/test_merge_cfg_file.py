import datetime
from pathlib import Path

from configcalc import merge_configs, read_config_file


def test_merge_configs():
    base_config = read_config_file(Path(r"tests/assets/test.toml"))
    second_config = read_config_file(Path(r"tests/assets/test_second.toml"))
    third_config = read_config_file(Path(r"tests/assets/test_third.toml"))
    merge_configs(base_config, second_config, third_config)

    final_config = base_config
    should_be_config = {
        "title": "TOML Example Updated Twice",
        "owner": {
            "info": {
                "name": "Tom Preston-Werner",
                "dob": datetime.datetime(
                    1979, 5, 27, 7, 32, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=57600))
                ),
                "nb_of_days_per_month": 28,
                "nb_of_months": 3,
                "nb_of_days": "=nb_of_months * nb_of_days_per_month + 5",
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
                "test": {"ip": "10.20.30.20", "role": "backend_test"},
                "prod": {"ip": "10.0.0.3", "role": "backend_prod"},
            },
        },
    }

    assert should_be_config == final_config
