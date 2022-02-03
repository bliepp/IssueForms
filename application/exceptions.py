class MissingKey(Exception):
    def __init__(self, cls, *args: object) -> None:
        self.cls = cls
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Subclass \"{self.cls}\" could not be registered without a valid key"



class MissingRequiredArgument(Exception):
    def __init__(self, key: str, *args: object) -> None:
        self.key = key
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Required argument \"{self.key}\" is missing"



class UnknownGithubElementType(Exception):
    def __init__(self, type, *args: object) -> None:
        super().__init__(*args)
        self.type = type

    def __str__(self) -> str:
        return f"{self.type}"
