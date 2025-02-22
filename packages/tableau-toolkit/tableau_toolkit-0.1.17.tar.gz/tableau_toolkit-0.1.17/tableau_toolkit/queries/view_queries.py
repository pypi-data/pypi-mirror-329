from psycopg2 import sql


def get_views_query():
    query = sql.SQL(
        """
    WITH
    performance_parser AS (
        SELECT
            CASE
                WHEN COALESCE(h.currentsheet, '') = '' OR h.currentsheet LIKE '%% %%' OR currentsheet LIKE '%%/null'
                THEN
                    SPLIT_PART(
                        CASE SPLIT_PART(http_request_uri, '/', 2)
                            WHEN 'views' THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                            WHEN 't' THEN SPLIT_PART(http_request_uri, '/', 5) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 6), '?', 1)
                            WHEN 'trusted' THEN SPLIT_PART(http_request_uri, '/', 5) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 6), '?', 1)
                            WHEN 'vizql' THEN
                                CASE SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 3)
                                    WHEN 'w' THEN
                                        CASE
                                            WHEN LEFT(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), 12) = '/vizql/w/ds:'
                                            THEN REPLACE(SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 4), 'ds:', '')
                                            ELSE SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 4)
                                        END ||
                                        CASE
                                            WHEN SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 6) = 'null'
                                            THEN ''
                                            ELSE '/' || SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 6)
                                        END
                                    WHEN 'authoring' THEN ''
                                    ELSE ''
                                END
                            WHEN 'askData' THEN SPLIT_PART(http_request_uri, '/', 3)
                            WHEN 'authoringNewWorkbook' THEN SPLIT_PART(http_request_uri, '/', 4)
                            WHEN 'authoring' THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                            WHEN 'startAskData' THEN SPLIT_PART(SPLIT_PART(http_request_uri, '/', 3), '?', 1)
                            WHEN 'offline_views' THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                            ELSE NULL
                        END,
                        '.',
                        1
                    )
                ELSE
                    CASE WHEN ( LEFT(currentsheet, 3) = 'ds:' OR LEFT(http_request_uri, 22) = '/authoringNewWorkbook/' OR LEFT(http_request_uri, 12) = '/vizql/w/ds:')
                    THEN
                        SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 1)
                    ELSE
                        SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 1)
                        || '/' ||
                        SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 2)
                    END
            END AS item_repository_url,
            CASE
                WHEN currentsheet LIKE 'ds:%%' OR LEFT(http_request_uri, 12) = '/vizql/w/ds:' OR LEFT(http_request_uri, 9) = '/askData/'
                THEN 'Data Source'
                WHEN http_request_uri LIKE '/authoringNewWorkbook/%%'
                OR 
                SPLIT_PART(
                    REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'),
                    '/',
                    6
                ) = 'null'
                AND
                currentsheet NOT LIKE '%%/%%'
                THEN 'Workbook'
                ELSE 'View'
            END AS item_type,
            h.site_id,
            date(h.created_at) event_date,
            sum(EXTRACT(EPOCH FROM (h.completed_at - h.created_at))) AS duration_secs_total_nbr,
            count(*) as event_count_total_nbr
        FROM http_requests AS h
        LEFT JOIN sites AS s ON h.site_id = s.id
        WHERE action = 'bootstrapSession'
        AND LEFT(CAST(h.status AS TEXT), 1) = '2'
        group by 1,2,3,4
    ),
    performance_summary AS (
        SELECT
        REPLACE(item_repository_url, '/', '/sheets/') AS view_repository_url,
        site_id,

        sum(duration_secs_total_nbr) / 
        NULLIF(sum(event_count_total_nbr), 0) AS duration_secs_avg_total_nbr,

        sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '7 days' THEN duration_secs_total_nbr ELSE 0 END) / 
        NULLIF(sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '7 days' THEN event_count_total_nbr ELSE 0 END), 0) AS duration_secs_avg_7d_nbr,

        sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '28 days' THEN duration_secs_total_nbr ELSE 0 END) / 
        NULLIF(sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '28 days' THEN event_count_total_nbr ELSE 0 END), 0) AS duration_secs_avg_28d_nbr,

        sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '90 days' THEN duration_secs_total_nbr ELSE 0 END) / 
        NULLIF(sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '90 days' THEN event_count_total_nbr ELSE 0 END), 0) AS duration_secs_avg_90d_nbr
        FROM performance_parser pp
        WHERE item_type = 'View'
        GROUP BY 1, 2
    ),
    total_usage as (
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
    usage_summary AS (
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
          'VIEW' object_type,
          v.name object_name,
          v.luid object_luid,
          '{tableau_server_url}' || 
          '/#' ||
           case when s.name <> 'Default' 
           then '/site/' || s.url_namespace
           else ''
           end || 
           '/views/' || replace(v.repository_url, '/sheets', '') object_location,
          null object_size,
          v.updated_at object_updated_at,
          su.name object_owner_username,
          su.friendly_name object_owner_displayname,
          su.email object_owner_email,
          pp.full_project_path object_full_project_path,
          s.name site_name,
          s.luid site_luid,

          ps.duration_secs_avg_total_nbr duration_avg_total_secs,
          ps.duration_secs_avg_7d_nbr duration_avg_7d_secs,
          ps.duration_secs_avg_28d_nbr duration_avg_28d_secs,
          ps.duration_secs_avg_90d_nbr duration_avg_90d_secs,

          us.unique_users_total_nbr unique_users_total_count,
          us.unique_users_7d_nbr unique_users_7d_count,
          us.unique_users_28d_nbr unique_users_28d_count,
          us.unique_users_90d_nbr unique_users_90d_count,

          us.event_count_total_nbr event_total_count,
          us.event_count_7d_nbr event_7d_count,
          us.event_count_28d_nbr event_28d_count,
          us.event_count_90d_nbr event_90d_count,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at,
          ((CURRENT_TIMESTAMP AT TIME ZONE 'UTC')::date - us.last_event_date) days_since_last_event
        from views v
        join sites s
          on s.id = v.site_id
        left outer join users u
          on u.id = v.owner_id
         and u.site_id = v.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join project_path pp
          on pp.content_id = v.workbook_id
         and pp.site_id = v.site_id
        left outer join performance_summary ps
          on ps.view_repository_url = v.repository_url
         and ps.site_id = v.site_id
        left outer join usage_summary us
          on us.view_id = v.id
         and us.site_id = v.site_id
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

    return query
