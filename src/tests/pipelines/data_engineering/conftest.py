import pandas as pd
import pytest
from kedro.config import ConfigLoader
from kedro.io import DataCatalog, MemoryDataSet
from typing import Any, Dict


def get_feed_dict(params) -> Dict[str, Any]:
    """Taken from KedroContext._get_feed_dict"""
    """Get parameters and return the feed dictionary."""
    feed_dict = {"parameters": params}

    def _add_param_to_feed_dict(param_name, param_value):
        """This recursively adds parameter paths to the `feed_dict`,
        whenever `param_value` is a dictionary itself, so that users can
        specify specific nested parameters in their node inputs.

        Example:

            >>> param_name = "a"
            >>> param_value = {"b": 1}
            >>> _add_param_to_feed_dict(param_name, param_value)
            >>> assert feed_dict["params:a"] == {"b": 1}
            >>> assert feed_dict["params:a.b"] == 1
        """
        key = "params:{}".format(param_name)
        feed_dict[key] = param_value

        if isinstance(param_value, dict):
            for key, val in param_value.items():
                _add_param_to_feed_dict("{}.{}".format(param_name, key), val)

    for param_name, param_value in params.items():
        _add_param_to_feed_dict(param_name, param_value)

    return feed_dict


@pytest.fixture(scope="module")
def data_catalog():
    catalog = DataCatalog(
        {
            "basic_data": MemoryDataSet(),
            "companies": MemoryDataSet(),
            "reviews": MemoryDataSet(),
            "shuttles": MemoryDataSet(),
            # "params:conversion_rate": MemoryDataSet(),
        }
    )

    conf_paths = ["conf/base", "conf/local"]
    conf_loader = ConfigLoader(conf_paths)
    parameters = conf_loader.get("parameters*", "parameters*/**", "**/parameters*")

    feed_dict = get_feed_dict(parameters)

    catalog.add_feed_dict(feed_dict)

    companies = pd.read_csv("data/01_raw/companies.csv")
    catalog.save("companies", companies)
    reviews = pd.read_csv("data/01_raw/reviews.csv")
    catalog.save("reviews", reviews)
    shuttles = pd.read_excel("data/01_raw/shuttles.xlsx")
    catalog.save("shuttles", shuttles)
    return catalog
