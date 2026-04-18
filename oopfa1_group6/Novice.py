from Character import Character # by importing the class character from the
# different file, the classes in this File can now utilize the usage of 
# the shared file

class Novice(Character):
    def basicAttack(self, character):
        character.reduceHp(self.getDamage())
        print(f"{self.getUsername()} performed Basic Attack! -{self.getDamage()}")


character1 = Novice("Jason")
print(character1.getUsername())
print(character1.getHp())