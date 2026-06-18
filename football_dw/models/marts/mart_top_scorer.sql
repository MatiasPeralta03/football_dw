select
    player_id,
    player,
    team,
    total_goals,
    ROW_NUMBEr() over (
        order by total_goals desc
    ) as rank
from {{ ref('int_top_scorer') }}
order by rank asc