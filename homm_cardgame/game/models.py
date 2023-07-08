from django.db import models

# from trait_functions import attacked, longspear
# Trait functions
longspear = ['Pikeman']
healer = ['Monk']

class Player(models.Model):
    name = models.CharField(max_length=50, default='Player')
    games_won = models.IntegerField()
    gold = models.IntegerField()
    health = models.IntegerField()
    human = models.BooleanField()
    attack = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}, {self.health}, {self.gold}'


class Faction(models.Model):

    name = models.CharField(default='Neutral')

    def _str_(self):
        return f'{self.name}'


class Card(models.Model):
    name = models.CharField(max_length=30)
    health = models.IntegerField()
    health_base = models.IntegerField(default=0)
    attack = models.IntegerField()
    cost = models.IntegerField()
    ranged = models.BooleanField()
    flying = models.BooleanField()
    attacked_this_turn = models.BooleanField(default=False)
    image = models.CharField(max_length=100, default=f'images/placeholder.webp',null=True)
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}, health: {self.health}, attack: {self.attack}, cost: {self.cost}'
    
    def fight_range(self, other):
        other.health = other.health - self.attack
        other.save()
        self.save()

    def fight_melee(self, other):
        if other.name in longspear:
            other.attacked(self)
        other.health -= self.attack
        self.health -= other.attack
        if isinstance(other, models.Model):
            other.save()
        if isinstance(self, models.Model):
            self.save()

    def attacked(self, other):
        other.health -= 1
        other.save()
        if other.health <= 0:
            other.attack = 0
            other = None

    def endofturn(self, board):
        # human_player = Player.objects.get(human=True)
        # opponent_player = Player.objects.get(human=False)
        if self.name in healer:
            for k,v in board.items():
                for i in range(len(v)):
                    if v[i] != None and v[i].health < v[i].health_base:
                        v[i].health += 1
                    # if board == player_board:
                    #     human_player.health += 1
                    # else:
                    #     opponent_player.health += 1

        
        





# Create your models here.
