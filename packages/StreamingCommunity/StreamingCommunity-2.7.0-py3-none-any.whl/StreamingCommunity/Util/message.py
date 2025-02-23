# 3.12.23

import os
import platform

# Internal utilities
from StreamingCommunity.Util.console import console
from StreamingCommunity.Util._jsonConfig import config_manager


# Variable
CLEAN = config_manager.get_bool('DEFAULT', 'clean_console')
SHOW = config_manager.get_bool('DEFAULT', 'show_message')


def start_message():
    """Display a stylized start message in the console."""
    
    msg = r'''
    ___                                                  _____ __                            _            
   /   |  ______________ _      ______ ______   _  __   / ___// /_________  ____ _____ ___  (_)___  ____ _
  / /| | / ___/ ___/ __ \ | /| / / __ `/ ___/  | |/_/   \__ \/ __/ ___/ _ \/ __ `/ __ `__ \/ / __ \/ __ `/
 / ___ |/ /  / /  / /_/ / |/ |/ / /_/ / /     _>  <    ___/ / /_/ /  /  __/ /_/ / / / / / / / / / / /_/ / 
/_/  |_/_/  /_/   \____/|__/|__/\__,_/_/     /_/|_|   /____/\__/_/   \___/\__,_/_/ /_/ /_/_/_/ /_/\__, /  
                                                                                                 /____/   
    '''.rstrip()

    if CLEAN: 
        os.system("cls" if platform.system() == 'Windows' else "clear")
    
    if SHOW:
        console.print(f"[purple]{msg}")

        # Print a decorative separator line using asterisks
        separator = "_" * (console.width - 2)  # Ridotto di 2 per il padding
        console.print(f"[cyan]{separator}[/cyan]\n")
