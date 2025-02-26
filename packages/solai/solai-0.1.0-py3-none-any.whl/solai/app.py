"""
solai - Your CLI Assistant
"""
import os
import sys
import click
import platform
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm

console = Console()

def get_openai_key():
    """Get OpenAI key from user and save it"""
    console.print("[yellow]First time setup: OpenAI API Key required[/yellow]")
    console.print("[blue]Get your API key from: https://platform.openai.com/api-keys[/blue]")
    api_key = click.prompt("Please enter your OpenAI API key", type=str)
    
    with open(os.path.expanduser('~/.solai.env'), 'w') as f:
        f.write(f"OPENAI_API_KEY={api_key}")
    
    return api_key

def get_system_info():
    """Get system information"""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macOS'
    elif system == 'linux':
        return 'Linux'
    elif system == 'windows':
        return 'Windows'
    return system

def load_config():
    """Load configuration"""
    config_path = os.path.expanduser('~/.solai.env')
    if not os.path.exists(config_path):
        return get_openai_key()
    
    load_dotenv(config_path)
    return os.getenv('OPENAI_API_KEY')

def get_command_suggestion(client, query):
    """Get command suggestion from OpenAI"""
    os_type = get_system_info()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": f"You are a CLI assistant for {os_type}. Return the command followed by '||' and a brief explanation of what it does. Format: 'command || explanation'. Ensure all commands are compatible with {os_type}."
            },
            {"role": "user", "content": query}
        ]
    )
    result = response.choices[0].message.content.strip()
    
    # Split command and explanation
    if '||' in result:
        command, explanation = result.split('||')
        return command.strip(), explanation.strip()
    return result.strip(), ""

@click.command()
@click.argument('query', nargs=-1)
def main(query):
    """CLI Assistant - Get command suggestions for your queries"""
    if not query:
        console.print("[red]Please provide a query[/red]")
        sys.exit(1)

    # Initialize OpenAI
    api_key = load_config()
    client = OpenAI(api_key=api_key)

    # Get the full query
    full_query = ' '.join(query)
    
    try:
        # Get command suggestion
        command, explanation = get_command_suggestion(client, full_query)
        
        # Display suggestion with explanation
        console.print("\n[green]Suggested command:[/green]")
        console.print(f"[yellow]{command}[/yellow]")
        if explanation:
            console.print(f"[blue]→ {explanation}[/blue]\n")
        
        # Ask for confirmation
        if Confirm.ask("Do you want to execute this command?"):
            os.system(command)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()
