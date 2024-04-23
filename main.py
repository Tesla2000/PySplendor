from collections import deque
from copy import deepcopy
from itertools import count

from Config import Config
from agent.Agent import Agent
from agent.load_agents import load_agents
from agent.save_agent import save_agent
from agent.self_play import self_play
from agent.train_agent import train_agent
from db.load_train_buffer import load_train_buffer
from db.save_train_buffer import save_train_buffer
from training_variants.train_to_go_fast import train_to_go_fast


def main():
    # train_loop()
    train_to_go_fast()


if __name__ == "__main__":
    main()
