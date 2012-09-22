# AI/Fighter Handler
import math, random, pygame
import GuiHandler as gui

game_state = ''

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
            gui.message('The ' + self.owner.name.capitalize() + ' misses ' + target.name + '.', pygame.Color(255,255,0))
        elif dice <= target.cognitive.agi:
            gui.message('The ' + target.name.capitalize() + ' dodges the ' + self.owner.name.capitalize() + '\'s attack!', pygame.Color(0,0,255))
        
        else:
            gui.message('The ' + self.owner.name.capitalize() + ' hits the ' + target.name + ' for ' + str(damage) + ' damage.', pygame.Color(255,0,0))
            target.cognitive.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.die()

    def die(self):
        global game_state
        if self.status == 'alive':
            self.owner.send_to_back()
            self.owner.char = '%'
            self.owner.color = pygame.Color(100,0,0)
            print self.owner.name
            print 'blocks before?' + str(self.owner.blocks)
            self.owner.blocks = False
            print 'blocks?' +  str(self.owner.blocks)
            self.status = 'dead'
            if self.owner.name == 'player':
                game_state = 'dead'
                gui.message('You have died.', pygame.Color(150,0,0))
            else:
                self.ai = None


class Enemy:
    def take_turn(self):
        enemy = self.owner.owner
        if fov_mp[enemy.x][enemy.y] == 1:
            if enemy.distance_to(player) >= 2:
                enemy.move_towards(player.x, player.y)
            else:
                self.owner.mel_attack(player)




