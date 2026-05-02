-- Capital Projects: Data Center Portfolio Analysis

-- Query 0: Row count verification across all tables
SELECT 'projects' as table_name, COUNT(*) as row_count FROM projects
UNION ALL
SELECT 'contracts', COUNT(*) FROM contracts
UNION ALL
SELECT 'change_events', COUNT(*) FROM change_events
UNION ALL
SELECT 'rfis', COUNT(*) FROM rfis
UNION ALL
SELECT 'submittals', COUNT(*) FROM submittals
UNION ALL
SELECT 'budget_tracking', COUNT(*) FROM budget_tracking;

-- Query 1: Budget variance by project
SELECT
    p.project_id,
    p.project_name,
    p.location,
    p.project_manager,
    p.total_budget,
    SUM(bt.actual_spend) AS total_actual_spend,
    SUM(bt.actual_spend) - p.total_budget AS budget_variance,
    ROUND((SUM(bt.actual_spend) - p.total_budget) / p.total_budget * 100, 2) AS variance_pct
FROM projects p
JOIN budget_tracking bt ON p.project_id = bt.project_id
GROUP BY p.project_id, p.project_name, p.location, p.project_manager, p.total_budget
ORDER BY budget_variance DESC;

-- Query 2: Change order cost impact by project
SELECT
    p.project_id,
    p.project_name,
    COUNT(ce.change_event_id) AS total_change_events,
    SUM(ce.cost_impact) AS total_cost_impact,
    AVG(ce.cost_impact) AS avg_cost_impact,
    SUM(ce.schedule_impact_days) AS total_schedule_impact_days
FROM projects p
JOIN change_events ce ON p.project_id = ce.project_id
GROUP BY p.project_id, p.project_name
ORDER BY total_cost_impact DESC;

-- Query 3: RFI volume and average response time by project
SELECT
    p.project_id,
    p.project_name,
    COUNT(r.rfi_id) AS total_rfis,
    SUM(CASE WHEN r.status = 'Open' THEN 1 ELSE 0 END) AS open_rfis,
    SUM(CASE WHEN r.status = 'Closed' THEN 1 ELSE 0 END) AS closed_rfis,
    SUM(CASE WHEN r.led_to_change_event = TRUE THEN 1 ELSE 0 END) AS led_to_change,
    ROUND(AVG(CASE WHEN r.date_responded IS NOT NULL 
        THEN (r.date_responded - r.date_submitted) 
        ELSE NULL END), 1) AS avg_response_days
FROM projects p
JOIN rfis r ON p.project_id = r.project_id
GROUP BY p.project_id, p.project_name
ORDER BY total_rfis DESC;

-- Query 4: Change event breakdown by type and reason
SELECT
    event_type,
    reason,
    COUNT(*) AS total_events,
    SUM(cost_impact) AS total_cost_impact,
    ROUND(AVG(cost_impact), 2) AS avg_cost_impact
FROM change_events
GROUP BY event_type, reason
ORDER BY total_cost_impact DESC;

-- Query 5: Submittal status detail by project
SELECT project_name, 'Approved' as status, approved as count FROM vw_submittal_summary
UNION ALL SELECT project_name, 'Approved as Noted', approved_as_noted FROM vw_submittal_summary
UNION ALL SELECT project_name, 'Revise and Resubmit', revise_resubmit FROM vw_submittal_summary
UNION ALL SELECT project_name, 'Rejected', rejected FROM vw_submittal_summary
UNION ALL SELECT project_name, 'Pending', pending FROM vw_submittal_summary
ORDER BY project_name, status;

-- Query 6: Planned vs actual spend over time by project
SELECT
    p.project_name,
    bt.period_date,
    bt.planned_spend,
    bt.actual_spend,
    bt.cumulative_planned,
    bt.cumulative_actual,
    ROUND(bt.cumulative_actual - bt.cumulative_planned, 2) AS cumulative_variance
FROM projects p
JOIN budget_tracking bt ON p.project_id = bt.project_id
ORDER BY p.project_id, bt.period_date;