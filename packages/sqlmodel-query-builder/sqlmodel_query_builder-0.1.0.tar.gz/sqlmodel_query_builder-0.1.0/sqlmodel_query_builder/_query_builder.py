from operator import eq, ge, gt, le, lt
from typing import Any, ClassVar, Self

from pydantic import BaseModel
from sqlmodel import select


class OnClause(BaseModel):
    mdl_l: str
    attr_l: str
    mdl_r: str
    attr_r: str


class JoinArgs(BaseModel):
    mdl: str
    onclause: OnClause | None = None
    isouter: bool = False
    full: bool = False


class WhereArgs(BaseModel):
    mdl: str
    attr: str
    op: str
    val: Any

    STR_TO_OP: ClassVar = {
        "==": eq,
        "<=": le,
        ">=": ge,
        "<": lt,
        ">": gt,
    }


class SelectArgs(BaseModel):
    mdl: str
    attr: str | None = None


class QueryArgs(BaseModel):
    selects: list[SelectArgs]
    joins: list[JoinArgs]
    wheres: list[WhereArgs]


class QueryBuilder(BaseModel):
    # NOTE: attribute cannot (or at least should not) be named "model_registry"
    #       because the "model_" prefix is reserved by pydantic
    mdl_registry: dict[str, type]

    def _retrieve(self: Self, mdl_name: str, property_name: str | None = None):
        # Validate model
        if mdl_name not in self.mdl_registry:
            raise Exception(
                f"Model {mdl_name} is not the model registry: {self.mdl_registry}"
            )
        model = self.mdl_registry[mdl_name]

        result = model
        if property_name is not None:
            # Validate property
            if not hasattr(model, property_name):
                raise Exception(
                    f"Model {mdl_name} does not have property: {property_name}"
                )
            result = getattr(model, property_name)
        return result

    def _onclause_to_arg(self: Self, onclause: OnClause):
        left = self._retrieve(onclause.mdl_l, onclause.attr_l)
        right = self._retrieve(onclause.mdl_r, onclause.attr_r)
        return left == right

    def _joinargs_to_kwarg(self: Self, joinargs: JoinArgs):
        target = self._retrieve(joinargs.mdl)

        onclause = None
        if joinargs.onclause is not None:
            onclause = self._onclause_to_arg(joinargs.onclause)

        return {
            "target": target,
            "onclause": onclause,
            "isouter": joinargs.isouter,
            "full": joinargs.full,
        }

    def _whereargs_to_arg(self: Self, whereargs: WhereArgs):
        column = self._retrieve(whereargs.mdl, whereargs.attr)
        operator = WhereArgs.STR_TO_OP[whereargs.op]
        whereclause = operator(column, whereargs.val)
        return whereclause

    def _selectargs_to_arg(self: Self, selectargs: SelectArgs):
        return self._retrieve(selectargs.mdl, selectargs.attr)

    def build_statement(self: Self, query_args: QueryArgs):
        # SELECT
        statement = select(*[self._selectargs_to_arg(s) for s in query_args.selects])

        # JOIN
        for j in query_args.joins:
            statement = statement.join(**self._joinargs_to_kwarg(j))

        # WHERE
        for w in query_args.wheres:
            statement = statement.where(self._whereargs_to_arg(w))

        return statement
