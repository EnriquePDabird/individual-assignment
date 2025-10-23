import java.io.*;
import java.lang.management.*;
import java.util.*;
import com.sun.management.OperatingSystemMXBean;

public class JavaBenchmark {

    private static double runMatrixProgram(int n) throws IOException, InterruptedException {
        // Compilar Matrix.java (solo la primera vez)
        ProcessBuilder compile = new ProcessBuilder("javac", "Matrix.java");
        compile.redirectErrorStream(true);
        compile.start().waitFor();

        // Ejecutar el programa con tamaño n
        ProcessBuilder run = new ProcessBuilder("java", "Matrix", String.valueOf(n));
        run.redirectErrorStream(true);

        long startWall = System.nanoTime();

        Process process = run.start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            while (reader.readLine() != null) {
                // descartar salida del programa
            }
        }

        process.waitFor();
        long endWall = System.nanoTime();

        return (endWall - startWall) / 1e9; // segundos
    }

    private static ResourceUsage getUsage() {
        ResourceUsage r = new ResourceUsage();
        OperatingSystemMXBean osBean =
            (OperatingSystemMXBean) ManagementFactory.getOperatingSystemMXBean();

        Runtime runtime = Runtime.getRuntime();

        r.cpuTotalSec = osBean.getProcessCpuTime() / 1e9; // nanosegundos → segundos
        r.memoryBytes = runtime.totalMemory() - runtime.freeMemory();
        return r;
    }

    static class ResourceUsage {
        double cpuTotalSec;
        long memoryBytes;
    }

    public static void main(String[] args) {
        int[] sizes = {128, 256, 512, 768, 1024};
        final int repetitions = 5;

        String outputPath = "C:\\Users\\USUARIO\\Desktop\\COLEGIO\\Curso 3\\Primer Semestre\\Big Data\\individual-assignment\\RESULTADOS\\JavaResultados.txt";

        try (PrintWriter writer = new PrintWriter(new FileWriter(outputPath))) {

            System.out.println("Benchmarking Java matrix multiplication program:");
            System.out.println("--------------------------------------------------------------------------------");
            System.out.printf("%-8s %-8s %-12s %-15s %-12s%n",
                    "Size", "Run", "Time(s)", "CPU_total(s)", "Memory(MB)");
            System.out.println("--------------------------------------------------------------------------------");

            writer.println("Benchmarking Java matrix multiplication program:");
            writer.println("--------------------------------------------------------------------------------");
            writer.printf("%-8s %-8s %-12s %-15s %-12s%n",
                    "Size", "Run", "Time(s)", "CPU_total(s)", "Memory(MB)");
            writer.println("--------------------------------------------------------------------------------");

            for (int n : sizes) {
                for (int run = 1; run <= repetitions; run++) {
                    try {
                        ResourceUsage before = getUsage();
                        double execTime = runMatrixProgram(n);
                        ResourceUsage after = getUsage();

                        double cpuUsed = after.cpuTotalSec - before.cpuTotalSec;
                        double memMB = after.memoryBytes / (1024.0 * 1024.0);

                        System.out.printf("%-8d %-8d %-12.6f %-15.6f %-12.2f%n",
                                n, run, execTime, cpuUsed, memMB);

                        writer.printf("%-8d %-8d %-12.6f %-15.6f %-12.2f%n",
                                n, run, execTime, cpuUsed, memMB);

                    } catch (IOException | InterruptedException e) {
                        System.err.println("Error running matrix for size " + n + ": " + e.getMessage());
                        writer.println("Error running matrix for size " + n + ": " + e.getMessage());
                    }
                }
            }

            System.out.println("\nResultados guardados en: " + outputPath);
            writer.println("\nResultados guardados en: " + outputPath);

        } catch (IOException e) {
            System.err.println("No se pudo escribir el archivo de resultados: " + e.getMessage());
        }
    }
}
