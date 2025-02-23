from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from dbox.templater import to_template

parent_dir = Path(__file__).parent
subquery_tpl = to_template(parent_dir / "templates" / "subquery.j2")


class SqlField(BaseModel):
    name: str
    type: Optional[str] = None
    # TODO: add more properties


class AbstractSqlBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = None

    def to_sql(self) -> str:
        raise NotImplementedError

    def get_fields(self) -> List[SqlField]:
        raise NotImplementedError

    def get_field_names(self) -> List[str]:
        return [f.name for f in self.get_fields()]

    def sql_target(self) -> str:
        return subquery_tpl.render(this=self)


class AbstractSqlFunction(AbstractSqlBlock):
    input_block: Optional[AbstractSqlBlock] = None

    def __call__(self, input_block: AbstractSqlBlock) -> "AbstractSqlBlock":
        assert self.input_block is None, "input_block is already set"
        return self.model_copy(update={"input_block": input_block})

    # pipe operator
    def __or__(self, other: "AbstractSqlBlock") -> "AbstractSqlBlock":
        return other(input_block=self)
