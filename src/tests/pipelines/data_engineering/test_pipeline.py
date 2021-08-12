# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This is a boilerplate test file for pipeline 'data_science'
generated using Kedro 0.16.4.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""


from kedro.runner import SequentialRunner
from spaceflights.pipelines.data_engineering.pipeline import create_pipeline

from kedro.io import DataCatalog, MemoryDataSet
import pandas as pd

catalog = DataCatalog(
    {
        "basic_data": MemoryDataSet(),
        "companies": MemoryDataSet(),
        "reviews": MemoryDataSet(),
        "shuttles": MemoryDataSet(),
        "params:conversion_rate": MemoryDataSet(),
    }
)

companies = pd.read_csv("data/01_raw/companies.csv")
catalog.save("companies", companies)
reviews = pd.read_csv("data/01_raw/reviews.csv")
catalog.save("reviews", reviews)
shuttles = pd.read_excel("data/01_raw/shuttles.xlsx")
catalog.save("shuttles", shuttles)
catalog.save("params:conversion_rate", 1.2)


def test_preproc_pipeline():
    runner = SequentialRunner()
    output_name = "outputs"

    pipeline = create_pipeline()
    # pipeline = create_pipeline(inputs="basic_data", outputs=output_name)

    pipeline_output = runner.run(pipeline, catalog)
