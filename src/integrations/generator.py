from src.inferencing.generator import Generator
from dotenv import load_dotenv
from asyncio import create_task, gather, run, Task

_ = load_dotenv()

messages: list[list[dict[str, str]]] = [
    [{"role": "user", "content": "Hello, how are you?"}],
    [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}],
    [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}],
    [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}],
    [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}],
    [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}],
    [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm doing well, thank you!"}, {"role": "user", "content": "Hello, how are you?"}],
]

async def main():
    generator = Generator(model="gpt-4.1-nano")
    tasks: list[Task[dict[str, str]]] = []
    for message in messages[:1]:
        tasks.append(create_task(generator.generate(message)))
    responses = await gather(*tasks)
    for i, response in enumerate(responses):
        print(f"Response {i}: {await generator.get_validated_content(response)}")
    
if __name__ == "__main__":
    run(main())
