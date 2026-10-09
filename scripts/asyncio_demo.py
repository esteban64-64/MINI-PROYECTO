"""
Demostración de AsyncIO para el curso de Ingeniería de Sistemas de IA.

Este script muestra cómo usar async/await para ejecutar tareas
concurrentemente, lo cual es fundamental para aplicaciones que
consumen servicios externos como APIs de LLM.
"""
import asyncio


async def task1():
    """Simula una operación I/O que tarda 2 segundos."""
    print("🔵 Tarea 1 iniciada")
    await asyncio.sleep(2)
    print("🟢 Tarea 1 completada")


async def task2():
    """Simula una operación I/O que tarda 1 segundo."""
    print("🟡 Tarea 2 iniciada")
    await asyncio.sleep(1)
    print("🟢 Tarea 2 completada")


async def task3():
    """Simula una operación I/O que tarda 1.5 segundos."""
    print("🟣 Tarea 3 iniciada")
    await asyncio.sleep(1.5)
    print("🟢 Tarea 3 completada")


async def main():
    """
    Ejecuta múltiples tareas concurrentemente usando asyncio.gather.

    Sin async/await, estas tareas se ejecutarían secuencialmente:
    2s + 1s + 1.5s = 4.5 segundos

    Con async/await, se ejecutan en paralelo:
    max(2s, 1s, 1.5s) = 2 segundos
    """
    print("⏱️  Ejecutando tareas concurrentemente...\n")

    start_time = asyncio.get_event_loop().time()

    await asyncio.gather(
        task1(),
        task2(),
        task3()
    )

    end_time = asyncio.get_event_loop().time()
    elapsed = end_time - start_time

    print(f"\n✅ Todas las tareas completadas en {elapsed:.2f} segundos")
    print(f"📊 Tiempo secuencial estimado: 4.5 segundos")
    print(f"🚀 Ahorro de tiempo: {4.5 - elapsed:.2f} segundos")


if __name__ == "__main__":
    asyncio.run(main())
