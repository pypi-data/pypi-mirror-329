from gooder_ai.config.types import Score


def get_dependent_variable(config: dict) -> str | None:
    return config.get("dependentVariable", None)


def set_dependent_variable(config: dict, value: str):
    config["dependentVariable"] = value


def get_models(config: dict) -> list[Score]:
    return config.get("scores", [])


def set_models(config: dict, value: Score):
    models: list[Score] = config.get("scores", [])
    models.append(value)
    config["scores"] = models
