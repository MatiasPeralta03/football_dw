select 
    avg(first_goal_minute)
from(
    select
        match_id,
        MIN(minute) as first_goal_minute
    from {{ ref('int_goals') }}
    group by match_id
) as first_goal