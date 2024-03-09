from Config import Config


def save_temp_buffer(buffer, train: bool):
    path = Config.training_data_path if train else Config.evaluation_data_path
    index = max((*tuple(int(path.name) for path in path.iterdir()), -1)) + 1
    path.joinpath(str(index)).write_text(
        str(list((list(sample[0]), list(sample[1]), sample[2]) for sample in buffer))
    )
