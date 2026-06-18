select
    match_id,
    home_team as team,
    true as is_home,
    home_score as goals_for,
    away_score as goals_against
from {{ ref('stg_matches') }}

union all

select
    match_id,
    away_team as team,
    false as is_home,
    away_score as goals_for,
    home_score as goals_against
from {{ ref('stg_matches') }}