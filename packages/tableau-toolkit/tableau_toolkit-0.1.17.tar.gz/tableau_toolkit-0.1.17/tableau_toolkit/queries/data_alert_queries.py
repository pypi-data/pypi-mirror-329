from psycopg2 import sql


def get_data_alerts_query():
    return sql.SQL(
        """
    with
    total_usage as (
    select
    date(created_at) event_date,
    SPLIT_PART(SPLIT_PART(he.details, 'dataAlertId:', 2), ',', 1)::int AS data_alert_id,
    SPLIT_PART(SPLIT_PART(he.details, 'siteId:', 2), ',', 1)::int AS site_id,
    SPLIT_PART(SPLIT_PART(he.details, 'userId:', 2), ',', 1)::int user_id,
    count(*) event_count
    from historical_events he
    where he.historical_event_type_id = 236
    group by 1,2,3,4
    ),
    usage_summary as (
    select
        data_alert_id,
        site_id,
        max(event_date) last_event_date,
        count(distinct user_id) unique_users_total_nbr,
        sum(event_count) event_count_total_nbr,
                    
        count(distinct case when event_date >= CURRENT_DATE - INTERVAL '7 days' then user_id end) unique_users_7d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) event_count_7d_nbr,
                    
        count(distinct case when event_date >= CURRENT_DATE - INTERVAL '28 days' then user_id end) unique_users_28d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) event_count_28d_nbr,
                    
        count(distinct case when event_date >= CURRENT_DATE - INTERVAL '90 days' then user_id end) unique_users_90d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '90 days' then event_count else 0 end) event_count_90d_nbr
    from total_usage
    group by 1,2
    ),
    final as (
    select
    'DATA_ALERT' object_type,
    da.luid object_luid,
    da.title object_name,
    '{tableau_server_url}' || 
    '/#' ||
    case when s.name <> 'Default' 
    then '/site/' || s.url_namespace
    else ''
    end || 
    '/tasks/dataAlerts' object_location,
    null object_size,
    da.updated_at object_updated_at,
    su.name object_owner_username,
    su.friendly_name object_owner_displayname,
    su.email object_owner_email,
    s.luid site_luid,
    s.name site_name,

    summ.unique_users_total_nbr unique_users_total_count,
    summ.unique_users_7d_nbr unique_users_7d_count,
    summ.unique_users_28d_nbr unique_users_28d_count,
    summ.unique_users_90d_nbr unique_users_90d_count,

    summ.event_count_total_nbr event_total_count,
    summ.event_count_7d_nbr event_7d_count,
    summ.event_count_28d_nbr event_28d_count,
    summ.event_count_90d_nbr event_90d_count,

    summ.last_event_date,
    CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at,
    ((CURRENT_TIMESTAMP AT TIME ZONE 'UTC')::date - summ.last_event_date) days_since_last_event
    from data_alerts da
    join sites s
    on s.id = da.site_id
    left join users u
    on u.id = da.creator_id
    and u.site_id = da.site_id
    left join system_users su
    on su.id = u.system_user_id
    left join usage_summary summ
    on summ.data_alert_id = da.id
    and summ.site_id = da.site_id
    )
    select * from final
    WHERE (%(owner_username)s::text IS NULL OR object_owner_username = %(owner_username)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )
