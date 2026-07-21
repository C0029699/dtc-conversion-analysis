-- new_vs_returning_baseline.sql
-- Establish baseline conversion metrics for new vs. returning visitors
-- Used to size the opportunity before experiment launch

WITH session_base AS (
    SELECT
        s.session_id,
        s.visitor_id,
        s.visitor_type,                  -- 'new' or 'returning' (from Amplitude)
        s.device_category,
        s.traffic_source,
        s.landing_page,
        MAX(CASE WHEN e.event_name = 'add_to_cart' THEN 1 ELSE 0 END)       AS added_to_cart,
        MAX(CASE WHEN e.event_name = 'checkout_started' THEN 1 ELSE 0 END)  AS started_checkout,
        MAX(CASE WHEN e.event_name = 'subscription_created' THEN 1 ELSE 0 END) AS subscribed,
        COALESCE(SUM(e.revenue), 0)                                          AS session_revenue
    FROM sessions s
    LEFT JOIN events e ON s.session_id = e.session_id
    WHERE s.session_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
      AND s.landing_page LIKE '%/daily-synbiotic%'
    GROUP BY 1, 2, 3, 4, 5, 6
)

SELECT
    visitor_type,
    device_category,
    COUNT(session_id)                           AS total_sessions,
    ROUND(AVG(added_to_cart), 4)               AS add_to_cart_rate,
    ROUND(AVG(started_checkout), 4)            AS checkout_rate,
    ROUND(AVG(subscribed), 4)                  AS subscription_rate,
    ROUND(AVG(session_revenue), 2)             AS avg_revenue_per_session,
    -- New visitor gap is our experiment target
    CASE WHEN visitor_type = 'new' THEN 'EXPERIMENT TARGET' ELSE 'CONTROL BASELINE' END AS segment_role
FROM session_base
GROUP BY 1, 2
ORDER BY visitor_type, device_category;
