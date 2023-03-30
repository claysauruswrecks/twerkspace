import asyncio


async def send_command_to_server(command):
    # Create a connection to the server
    reader, writer = await asyncio.open_connection("localhost", 8000)

    # Send the command to the server
    writer.write(command.encode())
    await writer.drain()

    # Wait for the response from the server
    response = await reader.readline()

    # Close the connection
    writer.close()
    await writer.wait_closed()

    return response.decode().strip()


# Start the asyncio event loop
async def main():
    while True:
        # Get input from the user
        command = input("Enter command (or 'quit' to exit): ")

        # Check if the user wants to quit
        if command.lower() == "quit":
            break

        # Send the command to the server
        response = await send_command_to_server(command + "\n")
        print(response)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
