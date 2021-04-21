from Monster import Monster
from Player import Player
from flask import Flask, request, render_template
from random import randint

app = Flask(__name__)
player = Player()


@app.route("/")
def index():
    player.skill = getParam("skill")
    return render_template("index.html", message="Hello Flask!")


@app.route("/init")
def initPlayer():
    if getParam("random") == 0:
        player.skill = getParam("skill")
        player.stamina = getParam("stamina")
        player.chance = getParam("chance")
        player.gold = getParam("gold")
        player.provisions = getParam("provisions")
    else:
        player.skill = rollDices(offset=6)
        player.stamina = rollDices(dices=2, offset=12)
        player.chance = rollDices(offset=6)
        player.gold = 1
        player.provisions = 10
    player.maxSkill = player.skill
    player.maxStamina = player.stamina
    player.maxChance = player.chance

    return render_template("init.html", player=player)


@app.route("/play")
def getPlayer():
    return render_template("play.html", player=player)


@app.route("/fight")
def doFight():
    monster = Monster(skill=getParam("skill"), stamina=getParam("stamina"))
    monster_bonus = getParam("monsterBonus")
    player_bonus = getParam("playerBonus")

    rounds = [
        {
            "player_stamina": player.stamina,
            "monster_stamina": monster.stamina,
            "player_score": "-",
            "monster_score": "-",
            "winner": "-",
        }
    ]
    round = 0

    while monster.stamina > 0 and player.stamina > 0:
        round += 1
        monster_attack = rollDices(dices=2, offset=monster.skill)
        player_attack = rollDices(dices=2, offset=player.skill)

        if player_attack > monster_attack:
            monster.updateStamina(monster_bonus - 2)
            winner = "player"
        elif monster_attack > player_attack:
            player.updateStamina(player_bonus - 2)
            winner = "monster"
        else:
            winner = "nobody"

        rounds.append({
            "player_stamina": player.stamina,
            "monster_stamina": monster.stamina,
            "player_score": player_attack,
            "monster_score": monster_attack,
            "winner": winner,
        })

    if player.stamina <= 0:
        end = "Le joueur est mort ..."
    else:
        end = "Le monstre est mort !"

    return render_template("fight.html", rounds=rounds, end=end)


@app.route("/manualFight")
def manualFight():
    monster = Monster(skill=getParam("skill"), stamina=getParam("stamina"))
    monster_bonus = getParam("monsterBonus")
    player_bonus = getParam("playerBonus")
    round = getParam("round")

    monster_attack = rollDices(dices=2, offset=monster.skill)
    player_attack = rollDices(dices=2, offset=player.skill)

    if player_attack > monster_attack:
        monster.updateStamina(monster_bonus - 2)
        winner = "player"
    elif monster_attack > player_attack:
        player.updateStamina(player_bonus - 2)
        winner = "monster"
    else:
        winner = "nobody"

    return render_template(
        "manualFight.html",
        player=player,
        player_bonus=player_bonus,
        monster=monster,
        monster_bonus=monster_bonus,
        round=round,
        winner=winner,
    )


@app.route("/fightChance")
def fightChance():
    monster = Monster(skill=getParam("skill"), stamina=getParam("stamina"))
    monster_bonus = getParam("monsterBonus")
    player_bonus = getParam("playerBonus")
    round = getParam("round")
    winner = getParam("winner")

    chance_result = chance()

    if winner == "player":
        if chance_result:
            monster.updateStamina(-2)
        else:
            monster.updateStamina(1)
    elif winner == "monster":
        if chance_result:
            player.updateStamina(1)
        else:
            monster.updateStamina(-1)

    return render_template(
        "fightChance.html",
        player=player,
        player_bonus=player_bonus,
        monster=monster,
        monster_bonus=monster_bonus,
        round=round,
        winner=winner,
        chance_result=chance_result,
    )


@app.route("/escape")
def escape():
    player.updateStamina(-1)
    return render_template("play.html", player=player)


@app.route("/updateSkill")
def updatePlayerSkill():
    points = getParam("points")
    player.updateSkill(points)
    if points > 0:
        points = f"+{points}"
    return render_template(
        "updateInventory.html",
        key="Habileté",
        value=f"{player.skill} ({points})"
    )


@app.route("/updateMaxSkill")
def updatePlayerMaxSkill():
    points = getParam("points")
    player.setMaxSkill(player.maxSkill + points)
    if points > 0:
        points = f"+{points}"
    return render_template(
        "updateInventory.html",
        key="Habileté maximum",
        value=f"{player.maxSkill} ({points})"
    )


@app.route("/updateStamina")
def updatePlayerStamina():
    points = getParam("points")
    player.updateStamina(points)
    if points > 0:
        points = f"+{points}"
    return render_template(
        "updateInventory.html",
        key="Endurance",
        value=f"{player.stamina} ({points})"
    )


@app.route("/updateMaxStamina")
def updatePlayerMaxStamina():
    points = getParam("points")
    player.setMaxStamina(player.maxStamina + points)
    if points > 0:
        points = f"+{points}"
    return render_template(
        "updateInventory.html",
        key="Endurance maximum",
        value=f"{player.maxStamina} ({points})"
    )


@app.route("/updateChance")
def updatePlayerChance():
    points = getParam("points")
    player.updateChance(points)
    if points > 0:
        points = f"+{points}"
    return render_template(
        "updateInventory.html",
        key="Chance",
        value=f"{player.chance} ({points})"
    )


@app.route("/updateMaxChance")
def updatePlayerMaxChance():
    points = getParam("points")
    player.setMaxChance(player.maxChance + points)
    if points > 0:
        points = f"+{points}"
    return render_template(
        "updateInventory.html",
        key="Chance maximum",
        value=f"{player.maxChance} ({points})"
    )


@app.route("/updateProvisions")
def updateProvisions():
    points = getParam("points")
    if points > 0:
        player.updateProvisions(points)
        return render_template(
            "updateInventory.html",
            key="Provisions",
            value=f"{player.provisions} ({points})"
        )
    else:
        player.updateProvisions(-1)
        player.updateStamina(4)
        return render_template(
            "updateInventory.html",
            key="Endurance et provisions",
            value=f"{player.stamina} (+4) - {player.provisions} (-1)"
        )


@app.route("/drinkSkillPotion")
def drinkSkillPotion():
    player.drinkSkillPotion()
    return render_template(
        "updateInventory.html",
        key="Habileté",
        value=f"{player.skill} (retour au max)"
    )


@app.route("/drinkStaminaPotion")
def drinkStaminaPotion():
    player.drinkStaminaPotion()
    return render_template(
        "updateInventory.html",
        key="Endurance",
        value=f"{player.stamina} (retour au max)"
    )


@app.route("/drinkChancePotion")
def drinkChancePotion():
    player.drinkChancePotion()
    return render_template(
        "updateInventory.html",
        key="Chance",
        value=f"{player.chance} (retour au max)"
    )


@app.route("/updateGold")
def updatePlayerGold():
    po = getParam("po")
    player.updateGold(po)
    if po > 0:
        po = f"+{po}"
    return render_template(
        "updateInventory.html",
        key="Or",
        value=f"{player.gold} ({po})"
    )


def chance():
    success = True
    if rollDices(dices=2) > player.chance:
        success = False
    player.updateChance(-1)
    return success


def rollDices(type=6, dices=1, offset=0, bonus=0):
    rand = 0
    for _ in range(dices):
        rand += randint(1, type)
    return offset + bonus + rand


def getParam(name):
    arg = request.args.get(name)
    if arg is None or arg == "":
        return 0
    try:
        return int(arg)
    except ValueError:
        return arg


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
