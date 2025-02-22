from psycopg2 import sql


def get_extract_refreshes_query():
    return sql.SQL(
        """
    WITH
    total_usage as (
      select
        date(bj.created_at) event_date,
        bj.task_id,
        bj.site_id,
        count(*) event_count
      from background_jobs bj
      join tasks t
        on t.id = bj.task_id
       and t.site_id = bj.site_id
      where t.type in ('RefreshExtractTask', 'IncrementExtractTask')
        and bj.finish_code = 0
      group by 1,2,3
    ),
    usage_summary AS (
        SELECT
            task_id,
            site_id,
            max(event_date) last_event_date,
            sum(event_count) AS event_count_total_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from total_usage
        group by 1,2
    ),
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                pc.content_type,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                ARRAY[p.name]::character varying[] AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type in ('datasource', 'workbook')
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                ph.content_type,
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
            content_type,
            replace(
                array_to_json(path)::text, 
                '"', '""'
            ) full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          'EXTRACT_REFRESH' object_type,
          t.luid object_luid,
          null object_size,
          coalesce(w.name, d.name) object_name,
          '{tableau_server_url}' || 
          '/#' ||
          case when s.name <> 'Default' 
          then '/site/' || s.url_namespace
          else ''
          end || 
          '/tasks/extractRefreshes' object_location,
          t.type extract_refresh_type,
          CASE
              WHEN t.state = 0 THEN 'Active'
              WHEN t.state = 1 THEN 'Suspended'
              WHEN t.state = 2 THEN 'Disabled'
              ELSE 'Unknown'
          END object_state,
          t.updated_at object_updated_at,
          CASE
              WHEN sch.schedule_type = 0 THEN 'Hourly'
              WHEN sch.schedule_type = 1 THEN 'Daily'
              WHEN sch.schedule_type = 2 THEN 'Weekly'
              WHEN sch.schedule_type = 3 THEN 'Monthly'
              ELSE 'Unknown'
          END schedule_type,
          coalesce(su.name, csu.name) object_owner_username,
          coalesce(su.friendly_name, csu.friendly_name) object_owner_displayname,
          coalesce(su.email, csu.email) object_owner_email,
          coalesce(w.name, d.name) content_name,
          t.obj_type content_type,
          csu.name content_owner_username,
          csu.friendly_name content_owner_displayname,
          csu.email content_owner_email,
          pp.full_project_path content_full_project_path,
          s.name site_name,
          s.luid site_luid,

          us.event_count_total_nbr event_total_count,
          us.event_count_7d_nbr event_7d_count,
          us.event_count_28d_nbr event_28d_count,
          us.event_count_90d_nbr event_90d_count,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at,
          ((CURRENT_TIMESTAMP AT TIME ZONE 'UTC')::date - us.last_event_date) days_since_last_event
        from tasks t
        join sites s
          on s.id = t.site_id
        left outer join users u
          on u.id = t.creator_id
         and u.site_id = t.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join usage_summary us
          on us.task_id = t.id
         and us.site_id = t.site_id
        left outer join project_path pp
          on pp.content_id = t.obj_id
         and pp.content_type = lower(t.obj_type)
         and pp.site_id = t.site_id
        left outer join workbooks w
          on w.id = t.obj_id
         and t.obj_type = 'Workbook'
         and w.site_id = t.site_id
        left outer join datasources d
          on d.id = t.obj_id
         and t.obj_type = 'Datasource'
         and d.site_id = t.site_id
        left outer join users cu
          on cu.id = coalesce(w.owner_id, d.owner_id)
         and cu.site_id = t.site_id
        left outer join system_users csu
          on csu.id = cu.system_user_id
        left outer join schedules sch
          on sch.id = t.schedule_id
        where t.type in ('RefreshExtractTask', 'IncrementExtractTask')
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
