# sqlalchemy_boltons

SQLAlchemy is great. However, it doesn't have everything built-in. Some important things are missing, and need to be
"bolted on".

(Name inspired from [boltons](https://pypi.org/project/boltons/). Not affiliated.)

## sqlite

SQLAlchemy doesn't automatically fix pysqlite's broken transaction handling. This module implements the
[usual fix](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl)
for that well-known broken behaviour, and also adds extra features on top of that.

You can [customize](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.execution_options),
on a per-engine or per-connection basis:

- `x_sqlite_begin_mode`: The type of transaction to be started, such as "BEGIN" or
  "[BEGIN IMMEDIATE](https://www.sqlite.org/lang_transaction.html)" (or
  "[BEGIN CONCURRENT](https://www.sqlite.org/cgi/src/doc/begin-concurrent/doc/begin_concurrent.md)" someday maybe).
- `x_sqlite_foreign_keys`: The [foreign-key enforcement setting](https://www.sqlite.org/foreignkeys.html). Can be
  `True`, `False`, or `"defer"`.
- `x_sqlite_journal_mode`: The [journal mode](https://www.sqlite.org/pragma.html#pragma_journal_mode) such as
  `"DELETE"` or `"WAL"`.

Here's a minimal example:

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy_boltons.sqlite import create_engine_sqlite

engine = create_engine_sqlite(
    "file.db",
    journal_mode="WAL",
    timeout=0.5,
    create_engine_args={"echo": True},
)

# Configure the engine to use a plain "BEGIN" to start transactions and
# and to use deferred enforcement of foreign keys (recommended!)
engine = engine.execution_options(
    x_sqlite_begin_mode=None, x_sqlite_foreign_keys="defer"
)

# Make a separate engine for write transactions using "BEGIN IMMEDIATE"
# for eager locking.
engine_w = engine.execution_options(x_sqlite_begin_mode="IMMEDIATE")

# Construct a sessionmaker for each engine.
Session = sessionmaker(engine)
SessionW = sessionmaker(engine_w)

# read-only transaction
with Session() as session:
    session.execute(select(...))

# lock the database eagerly for writing
with SessionW() as session:
    session.execute(update(...))
```
