select
    player_id,
    player,
    team,
    count(*) as total_goals
from {{ ref ('stg_events_shots') }}
where shot_outcome = 'Goal'
group by 1, 2, 3