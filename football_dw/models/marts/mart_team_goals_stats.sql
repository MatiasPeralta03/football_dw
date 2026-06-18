select
    team,
    count(*) Matches_Played,
    sum(goals_for) as Home_Goals,
    sum(goals_against) as Away_Goals,
    sum(goals_for) - sum(goals_against) as Goal_Diff
from
    {{ ref('int_team_matches') }}
group by 1
order by Goal_Diff desc