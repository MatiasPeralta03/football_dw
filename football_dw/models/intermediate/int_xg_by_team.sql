select
    team,
    count(*) as total_shots_per_team,
    avg(shot_statsbomb_xg) as avg_shots,
    sum(shot_statsbomb_xg) as total_acumulative
from {{ ref('stg_events_shots' )}}
group by team
order by 1 
