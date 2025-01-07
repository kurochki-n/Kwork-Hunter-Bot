import subprocess
import logging
import os
import re
import time
import signal
import platform
import psutil
from typing import Tuple


def start_tuna(port: int, subdomain: str, timeout: int = 60) -> Tuple[str | None, int | None]:
    """
    Starts tuna and returns the URL and PID.
    
    Args:
        port: Port to proxy.
        timeout: URL wait timeout in seconds.
        
    Returns:
        str: URL or None if not found.
        int: PID of the process or None if not found.
    """
    output_file = os.path.join('logs', 'tuna_output.log')
    
    try:
        with open(output_file, 'w') as f:
            process = subprocess.Popen(
                ['tuna', 'http', f'http://localhost:{port}/', f'--subdomain={subdomain}'],
                stdout=f,
                stderr=f,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == 'Windows' else 0
            )
            
            pid = process.pid
            logging.info(f"Tuna started on port {port} with PID {pid}")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    with open(output_file, 'r') as f:
                        content = f.read()
                        match = re.search(r'Forwarding (https://[^\s]+).*->', content)
                        if match:
                            url = match.group(1)
                            logging.info(f"URL found: {url}")
                            return url, pid
                except Exception as e:
                    logging.error(f"Error reading log file: {str(e)}")
                
                time.sleep(0.5)
            
            logging.error("URL not found in logs")
            stop_tuna(pid)
            return None, None
            
    except Exception as e:
        logging.error(f"Error starting tuna: {str(e)}")
        return None, None
    
    
def stop_tuna(pid: int) -> None:
    """
    Terminates a process by its PID.
    
    Args:
        pid: Process identifier to terminate.
        
    Returns:
        None
    """
    try:
        if platform.system() == 'Windows':
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
        else:
            os.kill(pid, signal.SIGTERM)
            
        if psutil.pid_exists(pid):
            logging.warning(f"Process {pid} still exists after termination attempt")
        else:
            logging.info(f"Tuna process with PID {pid} terminated")
            
    except subprocess.CalledProcessError as e:
        logging.error(f"Error terminating process: {e}")
    except ProcessLookupError:
        logging.error(f"Tuna process with PID {pid} not found")
    except Exception as e:
        logging.error(f"Error killing Tuna process: {str(e)}")
    
    
