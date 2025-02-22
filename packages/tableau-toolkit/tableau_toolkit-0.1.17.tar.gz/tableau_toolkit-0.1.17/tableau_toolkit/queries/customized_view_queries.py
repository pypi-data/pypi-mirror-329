from psycopg2 import sql


def get_customized_views_query():
    return sql.SQL(
        """
    WITH
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
        WHERE pc.content_type = 'workbook'
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
          'CUSTOMIZED_VIEW' object_type,
          v.name object_name,
          v.luid object_luid,
          '{tableau_server_url}' || 
          '/#' ||
           case when s.name <> 'Default' 
           then '/site/' || s.url_namespace
           else ''
           end || 
           '/views/' || replace(vv.repository_url, '/sheets', '') || 
           '/' || v.luid || 
           '/' || v.url_id object_location,
          null object_size,
          v.modified_at object_updated_at,
          su.name object_owner_username,
          su.friendly_name object_owner_displayname,
          su.email object_owner_email,
          pp.full_project_path object_full_project_path,
          s.name site_name,
          s.luid site_luid,
          date(v.accessed_at) last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
        from customized_views v
        join sites s
          on s.id = v.site_id
        join views vv
          on vv.id = v.view_id
         and vv.site_id = v.site_id
        left outer join users u
          on u.id = vv.owner_id
         and u.site_id = vv.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join project_path pp
          on pp.content_id = vv.workbook_id
         and pp.site_id = vv.site_id
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
