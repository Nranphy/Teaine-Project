CREATE TABLE activity_segment (
    id SERIAL NOT NULL,
    type VARCHAR NOT NULL,
    activity_id INTEGER NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    start_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    end_timestamp BIGINT,
    fields JSON NOT NULL DEFAULT '{}'::json,
    created_at BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (id)
);
