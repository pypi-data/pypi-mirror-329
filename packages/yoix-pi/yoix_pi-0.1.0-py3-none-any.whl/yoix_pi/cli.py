"""Command line interface for Yoix Persistent Includes."""

import click
from .processor import process_persistent_includes


@click.command()
@click.option(
    '--partials',
    '-p',
    default='includes/partials',
    help='Directory containing partial files',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=str)
)
@click.option(
    '--public',
    '-b',
    default='public',
    help='Directory containing HTML files to process',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=str)
)
def main(partials, public):
    """Process BBEdit-style includes in HTML files.
    
    This command processes HTML files in the public directory, replacing BBEdit-style
    includes with content from partial files in the partials directory.
    """
    config = {
        'partials_dir': partials,
        'public_dir': public
    }
    process_persistent_includes(config)


if __name__ == '__main__':
    main()
