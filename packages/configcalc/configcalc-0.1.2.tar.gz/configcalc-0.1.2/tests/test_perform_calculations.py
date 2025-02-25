import datetime
from decimal import Decimal
from pathlib import Path
from configcalc import perform_calculations
import pytest

from configcalc.utils import NumberType
from configcalc.read_cfg_file import read_config_file


@pytest.fixture
def config():
    return read_config_file(Path(r"tests/assets/test.toml"), parse_float=Decimal)


def test_perform_calculations(config):
    calculated_config = perform_calculations(
        config=config,
        context_variables={"_input_parts": 25},
        number_type=NumberType.DECIMAL,
    )
    should_be = {
        "title": "TOML Example",
        "owner": {
            "info": {
                "name": "Tom Preston-Werner",
                "dob": datetime.datetime(
                    1979,
                    5,
                    27,
                    7,
                    32,
                    tzinfo=datetime.timezone(
                        datetime.timedelta(days=-1, seconds=57600)
                    ),
                ),
                "nb_of_days_per_month": 30,
                "nb_of_months": 3,
                "nb_of_days": 90,
                "calculated_value": Decimal("2187000.610225252229589195312"),
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
    assert calculated_config == should_be
