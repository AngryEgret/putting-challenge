"""
Initial Schema
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
         CREATE TABLE scorecards (
            id SERIAL PRIMARY KEY ,
            created TIMESTAMP,
            grand_total INT,
            station_1 INT,
            station_2 INT,
            station_3 INT,
            station_4 INT,
            station_5 INT,
            raw TEXT
         );
         """,
         "DROP TABLE scorecards",
         ),
    step("CREATE INDEX created ON scorecards (created);",
         "DROP INDEX created")
]
