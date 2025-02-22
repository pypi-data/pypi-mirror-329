from psycopg2 import sql


def get_datasources_query():
    return sql.SQL(
        """
    WITH
    total_usage as (
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
    usage_summary AS (
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
        from total_usage
        group by 1,2
    ),
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                ARRAY[p.name]::character varying[] AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type = 'datasource'
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                p.id,
                p.name,
                p.parent_project_id,
                ph.level + 1,
                ARRAY[p.name] || ph.path
            FROM project_hierarchy ph
            JOIN projects p ON ph.parent_project_id = p.id
            AND ph.site_id = p.site_id
        )
        SELECT
            site_id,
            content_id,
            replace(
                array_to_json(path)::text, 
                '"', '""'
            ) full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          'DATASOURCE' object_type,
          d.name object_name,
          d.luid object_luid,
          '{tableau_server_url}' || 
          '/#' ||
          case when s.name <> 'Default' 
          then '/site/' || s.url_namespace
          else ''
          end || 
            case 
            when d.connectable
            then '/explore/datasource/' || d.id 
            else '/workbooks/' || d.parent_workbook_id || '/datasources' 
            end 
          object_location,
          d.size object_size,
          d.db_class object_db_class,
          d.connectable object_connectable,
          d.updated_at object_updated_at,
          w.name parent_workbook_name,
          w.luid parent_workbook_luid,
          su.name object_owner_username,
          su.friendly_name object_owner_displayname,
          su.email object_owner_email,
          pp.full_project_path object_full_project_path,
          s.name site_name,
          s.luid site_luid,

          us.unique_users_total_nbr unique_users_total_count,
          us.unique_users_7d_nbr unique_users_7d_count,
          us.unique_users_28d_nbr unique_users_28d_count,
          us.unique_users_90d_nbr unique_users_90d_count,

          us.event_count_total_nbr event_count_total_count,
          us.event_count_7d_nbr event_count_7d_count,
          us.event_count_28d_nbr event_count_28d_count,
          us.event_count_90d_nbr event_count_90d_count,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at,
          ((CURRENT_TIMESTAMP AT TIME ZONE 'UTC')::date - us.last_event_date) days_since_last_event
        from datasources d
        join sites s
          on s.id = d.site_id
        left outer join workbooks w
          on w.id = d.parent_workbook_id
         and w.site_id = d.site_id
        left outer join users u
          on u.id = d.owner_id
         and u.site_id = d.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join project_path pp
          on pp.content_id = d.id
         and pp.site_id = d.site_id
        left outer join usage_summary us
          on us.datasource_id = d.id
         and us.site_id = d.site_id
    )
    select * from final
    WHERE (%(owner_username)s::text IS NULL OR object_owner_username = %(owner_username)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    AND (%(luid)s::text IS NULL OR object_luid::text = %(luid)s::text)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )
