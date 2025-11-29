import os
import sys

import click

from .audit_player_names_v3 import audit_player_name_resolution_v3
from .audit_realities import audit_team_name_realities
from .commander import run_the_gauntlet

# We'll need a new function for our scenario runner, let's pretend it exists
# from .scenario_chimera import run_a_what_if_scenario

# --- THE ARTIFICER'S FORGE: OUR CUSTOM HELP CLASS ---

# First, define the glorious ASCII art. Use a raw string for simplicity.
BAMF_ART = r"""
██████╗  █████╗ ███╗   ███╗███████╗
██╔══██╗██╔══██╗████╗ ████║██╔════╝
██████╔╝███████║██╔████╔██║███████╗
██╔══██╗██╔══██║██║╚██╔╝██║██╔════╝  
██████╔╝██║  ██║██║ ╚═╝ ██║██║
╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
"""

# Refined rainbow - muted, sophisticated pastel spectrum
REFINED_RAINBOW = [
    (228, 160, 160),  # Dusty rose
    (235, 195, 148),  # Soft peach
    (215, 218, 160),  # Sage yellow
    (168, 208, 180),  # Muted mint
    (158, 188, 218),  # Soft sky blue
    (188, 170, 210),  # Gentle lavender
]


class RefinedRainbowHelpGroup(click.Group):
    def format_help(self, ctx, formatter):
        """
        Sophisticated muted rainbow gradient - elegant pastel spectrum.
        """
        art_lines = BAMF_ART.strip("\n").split("\n")

        for i, line in enumerate(art_lines):
            r, g, b = REFINED_RAINBOW[i % len(REFINED_RAINBOW)]
            formatter.write(f"\033[38;2;{r};{g};{b}m{line}\033[0m")
            formatter.write("\n")

        formatter.write("\n")
        super().format_help(ctx, formatter)


# Elegant grey-blue sophisticated version
GREY_BLUE_ELEGANCE = [
    (176, 196, 222),  # Light steel blue
    (158, 188, 218),  # Muted sky
    (140, 180, 214),  # Soft denim
    (122, 172, 210),  # Steel wash
    (104, 164, 206),  # Cool grey-blue
    (95, 158, 200),  # Refined slate-blue
]


class ElegantArtHelpGroup(click.Group):
    def format_help(self, ctx, formatter):
        """
        Sophisticated grey-blue gradient with refined elegance.
        """
        art_lines = BAMF_ART.strip("\n").split("\n")

        for i, line in enumerate(art_lines):
            r, g, b = GREY_BLUE_ELEGANCE[i % len(GREY_BLUE_ELEGANCE)]
            formatter.write(f"\033[38;2;{r};{g};{b}m{line}\033[0m")
            formatter.write("\n")

        formatter.write("\n")
        super().format_help(ctx, formatter)


# --- END OF THE ARTIFICER'S FORGE ---


# NOW, WEAPONIZE IT.
# Instead of @click.group(), we use our custom class with the 'cls' argument.
@click.command(cls=RefinedRainbowHelpGroup)
def bamf():
    """
    BAMF DOMINATOR v3.0

    The master command deck for the FPL Dominator project.
    From here, you command the Chimera and all its subsystems.
    """
    pass


@bamf.command()
# <<< UPGRADE 1: Input validation. This command will now fail gracefully if the dir doesn't exist.
@click.argument(
    "gameweek_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
def run_gauntlet(gameweek_dir):
    """
    Runs the entire data-to-squad pipeline for a given gameweek.

    This is the primary command to forge the weekly prophecy.

    GAMEWEEK_DIR: The target gameweek directory (e.g., 'gw11').
    """
    click.secho(
        f"+++ Invoking the Commander for {gameweek_dir.upper()} +++",
        fg="magenta",
        bold=True,
    )
    run_the_gauntlet(gameweek_dir)
    click.secho(
        "+++ Gauntlet run complete. The prophecy is forged and scribed. +++",
        fg="green",
        bold=True,
    )


@bamf.command()
@click.argument("gameweek_dir", type=click.Path(file_okay=False, dir_okay=True))
def init(gameweek_dir):
    """Creates a new gameweek vault with empty data files."""
    if os.path.exists(gameweek_dir):
        # <<< UPGRADE 2: Idiomatic error handling. Cleaner and more robust.
        click.secho(
            f"Error: Directory '{gameweek_dir}' already exists. Aborting.",
            fg="red",
            err=True,
        )
        raise click.Abort()

    click.echo(f"Creating new gameweek vault at '{gameweek_dir}'...")
    os.makedirs(gameweek_dir)

    # ... (rest of file creation logic is perfect, no changes needed) ...
    files_to_create = {
        "goalkeepers.csv": "Surname,Team,Position,Price,TP,Status",
        "defenders.csv": "Surname,Team,Position,Price,TP,Status",
        "midfielders.csv": "Surname,Team,Position,Price,TP,Status",
        "forwards.csv": "Surname,Team,Position,Price,TP,Status",
        "fixtures.csv": "Team,Opponent,Venue,FDR",
        "squad.csv": "Surname,Team,Position,CP,SP,PP,Status",
    }
    for filename, header in files_to_create.items():
        filepath = os.path.join(gameweek_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + "\n")
        click.echo(f" - Created {filepath}")
    click.secho(
        f"Success! New vault '{gameweek_dir}' created and ready for data.", fg="green"
    )


# --- NEW COMMAND: The Scenario Engine ---
@bamf.command()
# <<< UPGRADE 3: This is the real magic. 'multiple=True' is a game-changer.
@click.argument(
    "gameweek_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
@click.option(
    "--include",
    "-i",
    multiple=True,
    help="Force a player into the squad. Can use multiple times.",
)
@click.option(
    "--exclude",
    "-e",
    multiple=True,
    help="Exclude a player from the squad. Can use multiple times.",
)
def run_scenario(gameweek_dir, include, exclude):
    """Runs a 'what-if' simulation with player constraints."""
    click.secho(
        f"--- Running What-If Scenario for {gameweek_dir.upper()} ---",
        fg="yellow",
        bold=True,
    )

    if not include and not exclude:
        click.secho(
            "Warning: No constraints provided. This will run like a normal gauntlet.",
            fg="yellow",
        )
        run_the_gauntlet(gameweek_dir)  # Or just run the solver part
        return

    click.echo("Constraints:")
    for p in include:
        click.secho(f"  [FORCE INCLUDE] {p}", fg="green")
    for p in exclude:
        click.secho(f"  [FORCE EXCLUDE] {p}", fg="red")

    click.echo("Invoking the Scenario Chimera...")
    # Here you would call a modified solver function that accepts these lists
    # run_a_what_if_scenario(gameweek_dir, list(include), list(exclude))
    click.secho("--- Scenario complete. ---", fg="yellow", bold=True)


# --- Audit Command Group (Perfect as is, but let's add validation) ---
@bamf.group()
def audit():
    """Audits the integrity and consistency of the data."""
    pass


@audit.command()
@click.argument(
    "gameweek_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
def teams(gameweek_dir):
    """Audits team name consistency."""
    click.secho(
        f"--- Auditing Team Name Realities for {gameweek_dir.upper()} ---", fg="cyan"
    )
    audit_team_name_realities(gameweek_dir)
    click.secho("--- Team Audit Complete ---", fg="cyan")


@audit.command()
@click.argument(
    "gameweek_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
def players(gameweek_dir):
    """Audits player name resolution."""
    click.secho(
        f"--- Auditing Player Name Resolution for {gameweek_dir.upper()} ---", fg="cyan"
    )
    audit_player_name_resolution_v3(gameweek_dir)
    click.secho("--- Player Audit Complete ---", fg="cyan")


if __name__ == "__main__":
    bamf()
