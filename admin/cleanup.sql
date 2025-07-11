DELETE FROM events
WHERE timestamp < extract(epoch from now() - interval '5 seconds');