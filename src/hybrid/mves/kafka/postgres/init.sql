CREATE TABLE trips (
    trip_id     TEXT PRIMARY KEY,
    city        TEXT NOT NULL,
    distance_km DOUBLE PRECISION NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Columns expected by the Debezium outbox event router
CREATE TABLE outbox (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregatetype TEXT NOT NULL,
    aggregateid   TEXT NOT NULL,
    type          TEXT NOT NULL,
    payload       JSONB NOT NULL
);
