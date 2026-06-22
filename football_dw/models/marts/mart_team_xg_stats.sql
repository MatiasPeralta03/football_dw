select 
    tm.team,
    xg.total_acumulative,
    sum(tm.goals_for) as total_goals,
    sum(tm.goals_for) / xg.total_acumulative as shot_efficiency
from {{ ref('int_team_matches' )}} as tm
inner join {{ ref('int_xg_by_team' )}} as xg on tm.team = xg.team
group by tm.team, xg.total_acumulative
order by 1,2