CREATE TABLE generation (
    id SERIAL NOT NULL,
    activity_segment_id INTEGER NOT NULL,
    interaction_ids JSON NOT NULL DEFAULT '[]'::json,
    input_text TEXT NOT NULL DEFAULT '',
    output_text TEXT NOT NULL DEFAULT '',
    call_time BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    return_time BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    fields JSON NOT NULL DEFAULT '{}'::json,
    PRIMARY KEY (id)
);
