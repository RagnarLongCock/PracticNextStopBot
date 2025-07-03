DELETE FROM events
WHERE timestamp < extract(epoch from now() - interval '30 days');