-- lists Glam rock bands 
SELECT
    band_name,
    CASE
        WHEN split = 0 OR split IS NULL THEN 2024 - formed
        ELSE split - formed
    END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
