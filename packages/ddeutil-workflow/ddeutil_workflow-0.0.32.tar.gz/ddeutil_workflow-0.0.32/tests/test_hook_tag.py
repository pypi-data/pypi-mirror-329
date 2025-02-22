import shutil
from pathlib import Path
from textwrap import dedent

import pytest
from ddeutil.workflow.hook import Registry, make_registry


@pytest.fixture(scope="module")
def hook_function(test_path: Path):
    new_tasks_path: Path = test_path / "new_tasks"
    new_tasks_path.mkdir(exist_ok=True)

    with open(new_tasks_path / "__init__.py", mode="w") as f:
        f.write("from .dummy import *\n")

    with open(new_tasks_path / "dummy.py", mode="w") as f:
        f.write(
            dedent(
                """
            from ddeutil.workflow.hook import tag

            @tag("polars-dir", alias="el-csv-to-parquet")
            def dummy_task(source: str, sink: str) -> dict[str, int]:
                return {"records": 1}

            @tag("polars-dir", alias="el-csv-to-parquet")
            def dummy_task_override(source: str, sink: str) -> dict[str, int]:
                return {"records": 1}
            """.strip(
                    "\n"
                )
            )
        )

    yield

    shutil.rmtree(new_tasks_path)


def test_make_registry_not_found():
    rs: dict[str, Registry] = make_registry("not_found")
    assert rs == {}


def test_make_registry_raise(hook_function):

    # NOTE: Raise error duplicate tag name, polars-dir, that set in this module.
    with pytest.raises(ValueError):
        make_registry("new_tasks")
