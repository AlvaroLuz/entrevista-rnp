import os
import logging
import time
import requests

# --- Configuração do Agent ---
TARGETS = os.getenv("AGENT_TARGETS", "google.com").split(",")
INTERVAL_SECONDS = int(os.getenv("AGENT_INTERVAL_SECONDS", "60"))
DEBUG = bool(os.getenv("AGENT_DEBUG"))

# --- Configuração do logger ---
def setup_logger():
    level = "DEBUG" if DEBUG else "INFO"
    log_level = os.getenv("LOG_LEVEL", level).upper()
    logger = logging.getLogger("net-agent")
    logger.setLevel(log_level)

    # Evita adicionar múltiplos handlers se o logger já existir
    if not logger.handlers:
        # Handler padrão: console (stdout)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()



def ping_host(host: str) -> float:
    """Executa um ping simples e retorna latência média."""

    try:
        response = os.popen(f"ping -c 1 -W 2 {host}").read()
        if "time=" in response:
            latency = float(response.split("time=")[1].split(" ")[0])
        else:
            return None
    except Exception as e:
        logger.error(f"Erro ao pingar {host}: {e}")
        return None
    
    return latency

def check_http(url: str) -> tuple:
    """Verifica tempo de resposta e status HTTP."""
    start = time.time()
    
    try:
        r = requests.get(f"http://{url}", timeout=5)
        duration = round((time.time() - start) * 1000, 2)
    except Exception as e:
        logger.warning(f"Falha ao acessar {url}: {e}")
        return None, None
    
    return duration, r.status_code
    
def main():
    while True:
        for host in TARGETS:
            latency = ping_host(host)
            http_time, http_code = check_http(host)
            logger.info(f"{host} - Ping: {latency} ms, HTTP: {http_time} ms, Status: {http_code}")

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Encerrando agent...")
    except Exception as e:
        logger.exception("Erro fatal no agent: %s", e)