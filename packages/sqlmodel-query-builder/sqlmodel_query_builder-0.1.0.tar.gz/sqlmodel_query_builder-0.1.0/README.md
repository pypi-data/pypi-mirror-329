# SQLModel Query Builder

A serializable object for simple SQLModel queries.

## Why this exists

SQLModel is an Object Relation Mapper (ORM) library that provides great abstractions for interacting with relational databases, such as PostgreSQL and SQLite, via Python. SQLModel gives its users the option to write queries using its own "pythonic" functions, which is safer and easier (in my opinion) than writing raw SQL. Here's what an SQLModel looks like:

```python
with Session(engine) as session:
    statement = select(Hero, Team).join(Team).where(Team.name == "Preventers")
    results = session.exec(statement)
```

In this example, [from SQLModel's own documentation](https://sqlmodel.tiangolo.com/tutorial/connect/read-connected-data/#include-the-team), the words `Hero` and `Team` are classes that represent tables in the database. 

As convenient as it is, this approach to writing queries has a major drawback: there is no built-in to serialize SQLModel queries. The implication is that you cannot easily dump them into a JSON object that can be sent and received in a REST API, which is a major usecase when developing database applications.

Thus, `sqlmodel-query-builder` exists to close (or at least narrow) this gap by providing a serializable object for SQLModel queries. For now, it only supports simple queries that involve only `SELECT`, `JOIN`, and `WHERE` statements.

## License

This work is licensed under the terms of the GPLv3.

## Copyright

© 2024 Brazilian Center for Research in Energy and Materials (CNPEM)
