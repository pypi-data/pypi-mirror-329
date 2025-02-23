from pathlib import Path
from typing import ClassVar

import pytest
from pydantic import computed_field

from .base import AbstractSqlBlock
from .blocks import (
    HashData,
    JoinBlock,
    JoinTarget,
    PredefinedTemplateSqlBlock,
    SelectBlock,
    SqlTarget,
    StackBlock,
    TemplateSqlBlock,
)
from .ctx import SqlGenContext

template_dir = Path(__file__).parent / "templates"


def test_jinja2_block(ctx: SqlGenContext):
    class TestBlock0(PredefinedTemplateSqlBlock):
        template: ClassVar[Path] = template_dir / "tests" / "test0.j2"

        a: int = 1

        @computed_field
        def b(self) -> int:
            return self.a + 1

    block = TestBlock0(a=1)
    assert block.to_sql() == "select 1 as a, 2 as b"


@pytest.mark.parametrize(
    "input_block",
    [TemplateSqlBlock(template="select 1 as a, 2 as b"), SqlTarget(target="`project.dataset.table`")],
)
def test_hash_data(input_block: AbstractSqlBlock):
    block = HashData(input_block=input_block)
    query = block.to_sql()
    print(query)


def test_select_block(ctx: SqlGenContext):
    source = TemplateSqlBlock(template="select 1 as a, 2 as b")
    source.to_sql()
    apply1 = SelectBlock(
        selects=[
            "a",
            "b",
        ],
        filters=["b > 1"],
    )
    query = apply1(source).to_sql()
    print(query)


def test_stack_block(ctx: SqlGenContext):
    blocks = [
        TemplateSqlBlock(template="select 1 as a, 2 as b"),
        SelectBlock(
            selects=[
                "a",
                "b",
            ],
            filters=["b > 1"],
        ),
        HashData(),
    ]
    block = StackBlock(blocks=blocks)
    query = block.to_sql()
    print(query)


def test_joins(ctx):
    person = SqlTarget(
        name="person",
        target="person",
        fields=[{"name": "id"}, {"name": "name"}, {"name": "age"}, {"name": "department_id"}, {"name": "school_id"}],
    )
    department = SqlTarget(
        name="department", target="department", fields=[{"name": "id"}, {"name": "name"}, {"name": "company_id"}]
    )
    company = SqlTarget(name="company", target="company", fields=[{"name": "id"}, {"name": "name"}])
    school = SqlTarget(name="school", target="school", fields=[{"name": "id"}, {"name": "name"}])

    join = JoinBlock(
        base=person,
        joins=[
            JoinTarget(target=department, condition="person.department_id = department.id", alias="department"),
            JoinTarget(target=company, condition="department.company_id = company.id", alias="company"),
            JoinTarget(target=school, condition="person.school_id = school.id", alias="school"),
        ],
    )
    sql = join.to_sql()
    print(sql)
