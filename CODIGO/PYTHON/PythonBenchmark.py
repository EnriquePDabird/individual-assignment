import subprocess
import time
import psutil
import os

# Asegúrate de tener instalado psutil: pip install psutil

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
    
    try:
        exec_time = float(stdout.strip())  # si matrix.py imprime tiempo numérico
    except ValueError:
        exec_time = end_wall - start_wall  # fallback si no devuelve un número
    
    return exec_time, end_wall - start_wall


def get_usage():
    """Obtiene CPU total y memoria usada en MB."""
    process = psutil.Process(os.getpid())
    cpu_total = process.cpu_times().user + process.cpu_times().system
    mem_bytes = process.memory_info().rss
    return cpu_total, mem_bytes / (1024 * 1024)


def main():
    sizes = [128, 256, 512, 768, 1024]
    repetitions = 5

    output_path = r"C:\Users\USUARIO\Desktop\COLEGIO\Curso 3\Primer Semestre\Big Data\individual-assignment\RESULTADOS\PythonResultados.txt"

    print("Benchmarking Python matrix multiplication program:")
    print("--------------------------------------------------------------------------------")
    print(f"{'Size':<8} {'Run':<8} {'Time(s)':<12} {'CPU_total(s)':<15} {'Memory(MB)':<12}")
    print("--------------------------------------------------------------------------------")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Benchmarking Python matrix multiplication program:\n")
        f.write("--------------------------------------------------------------------------------\n")
        f.write(f"{'Size':<8} {'Run':<8} {'Time(s)':<12} {'CPU_total(s)':<15} {'Memory(MB)':<12}\n")
        f.write("--------------------------------------------------------------------------------\n")

        for n in sizes:
            for run in range(1, repetitions + 1):
                try:
                    before_cpu, before_mem = get_usage()
                    exec_time, wall_time = run_matrix_program(n)
                    after_cpu, after_mem = get_usage()

                    cpu_used = after_cpu - before_cpu
                    mem_used = after_mem - before_mem

                    line = f"{n:<8} {run:<8} {exec_time:<12.6f} {cpu_used:<15.6f} {mem_used:<12.2f}"
                    print(line)
                    f.write(line + "\n")

                except Exception as e:
                    error_msg = f"Error corriendo matrix para tamaño {n}: {e}"
                    print(error_msg)
                    f.write(error_msg + "\n")

        f.write(f"\nResultados guardados en: {output_path}\n")

    print(f"\nResultados guardados en: {output_path}")


if __name__ == "__main__":
    main()
