from dataclasses import dataclass

@dataclass
class Design:

    title: str

    description: str

    category: str

    fabric: str

    colors: list

    image: str = ""