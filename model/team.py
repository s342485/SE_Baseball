from dataclasses import dataclass

@dataclass
class Team:
    id: int
    team_code: str
    name: str


    def __str__(self):
        return (f"squadra {self.team_code} , id: {self.id} , name: {self.name}")

    def __hash__(self):
        return hash(self.team_code)

    def __eq__(self, other):
        return self.team_code == other.team_code