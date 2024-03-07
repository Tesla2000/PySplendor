from collections import deque

from Config import Config
from agent.Agent import Agent
from agent.self_play import self_play
from agent.train_agent import train_agent


def main():
    training_buffer = deque(maxlen=Config.training_buffer_len)
    agent = Agent(Config.n_players)
    for i in range(Config.n_games):
        training_buffer += self_play(agent)
        train_agent(agent, training_buffer)


if __name__ == "__main__":
    main()
