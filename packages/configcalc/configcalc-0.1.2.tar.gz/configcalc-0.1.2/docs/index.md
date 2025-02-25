# Configcalc

Configcalc is a library to handle TOML configuration files with formulas. Formulas can make simple operations between variables contained in other parts of the configuration or given by the user at runtime. 

# Usage

```python
import configcalc as cc
config1 = cc.read_config_file(Path(r"path/to/config_file1.toml"))
config2 = cc.read_config_file(Path(r"path/to/config_file2.toml"))
merged_config = cc.merge_configs(config1, config2)
calculated_config = cc.perform_calculations(
        config=config,
    )
```