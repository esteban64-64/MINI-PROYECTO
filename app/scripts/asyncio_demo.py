import asyncio

async def task1():
    print("Tarea 1 iniciada")
    await asyncio.sleep(2)
    print("Tarea 1 completada")

async def task2():
    print("Tarea 2 iniciada")
    await asyncio.sleep(1)
    print("Tarea 2 completada")

async def main():
    print("Ejecutando tareas concurrentemente...")
    await asyncio.gather(task1(), task2())
    print("Todas las tareas completadas")

if __name__ == "__main__":
    asyncio.run(main())