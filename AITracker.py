# AI/Fighter Handler
import math, random, pygame

game_state = 'normal'

class Cognitive:
    def __init__(self, con, agi, pwr, stg, itl, ai=None):
        # Constitution, Agility, Power, Strength, Intelligence
        self.hp = con * 10.0
        self.con = con
        self.agi = agi
        self.pwr = pwr
        self.stg = stg
        self.itl = itl
        self.ai = ai
        self.status = 'alive'
        if self.ai:
            self.ai.owner = self

    def mel_attack(self, target):
        damage = ((self.pwr * 2) + (round(.5 * self.stg)))

        dice = random.randint(0, 100)
        if dice == 100:
            print ('The ' + self.owner.name.capitalize() + ' misses ' + target.name + '.')
        elif dice <= target.cognitive.agi:
            print ('The ' + target.name.capitalize() + ' dodges the ' + self.owner.name.capitalize() + '\'s attack!')
        
        else:
            print ('The ' + self.owner.name.capitalize() + ' hits the ' + target.name + ' for ' + str(damage) + ' damage.')
            target.cognitive.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.die()

    def die(self):
        global game_state
        self.owner.send_to_back()
        self.owner.char = '%'
        self.owner.color = pygame.Color(100,0,0)
        self.owner.blocks = False
        if self.owner.name == 'player':
            game_state = 'dead'
            print 'You have died.'


class Enemy:
    def take_turn(self):
        enemy = self.owner.owner
        if fov_mp[enemy.x][enemy.y] == 1:
            if enemy.distance_to(player) >= 2:
                enemy.move_towards(player.x, player.y)
            else:
                self.owner.mel_attack(player)




