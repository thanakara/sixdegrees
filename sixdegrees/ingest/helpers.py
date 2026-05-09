import pandas as pd

from sixdegrees import log
from sixdegrees.config import settings
from sixdegrees.ingest import PROCESSED_PATH
from sixdegrees.app.extensions import get_session


def load(label: str, cypher: str, df: pd.DataFrame) -> None:
    """Batch-load a DataFrame into Neo4j, one session per batch."""

    df = df.where(pd.notnull(df), None)
    records = df.to_dict("records")
    total = len(records)
    batch_size = settings.batch_size

    log.info(f"Loading {label}: {total:,} rows in batches of {batch_size:,}")

    for i in range(0, total, batch_size):
        batch = records[i : i + batch_size]
        with get_session() as session:
            session.run(cypher, rows=batch)
        done = min(i + batch_size, total)
        log.debug(f"  {label}: {done:,} / {total:,}")

    log.info(f"  {label} ✓")


def read(filename: str) -> pd.DataFrame:
    return pd.read_csv(PROCESSED_PATH / filename)
