select
    player_id,
    player,
    team,
    minute,
    match_id
from {{ ref('stg_events_shots') }}
where shot_outcome = 'Goal'