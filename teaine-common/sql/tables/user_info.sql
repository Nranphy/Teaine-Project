CREATE TABLE user_info (
    id SERIAL NOT NULL,
    main_id INTEGER,
    platform VARCHAR NOT NULL,
    platform_user_id VARCHAR NOT NULL,
    platform_user_name VARCHAR NOT NULL DEFAULT '',
    platform_fields JSON NOT NULL DEFAULT '{}'::json,
    description TEXT NOT NULL DEFAULT '',
    register_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT uq_user_info_platform_user_id UNIQUE (platform, platform_user_id)
);
