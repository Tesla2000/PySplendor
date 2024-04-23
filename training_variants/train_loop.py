def train_loop():
    training_buffer = load_train_buffer()
    agents = load_agents()
    scores = deque(maxlen=Config.max_results_held)
    for _ in count() if Config.n_games is None else range(Config.n_games):
        buffer, winners = self_play(agents)
        save_train_buffer(buffer)
        for winner in winners:
            scores.append(agents[-1] is winner)
        if (
            len(scores) < Config.min_games_to_replace_agents
            and sum(scores)
            > Config.minimal_relative_agent_improvement
            * Config.min_games_to_replace_agents
            / len(agents)
        ) or (
            len(scores) > Config.min_games_to_replace_agents
            and sum(scores)
            >= Config.minimal_relative_agent_improvement * len(scores) / len(agents)
        ):
            save_agent(agents[-1])
            agents.append(Agent(Config.n_players))
            agents[-1].load_state_dict(deepcopy(agents[-2].state_dict()))
            agents[-1].training = True
            scores = deque(maxlen=Config.max_results_held)
        elif len(scores) >= Config.min_games_to_replace_agents:
            print(f"{len(scores)} {sum(scores) / len(scores):.2f}")
        else:
            print(f"{len(scores)} {sum(scores)}/{len(scores)}")
        training_buffer += buffer
        train_agent(agents[-1], training_buffer)