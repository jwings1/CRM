-- Idempotent schema. Applied on every boot (CREATE ... IF NOT EXISTS).

CREATE SEQUENCE IF NOT EXISTS object_id_seq START 1001;
CREATE SEQUENCE IF NOT EXISTS list_id_seq START 1;
CREATE SEQUENCE IF NOT EXISTS pipeline_id_seq START 1000;

CREATE TABLE IF NOT EXISTS objects (
    id           BIGINT PRIMARY KEY DEFAULT nextval('object_id_seq'),
    object_type  TEXT NOT NULL,
    properties   JSONB NOT NULL DEFAULT '{}'::jsonb,   -- values are strings
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    archived     BOOLEAN NOT NULL DEFAULT false,
    archived_at  TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS objects_type_id   ON objects (object_type, id);
CREATE INDEX IF NOT EXISTS objects_legacy    ON objects (object_type, (properties->>'id_legacy'));
CREATE INDEX IF NOT EXISTS objects_email     ON objects (lower(properties->>'email')) WHERE object_type = 'contacts';
CREATE INDEX IF NOT EXISTS objects_domain    ON objects (lower(properties->>'domain')) WHERE object_type = 'companies';
-- HubSpot: one live contact per email.
CREATE UNIQUE INDEX IF NOT EXISTS contacts_email_uq ON objects (lower(properties->>'email'))
    WHERE object_type = 'contacts' AND NOT archived AND coalesce(properties->>'email', '') <> '';

-- Both directions are stored. ids are global (one sequence for all types).
CREATE TABLE IF NOT EXISTS associations (
    from_type  TEXT   NOT NULL,
    from_id    BIGINT NOT NULL,
    to_type    TEXT   NOT NULL,
    to_id      BIGINT NOT NULL,
    category   TEXT   NOT NULL DEFAULT 'HUBSPOT_DEFINED',
    type_id    INT    NOT NULL,
    PRIMARY KEY (from_id, to_type, to_id, category, type_id)
);
CREATE INDEX IF NOT EXISTS associations_to ON associations (to_id);

-- hasUniqueValue properties (R7 partita_iva). Insert in the same txn as the write.
CREATE TABLE IF NOT EXISTS unique_values (
    object_type TEXT   NOT NULL,
    property    TEXT   NOT NULL,
    value       TEXT   NOT NULL,
    object_id   BIGINT NOT NULL,
    PRIMARY KEY (object_type, property, value)
);
CREATE INDEX IF NOT EXISTS unique_values_obj ON unique_values (object_id);

CREATE TABLE IF NOT EXISTS property_groups (
    object_type   TEXT NOT NULL,
    name          TEXT NOT NULL,
    label         TEXT NOT NULL,
    display_order INT  NOT NULL DEFAULT -1,
    archived      BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (object_type, name)
);

CREATE TABLE IF NOT EXISTS property_defs (
    object_type      TEXT NOT NULL,
    name             TEXT NOT NULL,
    label            TEXT NOT NULL DEFAULT '',
    type             TEXT NOT NULL DEFAULT 'string',
    field_type       TEXT NOT NULL DEFAULT 'text',
    group_name       TEXT NOT NULL DEFAULT '',
    description      TEXT NOT NULL DEFAULT '',
    options          JSONB NOT NULL DEFAULT '[]'::jsonb,
    display_order    INT  NOT NULL DEFAULT -1,
    has_unique_value BOOLEAN NOT NULL DEFAULT false,
    hidden           BOOLEAN NOT NULL DEFAULT false,
    form_field       BOOLEAN NOT NULL DEFAULT true,
    calculated       BOOLEAN NOT NULL DEFAULT false,
    read_only        BOOLEAN NOT NULL DEFAULT false,
    hubspot_defined  BOOLEAN NOT NULL DEFAULT false,
    archived         BOOLEAN NOT NULL DEFAULT false,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (object_type, name)
);

CREATE TABLE IF NOT EXISTS pipelines (
    object_type   TEXT NOT NULL,
    id            TEXT NOT NULL,
    label         TEXT NOT NULL,
    display_order INT  NOT NULL DEFAULT 0,
    archived      BOOLEAN NOT NULL DEFAULT false,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (object_type, id)
);

-- stage ids are unique per object type (HubSpot behaviour)
CREATE TABLE IF NOT EXISTS pipeline_stages (
    object_type   TEXT NOT NULL,
    pipeline_id   TEXT NOT NULL,
    id            TEXT NOT NULL,
    label         TEXT NOT NULL,
    display_order INT  NOT NULL DEFAULT 0,
    metadata      JSONB NOT NULL DEFAULT '{}'::jsonb,
    archived      BOOLEAN NOT NULL DEFAULT false,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (object_type, id)
);

CREATE TABLE IF NOT EXISTS lists (
    list_id         BIGINT PRIMARY KEY DEFAULT nextval('list_id_seq'),
    name            TEXT NOT NULL,
    object_type_id  TEXT NOT NULL,
    processing_type TEXT NOT NULL DEFAULT 'MANUAL',
    filter_branch   JSONB,
    archived        BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS list_memberships (
    list_id   BIGINT NOT NULL,
    record_id BIGINT NOT NULL,
    added_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (list_id, record_id)
);

-- R10/R11 "once per deal": INSERT ... ON CONFLICT DO NOTHING decides who fires.
CREATE TABLE IF NOT EXISTS automation_log (
    rule       TEXT   NOT NULL,
    object_id  BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (rule, object_id)
);

CREATE TABLE IF NOT EXISTS exports (
    id           BIGINT PRIMARY KEY,
    status       TEXT NOT NULL DEFAULT 'PENDING',
    request      JSONB,
    file_token   TEXT,
    content      BYTEA,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ
);
