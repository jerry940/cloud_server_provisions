create table if not exist servers (
    id          SERIAL PRIMARY KEY,
    hostname    TEXT NOT NULL UNIQUE,
    IP          INET NOT NULL,
    STATE       TEXT NOT NULL CHECK (state IN ('active', 'offline', 'retired')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_servers_state ON servers(state);