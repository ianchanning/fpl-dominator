import click
import sys
import os
from commander import run_the_gauntlet
from audit_realities import audit_team_name_realities
from audit_player_names_v3 import audit_player_name_resolution_v3

@click.group()
def cli():
    """
    BAMF DOMINATOR
    
    The master command deck for the FPL Dominator project.
    From here, you command the Chimera and all its subsystems.
    """
    pass

@cli.command()
@click.argument('gameweek_dir')
def run_gauntlet(gameweek_dir):
    """
    Runs the entire data-to-squad pipeline for a given gameweek.
    
    This is the primary command to forge the weekly prophecy.
    
    GAMEWEEK_DIR: The target gameweek directory (e.g., 'gw11').
    """
    click.secho(f"+++ Invoking the Commander for {gameweek_dir.upper()} +++", fg='magenta')
    run_the_gauntlet(gameweek_dir)
    click.secho("+++ Gauntlet run complete. The prophecy is forged and scribed. +++", fg='magenta')

@cli.command()
@click.argument('gameweek_dir')
def init(gameweek_dir):
    """Creates a new gameweek vault with empty data files."""
    if os.path.exists(gameweek_dir):
        click.secho(f"Error: Directory '{gameweek_dir}' already exists. Aborting.", fg='red')
        return

    click.echo(f"Creating new gameweek vault at '{gameweek_dir}'...")
    os.makedirs(gameweek_dir)

    files_to_create = {
        "goalkeepers.csv": "Surname,Team,Position,Price,TP,Status",
        "defenders.csv": "Surname,Team,Position,Price,TP,Status",
        "midfielders.csv": "Surname,Team,Position,Price,TP,Status",
        "forwards.csv": "Surname,Team,Position,Price,TP,Status",
        "fixtures.csv": "Team,Opponent,Venue,FDR",
        "squad.csv": "Surname,Team,Position,CP,SP,PP,Status"
    }

    for filename, header in files_to_create.items():
        filepath = os.path.join(gameweek_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + "\n")
        click.echo(f" - Created {filepath}")

    click.secho(f"Success! New vault '{gameweek_dir}' created and ready for data.", fg='green')

# --- Audit Command Group ---
@cli.group()
def audit():
    """Audits the integrity and consistency of the data."""
    pass

@audit.command()
@click.argument('gameweek_dir')
def teams(gameweek_dir):
    """
    Audits team name consistency between the player and set-piece databases.
    
    GAMEWEEK_DIR: The gameweek directory to use for the player database.
    """
    click.secho(f"--- Auditing Team Name Realities for {gameweek_dir.upper()} ---", fg='cyan')
    audit_team_name_realities(gameweek_dir)
    click.secho("--- Team Audit Complete ---", fg='cyan')

@audit.command()
@click.argument('gameweek_dir')
def players(gameweek_dir):
    """
    Audits player name resolution between set-piece takers and the main database.
    
    GAMEWEEK_DIR: The gameweek directory to use for the player database.
    """
    click.secho(f"--- Auditing Player Name Resolution for {gameweek_dir.upper()} ---", fg='cyan')
    audit_player_name_resolution_v3(gameweek_dir)
    click.secho("--- Player Audit Complete ---", fg='cyan')


if __name__ == '__main__':
    cli()
