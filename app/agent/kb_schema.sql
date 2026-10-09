-- Additive company-knowledge schema, in the same database as the CRM.
CREATE TABLE IF NOT EXISTS kb_documents (
    doc_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    revision INTEGER NOT NULL CHECK (revision > 0),
    content_hash TEXT NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    search_vector TSVECTOR NOT NULL
);
CREATE INDEX IF NOT EXISTS kb_documents_search ON kb_documents USING GIN(search_vector);
CREATE TABLE IF NOT EXISTS kb_document_versions (
    doc_id TEXT NOT NULL REFERENCES kb_documents(doc_id),
    revision INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    metadata JSONB NOT NULL,
    content_hash TEXT NOT NULL,
    archived BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (doc_id, revision)
);
CREATE TABLE IF NOT EXISTS kb_document_links (
    doc_id TEXT NOT NULL REFERENCES kb_documents(doc_id),
    object_id BIGINT NOT NULL REFERENCES objects(id) ON DELETE CASCADE,
    relation TEXT NOT NULL DEFAULT 'mentions',
    PRIMARY KEY (doc_id, object_id, relation)
);
CREATE INDEX IF NOT EXISTS kb_document_links_object ON kb_document_links(object_id);
CREATE TABLE IF NOT EXISTS agent_users (
    legacy_id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    active BOOLEAN NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS agent_users_email ON agent_users(lower(email));
