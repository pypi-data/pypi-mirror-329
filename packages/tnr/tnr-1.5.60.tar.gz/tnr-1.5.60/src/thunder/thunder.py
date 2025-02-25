import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    import rich_click as click
    import rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.live import Live
    from rich import box
    from thunder import auth
    import os
    from os.path import join
    import json
    from scp import SCPClient, SCPException
    import paramiko
    from paramiko import ssh_exception
    import subprocess
    import time
    import platform
    from contextlib import contextmanager
    from threading import Timer

    from thunder import utils
    from thunder.config import Config
    from thunder.get_latest import get_latest
    from thunder import setup_cmd

    try:
        from importlib.metadata import version
    except Exception as e:
        from importlib_metadata import version

    import requests
    from packaging import version as version_parser
    from pathlib import Path
    from pathlib import Path
    import atexit
    from os.path import join
    from string import ascii_uppercase
    import socket
    import datetime
    import logging
    from subprocess import Popen
    from logging.handlers import RotatingFileHandler
    import sys
    import sentry_sdk
    import traceback
    from functools import wraps

def capture_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Get user context for this command execution
            try:
                token = get_token()
                uid = utils.get_uid(token)
                with sentry_sdk.configure_scope() as scope:
                    scope.set_user({"id": uid})
                    scope.set_tag("command", func.__name__)
                    scope.set_context("command_args", {
                        "args": args[1:] if args else None,  # Skip first arg (click context)
                        "kwargs": kwargs
                    })
            except Exception:
                # If we can't get the user context, still proceed with command
                pass
                
            return func(*args, **kwargs)
        except Exception as e:
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            try:
                sentry_sdk.capture_exception(e)
                sentry_sdk.flush()
            finally:
                sys.stdout = old_stdout
            raise
    return wrapper

def handle_click_exception(e):
    """Custom exception handler for Click that sends to Sentry before displaying"""
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
    finally:
        sys.stdout = old_stdout
    
    # Use Click's default exception rendering
    click.utils.echo(f"Error: {e.format_message()}", err=True)
    sys.exit(e.exit_code)

# Decorate all command functions with the capture_exception decorator
for attr_name in dir(sys.modules[__name__]):
    attr = getattr(sys.modules[__name__], attr_name)
    if hasattr(attr, '__click_params__'):  # Check if it's a Click command
        setattr(sys.modules[__name__], attr_name, capture_exception(attr))

PACKAGE_NAME = "tnr"
ENABLE_RUN_COMMANDS = True if platform.system() == "Linux" else False
IS_WINDOWS = platform.system() == "Windows"
INSIDE_INSTANCE = False
INSTANCE_ID = None
OPEN_PORTS = {
    'comfy-ui': [8188],
    'ollama': [8080],
    'webui-forge': [7860],
}
AUTOMOUNT_FOLDERS = {
    'comfy-ui': "/home/ubuntu/ComfyUI",
    'webui-forge': "/home/ubuntu/stable-diffusion-webui-forge",
}


# Remove the DefaultCommandGroup class
DISPLAYED_WARNING = False
logging_in = False

@contextmanager
def DelayedProgress(*progress_args, delay=0.1, **progress_kwargs):
    progress = Progress(*progress_args, **progress_kwargs)
    timer = Timer(delay, progress.start)
    timer.start()
    try:
        yield progress
        timer.cancel()
        if progress.live.is_started: progress.stop()
    finally:
        timer.cancel()
        if progress.live.is_started: progress.stop()

def get_token():
    global logging_in, DISPLAYED_WARNING

    if "TNR_API_TOKEN" in os.environ:
        return os.environ["TNR_API_TOKEN"]

    token_file = auth.get_credentials_file_path()
    if not os.path.exists(token_file):
        logging_in = True
        auth.login()

    with open(auth.get_credentials_file_path(), "r") as f:
        lines = f.readlines()
        if len(lines) == 1:
            token = lines[0].strip()
            return token

    auth.logout()
    logging_in = True
    token = auth.login()
    return token

def setup_shell_completion():
    # Skip for root/admin users
    try:
        is_root = False
        if not IS_WINDOWS:  # Unix-like
            is_root = os.geteuid() == 0
            if is_root:
                return
    except Exception:
        # If we can't determine admin status, continue anyway
        pass
    
    # Check if we've already asked about completion
    pref_file = os.path.expanduser('~/.thunder/autocomplete')
    if os.path.exists(pref_file):
        with open(pref_file, 'r') as f:
            if f.read().strip() == 'no':
                return
    
    # Detect current shell
    if IS_WINDOWS:
        # For Windows, we only support bash through Git Bash or similar
        if os.environ.get('SHELL'):
            shell = os.environ.get('SHELL').lower()
            rc_file = os.path.expanduser('~/.bashrc')
            completion_line = 'eval "$(_TNR_COMPLETE=bash_source tnr)"'
        else:
            return  # No supported shell found on Windows
    else:
        shell = os.environ.get('SHELL', '').lower()
        
        if 'zsh' in shell:
            rc_file = os.path.expanduser('~/.zshrc')
            completion_line = 'eval "$(_TNR_COMPLETE=zsh_source tnr)"'
        elif 'bash' in shell:
            rc_file = os.path.expanduser('~/.bashrc')
            completion_line = 'eval "$(_TNR_COMPLETE=bash_source tnr)"'
        elif 'fish' in shell:
            rc_file = os.path.expanduser('~/.config/fish/completions/tnr.fish')
            completion_line = '_TNR_COMPLETE=fish_source tnr | source'
        else:
            return  # Unsupported shell
    
    # Check if completion is already configured
    try:
        if os.path.exists(rc_file):
            with open(rc_file, 'r') as f:
                if completion_line in f.read():
                    return  # Already configured
        
        # If we haven't asked before, prompt the user
        if not os.path.exists(pref_file):
            shell_name = 'fish' if 'fish' in shell else ('zsh' if 'zsh' in shell else 'bash')
            if click.confirm(f'Would you like to enable Thunder CLI command completion for {shell_name}?', default=True):
                # For fish shell, create completions directory if it doesn't exist
                if 'fish' in shell:
                    os.makedirs(os.path.dirname(rc_file), exist_ok=True)
                    
                # Add completion line to rc file
                with open(rc_file, 'a') as f:
                    f.write(f'\n# Thunder CLI completion\n{completion_line}\n')
                    
                # For non-fish shells, source the rc file using the actual shell
                if 'fish' not in shell:
                    subprocess.run([shell, '-ic', f'source {rc_file}'], stderr=subprocess.DEVNULL)
                
                # Save preference
                os.makedirs(os.path.dirname(pref_file), exist_ok=True)
                with open(pref_file, 'w') as f:
                    f.write('yes')
            else:
                # Save negative preference
                os.makedirs(os.path.dirname(pref_file), exist_ok=True)
                with open(pref_file, 'w') as f:
                    f.write('no')
                    
    except Exception as e:
        pass

def init():
    global INSIDE_INSTANCE, INSTANCE_ID, ENABLE_RUN_COMMANDS
    try:
        Config().setup(get_token())
        deployment_mode = Config().get("deploymentMode", "public")

        if deployment_mode == "public":
            # Check if we're in an instance based on config.json
            INSTANCE_ID = Config().getX("instanceId")
            if INSTANCE_ID == -1 or INSTANCE_ID is None:
                INSIDE_INSTANCE = False
                INSTANCE_ID = None
            else:
                INSIDE_INSTANCE = True

        elif deployment_mode == "test":
            ENABLE_RUN_COMMANDS = True
            INSTANCE_ID = 0

        else:
            raise click.ClickException(
                f"deploymentMode field in `{Config().file}` is set to an invalid value"
            )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

init()
# Setup Sentry for error reporting with more context
sentry_sdk.init(
    dsn="https://ba3a63bb837905e030f7184f1ca928d3@o4508006349012992.ingest.us.sentry.io/4508802738683904",
    send_default_pii=True,
    traces_sample_rate=1.0,
    debug=False,
    attach_stacktrace=True,
    shutdown_timeout=0,
    before_send=lambda event, hint: {
        **event,
        'extra': {
            **(event.get('extra', {})),
            'platform': platform.system(),
            'python_version': platform.python_version(),
            'inside_instance': INSIDE_INSTANCE,
            'instance_id': INSTANCE_ID,
            'package_version': version(PACKAGE_NAME),
            'deployment_mode': Config().get("deploymentMode", "public") if Config().file else None
        }
    }
)
sentry_sdk.profiler.start_profiler()
try:
    setup_shell_completion()
except Exception as e:
    pass

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.COMMAND_GROUPS = {
    "cli": [
        {
            "name": "Instance management",
            "commands": ["create", "delete", "start", "stop", "modify"],
        },
        {
            "name": "Utility",
            "commands": ["connect", "status", "scp"],
        },
        {
            "name": "Account management",
            "commands": ["login", "logout"],
        },
    ]
}

COLOR = "cyan"
click.rich_click.STYLE_OPTION = COLOR
click.rich_click.STYLE_COMMAND = COLOR
click.exceptions.ClickException.show = handle_click_exception

main_message = (
    f":laptop_computer: [bold {COLOR}]You're in a local environment, use these commands to manage your Thunder Compute instances[/]"
)


class VersionCheckGroup(click.RichGroup):
    def __call__(self, ctx=None, *args, **kwargs):
        # Do version check before any command processing
        meets_version, versions = does_meet_min_required_version()
        if not meets_version:
            error_msg = (
                f'Failed to meet minimum required tnr version to proceed '
                f'(current=={versions[0]}, required=={versions[1]}), '
                'please run "pip install --upgrade tnr" to update'
            )
            # Create and display error panel
            panel = Panel(
                error_msg,
                title="Error",
                style="white",
                border_style="red",
                width=80
            )
            Console().print(panel)
            # Exit with error code 1
            sys.exit(1)
            
        # Prevent any command execution when inside an instance
        if INSIDE_INSTANCE:
            error_msg = "The 'tnr' command line tool is not available inside Thunder Compute instances."
            panel = Panel(
                error_msg,
                title="Error",
                style="white",
                border_style="red",
                width=80
            )
            Console().print(panel)
            sys.exit(1)
            
        return super().__call__(ctx, *args, **kwargs)

@click.group(
    cls=VersionCheckGroup,
    help=main_message,
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
)
@click.version_option(version=version(PACKAGE_NAME))
def cli():
    # utils.validate_config()
    pass

# @click.group(
#     cls=click.RichGroup,
#     help=main_message,
#     context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
# )
# @click.version_option(version=version(PACKAGE_NAME))
# @click.pass_context
# def cli(ctx):
#     ctx.start_time = time.time()
    
#     meets_version, versions = does_meet_min_required_version()
#     if not meets_version:
#         raise click.ClickException(
#             f'Failed to meet minimum required tnr version to proceed (current=={versions[0]}, required=={versions[1]}), please run "pip install --upgrade tnr" to update'
#         )
#     utils.validate_config()
    
#     # Add CLI initialization timing
#     cli_init_time = time.time()
    
#     # Store the initialization end time for command timing
#     ctx.init_end_time = cli_init_time
    
#     # Create a callback that includes the context
#     ctx.call_on_close(lambda: print_execution_time(ctx))

# def print_execution_time(ctx):
#     end_time = time.time()
#     # Calculate total execution time from click config
#     total_execution_time = end_time - ctx.start_time
#     # Calculate command execution time     
#     print(f"⏱️ Total execution time: {total_execution_time:.2f}s")

if ENABLE_RUN_COMMANDS:

    @cli.command(
        help="Runs process on a remote Thunder Compute GPU. The GPU type is specified in the ~/.thunder/dev file. For more details, please go to thundercompute.com",
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
        hidden=True,
    )
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    @click.option("--nowarnings", is_flag=True, help="Hide warning messages")
    def run(args, nowarnings):
        if not args:
            raise click.ClickException("No arguments provided. Exiting...")

        token = get_token()
        uid = utils.get_uid(token)

        # Run the requested process
        if not INSIDE_INSTANCE and not nowarnings:
            message = "[yellow]Attaching to a remote GPU from a non-managed instance - this will hurt performance. If this is not intentional, please connect to a managed CPU instance using tnr create and tnr connect <INSTANCE ID>[/yellow]"
            panel = Panel(
                message,
                title=":warning:  Warning :warning: ",
                title_align="left",
                highlight=True,
                width=100,
                box=box.ROUNDED,
            )
            rich.print(panel)

        # config = utils.read_config()
        if Config().contains("binary"):
            binary = Config().get("binary")
            if not os.path.isfile(binary):
                raise click.ClickException(
                    "Invalid path to libthunder.so in config.binary"
                )
        else:
            binary = get_latest("client", "~/.thunder/libthunder.so")
            if binary == None:
                raise click.ClickException("Failed to download binary")

        device = Config().get("gpuType", "t4")
        if device.lower() != "cpu":
            os.environ["LD_PRELOAD"] = f"{binary}"

        # This should never return
        try:
            os.execvp(args[0], args)
        except FileNotFoundError:
            raise click.ClickException(f"Invalid command: \"{' '.join(args)}\"")
        except Exception as e:
            raise click.ClickException(f"Unknown exception: {e}")

    @cli.command(
        help="View or change the GPU configuration for this instance. Run without arguments to see current GPU and available options.",
        hidden=not INSIDE_INSTANCE,
    )
    @click.argument("gpu_type", required=False)
    @click.option("-n", "--ngpus", type=int, help="Number of GPUs to request (default: 1). Multiple GPUs increase costs proportionally")
    @click.option("--raw", is_flag=True, help="Output device name and number of devices as an unformatted string")
    def device(gpu_type, ngpus, raw):
        # config = utils.read_config()
        supported_devices = set(
            [
                "cpu",
                "t4",
                "v100",
                "a100",
                "a100xl",
                "l4",
                "p4",
                "p100",
                "h100",
            ]
        )

        if gpu_type is None:
            # User wants to read current device
            device = Config().get("gpuType", "t4")
            gpu_count = Config().get("gpuCount", 1)

            if raw is not None and raw:
                if gpu_count <= 1:
                    click.echo(device.upper())
                else:
                    click.echo(f"{gpu_count}x{device.upper()}")
                return

            if device.lower() == "cpu":
                click.echo(
                    click.style(
                        "📖 No GPU selected - use `tnr device <gpu-type>` to select a GPU",
                        fg="white",
                    )
                )
                return

            console = Console()
            if gpu_count == 1:
                console.print(f"[bold green]📖 Current GPU:[/] {device.upper()}")
            else:
                console.print(
                    f"[bold green]📖 Current GPUs:[/][white] {gpu_count} x {device.upper()}[/]"
                )

            utils.display_available_gpus()
            return

        if gpu_type.lower() not in supported_devices:
            raise click.ClickException(
                f"Unsupported device type: {gpu_type}. Please use tnr device (without arguments) to view available devices."
            )

        if ngpus is not None and ngpus < 1:
            raise click.ClickException(
                f"Unsupported device count {ngpus} - must be at least 1"
            )

        if gpu_type.lower() == "cpu":
            Config().set("gpuType", "cpu")
            Config().set("gpuCount", 0)

            click.echo(
                click.style(
                    f"✅ Device set to CPU, your instance does not have access to GPUs.",
                    fg="green",
                )
            )
        else:
            Config().set("gpuType", gpu_type.lower())

            gpu_count = ngpus if ngpus is not None else 1
            Config().set("gpuCount", gpu_count)
            click.echo(
                click.style(
                    f"✅ Device set to {gpu_count} x {gpu_type.upper()}", fg="green"
                )
            )
        Config().save()

    @cli.command(
        help="Activate a tnr shell environment. Anything that you run in this shell has access to GPUs through Thunder Compute",
        hidden=True,
    )
    def activate():
        if INSIDE_INSTANCE:
            raise click.ClickException(
                "The 'tnr' command line tool is not available inside Thunder Compute instances."
            )
        pass

    @cli.command(
        help="Deactivate a tnr shell environment. Your shell will no longer have access to GPUs through Thunder Compute",
        hidden=True,
    )
    def deactivate():
        if INSIDE_INSTANCE:
            raise click.ClickException(
                "The 'tnr' command line tool is not available inside Thunder Compute instances."
            )
        pass

# else:

    # @cli.command(hidden=True)
    # @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    # def run(args):
    #     raise click.ClickException(
    #         "tnr run is supported within Thunder Compute instances. Create one with 'tnr create' and connect to it using 'tnr connect <INSTANCE ID>'"
    #     )

    # @cli.command(hidden=True)
    # @click.argument("gpu_type", required=False)
    # @click.option("-n", "--ngpus", type=int, help="Number of GPUs to use")
    # @click.option("--raw", is_flag=True, help="Output raw device information")
    # def device(gpu_type, ngpus, raw):
    #     raise click.ClickException(
    #         "tnr device is supported within Thunder Compute instances. Create one with 'tnr create' and connect to it using 'tnr connect <INSTANCE ID>'"
    #     )


@cli.command(hidden=True)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def launch(args):
    return run(args)

if INSIDE_INSTANCE:
    @cli.command(
        help="Display status and details of all your Thunder Compute instances, including running state, IP address, hardware configuration, and resource usage"
    )
    def status():
        with DelayedProgress(
            SpinnerColumn(spinner_name="dots", style="white"),
            TextColumn("[white]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("Loading", total=None)  # No description text

            token = get_token() 

        # Retrieve IP address and active sessions in one call
            current_ip, active_sessions = utils.get_active_sessions(token)

            # Extract storage information
            storage_total = (
                subprocess.check_output("df -h / | awk 'NR==2 {print $2}'", shell=True)
                .decode()
                .strip()
            )
            storage_used = (
                subprocess.check_output("df -h / | awk 'NR==2 {print $3}'", shell=True)
                .decode()
                .strip()
            )

            disk_space_text = Text(
                f"Disk Space: {storage_used} / {storage_total} (Used / Total)", 
                style="white"
            )

            # Format INSTANCE_ID and current_ip as Text objects with a specific color (e.g., white)
            instance_id_text = Text(f"ID: {INSTANCE_ID}", style="white")
            current_ip_text = Text(f"Public IP: {current_ip}", style="white")

        # Console output for instance details
        console = Console()
        console.print(Text("Instance Details", style="bold green"))
        console.print(instance_id_text)
        console.print(current_ip_text)
        console.print(disk_space_text)
        console.print()

        # GPU Processes Table
        gpus_table = Table(
            title="Active GPU Processes",
            title_style="bold green",
            title_justify="left",
            box=box.ROUNDED,
        )

        gpus_table.add_column("GPU Type", justify="center")
        gpus_table.add_column("Duration", justify="center")

        # Populate table with active sessions data
        for session_info in active_sessions:
            gpus_table.add_row(
                f'{session_info["count"]} x {session_info["gpu"]}',
                f'{session_info["duration"]}s',
            )

        # If no active sessions, display placeholder
        if not active_sessions:
            gpus_table.add_row("--", "--")

        # Print table
        console.print(gpus_table)

else:

    @cli.command(help="List details of Thunder Compute instances within your account")
    @click.option('--no-wait', is_flag=True, help="Don't wait for status updates")
    def status(no_wait):
        def get_table(instances, show_timestamp=False, changed=False, loading=False):
            instances_table = Table(
                title="Thunder Compute Instances",
                title_style="bold cyan",
                title_justify="left",
                box=box.ROUNDED,
            )

            instances_table.add_column("ID", justify="center")
            instances_table.add_column("Status", justify="center")
            instances_table.add_column("Address", justify="center")
            instances_table.add_column("Disk", justify="center")
            instances_table.add_column("GPU", justify="center")
            instances_table.add_column("vCPUs", justify="center")
            instances_table.add_column("RAM", justify="center")
            instances_table.add_column("Creation Date", justify="center")

            if loading:
                instances_table.add_row(
                    "...", 
                    Text("LOADING", style="cyan"), 
                    "...",
                    "...",
                    "...",
                    "...",
                    "...",
                    "..."
                )
            else:
                for instance_id, metadata in instances.items():
                    if metadata["status"] == "RUNNING":
                        status_color = "green"
                    elif metadata["status"] == "STOPPED":
                        status_color = "red"
                    else:
                        status_color = "yellow"

                    ip_entry = metadata["ip"] if metadata["ip"] else "--"
                    gpu_count = metadata['numGpus'] if metadata['numGpus'] else '1'
                    gpu_type = metadata['gpuType'].upper() if metadata['gpuType'] else "--"
                    gpu_entry = f"{gpu_count}x{gpu_type}" if str(gpu_count) != '1' else gpu_type if gpu_type != "--" else "--"
                    instances_table.add_row(
                        str(instance_id),
                        Text(metadata["status"], style=status_color),
                        str(ip_entry),
                        f"{metadata['storage']}GB",
                        str(gpu_entry),
                        str(metadata['cpuCores']),
                        f"{int(metadata['cpuCores'])*4}GB",
                        str(metadata["createdAt"]),
                    )

                if len(instances) == 0:
                    instances_table.add_row("--", "--", "--", "--", "--", "--", "--", "--")
            
            if show_timestamp:
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                status = "Status change detected! Monitoring stopped." if changed else "Press Ctrl+C to stop monitoring"
                if loading:
                    status = "Loading initial state..."
                instances_table.caption = f"Last updated: {timestamp}\n{status}"
                
            return instances_table

        def fetch_data(show_progress=True):
            token = get_token()
            success, error, instances = utils.get_instances(token, use_cache=False)
            
            if not success:
                raise click.ClickException(f"Status command failed with error: {error}")
            return instances

        def instances_changed(old_instances, new_instances):
            if old_instances is None:
                return False
                
            # Compare instance statuses - we can add other stuff here, 
            # but figured this would be the most useful
            return (
                any(
                    old_instances[id]["status"] != new_instances[id]["status"]
                    for id in old_instances if id in new_instances
                )
            )
        
        def in_transition(instances):
            if instances is None:
                return False
                
            return (
                any(
                    instances[id]["status"] in ["STARTING", "STOPPING", "PENDING", "STAGING", "PROVISIONING"]
                    for id in instances
                )
            )

        console = Console()
        
        if not no_wait:
            previous_instances = None
            final_table = None
            initial_table = get_table({}, show_timestamp=True, loading=True)
            
            try:
                # Provide initial table to Live to show immediately
                with Live(initial_table, refresh_per_second=4, transient=True) as live:
                    # Fetch initial data
                    current_instances = fetch_data(show_progress=False)
                    previous_instances = current_instances
                    while True:
                        table = get_table(current_instances, show_timestamp=True, changed=False)
                        final_table = table  # Keep track of last state
                        live.update(table)
                        
                        time.sleep(5)
                        current_instances = fetch_data(show_progress=False)
                        changed = instances_changed(previous_instances, current_instances)
                        transitioning = in_transition(current_instances)
                        if not transitioning or (changed and previous_instances is not None):
                            table = get_table(current_instances, show_timestamp=True, changed=True)
                            final_table = table
                            live.update(table)
                            break  # Exit the loop if changes detected (and not first run)
                            
                        previous_instances = current_instances
            
            except KeyboardInterrupt:
                pass  # Don't let the command abort - we want to print out the table after
            
            if final_table:
                console.print(final_table)
                
        else:
            # Single display mode
            # Show initial loading skeleton in a Live display
            with Live(get_table({}, loading=True), refresh_per_second=4) as live:
                instances = fetch_data(show_progress=False)
                table = get_table(instances)
                live.update(table)
            
            if len(instances) == 0:
                console.print("Tip: use `tnr create` to create a Thunder Compute instance")

@cli.command(
    help="Create a new Thunder Compute instance. Available templates: base (default), comfy-ui, ollama",
    hidden=INSIDE_INSTANCE,
)
@click.option('--vcpus', type=click.Choice(['4', '8', '16', '32', '64']), default='4', 
    help='Number of vCPUs (4 or 8). Cost scales with vCPU count')
@click.option('--template', type=click.Choice(['base', 'comfy-ui', 'ollama', 'webui-forge']), default='base',
    help='Environment template: base (standard ML tools), comfy-ui, ollama, or webui-forge')
@click.option('--gpu', type=click.Choice(['t4', 'a100','a100xl']), default='a100', 
    help='GPU type: T4 (16GB, inference) or A100 (40GB, training), or A100XL (80GB, training)')
@click.option('--num-gpus', type=click.Choice(['1', '2']), default='1', hidden=True, help='Number of GPUs to request (default: 1). Multiple GPUs increase costs proportionally')
@click.option("--disk_size_gb", type=int, default=100, metavar="SIZE_GB", help="Disk size in GB (default: 100, max: 1024)")
def create(vcpus, template, gpu, num_gpus, disk_size_gb):
    if disk_size_gb > 1024:
        raise click.ClickException(
            f"❌ The requested size ({disk_size_gb}GB) exceeds the 1TB limit."
        )
    if template == 'webui-forge' and (gpu == 't4' or int(vcpus) < 8):
        message = "[yellow]The FLUX models pre-loaded onto this template are not supported on T4 GPUs. If your goal is to run FLUX, please use an A100 by setting --gpu a100 or a100xl. It's also recommended to use at least 8 vCPUs.[/yellow]"
        panel = Panel(
            message,
            title=":warning:  Warning :warning: ",
            title_align="left",
            highlight=True,
            width=100,
            box=box.ROUNDED,
        )
        rich.print(panel)
        # Ask user if they want to continue
        if not click.confirm(click.style("Do you want to continue running this template with lower than recommended specifications?", fg="cyan")):
            return
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)  # No description text
        token = get_token()
        success, error, instance_id = utils.create_instance(token, vcpus, gpu, template, num_gpus, disk_size_gb)
    
    if success:
        # Attempt to add key to instance right away (optional)
        if not utils.add_key_to_instance(instance_id, token):
            click.echo(click.style(
                f"Warning: Unable to create or attach SSH key for instance {instance_id} immediately. The background config will try again.",
                fg="yellow"
            ))
        
        start_background_config(instance_id, token)
        click.echo(
            click.style(
                f"Successfully created Thunder Compute instance {instance_id}! View this instance with 'tnr status'",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to create Thunder Compute instance: {error}"
        )


@cli.command(
    help="Permanently delete a Thunder Compute instance. This action is not reversible",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def delete(instance_id):
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)  # No description text
        token = get_token()
        _, _, instances = utils.get_instances(token, use_cache=False)
        delete_success, error = utils.delete_instance(instance_id, token)
        
    if delete_success:
        click.echo(
            click.style(
                f"Successfully deleted Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )
        utils.remove_instance_from_ssh_config(f"tnr-{instance_id}")
        try:
            device_ip = instances[instance_id]['ip']
            utils.remove_host_key(device_ip)
        except Exception as _:
            pass
    else:
        raise click.ClickException(
            f"Failed to delete Thunder Compute instance {instance_id}: {error}"
        )

def setup_background_logging():
    log_dir = os.path.expanduser("~/.thunder/logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "background_config.log")
    
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger("thunder_background")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

def get_instance_lock_file(instance_id):
    """Get the path to the lockfile for a specific instance."""
    lock_dir = os.path.expanduser("~/.thunder/locks")
    os.makedirs(lock_dir, exist_ok=True)
    return os.path.join(lock_dir, f"instance_{instance_id}.lock")

def write_lock_file(lock_file):
    """Write the current process ID to the lock file."""
    try:
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
    except Exception:
        pass

def is_lock_stale(lock_file):
    """Check if the lockfile exists and if the process is still running."""
    try:
        if not os.path.exists(lock_file):
            return False
            
        with open(lock_file, 'r') as f:
            pid = int(f.read().strip())
            
        # Check if process exists
        try:
            # Don't actually send a signal, just check if we can
            os.kill(pid, 0)
            return False
        except ProcessLookupError:  # Process doesn't exist
            return True
        except PermissionError:  # Process exists but we don't have permission (still means it's running)
            return False
    except Exception:
        return True  # If we can't read the file or it's invalid, consider it stale
    
def check_active_ssh_sessions(ssh):
    """Check if there are any active SSH sessions on the remote host."""
    try:
        # Count SSH processes excluding our current connection and sshd
        # The [s] trick prevents the grep itself from showing up
        # -v grep excludes our check command
        # We look for established connections only
        cmd = "ps aux | grep '[s]sh.*ubuntu@' | grep -v grep | wc -l"
        _, stdout, _ = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            return False
        count = stdout.read().decode().strip()
        
        try:
            # If we get more than 1 connection (excluding our current one)
            return int(count) > 1
        except ValueError:
            return False
    except Exception:
        return False

def wait_for_background_config(instance_id, timeout=60):
    """Wait for background configuration to complete by checking lockfile."""
    lock_file = get_instance_lock_file(instance_id)
    start_time = time.time()
    
    while os.path.exists(lock_file):
        if time.time() - start_time > timeout:
            return False
        time.sleep(1)
    return True

def robust_ssh_connect(ip, keyfile, max_wait=120, interval=5, username="ubuntu"):
    """
    Attempt to connect to the given IP using provided keyfile for up to max_wait seconds,
    retrying every 'interval' seconds. Returns an SSHClient on success, or raises an Exception on failure.
    """
    start_time = time.time()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    last_error = None
    connection = None

    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]Establishing SSH connection..."),
        transient=True
    ) as progress:
        progress.add_task("", total=None)
        
        while time.time() - start_time < max_wait:
            try:
                ssh.connect(ip, username=username, key_filename=keyfile, timeout=15)
                connection = ssh
                break
            except (socket.timeout, TimeoutError, paramiko.SSHException, Exception) as e:
                last_error = e
                time.sleep(interval)

    if connection:
        return connection
        
    raise RuntimeError(f"Failed to establish SSH connection to {ip} within {max_wait} seconds. Last error: {last_error}. Please try again or contact support@thundercompute.com if the issue persists.")


def wait_and_configure_ssh(instance_id, token):
    logger = setup_background_logging()
    logger.info(f"Starting background configuration for instance {instance_id}")
    lock_file = get_instance_lock_file(instance_id)
    try:
        max_attempts = 120  # 5 minutes total (60 * 5 seconds)
        max_instance_not_found_attempts = 5
        attempt = 0
        instance_not_found_attempt = 0

        while attempt < max_attempts:
            success, error, instances = utils.get_instances(token, use_cache=False)
            if not success:
                logger.error(f"Failed to get instances: {error}")
                return
                
            if instance_id not in instances:
                logger.error(f"Instance {instance_id} not found")
                # Sometimes GCP does this weird thing where they set a STOPPING of the instance
                # before it actually starts. Going to set a max-retry for this
                instance_not_found_attempt += 1
                if instance_not_found_attempt == max_instance_not_found_attempts:
                    return
                else:
                    time.sleep(1)
                    continue
                
            instance = instances[instance_id]
            if instance.get("status") == "RUNNING" and instance.get("ip"):
                ip = instance["ip"]
                keyfile = utils.get_key_file(instance["uuid"])

                if not os.path.exists(keyfile):
                    created, key_error = utils.add_key_to_instance(instance_id, token)
                    if not created or not os.path.exists(keyfile):
                        logger.error("Failed to create/retrieve SSH key for instance.")
                        return

                try:
                    ssh = robust_ssh_connect(ip, keyfile, max_wait=180, interval=5, username="ubuntu")
                    # Write PID to lockfile only after successful connection
                    # Check if there's already a connection attempt in progress
                    if os.path.exists(lock_file):
                        try:
                            with open(lock_file, 'r') as f:
                                pid = int(f.read().strip())
                            
                            # Check if process exists and it's not our parent
                            if not is_lock_stale(lock_file) and pid != os.getppid():
                                logger.error("Another connection attempt is already in progress")
                                return
                            else:
                                # Either stale or our parent process, safe to remove
                                try:
                                    os.remove(lock_file)
                                except Exception as e:
                                    logger.error(f"Failed to remove stale lockfile: {e}")
                                    return
                        except Exception:
                            # If we can't read the PID, try to remove the lockfile
                            try:
                                os.remove(lock_file)
                            except Exception as e:
                                logger.error(f"Failed to remove invalid lockfile: {e}")
                                return
                    write_lock_file(lock_file)
                    logger.info(f"Successfully connected to {ip} for instance {instance_id}")

                    # Add token to environment
                    _, stdout, _ = ssh.exec_command("grep 'export TNR_API_TOKEN' /home/ubuntu/.bashrc")
                    if not stdout.read():
                        cmd = f"""echo 'export TNR_API_TOKEN={token}' >> /home/ubuntu/.bashrc"""
                        ssh.exec_command(cmd)
                        logger.info(f"Added TNR_API_TOKEN to environment for {instance_id}")

                    # Update binary and write config
                    has_active_sessions = check_active_ssh_sessions(ssh)
                    if has_active_sessions:
                        pass
                    else:
                        try:
                            # Check for existing config first
                            _, stdout, _ = ssh.exec_command("cat /home/ubuntu/.thunder/config.json 2>/dev/null || echo ''")
                            existing_config = stdout.read().decode().strip()
                            device_id = None
                            
                            try:
                                if existing_config:
                                    config_data = json.loads(existing_config)
                                    if config_data.get("deviceId") and int(config_data.get("deviceId")) > 0:
                                        device_id = config_data["deviceId"]
                            except Exception:
                                # If we can't parse the existing config, we'll just get a new device ID
                                pass

                            # Only get new device ID if we couldn't read it from existing config
                            if device_id is None:
                                device_id, error = utils.get_next_id(token)
                                if error:
                                    logger.warning(f"Could not grab next device ID: {error}")
                                    return

                            config = {
                                "instanceId": instance_id,
                                "deviceId": device_id,
                                "gpuType": instance.get('gpuType', 't4').lower(),
                                "gpuCount": int(instance.get('numGpus', 1))
                            }

                            # Update binary and write config in a single command
                            remote_path = '/home/ubuntu/.thunder/libthunder.so'
                            remote_config_path = '/home/ubuntu/.thunder/config.json'
                            remote_token_path = '/home/ubuntu/.thunder/token'
                            thunder_dir = '/etc/thunder'
                            thunder_lib_path = f'{thunder_dir}/libthunder.so'
                            config_json = json.dumps(config, indent=4)
                            
                            commands = [
                                # Create directories with explicit permissions
                                f'sudo install -d -m 755 {thunder_dir}',
                                'sudo install -d -m 755 /home/ubuntu/.thunder',
                                
                                # Back up existing preload file
                                'sudo cp -a /etc/ld.so.preload /etc/ld.so.preload.bak || true',
                                
                                # Download to a temporary file first
                                f'curl -L https://storage.googleapis.com/client-binary/client_linux_x86_64 -o /tmp/libthunder.tmp',
                                f'sudo install -m 755 -o root -g root /tmp/libthunder.tmp {remote_path}',
                                'rm -f /tmp/libthunder.tmp',
                                f'[ -f "{remote_path}" ] && [ -s "{remote_path}" ] || (echo "Download failed" && exit 1)',
                                
                                # Create symlink for libthunder.so
                                f'sudo rm -f {thunder_lib_path} || true',
                                f'sudo ln -sf {remote_path} {thunder_lib_path}',
                                'sudo chown root:root /etc/thunder/libthunder.so',
                                'sudo chmod 755 /etc/thunder/libthunder.so',
                                
                                # Update preload file to use the symlinked path
                                f'echo "{thunder_lib_path}" | sudo tee /etc/ld.so.preload.new',
                                'sudo chown root:root /etc/ld.so.preload.new',
                                'sudo chmod 644 /etc/ld.so.preload.new',
                                'sudo mv /etc/ld.so.preload.new /etc/ld.so.preload',
                                
                                # Write config files
                                f'echo \'{config_json}\' > /tmp/config.tmp',
                                f'sudo install -m 644 -o root -g root /tmp/config.tmp {remote_config_path}',
                                'rm -f /tmp/config.tmp',
                                
                                f'echo \'{token}\' > /tmp/token.tmp',
                                f'sudo install -m 600 -o root -g root /tmp/token.tmp {remote_token_path}',
                                'rm -f /tmp/token.tmp',

                                # Symlink config and token to .thunder
                                'sudo rm -f /etc/thunder/config.json || true',
                                f'sudo ln -sf {remote_config_path} /etc/thunder/config.json',
                                'sudo chown root:root /etc/thunder/config.json',
                                'sudo chmod 644 /etc/thunder/config.json',
                                'sudo rm -f /etc/thunder/token || true',
                                f'sudo ln -sf {remote_token_path} /etc/thunder/token',
                                'sudo chown root:root /etc/thunder/token',
                                'sudo chmod 644 /etc/thunder/token'
                            ]
                            
                            command_string = ' && '.join(commands)
                            _, stdout, stderr = ssh.exec_command(command_string)
                            
                            exit_status = stdout.channel.recv_exit_status()
                            if exit_status != 0:
                                error_message = stderr.read().decode('utf-8')
                                raise Exception(f"Failed to update binary and write config: {error_message}")
                                
                            output = stdout.read().decode('utf-8')
                            logger.info(f"Binary transfer and config setup completed. Output: {output}")
                        
                        except Exception as e:
                            logger.error(f"Failed to update binary and write config: {e}")
                            return

                    # SSH Config stuff
                    host_alias = f"tnr-{instance_id}"
                    exists, _ = utils.get_ssh_config_entry(host_alias)
                    if not exists:
                        utils.add_instance_to_ssh_config(ip, keyfile, host_alias)
                        logger.info(f"Added new SSH config entry for {instance_id}")
                    else:
                        utils.update_ssh_config_ip(host_alias, ip, keyfile=keyfile)
                        logger.info(f"Updated SSH config IP for {instance_id}")

                    return
                    
                except ssh_exception.AuthenticationException:
                    logger.error("SSH authentication failed for instance %s", instance_id)
                    return
                except ssh_exception.NoValidConnectionsError:
                    logger.error("No valid connections could be established to instance %s", instance_id)
                    return
                except ssh_exception.SSHException as e:
                    logger.error(f"SSH error for instance %s: %s", instance_id, str(e))
                    return
                except Exception as e:
                    logger.error(f"Error connecting to instance {instance_id}: {str(e)}")
                    return
                    
            attempt += 1
            time.sleep(2)
            
        logger.error(f"Timed out waiting for instance {instance_id} to start")
    finally:
        # Always remove the lockfile, even if we error out
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
        except Exception as e:
            logger.error(f"Failed to remove lockfile: {e}")

def start_background_config(instance_id, token):
    """
    Spawn the background process to handle SSH configuration
    """
    # Instead of trying to re-run the script, we'll run Python with the command directly
    cmd = [
        sys.executable,
        "-c",
        f"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('{os.path.dirname(__file__)}'))))
from thunder import utils
from thunder.thunder import wait_and_configure_ssh
wait_and_configure_ssh('{instance_id}', '{token}')
        """
    ]
    
    try:
        Popen(
            cmd,
            start_new_session=True,  # Detach from parent process
            stdout=open(os.devnull, 'w'),
            stderr=open(os.devnull, 'w')
        )
    except Exception as e:
        # Log error but don't fail the main command
        logger = logging.getLogger("thunder")
        logger.error(f"Failed to start background configuration: {e}")
    
@cli.command(
    help="Start a stopped Thunder Compute instance. All data in the persistent storage will be preserved",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def start(instance_id):
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)
        token = get_token()
        
        # First check instance status
        success, error, instances = utils.get_instances(token, use_cache=False)
        if not success:
            raise click.ClickException(f"Failed to get instance status: {error}")
            
        instance = instances.get(instance_id)
        if not instance:
            raise click.ClickException(f"Instance {instance_id} not found")
            
        if instance["status"] == "STOPPING":
            raise click.ClickException(f"Cannot start instance {instance_id} while it is stopping. Please wait for it to fully stop first.")
            
        if instance["status"] == "RUNNING":
            click.echo(click.style(f"Instance {instance_id} is already running", fg="yellow"))
            return
            
        success, error = utils.start_instance(instance_id, token)
        
    if success:
        # Attempt immediate key creation
        if not utils.add_key_to_instance(instance_id, token):
            click.echo(click.style(
                f"Warning: Unable to create or attach SSH key for instance {instance_id} at start. The background config will retry automatically.",
                fg="yellow"
            ))
        
        start_background_config(instance_id, token)
        click.echo(
            click.style(
                f"Successfully started Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )
    else:
        raise click.ClickException(
            f"Failed to start Thunder Compute instance {instance_id}: {error}"
        )


@cli.command(hidden=True)
@click.argument("instance_id")
@click.argument("token")
def background_config(instance_id, token):
    """Hidden command to handle background SSH configuration"""
    wait_and_configure_ssh(instance_id, token)


@cli.command(
    help="Stop a running Thunder Compute instance. Stopped instances have persistent storage and can be restarted at any time",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
def stop(instance_id):
    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading", total=None)  # No description text
        token = get_token()
        _, _, instances = utils.get_instances(token, use_cache=False)
        for instance in instances:
            instance_not_found = True
            if instance == instance_id:
                instance_not_found = False
                success, error = utils.stop_instance(instance_id, token)
                break
    if instance_not_found:
        raise click.ClickException(f"Instance {instance_id} not found")
    elif success:
        click.echo(
            click.style(
                f"Successfully stopped Thunder Compute instance {instance_id}",
                fg="cyan",
            )
        )
        try:
            device_ip = instances[instance_id]['ip']
            utils.remove_host_key(device_ip)
            utils.remove_instance_from_ssh_config(f"tnr-{instance_id}")
        except Exception as _:
            pass
    else:
        raise click.ClickException(
            f"Failed to stop Thunder Compute instance {instance_id}: {error}"
        )
    
def get_next_drive_letter():
    """Find the next available drive letter on Windows"""
    if platform.system() != "Windows":
        return None
    
    used_drives = set()
    for letter in ascii_uppercase:
        if os.path.exists(f"{letter}:"):
            used_drives.add(letter)

    for letter in ascii_uppercase:
        if letter not in used_drives:
            return f"{letter}:"
    raise RuntimeError("No available drive letters")

def cleanup_mount(mount_point, hide_warnings=False):
    """Unmount the SMB share"""
    os_type = platform.system()
    
    if os_type == "Windows":
        if ":" in str(mount_point):  # It's a drive letter
            cmd = ["net", "use", str(mount_point), "/delete", "/y"]
    elif os_type == "Darwin":
        cmd = ["diskutil", "unmount", str(mount_point)]
    else:  # Linux
        cmd = ["sudo", "umount", str(mount_point)]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        click.echo(click.style(f"📤 Unmounted {mount_point}", fg="yellow"))
    except subprocess.CalledProcessError:
        if not hide_warnings:
            click.echo(click.style(f"⚠️  Failed to unmount {mount_point}", fg="red"))

def mount_smb_share(share_name):
    """
    Mount SMB share based on OS and share_name under ~/tnrmount/<share_name> on non-Windows.
    On Windows, assign a drive letter.
    """
    os_type = platform.system()
    base_mount_dir = Path.home() / "tnrmount"
    if os_type != "Windows":
        local_mount_point = base_mount_dir / share_name
        local_mount_point = local_mount_point.expanduser()
    else:
        local_mount_point = get_next_drive_letter()

    # Attempt to unmount if exists
    if os_type != "Windows" and local_mount_point.exists():
        cleanup_mount(local_mount_point, hide_warnings=True)
    
    try:
        if os_type == "Windows":
            # Ensure the SMB share is accessible on default SMB port 445
            # Requires `ssh -L 445:localhost:445 ubuntu@<instance_ip>` done beforehand.

            # Use a standard UNC path without port
            net_cmd = "C:\\Windows\\System32\\net.exe"
            if not os.path.exists(net_cmd):
                net_cmd = "net"  # fallback if System32 isn't accessible

            cmd = [net_cmd, "use", local_mount_point, f"\\\\localhost\\{share_name}", '/TCPPORT:1445']
            subprocess.run(cmd, check=True, capture_output=True)
            return local_mount_point
        else:
            local_mount_point.mkdir(parents=True, exist_ok=True)
            if os_type == "Linux":
                click.echo(click.style(f"Mounting SMB share {share_name} to {local_mount_point}. You may be required to enter your password.", fg="cyan"))
                cmd = [
                    "sudo", "mount", "-t", "cifs", f"//localhost/{share_name}", str(local_mount_point),
                    "-o", "user=guest,password='',port=1445,rw"
                ]
            else:  # macOS
                cmd = ["mount_smbfs", f"//guest@localhost:1445/{share_name}", str(local_mount_point)]

            subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL, timeout=5)
            return local_mount_point
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)
        if 'exit status 32' in error_msg and os_type == "Linux":
            click.echo(click.style(f"❌ To enable SMB mounting, cifs-utils must be installed. If you'd like to connect to the instance without mounting, please use the --nomount flag", fg="red"))
        else:
            click.echo(click.style(f"❌ Error mounting share '{share_name}'", fg="red"))
            if IS_WINDOWS:
                click.echo(click.style(f"If you're seeing issues mounting network shares, you may want to turning off the Windows SMB server and restarting.", fg="cyan"))
        raise
    except subprocess.TimeoutExpired:
        click.echo(click.style(f"❌ Error mounting share '{share_name}'", fg="red"))
        if os_type == "Darwin":
            click.echo("""
Looks like you're on a Mac. Try restarting the SMB process:
sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.smbd.plist
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.smbd.plist
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server.plist EnabledServices -array disk
            """, fg="cyan")
        raise

def configure_remote_samba_shares(ssh, shares):
    """
    Append shares configuration to remote /etc/samba/shares.conf (included by smb.conf) and restart smbd.
    Backup original config first.
    """
    # Ensure shares.conf exists
    stdin, stdout, stderr = ssh.exec_command("sudo touch /etc/samba/shares.conf && sudo chmod 644 /etc/samba/shares.conf")
    stdout.read()
    err = stderr.read().decode()
    if err:
        raise RuntimeError(f"Error preparing shares.conf: {err}")

    backup_cmd = "sudo cp /etc/samba/shares.conf /etc/samba/shares.conf.bak"
    stdin, stdout, stderr = ssh.exec_command(backup_cmd)
    stdout.read()
    err = stderr.read().decode()
    if err:
        # Not critical if backup fails (maybe first time run), but let's warn
        click.echo(click.style(f"⚠️ Warning: Could not backup shares.conf: {err}", fg="yellow"))

    # Build share config
    share_config_lines = []
    for share in shares:
        share_config_lines.append(f"[{share['name']}]")
        share_config_lines.append(f"path = {share['path']}")
        share_config_lines.append("browseable = yes")
        share_config_lines.append("writable = yes")
        share_config_lines.append("read only = no")
        share_config_lines.append("guest ok = yes")
        share_config_lines.append("force user = root")
        share_config_lines.append("create mask = 0777")
        share_config_lines.append("directory mask = 0777")
        share_config_lines.append("")
    share_config = "\n".join(share_config_lines)

    # Write shares to shares.conf (overwrite rather than append to keep control)
    cmd = f'echo "{share_config}" | sudo tee /etc/samba/shares.conf'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()
    err = stderr.read().decode()
    if err:
        raise RuntimeError(f"Error writing shares to shares.conf: {err}")

    # Restart Samba service
    restart_cmd = "sudo systemctl restart smbd"
    stdin, stdout, stderr = ssh.exec_command(restart_cmd)
    stdout.read()
    err = stderr.read().decode()
    if err:
        raise RuntimeError(f"Error restarting smbd: {err}")

def restore_original_smb_conf(ssh):
    """
    Restore the original shares.conf and restart Samba.
    """
    restore_cmd = "sudo cp /etc/samba/shares.conf.bak /etc/samba/shares.conf && sudo systemctl restart smbd"
    _, stdout, stderr = ssh.exec_command(restore_cmd)
    stdout.read()
    err = stderr.read().decode()
    if err:
        # If restore failed, just warn
        click.echo(click.style(f"⚠️  Failed to restore original shares.conf: {err}", fg="red"))

def echo_openssh_instructions():
    """Echo the OpenSSH instructions in a nicely formatted panel."""
    instructions = [
        "[white]1. Open Windows Settings (Windows key + I)",
        "2. Go to System > Optional features",
        "3. Click '+ Add a feature'",
        "4. Search for 'OpenSSH Client'",
        "5. Click Install",
        "6. Restart your terminal[/white]"
    ]
    
    panel = Panel(
        "\n".join(instructions),
        title="[cyan]Install OpenSSH Client[/cyan]",
        title_align="left",
        border_style="cyan",
        highlight=True,
        width=60,
        box=box.ROUNDED
    )
    Console().print(panel)

def check_windows_openssh():
    """Check if OpenSSH is available on Windows and provide guidance if it's not."""
    if not IS_WINDOWS:
        return True
    
    try:
        # Try to run ssh to check if it exists
        subprocess.run(["ssh", "-V"], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        # Check if we're running in PowerShell
        try:
            # This command will succeed in PowerShell and fail in cmd/other shells
            subprocess.run(["powershell", "-Command", "$PSVersionTable"], capture_output=True, check=True)
            is_powershell = True
        except (FileNotFoundError, subprocess.CalledProcessError):
            is_powershell = False

        if is_powershell:
            click.echo(click.style("\n🔍 OpenSSH is not installed. Attempting to install automatically. This may take a few minutes...", fg="yellow"))
            try:
                # Get the latest OpenSSH version and install it
                install_command = """
                $ErrorActionPreference = 'Stop'
                try {
                    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
                    Write-Output "ISADMIN:$isAdmin"
                    $sshCapability = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Client*' | Select-Object -First 1
                    if ($sshCapability) {
                        Add-WindowsCapability -Online -Name $sshCapability.Name
                        Write-Output $sshCapability.Name
                    } else {
                        Write-Error "OpenSSH Client package not found"
                    }
                } catch {
                    Write-Error $_.Exception.Message
                    exit 1
                }
                """
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-NonInteractive", "-Command", install_command],
                    capture_output=True,
                    text=True
                )
                
                # Check if we're admin from PowerShell output
                is_admin = "ISADMIN:True" in result.stdout

                if result.returncode == 0 and "OpenSSH.Client" in result.stdout:
                    version = [line for line in result.stdout.splitlines() if "OpenSSH.Client" in line][0]
                    click.echo(click.style(f"✅ Successfully installed OpenSSH {version}!", fg="green"))
                    click.echo(click.style("🔄 Please restart your terminal for the changes to take effect.", fg="cyan"))
                    return False
                else:
                    error_output = result.stderr.strip() if result.stderr else "Unknown error"
                    if "requires elevation" in error_output.lower() or "administrator" in error_output.lower():
                        click.echo(click.style("\n❌ Administrator privileges required for installation.", fg="red"))
                        click.echo(click.style("Please run your terminal as Administrator and try again. Alternatively:", fg="yellow"))
                        echo_openssh_instructions()
                    else:
                        click.echo(click.style(f"\n❌ Failed to install OpenSSH: {error_output}", fg="red"))
                        if is_admin:
                            click.echo(click.style("\nSince automatic installation failed with admin privileges, try these manual steps:", fg="cyan"))
                            echo_openssh_instructions()
            except Exception as e:
                # Handle any other exceptions that might occur
                error_msg = str(e)
                click.echo(click.style("\n❌ Automatic installation failed.", fg="red"))
                click.echo(click.style(f"Error: {error_msg}", fg="yellow"))
        
        # If not in PowerShell or auto-install failed without admin, show standard instructions
        if not is_powershell:
            echo_openssh_instructions()
            click.echo(click.style("\nAlternatively, you can run PowerShell as Administrator and run 'tnr connect' again", fg="cyan"))
        return False
    except subprocess.CalledProcessError:
        return False

@cli.command(
    help="Connect to the Thunder Compute instance with the specified instance_id",
)
@click.argument("instance_id", required=False)
@click.option("-t", "--tunnel", type=int, multiple=True, help="Forward specific ports from the remote instance to your local machine (e.g. -t 8080 -t 3000). Can be specified multiple times")
@click.option("--mount", type=str, multiple=True, help="Mount local folders to the remote instance. Specify the remote path (e.g. --mount /home/ubuntu/data). Can use ~ for home directory. Can be specified multiple times")
@click.option("--nomount", is_flag=True, default=False, help="Disable automatic folder mounting, including template-specific defaults like ComfyUI folders")
@click.option("--debug", is_flag=True, default=False, hidden=True, help="Show debug timing information")
def connect(tunnel, instance_id=None, mount=None, nomount=False, debug=False):
    # Check for OpenSSH on Windows first
    if not check_windows_openssh():
        return
        
    # Initialize timing dictionary to store all timings
    timings = {}
    start_time = time.time()
    
    instance_id = instance_id or "0"
    click.echo(click.style(f"Connecting to Thunder Compute instance {instance_id}...", fg="cyan"))
    
    # Check for existing lockfile
    lock_check_start = time.time()
    lock_file = get_instance_lock_file(instance_id)
    if os.path.exists(lock_file):
        try:
            with open(lock_file, 'r') as f:
                pid = int(f.read().strip())
                
            # Check if it's our own process (parent process)
            if pid == os.getppid():
                # This is a background config we spawned, wait for it
                click.echo(click.style("Waiting for background configuration to complete...", fg="yellow"))
                if not wait_for_background_config(instance_id):
                    raise click.ClickException(
                        "Timed out waiting for background configuration to complete. Please try again or contact support@thundercompute.com"
                    )
            elif is_lock_stale(lock_file):
                try:
                    os.remove(lock_file)
                except Exception:
                    pass
        except ValueError:
            try:
                os.remove(lock_file)
            except Exception:
                pass
    timings['lock_check'] = time.time() - lock_check_start
    
    # Create our own lockfile
    try:
        write_lock_start = time.time()
        write_lock_file(lock_file)
        timings['write_lock'] = time.time() - write_lock_start

        token_start = time.time()
        token = get_token()
        timings['get_token'] = time.time() - token_start

        instances_start = time.time()
        success, error, instances = utils.get_instances(token, update_ips=True)
        if not success:
            raise click.ClickException(f"Failed to list Thunder Compute instances: {error}")
        timings['get_instances'] = time.time() - instances_start

        instance_check_start = time.time()
        instance = next(((curr_id, meta) for curr_id, meta in instances.items() if curr_id == instance_id), None)
        if not instance:
            raise click.ClickException(
                f"Unable to find instance {instance_id}. Check available instances with `tnr status`"
            )
        
        instance_id, metadata = instance
        ip = metadata.get("ip")
        if not ip:
            raise click.ClickException(
                f"Unable to connect to instance {instance_id}, the instance is not reporting an IP address (is it fully started?)."
            )
        timings['instance_check'] = time.time() - instance_check_start

        keyfile_start = time.time()
        keyfile = utils.get_key_file(metadata["uuid"])
        if not os.path.exists(keyfile):
            created, key_error = utils.add_key_to_instance(instance_id, token)
            if not created or not os.path.exists(keyfile):
                # improved error usage
                user_msg = key_error or f"Unable to find or create a valid SSH key for instance {instance_id}."
                raise click.ClickException(user_msg)
        timings['keyfile_setup'] = time.time() - keyfile_start

        # Attempt SSH connection
        ssh_connect_start = time.time()
        try:
            ssh = robust_ssh_connect(ip, keyfile, max_wait=60, interval=1, username="ubuntu")
        except Exception as e:
            raise click.ClickException(f"Failed to connect to instance {instance_id}: {e} due to ssh connection issues")
        timings['ssh_connect'] = time.time() - ssh_connect_start

        # Add token to environment
        token_env_start = time.time()
        cmd = f"""grep -q 'export TNR_API_TOKEN' /home/ubuntu/.bashrc || echo 'export TNR_API_TOKEN={token}' >> /home/ubuntu/.bashrc"""
        _, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            error = stderr.read().decode().strip()
            click.echo(click.style(f"Warning: Token environment setup failed: {error}", fg="yellow"))
        timings['token_env_setup'] = time.time() - token_env_start

        # Check for active SSH sessions before updating binary and writing config
        binary_update_start = time.time()
        has_active_sessions = check_active_ssh_sessions(ssh)
        if not has_active_sessions:
            # Check for existing config first
            _, stdout, _ = ssh.exec_command("cat /home/ubuntu/.thunder/config.json 2>/dev/null || echo ''")
            existing_config = stdout.read().decode().strip()
            device_id = None
            
            try:
                if existing_config:
                    config_data = json.loads(existing_config)
                    if config_data.get("deviceId") and int(config_data.get("deviceId")) > 0:
                        device_id = config_data["deviceId"]
            except Exception:
                # If we can't parse the existing config, we'll just get a new device ID
                pass

            # Only get new device ID if we couldn't read it from existing config
            if device_id is None:
                device_id, error = utils.get_next_id(token)
                if error:
                    raise click.ClickException(f"Could not grab next device ID: {error}")
            
            config = {
                "instanceId": instance_id,
                "deviceId": device_id,
                "gpuType": metadata.get('gpuType', 't4').lower(),
                "gpuCount": int(metadata.get('numGpus', 1))
            }
            
            # Update binary and write config in a single command
            try:
                remote_path = '/home/ubuntu/.thunder/libthunder.so'
                remote_config_path = '/home/ubuntu/.thunder/config.json'
                remote_token_path = '/home/ubuntu/.thunder/token'
                thunder_dir = '/etc/thunder'
                thunder_lib_path = f'{thunder_dir}/libthunder.so'
                config_json = json.dumps(config, indent=4)
                
                commands = [
                    # Create directories with explicit permissions
                    f'sudo install -d -m 755 {thunder_dir}',
                    'sudo install -d -m 755 /home/ubuntu/.thunder',
                    
                    # Back up existing preload file
                    'sudo cp -a /etc/ld.so.preload /etc/ld.so.preload.bak || true',
                    
                    # Download to a temporary file first
                    f'curl -L https://storage.googleapis.com/client-binary/client_linux_x86_64 -o /tmp/libthunder.tmp',
                    f'sudo install -m 755 -o root -g root /tmp/libthunder.tmp {remote_path}',
                    'rm -f /tmp/libthunder.tmp',
                    f'[ -f "{remote_path}" ] && [ -s "{remote_path}" ] || (echo "Download failed" && exit 1)',
                    
                    # Create symlink for libthunder.so
                    f'sudo rm -f {thunder_lib_path} || true',
                    f'sudo ln -sf {remote_path} {thunder_lib_path}',
                    'sudo chown root:root /etc/thunder/libthunder.so',
                    'sudo chmod 755 /etc/thunder/libthunder.so',
                    
                    # Update preload file to use the symlinked path
                    f'echo "{thunder_lib_path}" | sudo tee /etc/ld.so.preload.new',
                    'sudo chown root:root /etc/ld.so.preload.new',
                    'sudo chmod 644 /etc/ld.so.preload.new',
                    'sudo mv /etc/ld.so.preload.new /etc/ld.so.preload',
                    
                    # Write config files
                    f'echo \'{config_json}\' > /tmp/config.tmp',
                    f'sudo install -m 644 -o root -g root /tmp/config.tmp {remote_config_path}',
                    'rm -f /tmp/config.tmp',
                    
                    f'echo \'{token}\' > /tmp/token.tmp',
                    f'sudo install -m 600 -o root -g root /tmp/token.tmp {remote_token_path}',
                    'rm -f /tmp/token.tmp',

                    # Symlink config and token to .thunder
                    'sudo rm -f /etc/thunder/config.json || true',
                    f'sudo ln -sf {remote_config_path} /etc/thunder/config.json',
                    'sudo chown root:root /etc/thunder/config.json',
                    'sudo chmod 644 /etc/thunder/config.json',
                    'sudo rm -f /etc/thunder/token || true',
                    f'sudo ln -sf {remote_token_path} /etc/thunder/token',
                    'sudo chown root:root /etc/thunder/token',
                    'sudo chmod 644 /etc/thunder/token'
                ]
                
                command_string = ' && '.join(commands)
                _, stdout, stderr = ssh.exec_command(command_string)
                
                exit_status = stdout.channel.recv_exit_status()
                if exit_status != 0:
                    error_message = stderr.read().decode('utf-8')
                    raise click.ClickException(f"Failed to update binary and write config: {error_message}")
            except Exception as e:
                raise click.ClickException(f"Failed to update binary and write config: {e}")
        timings['binary_update'] = time.time() - binary_update_start
        
        # Add to SSH config
        try:
            ssh_config_start = time.time()
            host_alias = f"tnr-{instance_id}"
            exists, _ = utils.get_ssh_config_entry(host_alias)
            if not exists:
                utils.add_instance_to_ssh_config(ip, keyfile, host_alias)
            else:
                utils.update_ssh_config_ip(host_alias, ip, keyfile=keyfile)
            timings['ssh_config_setup'] = time.time() - ssh_config_start
        except Exception as e:
            click.echo(click.style(f"Error adding instance to SSH config. Proceeding with connection... {e}", fg="red"))

        tunnel_setup_start = time.time()
        tunnel_args = []
        for port in tunnel:
            tunnel_args.extend(["-L", f"{port}:localhost:{port}"])

        template = metadata.get('template', 'base')
        template_ports = OPEN_PORTS.get(template, [])
        for port in template_ports:
            tunnel_args.extend(["-L", f"{port}:localhost:{port}"])
        timings['tunnel_setup'] = time.time() - tunnel_setup_start

        mount = list(mount)

        # Automatically mount folders for templates - don't do this for Windows
        mount_setup_start = time.time()
        if template in AUTOMOUNT_FOLDERS.keys() and not nomount and not IS_WINDOWS:
            if AUTOMOUNT_FOLDERS[template] not in mount:
                mount.append(AUTOMOUNT_FOLDERS[template])

        shares_to_mount = []
        remote_home = "/home/ubuntu"
        for share_path in mount:
            # Expand ~ to /home/ubuntu if present
            # This is still allowed, just optional
            remote_home = "/home/ubuntu"
            if share_path.startswith("~"):
                share_path = share_path.replace("~", remote_home, 1)

            if share_path.startswith(remote_home):
                chmod_cmd = f"sudo chmod -R 777 '{share_path}'"
                ssh.exec_command(chmod_cmd)
            # Just ensure directory exists
            _, stdout, _ = ssh.exec_command(f"[ -d '{share_path}' ] && echo 'OK' || echo 'NO'")
            result = stdout.read().decode().strip()
            if result != "OK":
                raise click.ClickException(f"The directory '{share_path}' does not exist on the remote instance.")

            share_name = os.path.basename(share_path.strip("/")) or "root"

            shares_to_mount.append({
                "name": share_name,
                "path": share_path
            })
        timings['mount_setup'] = time.time() - mount_setup_start

        ssh_interactive_cmd = [
            "ssh",
            "-q",
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "IdentitiesOnly=yes",
            "-o", "UserKnownHostsFile=/dev/null",
            "-i", keyfile,
            "-t"
        ] + tunnel_args + [
            f"ubuntu@{ip}"
        ]

        smb_tunnel_cmd = [
            "ssh",
            "-q",
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "IdentitiesOnly=yes",
            "-i", keyfile,
            "-L", "1445:localhost:445",
            "-N",
            f"ubuntu@{ip}"
        ]

        tunnel_process = None
        mounted_points = []

        def cleanup():
            for mp in mounted_points:
                cleanup_mount(mp)
            if tunnel_process and tunnel_process.poll() is None:
                tunnel_process.terminate()
                tunnel_process.wait()
            restore_original_smb_conf(ssh)

        try:
            smb_setup_start = time.time()
            if shares_to_mount and not nomount:
                atexit.register(cleanup)
                # Configure shares on remote
                try:
                    configure_remote_samba_shares(ssh, shares_to_mount)
                except Exception as e:
                    click.echo(click.style(f"❌ Error configuring samba shares: {e}", fg="red"))
                    return

                # Start SMB tunnel
                tunnel_process = subprocess.Popen(
                    smb_tunnel_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                # Test tunnel
                max_retries = 3
                for attempt in range(max_retries):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(5)
                    try:
                        s.connect(("localhost", 1445))
                        s.close()
                        break
                    except socket.error:
                        s.close()
                        if attempt < max_retries - 1:
                            click.echo(click.style("Retrying SMB tunnel connection...", fg="yellow"))
                            time.sleep(2)
                        else:
                            raise RuntimeError("Failed to establish SMB tunnel")

                # Mount each share
                for share in shares_to_mount:
                    share_name = share["name"]
                    click.echo(click.style(f"📥 Mounting SMB share '{share_name}'...", fg="green"))
                    try:
                        mp = mount_smb_share(share_name)
                        mounted_points.append(mp)
                        click.echo(click.style(f"✅ Mounted {share_name} at {mp}\n", fg="green"))
                    except Exception:
                        # If mounting fails for this share, cleanup will occur at exit
                        pass
            timings['smb_setup'] = time.time() - smb_setup_start

            # Delete lockfile if it exists
            if os.path.exists(lock_file):
                os.remove(lock_file)

            # Print timing summary before interactive session
            if debug:
                total_time = time.time() - start_time
                click.echo("\n🕒 Connection timing breakdown:")
                for operation, duration in timings.items():
                    percentage = (duration / total_time) * 100
                    click.echo(f"  • {operation}: {duration:.2f}s ({percentage:.1f}%)")
                click.echo(f"  Total setup time: {total_time:.2f}s\n")

            # Start interactive SSH
            subprocess.run(ssh_interactive_cmd)
        except KeyboardInterrupt:
            click.echo(click.style("\n🛑 Interrupted by user", fg="yellow"))
        except Exception as e:
            click.echo(click.style(f"❌ Error: {str(e)}", fg="red"))
        finally:
            click.echo(click.style("⚡ Exiting thunder instance ⚡", fg="green"))
    finally:
        # Always clean up our lockfile
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
        except Exception as e:
            pass

def _complete_path(ctx, param, incomplete):
    """Custom path completion that handles both local paths and remote paths."""        
    # Unix-style path handling for remote paths
    if ':' in incomplete:
        instance_id, path = incomplete.split(':', 1)
        return []
    
    # For local paths, use Click's built-in path completion
    return click.Path(exists=True).shell_complete(ctx, param, incomplete)

def _parse_path(path):
    """Parse a path into (instance_id, path) tuple."""
    # First check if it matches the remote path pattern (instance_id:path)
    parts = path.split(":", 1)
    if len(parts) > 1:
        # Check if this is actually a Windows drive path (e.g. C:\path)
        if platform.system() == "Windows" and len(parts[0]) == 1 and parts[0].isalpha():
            return (None, path)
        return (parts[0], parts[1])
    
    return (None, path)

@cli.command()
@click.argument("source_path", required=True, shell_complete=_complete_path if not platform.system() == "Windows" else None)
@click.argument("destination_path", required=True, shell_complete=_complete_path if not platform.system() == "Windows" else None)
def scp(source_path, destination_path):
    """Transfers files between your local machine and Thunder Compute instances.

    Arguments:\n
        SOURCE_PATH: Path to copy from. For instance files use 'instance_id:/path/to/file'\n
        DESTINATION_PATH: Path to copy to. For instance files use 'instance_id:/path/to/file'\n\n

    Examples:\n
        Copy local file to instance\n
            $ tnr scp myfile.py abc123:/home/ubuntu/\n
        Copy from instance to local\n
            $ tnr scp abc123:/home/ubuntu/results.csv ./
    """
    try:
        token = get_token()
        success, error, instances = utils.get_instances(token)
        if not success:
            raise click.ClickException(f"Failed to list Thunder Compute instances: {error}")

        # Parse source and destination paths
        src_instance, src_path = _parse_path(source_path)
        dst_instance, dst_path = _parse_path(destination_path)

        # Validate that exactly one path is remote
        if (src_instance and dst_instance) or (not src_instance and not dst_instance):
            raise click.ClickException(
                "Please specify exactly one remote path (instance_id:path) and one local path"
            )

        # Determine direction and get instance details
        instance_id = src_instance or dst_instance
        local_to_remote = bool(dst_instance)
        
        if instance_id not in instances:
            raise click.ClickException(f"Instance '{instance_id}' not found")

        metadata = instances[instance_id]
        if not metadata["ip"]:
            raise click.ClickException(
                f"Instance {instance_id} is not available. Use 'tnr status' to check if the instance is running"
            )

        # Setup SSH connection
        ssh = _setup_ssh_connection(instance_id, metadata, token)
        
        # Prepare paths
        local_path = source_path if local_to_remote else destination_path
        remote_path = dst_path if local_to_remote else src_path
        remote_path = remote_path or "~/"

        # Normalize paths for Windows
        if platform.system() == "Windows":
            # Store original path for error messages
            original_local_path = local_path
            
            # Convert to proper Windows path
            local_path = os.path.normpath(local_path)
            
            # Handle relative paths starting with ./ or .\ by removing them
            if local_path.startswith('.\\') or local_path.startswith('./'):
                local_path = local_path[2:]
            
            # For display purposes
            display_path = original_local_path
        else:
            display_path = local_path

        # Verify remote path exists before transfer
        if not local_to_remote:
            if not _verify_remote_path(ssh, remote_path):
                raise click.ClickException(
                    f"Remote path '{remote_path}' does not exist on instance {instance_id}"
                )

        # Setup progress bar
        with Progress(
            BarColumn(
                complete_style="cyan",
                finished_style="cyan",
                pulse_style="white"
            ),
            TextColumn("[cyan]{task.description}", justify="right"),
            transient=True
        ) as progress:
            click.echo(click.style(
                f"Copying {display_path} {'to' if local_to_remote else 'from'} {remote_path} {'on' if local_to_remote else 'from'} remote instance {instance_id}...",
                fg="white"
            ))
            
            # Perform transfer
            _perform_transfer(
                ssh, 
                local_path, 
                remote_path, 
                instance_id, 
                local_to_remote, 
                progress
            )

    except paramiko.SSHException as e:
        raise click.ClickException(f"SSH connection error: {str(e)}")
    except SCPException as e:
        error_msg = str(e)
        if "No such file or directory" in error_msg:
            if local_to_remote:
                raise click.ClickException(f"Local file '{display_path}' not found")
            else:
                raise click.ClickException(
                    f"Remote file '{remote_path}' not found on instance {instance_id}"
                )
        raise click.ClickException(f"SCP transfer failed: {error_msg}")
    except Exception as e:
        raise click.ClickException(f"Unexpected error: {str(e)}")

def _verify_remote_path(ssh, path):
    """Check if remote path exists."""
    cmd = f'test -e $(eval echo {path}) && echo "EXISTS"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode().strip() == "EXISTS"

def _setup_ssh_connection(instance_id, metadata, token):
    """Setup and return SSH connection to instance."""
    keyfile = utils.get_key_file(metadata["uuid"])
    if not os.path.exists(keyfile):
        if not utils.add_key_to_instance(instance_id, token):
            raise click.ClickException(
                f"Unable to find or create SSH key file for instance {instance_id}"
            )

    # Try to connect for up to 60 seconds
    start_time = time.time()
    last_error = None
    while time.time() - start_time < 60:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                metadata["ip"],
                username="ubuntu",
                key_filename=keyfile,
                timeout=10
            )
            return ssh
        except Exception as e:
            last_error = e
            time.sleep(2)  # Add small delay between retries
            
    raise click.ClickException(
        f"Failed to connect to instance {instance_id} after 60 seconds: {str(last_error)}"
    )

def _get_remote_size(ssh, path):
    """Calculate total size of remote file or directory."""
    # Expand any ~ in the path
    cmd = f'eval echo {path}'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    expanded_path = stdout.read().decode().strip()
    
    # Check if it's a file
    cmd = f'if [ -f "{expanded_path}" ]; then stat --format=%s "{expanded_path}"; else echo "DIR"; fi'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().decode().strip()
    
    if result != "DIR":
        try:
            return int(result)
        except ValueError:
            return None
    
    # If it's a directory, get total size
    cmd = f'du -sb "{expanded_path}" | cut -f1'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    try:
        size = int(stdout.read().decode().strip())
        return size
    except (ValueError, IndexError):
        return None

def _get_local_size(path):
    """Calculate total size of local file or directory."""
    path = os.path.expanduser(path)
    if os.path.isfile(path):
        return os.path.getsize(path)
    
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total

def _perform_transfer(ssh, local_path, remote_path, instance_id, local_to_remote, progress):
    """Perform the actual SCP transfer with progress bar."""
    total_size = 0
    transferred_size = 0
    file_count = 0
    current_file = ""
    current_file_size = 0
    current_file_transferred = 0

    # Pre-calculate total size
    try:
        if local_to_remote:
            total_size = _get_local_size(local_path)
        else:
            total_size = _get_remote_size(ssh, remote_path)
    except Exception as e:
        click.echo(click.style("Warning: Could not pre-calculate total size", fg="yellow"))
        total_size = None

    def progress_callback(filename, size, sent):
        nonlocal transferred_size, file_count, current_file, current_file_size, current_file_transferred
        
        if sent == 0:  # New file started
            file_count += 1
            current_file = os.path.basename(filename)
            current_file_size = size
            current_file_transferred = 0
            
            # Handle both bytes and string filenames
            display_filename = current_file.decode('utf-8') if isinstance(current_file, bytes) else current_file
            
            if total_size is None:
                progress.update(
                    task,
                    description=f"File {file_count}: {display_filename} - {_format_size(0)}/{_format_size(size)}"
                )
            else:
                progress.update(
                    task,
                    description=f"File {file_count}: {display_filename} - {_format_size(0)}/{_format_size(size)}"
                )
        else:
            # Calculate the increment since last update
            increment = sent - current_file_transferred
            transferred_size += increment
            current_file_transferred = sent
            
            if total_size is not None:
                progress.update(task, completed=transferred_size)
            
            # Handle both bytes and string filenames
            display_filename = current_file.decode('utf-8') if isinstance(current_file, bytes) else current_file
            
            progress.update(
                task,
                description=f"File {file_count}: {display_filename} - {_format_size(sent)}/{_format_size(current_file_size)}"
            )

    if local_to_remote:
        action_text = f"Copying {local_path} to {remote_path} on remote instance {instance_id}"
    else:
        action_text = f"Copying {remote_path} from instance {instance_id} to {local_path}"

    click.echo(click.style(f"{action_text}...", fg="white"))
    
    task = progress.add_task(
        description="Starting transfer...",
        total=total_size if total_size else None
    )
    
    transport = ssh.get_transport()
    transport.use_compression(True)

    with SCPClient(transport, progress=progress_callback) as scp:
        if local_to_remote:
            scp.put(local_path, remote_path, recursive=True)
        else:
            scp.get(remote_path, local_path, recursive=True)

    click.echo(click.style(
        f"\nSuccessfully transferred {file_count} files ({_format_size(total_size)})",
        fg="cyan"
    ))

def _format_size(size):
    """Convert size in bytes to human readable format."""
    if size is None:
        return "unknown size"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024 or unit == 'TB':
            return f"{size:.2f} {unit}"
        size /= 1024


@cli.command(
    help="Log in to Thunder Compute, prompting the user to generate an API token at console.thundercompute.com. Saves the API token to ~/.thunder/token",
    hidden=INSIDE_INSTANCE,
)
def login():
    if not logging_in:
        auth.login()


@cli.command(
    help="Log out of Thunder Compute and deletes the saved API token",
    hidden=INSIDE_INSTANCE,
)
def logout():
    auth.logout()


def get_version_cache_file():
    basedir = join(os.path.expanduser("~"), ".thunder", "cache")
    if not os.path.isdir(basedir):
        os.makedirs(basedir)
    return join(basedir, "version_requirements.json")

def does_meet_min_required_version():
    CACHE_TTL = 3600  # 1 hour
    cache_file = get_version_cache_file()
    
    # Check if we have a valid cached result
    try:
        if os.path.exists(cache_file):
            with open(cache_file) as f:
                cached = json.load(f)
                current_version = version(PACKAGE_NAME)
                # If a user updates, we want to wipe the cache
                if cached['current_version'] != current_version:
                    pass
                elif time.time() - cached['timestamp'] < CACHE_TTL:
                    return tuple(cached['result'])
    except Exception:
        # If there's any error reading cache, continue to make the API call
        pass

    try:
        current_version = version(PACKAGE_NAME)
        response = requests.get(
            f"https://api.thundercompute.com:8443/min_version", timeout=10
        )
        json_data = response.json() if response else {}
        min_version = json_data.get("version")
        
        if version_parser.parse(current_version) < version_parser.parse(min_version):
            result = (False, (current_version, min_version))
        else:
            result = (True, None)

        # Cache the result
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'result': result,
                    'min_version': min_version,  # Store the actual API response
                    'current_version': current_version
                }, f)
        except Exception:
            # If caching fails, just continue
            pass
        return result

    except Exception as e:
        print(e)
        click.echo(
            click.style(
                "Warning: Failed to fetch minimum required tnr version",
                fg="yellow",
            )
        )
        return True, None

@cli.command(hidden=True)
def creds():
    token = get_token()
    uid = utils.get_uid(token)
    click.echo(f'{token},{uid}')
    
@cli.command(
    help="Setup",
    hidden=True,
)
@click.option('-g', '--global', 'global_setup', is_flag=True, help='Perform global setup')
def setup(global_setup):
    if not IS_WINDOWS:
        setup_cmd.setup(global_setup, get_token())
    else:
        raise click.ClickException("Setup is not supported on Windows")

@cli.command(
    help="Modify a Thunder Compute instance's properties (CPU, GPU, storage)",
    hidden=INSIDE_INSTANCE,
)
@click.argument("instance_id", required=True)
@click.option('--vcpus', type=click.Choice(['4', '8', '16', '32', '64']), 
    help='New number of vCPUs. Cost scales with vCPU count')
@click.option('--gpu', type=click.Choice(['t4', 'a100', 'a100xl']), 
    help='New GPU type: T4 (16GB, inference) or A100 (40GB, training), or A100XL (80GB, training)')
@click.option('--num-gpus', hidden=True, type=click.Choice(['1', '2']), 
    help='New number of GPUs to request. Multiple GPUs increase costs proportionally')
@click.option("--disk-size-gb", type=int, metavar="SIZE_GB", 
    help="New disk size in GB (max: 1024). Can only increase disk size")
def modify(instance_id, vcpus, gpu, num_gpus, disk_size_gb):
    """Modify properties of a Thunder Compute instance.
    
    For running instances, only disk size increases are allowed.
    For stopped instances, all properties can be modified.
    At least one modification option must be specified.
    """
    # Validate at least one option is provided
    if not any([vcpus, gpu, num_gpus, disk_size_gb]):
        raise click.ClickException(
            "At least one modification option (--vcpus, --gpu, --num-gpus, or --disk-size-gb) must be specified"
        )

    token = get_token()
    success, error, instances = utils.get_instances(token)
    if not success:
        raise click.ClickException(f"Failed to list Thunder Compute instances: {error}")

    metadata = instances.get(instance_id)
    if not metadata:
        raise click.ClickException(f"Instance {instance_id} not found")

    is_running = metadata["status"] != "STOPPED"
    is_pending = metadata["status"] == "PENDING"
    
    if is_pending:
        raise click.ClickException("Instance is pending. Please wait for the previous operation to complete.")
    
    # If instance is running, only allow disk resize
    if is_running:
        if any([vcpus, gpu, num_gpus]):
            raise click.ClickException("Cannot modify running instances. Stop your instance with `tnr stop` and retry.")
        if not disk_size_gb:
            raise click.ClickException("No modifications specified")
    
    # Validate disk size changes
    if disk_size_gb:
        current_size = int(metadata["storage"])
        if current_size >= disk_size_gb:
            raise click.ClickException(f"Current disk size ({current_size}GB) is already greater than or equal to requested size ({disk_size_gb}GB)")
        if disk_size_gb > 1024:
            raise click.ClickException(f"The requested size ({disk_size_gb}GB) exceeds the 1TB limit")

    # For running instances, handle disk resize specially
    if is_running and disk_size_gb:
        ip = metadata["ip"]
        if not ip:
            raise click.ClickException(f"Instance {instance_id} has no valid IP")

        keyfile = utils.get_key_file(metadata["uuid"])
        if not os.path.exists(keyfile):
            if not utils.add_key_to_instance(instance_id, token):
                raise click.ClickException(f"Unable to find or create SSH key file for instance {instance_id}")

        # Establish SSH connection with retries
        start_time = time.time()
        connection_successful = False
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        while time.time() - start_time < 60:
            try:
                timeout = 10 if platform.system() == 'Darwin' else None
                ssh.connect(ip, username="ubuntu", key_filename=keyfile, timeout=timeout)
                connection_successful = True
                break
            except Exception:
                time.sleep(5)

        if not connection_successful:
            raise click.ClickException(
                "Failed to connect to the instance within a minute. Please retry or contact support@thundercompute.com if the issue persists"
            )

        if current_size >= disk_size_gb:
            click.echo(click.style(
                f"❌ The current disk size ({current_size}GB) is already greater than or equal to the requested size ({disk_size_gb}GB)",
                fg="yellow"
            ))
            ssh.close()
            return

        message = "[yellow]This action cannot be undone, persistent disk size can only be increased.[/yellow]"
        panel = Panel(
            message,
            title=":warning:  Warning :warning: ",
            title_align="left",
            highlight=True,
            width=100,
            box=box.ROUNDED,
        )
        rich.print(panel)
        if not click.confirm("Would you like to continue?"):
            click.echo(click.style(
                "The operation has been cancelled. No changes to the instance have been made.",
                fg="cyan",
            ))
            ssh.close()
            return

        with DelayedProgress(
            SpinnerColumn(spinner_name="dots", style="white"),
            TextColumn("[white]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task("Resizing disk, this may take a minute", total=None)
            payload = {
                'disk_size_gb': disk_size_gb
            }
            success, error, _ = utils.modify_instance(instance_id, payload, token)
            if success:
                _, stdout, stderr = ssh.exec_command("""
                    sudo apt install -y cloud-guest-utils
                    sudo growpart /dev/sda 1
                    sudo resize2fs /dev/sda1
                """)
                stdout.read().decode()
                stderr.read().decode()
            
            ssh.close()

        if success:
            click.echo(click.style(
                f"Successfully resized the persistent disk for instance {instance_id} to {disk_size_gb}GB",
                fg="cyan",
            ))
        else:
            raise click.ClickException(f"Failed to resize the persistent disk: {error}")
        return

    # For stopped instances, proceed with normal modification logic
    if gpu and metadata["gpuType"] == gpu:
        raise click.ClickException("GPU type is already the same as the requested GPU type")
    if num_gpus and int(metadata["numGpus"]) == int(num_gpus):
        raise click.ClickException("Number of GPUs is already the same as the requested number of GPUs")
    if vcpus and int(metadata["cpuCores"]) == int(vcpus):
        raise click.ClickException("Number of vCPUs is already the same as the requested number of vCPUs")

    message = [
        "[yellow]This action will modify the instance's properties to:[/yellow]",
        f"[cyan]- {vcpus} vCPUs" if vcpus else None,
        f"[cyan]- {gpu.upper()} GPU" if gpu else None,
        f"[cyan]- {disk_size_gb}GB disk" if disk_size_gb else None,    ]
    panel = Panel(
        "\n".join([line for line in message if line]),
        highlight=True,
        width=100,
        box=box.ROUNDED,
    )
    rich.print(panel)
    if not click.confirm("Would you like to continue?"):
        click.echo(click.style(
            "The operation has been cancelled. No changes to the instance have been made.",
            fg="cyan",
        ))
        return

    # Prepare modification payload
    payload = {}
    if vcpus:
        payload['cpu_cores'] = int(vcpus)
    if gpu:
        payload['gpu_type'] = gpu
    if num_gpus:
        payload['num_gpus'] = int(num_gpus)
    if disk_size_gb:
        payload['disk_size_gb'] = disk_size_gb

    with DelayedProgress(
        SpinnerColumn(spinner_name="dots", style="white"),
        TextColumn("[white]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Modifying instance", total=None)
        success, error, _ = utils.modify_instance(instance_id, payload, token)
        time.sleep(10)

    if success:
        click.echo(click.style(
            f"Successfully queued instance modification! Track instance status with `tnr status`",
            fg="cyan",
        ))
    else:
        raise click.ClickException(f"Failed to modify instance: {error}")

if __name__ == "__main__":
    cli()

