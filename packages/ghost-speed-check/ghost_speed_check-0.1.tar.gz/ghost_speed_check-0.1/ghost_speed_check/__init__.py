import speedtest
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime
import requests
from time import time

def format_speed(speed_bps):
    """Convert speed from bits per second to a readable format"""
    speed_mbps = speed_bps / 1_000_000
    return f"{speed_mbps:.2f} Mbps"

def get_speed():
    console = Console()
    results = {"download": 0, "upload": 0, "ping": 0, "server": None}
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Initialize speedtest
            st = speedtest.Speedtest()
            
            # Get best server
            progress.add_task(description="Finding best server...", total=None)
            st.get_best_server()
            server_name = f"{st.results.server['name']} ({st.results.server['country']})"
            results["server"] = server_name
            
            # Test download
            progress.add_task(description="Testing download speed...", total=None)
            download = st.download()
            results["download"] = download
            
            # Test upload
            progress.add_task(description="Testing upload speed...", total=None)
            upload = st.upload()
            results["upload"] = upload
            
            # Get ping
            results["ping"] = st.results.ping
            
    except Exception as e:
        console.print(f"[red]Error during speed test: {str(e)}")
        return None
    
    return results

def get_ip():
    try:
        # Try multiple IP services in case one fails
        services = [
            'https://api.ipify.org',
            'https://api.my-ip.io/ip',
            'https://ip.seeip.org'
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue
                
        return "Unable to fetch IP"
    except:
        return "Unable to fetch IP"

def main():
    console = Console()
    console.clear()
    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the layout
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
    
    # Get IP first (it's faster)
    ip = get_ip()
    
    # Create the time and IP panel
    info_table = Table(show_header=False, box=None)
    info_table.add_row("[bold cyan]Time:", f"[white]{current_time}")
    info_table.add_row("[bold cyan]IP Address:", f"[white]{ip}")
    
    # Run speed test
    results = get_speed()
    
    if results:
        # Create the speed test panel
        speed_table = Table(title="Speed Test Results", show_header=True)
        speed_table.add_column("Metric", style="cyan")
        speed_table.add_column("Value", style="green")
        
        speed_table.add_row("Server", results["server"])
        speed_table.add_row("Download", format_speed(results["download"]))
        speed_table.add_row("Upload", format_speed(results["upload"]))
        speed_table.add_row("Ping", f"{results['ping']:.2f} ms")
        
        title = "[green]Speed Test Completed Successfully"
    else:
        speed_table = Table(show_header=False)
        speed_table.add_row("[red]Speed test failed. Please check your internet connection.")
        title = "[red]Speed Test Failed"
    
    # Add panels to layout
    layout["upper"].update(Panel(info_table, title="System Information"))
    layout["lower"].update(Panel(speed_table, title=title))
    
    # Print layout
    console.print(layout)

if __name__ == "__main__":
    main()