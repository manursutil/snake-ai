import torch
from snake_env import SnakeEnv
from model import DQN # type: ignore


device = torch.device("cpu")

env = SnakeEnv()
env.lib.engine_render_init()

model = DQN(11, 4)
model.load_state_dict(torch.load("model/snake_dqn.pt", map_location=device))
model.eval()

state = env.reset()

while not env.lib.WindowShouldClose():
    with torch.no_grad():
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        action = model(state_tensor).argmax().item()

    state, reward, done = env.step(action)

    env.lib.engine_render()

    # time.sleep(0.05)

    if done:
        state = env.reset()
