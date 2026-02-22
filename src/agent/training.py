import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import math
import matplotlib.pyplot as plt

from snake_env import SnakeEnv
from model import DQN # type: ignore

n_observations = 11
n_actions = 4

BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 2500
TAU = 0.005
LR = 3e-4

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env = SnakeEnv()
model = DQN(n_observations, n_actions).to(DEVICE)
target = DQN(n_observations, n_actions).to(DEVICE)
target.load_state_dict(model.state_dict())

optimizer = optim.Adam(model.parameters(), lr=LR, amsgrad=True)
criterion = nn.MSELoss()

memory = deque(maxlen=100000)

steps_done = 0


def select_action(state_tensor: torch.Tensor) -> torch.Tensor:
    global steps_done

    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(
        -1.0 * steps_done / EPS_DECAY
    )
    steps_done += 1

    if sample > eps_threshold:
        with torch.no_grad():
            q = model(state_tensor.unsqueeze(0))
            return q.argmax(dim=1).view(1, 1)
    else:
        return torch.tensor(
            [[random.randrange(n_actions)]], device=DEVICE, dtype=torch.long
        )


episode_durations = []


def plot_durations():
    plt.figure(1)
    plt.clf()

    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    plt.title("Training...")
    plt.xlabel("Episode")
    plt.ylabel("Duration")
    plt.plot(durations_t.numpy())

    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return

    batch = random.sample(memory, BATCH_SIZE)
    states, actions, rewards, next_states, dones = zip(*batch)

    states_t = torch.tensor(states, dtype=torch.float32, device=DEVICE)
    actions_t = torch.tensor(actions, dtype=torch.long, device=DEVICE).unsqueeze(1)
    rewards_t = torch.tensor(rewards, dtype=torch.float32, device=DEVICE).unsqueeze(1)
    next_states_t = torch.tensor(next_states, dtype=torch.float32, device=DEVICE)
    dones_t = torch.tensor(dones, dtype=torch.float32, device=DEVICE).unsqueeze(1)

    q_values = model(states_t).gather(1, actions_t)

    with torch.no_grad():
        next_q = target(next_states_t).max(1)[0].unsqueeze(1)
        target_q = rewards_t + GAMMA * next_q * (1.0 - dones_t)

    loss = criterion(q_values, target_q)

    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 10.0)
    optimizer.step()

    with torch.no_grad():
        for t_param, p_param in zip(target.parameters(), model.parameters()):
            t_param.data.mul_(1.0 - TAU)
            t_param.data.add_(TAU * p_param.data)


EPISODES = 750

for episode in range(EPISODES):
    state = env.reset()
    state_t = torch.tensor(state, dtype=torch.float32, device=DEVICE)

    done = False
    total_reward = 0.0
    t = 0

    while not done:
        action_t = select_action(state_t)
        action = int(action_t.item())

        next_state, reward, done = env.step(action)
        next_state_t = torch.tensor(next_state, dtype=torch.float32, device=DEVICE)

        memory.append((state, action, float(reward), next_state, bool(done)))

        state = next_state
        state_t = next_state_t
        total_reward += float(reward)
        t += 1

        optimize_model()

    episode_durations.append(t)

    if episode % 10 == 0:
        plot_durations()

    print(f"Episode {episode}, steps: {t}, total_reward: {total_reward:.2f}")

torch.save(model.state_dict(), "model/snake_dqn.pt")
print("Model saved to snake_dqn.pt")
