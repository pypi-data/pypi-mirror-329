from psycopg2 import sql


def get_groups_query():
    return sql.SQL(
        """
    WITH
    ds_total_usage as (
      select
        date(he.created_at) event_date,
        d.id datasource_id,
        hs.site_id,
        he.hist_actor_user_id,
        count(*) event_count
      from historical_events he
      join hist_datasources hd
        on he.hist_datasource_id = hd.id
      join hist_sites hs
        on hs.id = he.hist_target_site_id
      join datasources d
        on d.id = hd.datasource_id and d.site_id = hs.site_id
      group by 1,2,3,4
    ),
    ds_usage_summary AS (
        SELECT
            datasource_id,
            site_id,
            max(event_date) last_event_date,

            COUNT(DISTINCT hist_actor_user_id) AS unique_users_total_nbr,
            sum(event_count) AS event_count_total_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '7 days' then hist_actor_user_id end) AS unique_users_7d_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '28 days' then hist_actor_user_id end) AS unique_users_28d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '90 days' then hist_actor_user_id end) AS unique_users_90d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from ds_total_usage
        group by 1,2
    ),
    wb_total_usage as (
      select
        date(he.created_at) event_date,
        v.workbook_id,
        hs.site_id,
        he.hist_actor_user_id,
        count(*) event_count
      from historical_events he
      join hist_views hv 
        on he.hist_view_id = hv.id
      join hist_sites hs
        on hs.id = he.hist_target_site_id
      join views v
        on v.id = hv.view_id and v.site_id = hs.site_id
      group by 1,2,3,4
    ),
    wb_usage_summary AS (
        SELECT
            workbook_id,
            site_id,
            max(event_date) last_event_date,

            COUNT(DISTINCT hist_actor_user_id) AS unique_users_total_nbr,
            sum(event_count) AS event_count_total_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '7 days' then hist_actor_user_id end) AS unique_users_7d_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '28 days' then hist_actor_user_id end) AS unique_users_28d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '90 days' then hist_actor_user_id end) AS unique_users_90d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from wb_total_usage
        group by 1,2
    ),
    view_total_usage as (
      select
        date(he.created_at) event_date,
        v.id view_id,
        hs.site_id,
        he.hist_actor_user_id,
        count(*) event_count
      from historical_events he
      join hist_views hv 
        on he.hist_view_id = hv.id
      join hist_sites hs
        on hs.id = he.hist_target_site_id
      join views v
        on v.id = hv.view_id and v.site_id = hs.site_id
      group by 1,2,3,4
    ),
    view_usage_summary AS (
        SELECT
            view_id,
            site_id,
            max(event_date) last_event_date,

            COUNT(DISTINCT hist_actor_user_id) AS unique_users_total_nbr,
            sum(event_count) AS event_count_total_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '7 days' then hist_actor_user_id end) AS unique_users_7d_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '28 days' then hist_actor_user_id end) AS unique_users_28d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '90 days' then hist_actor_user_id end) AS unique_users_90d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from view_total_usage
        group by 1,2
    ),
    group_usage_summary as (
      select
        'View' authorizable_type,
        view_id authorizable_id,
        site_id,
        unique_users_total_nbr,
        unique_users_7d_nbr,
        unique_users_28d_nbr,
        unique_users_90d_nbr,

        event_count_total_nbr,
        event_count_7d_nbr,
        event_count_28d_nbr,
        event_count_90d_nbr
      from view_usage_summary

      union all

      select
        'Datasource' authorizable_type,
        datasource_id authorizable_id,
        site_id,
        unique_users_total_nbr,
        unique_users_7d_nbr,
        unique_users_28d_nbr,
        unique_users_90d_nbr,

        event_count_total_nbr,
        event_count_7d_nbr,
        event_count_28d_nbr,
        event_count_90d_nbr
      from ds_usage_summary

      union all

      select
        'Workbook' authorizable_type,
        workbook_id authorizable_id,
        site_id,
        unique_users_total_nbr,
        unique_users_7d_nbr,
        unique_users_28d_nbr,
        unique_users_90d_nbr,

        event_count_total_nbr,
        event_count_7d_nbr,
        event_count_28d_nbr,
        event_count_90d_nbr
      from wb_usage_summary
    ),
    site_md as (
        select
          s.luid,
          max(s.id) site_id,
          max(s.name) site_name,
          max(s.url_namespace) site_url_namespace,
          replace(
            to_json(json_agg(su.name))::text, 
            '"', '""'
          ) AS site_admin_usernames,
          replace(
            to_json(json_agg(su.friendly_name))::text, 
            '"', '""'
          ) AS site_admin_displaynames,
          replace(
            to_json(json_agg(su.email))::text, 
            '"', '""'
          ) AS site_admin_emails
        from sites s
        left join users u
          on u.site_id = s.id
         and u.site_role_id in (0,11) -- SiteAdministratorExplorer, SiteAdministratorCreator
        left join system_users su
          on su.id = u.system_user_id
        group by s.luid
    ),
    next_gen_permissions_md as (
        select
            grantee_id,
            grantee_type,
            site_id,
            authorizable_id,
            authorizable_type
        from next_gen_permissions
        where grantee_type = 'Group'
        group by 1,2,3,4,5
    ),
    final as (
    SELECT 
        'GROUP' object_type,
        g.luid object_luid,
        max(g.name) AS object_name,
        '{tableau_server_url}' || 
        '/#' ||
        case when max(s.site_name) <> 'Default' 
        then '/site/' || max(s.site_url_namespace)
        else ''
        end || 
        '/groups/' || max(g.id) || '/users' object_location,
        null object_size,
        max(g.grant_license_mode) AS object_grant_license_mode,
        s.luid site_luid,
        max(s.site_name) site_name,
        max(s.site_admin_usernames) site_admin_usernames,
        max(s.site_admin_displaynames) site_admin_displaynames,
        max(s.site_admin_emails) site_admin_emails,
        max(user_count) group_user_count,
        COUNT(DISTINCT ngp.authorizable_id) AS group_object_reference_count,
        sum(coalesce(unique_users_total_nbr, 0)) as unique_users_total_count,
        sum(coalesce(unique_users_7d_nbr, 0)) as unique_users_7d_count,
        sum(coalesce(unique_users_28d_nbr, 0)) as unique_users_28d_count,
        sum(coalesce(unique_users_90d_nbr, 0)) as unique_users_90d_count,

        sum(coalesce(event_count_total_nbr, 0)) as event_total_count,
        sum(coalesce(event_count_7d_nbr, 0)) as event_7d_count,
        sum(coalesce(event_count_28d_nbr, 0)) as event_28d_count,
        sum(coalesce(event_count_90d_nbr, 0)) as event_90d_count,
        CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
    FROM groups g
    left join group_users_count gc
      on gc.group_id = g.id and gc.site_id = g.site_id
    left join site_md s
      on s.site_id = g.site_id
    left JOIN next_gen_permissions_md ngp 
      ON g.id = ngp.grantee_id
     and g.site_id = ngp.site_id
    left join group_usage_summary gu
      on gu.authorizable_id = ngp.authorizable_id
     and gu.site_id = ngp.site_id
     and gu.authorizable_type = ngp.authorizable_type
    GROUP BY s.luid, g.luid
    )
    select * from final
    WHERE (%(site_admin_username)s::text IS NULL OR object_name LIKE '%%' || %(site_admin_username)s::text || '%%')
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    AND (%(exclude_grant_license_mode)s::boolean IS FALSE OR object_grant_license_mode IS NULL)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )
