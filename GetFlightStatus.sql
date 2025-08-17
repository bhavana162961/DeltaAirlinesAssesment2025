WITH cte AS (
    SELECT
        flightkey,
        flightnum,
        flight_dt,
        orig_arpt,
        dest_arpt,
        flightstatus,
        lastupdt,
        ROW_NUMBER() OVER (
            PARTITION BY flightkey
            ORDER BY lastupdt DESC
        ) AS rn
    FROM flight_leg
)
SELECT
    flightkey,
    flightnum,
    flight_dt,
    orig_arpt,
    dest_arpt,
    flightstatus,
    lastupdt
FROM cte
WHERE rn = 1;
