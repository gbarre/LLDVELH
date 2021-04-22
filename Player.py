from werkzeug.exceptions import Forbidden


class Player:
    skill: int = 0
    maxSkill: int = 0
    stamina: int = 0
    maxStamina: int = 0
    chance: int = 0
    maxChance: int = 0
    gold: int = 0
    provisions: int = 0
    skillPotion: int = 0
    staminaPotion: int = 0
    chancePotion: int = 0
    inventory = []

    def __init__(self,
                 skill: int = 0,
                 stamina: int = 0,
                 chance: int = 0,
                 gold: int = 0,
                 provisions: int = 0,
                 potion: str = ""):

        self.skill = skill
        self.setMaxSkill(skill)
        self.stamina = stamina
        self.setMaxStamina(stamina)
        self.chance = chance
        self.setMaxChance(chance)
        self.gold = gold
        self.provisions = provisions
        self.inventory = []

        if potion == "skill":
            self.skillPotion = 2
        if potion == "stamina":
            self.staminaPotion = 2
        if potion == "chance":
            self.chancePotion = 2

    def setMaxSkill(self, max):
        self.maxSkill = max
        if self.skill > max:
            self.skill = max

    def setMaxStamina(self, max):
        self.maxStamina = max
        if self.stamina > max:
            self.stamina = max

    def setMaxChance(self, max):
        self.maxChance = max
        if self.chance > max:
            self.chance = max

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

    def updateChance(self, points: int):
        if self.chance + points > self.maxChance:
            self.chance = self.maxChance
        elif self.chance + points < 0:
            self.chance = 0
        else:
            self.chance += points

    def updateGold(self, po: int):
        if self.gold + po < 0:
            raise Forbidden(description="Vous n'avez pas assez d'or !")
        else:
            self.gold += po

    def updateProvisions(self, points: int):
        if self.provisions + points < 0:
            msg = "Vous n'avez pas assez de provisions !"
            raise Forbidden(description=msg)
        else:
            self.provisions += points

    def updateInventory(self, action, element):
        if action == "add":
            self.inventory.append(element)
        if action == "delete":
            self.inventory.remove(element)

    def drinkSkillPotion(self):
        if self.skillPotion > 0:
            self.skillPotion -= 1
            self.skill = self.maxSkill
        else:
            msg = "Vous n'avez pas de potion d'habileté"
            raise Forbidden(description=msg)

    def drinkStaminaPotion(self):
        if self.stamina > 0:
            self.staminaPotion -= 1
            self.stamina = self.maxStamina
        else:
            msg = "Vous n'avez pas de potion d'endurance"
            raise Forbidden(description=msg)

    def drinkChancePotion(self):
        if self.chancePotion > 0:
            self.chancePotion -= 1
            self.maxChance += 1
            self.chance = self.maxChance
        else:
            msg = "Vous n'avez pas de potion de chance"
            raise Forbidden(description=msg)
