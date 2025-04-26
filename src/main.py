import os
import click
from src.arxml_parser import ARXMLParser
from src.arxml_editor import ARXMLEditor

@click.group()
def cli():
    """ARXML Parser and Editor Tool"""
    pass

@cli.command("info")
@click.argument("arxml_file", type=click.Path(exists=True))
@click.option("--validate/--no-validate", default=True, help="Enable/disable schema validation")
def show_info(arxml_file, validate):
    """Display information about an ARXML file"""
    parser = ARXMLParser()
    if parser.load_file(arxml_file):
        click.echo(f"Successfully parsed: {arxml_file}")
        click.echo("\nFile structure:")
        parser.print_structure()

@cli.command("update-param")
@click.argument("arxml_file", type=click.Path(exists=True))
@click.argument("param_name")
@click.argument("new_value")
@click.option("--output", "-o", help="Output file path (default: overwrites input)")
def update_parameter(arxml_file, param_name, new_value, output):
    """Update a parameter value in an ARXML file"""
    editor = ARXMLEditor()
    if editor.load(arxml_file):
        if editor.update_parameter_value(param_name, new_value):
            output_path = output if output else arxml_file
            if editor.save(output_path):
                click.echo(f"Parameter '{param_name}' updated successfully")

@cli.command("rename-component")
@click.argument("arxml_file", type=click.Path(exists=True))
@click.argument("old_name")
@click.argument("new_name")
@click.option("--output", "-o", help="Output file path (default: overwrites input)")
def rename_component(arxml_file, old_name, new_name, output):
    """Rename a software component in an ARXML file"""
    editor = ARXMLEditor()
    if editor.load(arxml_file):
        if editor.update_component_name(old_name, new_name):
            output_path = output if output else arxml_file
            if editor.save(output_path):
                click.echo(f"Component renamed from '{old_name}' to '{new_name}' successfully")

@cli.command("merge")
@click.argument("base_file", type=click.Path(exists=True))
@click.argument("other_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def merge_files(base_file, other_file, output_file):
    """Merge two ARXML files"""
    editor = ARXMLEditor()
    if editor.load(base_file):
        if editor.merge_arxml(other_file):
            if editor.save(output_file):
                click.echo(f"Files merged successfully into {output_file}")

@cli.command("add-component")
@click.argument("arxml_file", type=click.Path(exists=True))
@click.argument("component_name")
@click.option("--output", "-o", help="Output file path (default: overwrites input)")
def add_component(arxml_file, component_name, output):
    """Add a new software component to an ARXML file"""
    editor = ARXMLEditor()
    if editor.load(arxml_file):
        if editor.add_software_component(component_name):
            output_path = output if output else arxml_file
            if editor.save(output_path):
                click.echo(f"Component '{component_name}' added successfully")

@cli.command("restore-backup")
@click.argument("arxml_file", type=click.Path(exists=True))
@click.option("--backup-path", help="Specific backup file to restore (default: most recent)")
def restore_backup(arxml_file, backup_path):
    """Restore an ARXML file from backup"""
    editor = ARXMLEditor()
    editor.current_file = arxml_file  # Set current file without loading
    if editor.restore_from_backup(backup_path):
        click.echo("Backup restored successfully")
    else:
        click.echo("Failed to restore backup")

@cli.command("cleanup-backups")
@click.argument("arxml_file", type=click.Path(exists=True))
@click.option("--keep-days", default=30, help="Number of days to keep backups (default: 30)")
def cleanup_backups(arxml_file, keep_days):
    """Clean up old backup files"""
    editor = ARXMLEditor()
    editor.current_file = arxml_file  # Set current file without loading
    editor.cleanup_backups(keep_days)
    click.echo(f"Cleaned up backups older than {keep_days} days")

if __name__ == "__main__":
    cli()