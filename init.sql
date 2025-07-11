-- Table: public.events

-- DROP TABLE IF EXISTS public.events;

CREATE TABLE IF NOT EXISTS public.events
(
    id integer NOT NULL DEFAULT nextval('events_id_seq'::regclass),
    sender_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    type_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    "timestamp" double precision,
    intent_name character varying(255) COLLATE pg_catalog."default",
    action_name character varying(255) COLLATE pg_catalog."default",
    data text COLLATE pg_catalog."default",
    CONSTRAINT events_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.events
    OWNER to postgres;
-- Index: ix_events_sender_id

-- DROP INDEX IF EXISTS public.ix_events_sender_id;

CREATE INDEX IF NOT EXISTS ix_events_sender_id
    ON public.events USING btree
    (sender_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;