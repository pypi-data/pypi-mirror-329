from psycopg2 import sql


def get_users_query():
    return sql.SQL(
        """
    with
    total_usage as (
    select
    date(he.created_at) event_date,
    et.action_type,
    hs.site_id,
    hu.user_id,
    count(*) event_count
    from historical_events he
    join historical_event_types et
      on et.type_id = he.historical_event_type_id
    join hist_sites hs
      on hs.id = he.hist_actor_site_id
    join hist_users hu
      on hu.id = he.hist_actor_user_id
    group by 1,2,3,4
    ),
    usage_summary as (
    select
        user_id,
        site_id,
        max(event_date) last_event_date,
        sum(event_count) event_count_total_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '7 days' then 1 else 0 end) event_count_7d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '28 days' then 1 else 0 end) event_count_28d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) event_count_90d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '180 days' then 1 else 0 end) event_count_180d_nbr,

        sum(case when action_type = 'Access' then event_count else 0 end) access_event_count_total_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) access_event_count_7d_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) access_event_count_28d_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) access_event_count_90d_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '180 days' then 1 else 0 end) access_event_count_180d_nbr,

        sum(case when action_type = 'Create' then event_count else 0 end) create_event_count_total_nbr,
        sum(case when action_type = 'Create' and event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) create_event_count_7d_nbr,
        sum(case when action_type = 'Create' and event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) create_event_count_28d_nbr,
        sum(case when action_type = 'Create' and event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) create_event_count_90d_nbr,
        sum(case when action_type = 'Create' and event_date >= CURRENT_DATE - INTERVAL '180 days' then 1 else 0 end) create_event_count_180d_nbr,

        sum(case when action_type = 'Publish' then event_count else 0 end) publish_event_count_total_nbr,
        sum(case when action_type = 'Publish' and event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) publish_event_count_7d_nbr,
        sum(case when action_type = 'Publish' and event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) publish_event_count_28d_nbr,
        sum(case when action_type = 'Publish' and event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) publish_event_count_90d_nbr,
        sum(case when action_type = 'Publish' and event_date >= CURRENT_DATE - INTERVAL '180 days' then 1 else 0 end) publish_event_count_180d_nbr
    from total_usage
    group by 1,2
    ),
    final as (
    select
    'USER' object_type,
    u.luid object_luid,
    '{tableau_server_url}' || 
    '/#' ||
    case when s.name <> 'Default' 
    then '/site/' || s.url_namespace
    else ''
    end || 
    '/user/' || d.name || '/' || su.name object_location,
    su.name object_username,
    su.friendly_name object_displayname,
    su.email object_email,
    REGEXP_REPLACE(sr.display_name, '[\\s()]', '', 'g') site_role_name,
    u.system_admin_auto,
    s.luid site_luid,
    s.name site_name,

    summ.event_count_total_nbr event_total_count,
    summ.event_count_7d_nbr event_7d_count,
    summ.event_count_28d_nbr event_28d_count,
    summ.event_count_90d_nbr event_90d_count,
    summ.event_count_180d_nbr event_180d_count,

    summ.access_event_count_total_nbr access_event_total_count,
    summ.access_event_count_7d_nbr access_event_7d_count,
    summ.access_event_count_28d_nbr access_event_28d_count,
    summ.access_event_count_90d_nbr access_event_90d_count,
    summ.access_event_count_180d_nbr access_event_180d_count,

    summ.create_event_count_total_nbr create_event_total_count,
    summ.create_event_count_7d_nbr create_event_7d_count,
    summ.create_event_count_28d_nbr create_event_28d_count,
    summ.create_event_count_90d_nbr create_event_90d_count,
    summ.create_event_count_180d_nbr create_event_180d_count,

    summ.publish_event_count_total_nbr publish_event_total_count,
    summ.publish_event_count_7d_nbr publish_event_7d_count,
    summ.publish_event_count_28d_nbr publish_event_28d_count,
    summ.publish_event_count_90d_nbr publish_event_90d_count,
    summ.publish_event_count_180d_nbr publish_event_180d_count,

    summ.last_event_date,
    CURRENT_TIMESTAMP AT TIME ZONE 'UTC' snapshot_at,
    ((CURRENT_TIMESTAMP AT TIME ZONE 'UTC')::date - summ.last_event_date) days_since_last_event
    from system_users su
    join domains d
      on d.id = su.domain_id
    join users u
      on u.system_user_id = su.id
    join site_roles sr
      on sr.id = u.site_role_id
    join sites s
      on s.id = u.site_id
    left join usage_summary summ
      on summ.user_id = u.id
     and summ.site_id = u.site_id
    )
    select * from final
    WHERE (%(username)s::text IS NULL OR object_username = %(username)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    AND (%(exclude_unlicensed)s::boolean IS FALSE OR site_role_name <> 'Unlicensed')
    AND (%(exclude_guest)s::boolean IS FALSE OR site_role_name <> 'Guest')
    AND (%(exclude_has_email)s::boolean IS FALSE OR object_email is null)
    AND (%(exclude_system_admin_auto)s::boolean IS FALSE OR not system_admin_auto)
    AND (not %(only_inactive_180d)s::boolean or (event_180d_count = 0 or event_180d_count is null))
    AND object_username <> '_system'
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )
