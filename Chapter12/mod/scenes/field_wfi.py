def eat_food(food, pl_life, pl_lifemax):
    # pl_life -= 100
    if food > 0:
        food -= 1
        pl_life = pl_life+1 if pl_life<pl_lifemax else pl_lifemax
    else:
        pl_life = pl_life-5 if pl_life>5 else 0
    return food, pl_life
