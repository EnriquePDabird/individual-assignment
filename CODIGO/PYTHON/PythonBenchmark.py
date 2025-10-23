import subprocess
import time
import psutil
import os

# Asegúrate de instalar psutil: pip install psutil

def run_matrix_program(n):
    """Ejecuta matrix.py con tamaño n y devuelve tiempo de ejecución (s)."""
    start_wall = time.time()
    
    process = subprocess.Popen(
        ["python", "matrix.py", str(n)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate()
    end_wall = time.time()
    
    if process.returncode != 0:
        raise RuntimeError(f"Error ejecutando matrix.py: {stderr.strip()}")
    
    exec_time = float(stdout.strip())  # tiempo que imprime matrix.py
    return exec_time, end_wall - start_wall

def get_usage():
    """Obtiene CPU total y memoria usada en MB."""
    process = psutil.Process(os.getpid())
    cpu_total = process.cpu_times().user + process.cpu_times().system
    mem_bytes = process.memory_info().rss
    return cpu_total, mem_bytes / (1024*1024)

def main():
    sizes = [128, 256, 512, 768, 1024]

    print("Benchmarking Python matrix multiplication program:")
    print("--------------------------------------------------------------------------")
    print(f"{'Size':<8} {'Time(s)':<12} {'CPU_total(s)':<15} {'Memory(MB)':<12}")
    print("--------------------------------------------------------------------------")

    for n in sizes:
        try:
            # Pasar el tamaño al script matrix.py modificando sys.argv dentro de matrix.py
            # O podemos modificar matrix.py para que use sys.argv[1] si está presente
            before_cpu, before_mem = get_usage()
            exec_time, wall_time = run_matrix_program(n)
            after_cpu, after_mem = get_usage()

            cpu_used = after_cpu - before_cpu
            mem_used = after_mem - before_mem

            print(f"{n:<8} {exec_time:<12.6f} {cpu_used:<15.6f} {mem_used:<12.2f}")
        except Exception as e:
            print(f"Error corriendo matrix para tamaño {n}: {e}")

if __name__ == "__main__":
    main()
