with results as (
    select
        match_id,
        home_team,
        away_team,
        home_score,
        away_score,
        case
            when home_score > away_score then home_team
            when away_score > home_score then away_team
            else 'Draw'
        end as winner
    from {{ ref('stg_matches') }}
)

select * from results