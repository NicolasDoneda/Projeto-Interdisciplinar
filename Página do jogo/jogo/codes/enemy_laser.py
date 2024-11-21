from laser import Laser

class EnemyLaser(Laser):
    def __init__(self, pos, speed):
        super().__init__(pos, speed, 600)
        self.image.fill("red")  # Lasers inimigos em vermelho