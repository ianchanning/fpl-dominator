import click
import sys
from commander import run_the_gauntlet

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

if __name__ == '__main__':
    cli()
