class Monster:
    skill: int = 0
    maxSkill: int = 0
    stamina: int = 0
    maxStamina: int = 0

    def __init__(self, skill: int, stamina: int):

        self.skill = skill
        self.maxSkill = skill
        self.stamina = stamina
        self.maxStamina = stamina

    def updateSkill(self, points: int):
        if self.skill + points > self.maxSkill:
            self.skill = self.maxSkill
        else:
            self.skill += points

    def updateStamina(self, points: int):
        if self.stamina + points > self.maxStamina:
            self.stamina = self.maxStamina
        else:
            self.stamina += points
