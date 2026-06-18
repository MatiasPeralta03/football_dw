select
    competition_id,
    season_id,
    country_name,
    competition_name,
    competition_gender,
    competition_youth,
    competition_international,
    season_name
from {{ source('raw', 'competitions') }}