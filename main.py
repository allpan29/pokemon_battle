import os
import time
import random
from pokedex import POKEMON_DB, SPRITES

PIKACHU_BACK = r""" [피카츄 뒷모습] """

TYPE_CHART = {
    "노말": {"바위": 0.5, "고스트": 0.0, "강철": 0.5},
    "불꽃": {"불꽃": 0.5, "물": 0.5, "풀": 2.0, "얼음": 2.0, "벌레": 2.0, "바위": 0.5, "드래곤": 0.5, "강철": 2.0},
    "물": {"불꽃": 2.0, "물": 0.5, "풀": 0.5, "땅": 2.0, "바위": 2.0, "드래곤": 0.5},
    "풀": {"불꽃": 0.5, "물": 2.0, "풀": 0.5, "독": 0.5, "땅": 2.0, "비행": 0.5, "벌레": 0.5, "바위": 2.0, "드래곤": 0.5, "강철": 0.5},
    "전기": {"물": 2.0, "풀": 0.5, "전기": 0.5, "땅": 0.0, "비행": 2.0, "드래곤": 0.5},
    "얼음": {"불꽃": 0.5, "물": 0.5, "풀": 2.0, "얼음": 0.5, "땅": 2.0, "비행": 2.0, "드래곤": 2.0, "강철": 0.5},
    "격투": {"노말": 2.0, "얼음": 2.0, "독": 0.5, "비행": 0.5, "에스퍼": 0.5, "벌레": 0.5, "바위": 2.0, "고스트": 0.0, "악": 2.0, "강철": 2.0, "페어리": 0.5},
    "독": {"풀": 2.0, "독": 0.5, "땅": 0.5, "바위": 0.5, "고스트": 0.5, "강철": 0.0, "페어리": 2.0},
    "땅": {"불꽃": 2.0, "풀": 0.5, "전기": 2.0, "독": 2.0, "비행": 0.0, "벌레": 0.5, "바위": 2.0, "강철": 2.0},
    "비행": {"풀": 2.0, "전기": 0.5, "격투": 2.0, "벌레": 2.0, "바위": 0.5, "강철": 0.5},
    "에스퍼": {"격투": 2.0, "독": 2.0, "에스퍼": 0.5, "악": 0.0, "강철": 0.5},
    "벌레": {"불꽃": 0.5, "풀": 2.0, "격투": 0.5, "독": 0.5, "비행": 0.5, "에스퍼": 2.0, "고스트": 0.5, "악": 2.0, "강철": 0.5, "페어리": 0.5},
    "바위": {"불꽃": 2.0, "얼음": 2.0, "격투": 0.5, "땅": 0.5, "비행": 2.0, "벌레": 2.0, "강철": 0.5},
    "고스트": {"노말": 0.0, "에스퍼": 2.0, "고스트": 2.0, "악": 0.5},
    "드래곤": {"드래곤": 2.0, "강철": 0.5, "페어리": 0.0},
    "악": {"격투": 0.5, "에스퍼": 2.0, "고스트": 2.0, "악": 0.5, "페어리": 0.5},
    "강철": {"불꽃": 0.5, "물": 0.5, "전기": 0.5, "얼음": 2.0, "바위": 2.0, "강철": 0.5, "페어리": 2.0},
    "페어리": {"불꽃": 0.5, "격투": 2.0, "독": 0.5, "드래곤": 2.0, "악": 2.0, "강철": 0.5}
}

class Pokemon:
    def __init__(self, name, level, hp, atk, def_stat, speed, p_type, sprite, moves):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.def_stat = def_stat
        self.speed = speed
        self.p_type = p_type
        self.sprite = sprite
        self.moves = moves

    def heal(self):
        self.hp = self.max_hp

    def draw_hp_bar(self):
        bar_length = 20
        ratio = max(0, self.hp / self.max_hp)
        filled = int(bar_length * ratio)
        bar = "█" * filled + "-" * (bar_length - filled)
        return f"[{bar}] {int(self.hp)}/{self.max_hp}"

def calculate_damage(attacker, defender, move_power, move_type):
    # 상성 계산
    effectiveness = TYPE_CHART.get(move_type, {}).get(defender.p_type, 1.0)
    # 자속 보정 (STAB)
    stab = 1.5 if move_type == attacker.p_type else 1.0
    
    # 데미지 계산 공식 적용
    level_factor = (attacker.level * 2) / 5 + 2
    random_factor = random.uniform(0.85, 1.0)
    
    base_damage = (level_factor * move_power * attacker.atk) / (defender.def_stat * 50 + 2)
    final_damage = base_damage * effectiveness * stab * random_factor
    
    return int(final_damage), effectiveness

def render(player, enemy, message=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{' ' * 35}상대: Lv.{enemy.level} {enemy.name}")
    print(f"{' ' * 35}{enemy.draw_hp_bar()}")
    for line in enemy.sprite.strip().split('\n'):
        print(f"{' ' * 35}{line}")
    print("\n")
    for line in player.sprite.strip().split('\n'):
        print(f"  {line}")
    print(f"나: Lv.{player.level} {player.name}")
    print(f"{player.draw_hp_bar()}")
    print("-" * 70)
    print(f" {message}")
    print("-" * 70)

def battle(player_poka):
    wild_id = random.choice(list(POKEMON_DB.keys()))
    wild_info = POKEMON_DB[wild_id]
    
    # Pokemon 객체 생성 (도감 데이터를 클래스 인자에 맞게 매핑)
    wild_poka = Pokemon(
        name=wild_info["name"],
        level=random.randint(18, 25), # 야생 레벨 범위
        p_type=wild_info["type"],
        hp=wild_info["hp"],
        atk=wild_info["atk"],
        def_stat=wild_info["def"],
        speed=wild_info["spd"],
        sprite=SPRITES.get(wild_info["name"], f"[{wild_info['name']} 아트 준비 중]"),
        moves=wild_info["moves"]
    )
    
    msg = f"앗! 야생의 {wild_poka.name}(이)가 나타났다!"
    
    while player_poka.hp > 0 and wild_poka.hp > 0:
        render(player_poka, wild_poka, msg)
        print(f" 무엇을 할까?")
        for i, m in enumerate(player_poka.moves):
            print(f" {i+1}.{m[0]} ", end="")
        print("\n")
        
        try:
            choice = int(input(" >> ")) - 1
            p_move = player_poka.moves[choice]
        except: continue

        e_move = random.choice(wild_poka.moves)

        # 스피드 비교 후 턴 진행
        if player_poka.speed >= wild_poka.speed:
            order = [(player_poka, wild_poka, p_move), (wild_poka, player_poka, e_move)]
        else:
            order = [(wild_poka, player_poka, e_move), (player_poka, wild_poka, p_move)]

        for atk, dfd, move in order:
            if atk.hp <= 0: continue
            dmg, eff = calculate_damage(atk, dfd, move[1], move[2])
            dfd.hp -= dmg
            msg = f"{atk.name}의 {move[0]}!"
            if eff > 1.0: 
                msg += " 효과가 굉장했다!"
            elif eff < 1.0 and eff > 0: 
                msg += " 효과가 별로인 듯하다..."
            elif eff == 0: 
                msg += " 효과가 없는 듯하다..."
            
            render(player_poka, wild_poka, msg)
            time.sleep(1.2)
            if dfd.hp <= 0: break

    if player_poka.hp <= 0:
        render(player_poka, wild_poka, f"{player_poka.name}(은)는 쓰러졌다...")
        return False
    else:
        render(player_poka, wild_poka, f"야생의 {wild_poka.name}(을)를 쓰러트렸다!")
        time.sleep(1.5)
        player_poka.heal()
        return True

def main():
    pika_moves = [("10만볼트", 90, "전기"), ("전광석화", 40, "노말"), ("파도타기", 90, "물"), ("깨트리기", 75, "격투")]
    pika = Pokemon("피카츄", 25, 60, 55, 40, 60, "전기", PIKACHU_BACK, pika_moves)
    
    try:
        while True:
            if not battle(pika):
                if input("다시 도전? (y/n): ").lower() == 'y':
                    pika.heal()
                    continue
                else: break
    except KeyboardInterrupt:
        print("\n모험을 종료합니다!")

if __name__ == "__main__":
    main()