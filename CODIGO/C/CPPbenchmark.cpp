#include <iostream>
#include <iomanip>
#include <chrono>
#include <vector>
#include <string>
#include <cstdlib>
#include <windows.h>
#include <psapi.h>

// Ejecuta el programa matrix.exe con el tamaño especificado
double run_matrix_program(int n) {
    std::string cmd = "matrix.exe " + std::to_string(n);
    auto start = std::chrono::high_resolution_clock::now();
    int ret = std::system(cmd.c_str());
    auto stop = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> diff = stop - start;
    return diff.count(); // segundos
}

// Estructura para almacenar las métricas
struct ResourceUsage {
    double user_cpu_sec;
    double sys_cpu_sec;
    SIZE_T memory_bytes;
};

// Obtiene el uso de CPU y memoria del proceso actual
ResourceUsage get_usage() {
    PROCESS_MEMORY_COUNTERS_EX pmc;
    GetProcessMemoryInfo(GetCurrentProcess(), (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc));

    FILETIME createTime, exitTime, kernelTime, userTime;
    GetProcessTimes(GetCurrentProcess(), &createTime, &exitTime, &kernelTime, &userTime);

    ULARGE_INTEGER u, k;
    u.LowPart = userTime.dwLowDateTime;
    u.HighPart = userTime.dwHighDateTime;
    k.LowPart = kernelTime.dwLowDateTime;
    k.HighPart = kernelTime.dwHighDateTime;

    ResourceUsage r{};
    r.user_cpu_sec = u.QuadPart * 1e-7; // 100-ns units → seconds
    r.sys_cpu_sec = k.QuadPart * 1e-7;
    r.memory_bytes = pmc.PrivateUsage;
    return r;
}

int main() {
    std::vector<int> sizes = {128, 256, 512, 768, 1024};

    std::cout << "Benchmarking C matrix multiplication program (Windows):\n";
    std::cout << "---------------------------------------------------------------------\n";
    std::cout << std::left
              << std::setw(8)  << "Size"
              << std::setw(12) << "Time(s)"
              << std::setw(15) << "CPU_user(s)"
              << std::setw(15) << "CPU_sys(s)"
              << std::setw(12) << "Memory(MB)"
              << "\n";
    std::cout << "---------------------------------------------------------------------\n";

    for (int n : sizes) {
        double exec_time = run_matrix_program(n);
        auto usage = get_usage();
        double mem_mb = usage.memory_bytes / (1024.0 * 1024.0);

        std::cout << std::left << std::fixed << std::setprecision(6)
                  << std::setw(8)  << n
                  << std::setw(12) << exec_time
                  << std::setw(15) << usage.user_cpu_sec
                  << std::setw(15) << usage.sys_cpu_sec
                  << std::setw(12) << mem_mb
                  << "\n";
    }

    return 0;
}
