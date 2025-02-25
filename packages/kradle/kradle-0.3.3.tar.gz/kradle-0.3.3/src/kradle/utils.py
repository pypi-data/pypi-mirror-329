import threading

def setup_server(instance, port: int, host: str = 'localhost') -> None:
    """Set up and start the server."""
    if not instance._is_port_available(port):
        instance._logger.log_error(f"Port {port} is not available")
        raise ValueError(f"Port {port} is not available")
    
    instance._setup_signal_handlers()
    instance._server_thread = threading.Thread(target=instance._run_server, daemon=True)
    instance._server_thread.start()
    
    if not instance._server_ready.wait(timeout=5.0):
        instance._logger.log_error("Server failed to start within timeout")
        raise RuntimeError("Server failed to start within timeout")
