import random
from Character import Character
from Novice import Novice
from Swordsman import Swordsman
from Archer import Archer
from Magician import Magician
from Boss import Boss


# ──────────────────────────────────────────────
#  Helper utilities
# ──────────────────────────────────────────────

def divider(char="─", width=50):
    print(char * width)

def header(title):
    divider("═")
    print(f"  {title}")
    divider("═")

def pause():
    input("\n  [Press Enter to continue...]\n")


# ──────────────────────────────────────────────
#  Character factory
# ──────────────────────────────────────────────

ROLE_MAP = {
    "1": ("Novice",    Novice),
    "2": ("Swordsman", Swordsman),
    "3": ("Archer",    Archer),
    "4": ("Magician",  Magician),
}

def pick_role(player_label, allow_novice=True):
    """Prompt a player to choose a role. Returns an instantiated character."""
    print(f"\n  {player_label} — Choose your role:")
    options = list(ROLE_MAP.items())
    if not allow_novice:
        options = [(k, v) for k, v in options if v[0] != "Novice"]
    for key, (name, _) in options:
        print(f"    [{key}] {name}")
    valid = {k for k, _ in options}
    while True:
        choice = input("  Your choice: ").strip()
        if choice in valid:
            name, cls = ROLE_MAP[choice]
            username = input(f"  Enter username for {player_label}: ").strip() or player_label
            return cls(username)
        print("  ✗ Invalid choice. Try again.")

def get_attacks(character):
    """Return list of (label, callable) attack tuples available to character."""
    attacks = [("Basic Attack", lambda c: character.basicAttack(c))]
    if isinstance(character, Swordsman):
        attacks.append(("Slash Attack", lambda c: character.slashAttack(c)))
    if isinstance(character, Archer):
        attacks.append(("Ranged Attack", lambda c: character.rangedAttack(c)))
    if isinstance(character, Magician):
        attacks.append(("Magic Attack",  lambda c: character.magicAttack(c)))
        attacks.append(("Heal",          lambda c: character.heal()))
    return attacks

def show_status(a, b):
    print(f"\n  {'Name':<18} {'HP':>6}")
    divider("-")
    print(f"  {a.getUsername():<18} {a.getHp():>6}")
    print(f"  {b.getUsername():<18} {b.getHp():>6}")
    divider("-")


# ──────────────────────────────────────────────
#  Core match engine
# ──────────────────────────────────────────────

def player_turn(attacker, defender):
    """Human player picks an action."""
    attacks = get_attacks(attacker)
    print(f"\n  {attacker.getUsername()}'s turn — Choose action:")
    for i, (label, _) in enumerate(attacks, 1):
        print(f"    [{i}] {label}")
    while True:
        try:
            idx = int(input("  Your choice: ").strip()) - 1
            if 0 <= idx < len(attacks):
                print()
                attacks[idx][1](defender)
                return
        except ValueError:
            pass
        print("  ✗ Invalid. Try again.")

def cpu_turn(attacker, defender):
    """CPU picks a random action."""
    attacks = get_attacks(attacker)
    label, action = random.choice(attacks)
    print(f"\n  {attacker.getUsername()} uses {label}!")
    action(defender)

def run_match(player_char, opponent_char, player_is_human=True, opponent_is_human=False):
    """
    Run a single match between two characters.
    Returns the winning character.
    """
    header(f"  ⚔  {player_char.getUsername()} vs {opponent_char.getUsername()}")

    # Randomise who goes first
    order = [player_char, opponent_char]
    random.shuffle(order)
    first, second = order[0], order[1]

    # Map each character to whether it's human-controlled
    is_human = {
        player_char.getUsername():   player_is_human,
        opponent_char.getUsername(): opponent_is_human,
    }

    print(f"\n  {first.getUsername()} goes first!\n")
    pause()

    round_num = 1
    while player_char.getHp() > 0 and opponent_char.getHp() > 0:
        print(f"\n  ── Round {round_num} ──")
        show_status(player_char, opponent_char)

        for attacker in [first, second]:
            defender = opponent_char if attacker is player_char else player_char
            if attacker.getHp() <= 0:
                continue
            if is_human.get(attacker.getUsername(), False):
                player_turn(attacker, defender)
            else:
                cpu_turn(attacker, defender)
            if defender.getHp() <= 0:
                break

        round_num += 1

    # Determine winner
    if player_char.getHp() > 0:
        winner = player_char
    else:
        winner = opponent_char

    header(f"  🏆  {winner.getUsername()} wins the match!")
    show_status(player_char, opponent_char)
    pause()
    return winner


# ──────────────────────────────────────────────
#  Single-player mode
# ──────────────────────────────────────────────

def single_player_game():
    header("SINGLE PLAYER MODE")
    p_name = input("  Enter your username: ").strip() or "Player"

    player = Novice(p_name)
    wins = 0
    promoted = False

    print(f"\n  Welcome, {player.getUsername()}! You start as a Novice.")
    print("  Defeat the Boss 2 times to unlock a class promotion!")
    pause()

    while True:
        # Re-create a fresh Boss for every match
        boss = Boss("Monster")

        winner = run_match(player, boss, player_is_human=True, opponent_is_human=False)

        if winner.getUsername() == player.getUsername():
            wins += 1
            print(f"  🎉 You have {wins} win(s)!")

            # Promotion after 2 wins (only once)
            if wins == 2 and not promoted:
                print("\n  ⭐  You've proven yourself! Choose a new class:")
                print("    [2] Swordsman\n    [3] Archer\n    [4] Magician")
                while True:
                    choice = input("  Your choice: ").strip()
                    if choice in ("2", "3", "4"):
                        name, cls = ROLE_MAP[choice]
                        player = cls(player.getUsername())
                        print(f"\n  You are now a {name}!")
                        promoted = True
                        break
                    print("  ✗ Invalid choice.")
        else:
            print(f"  💀 You lost! The Monster defeated you.")

        print(f"\n  📊 Your total wins: {wins}")
        again = input("  Play another match? (y/n): ").strip().lower()
        if again != "y":
            break

    return wins


# ──────────────────────────────────────────────
#  Player vs Player mode
# ──────────────────────────────────────────────

def pvp_game():
    header("PLAYER VS PLAYER MODE")

    p1 = pick_role("Player 1", allow_novice=True)
    p2 = pick_role("Player 2", allow_novice=True)

    p1_wins = 0
    p2_wins = 0

    while True:
        # Re-instantiate characters to restore HP each match
        p1_fresh = p1.__class__(p1.getUsername())
        p2_fresh = p2.__class__(p2.getUsername())

        winner = run_match(p1_fresh, p2_fresh, player_is_human=True, opponent_is_human=True)

        if winner.getUsername() == p1.getUsername():
            p1_wins += 1
        else:
            p2_wins += 1

        print(f"\n  📊 Scoreboard:")
        print(f"     {p1.getUsername()}: {p1_wins} win(s)")
        print(f"     {p2.getUsername()}: {p2_wins} win(s)")

        again = input("\n  Play another match? (y/n): ").strip().lower()
        if again != "y":
            break

    return p1_wins, p2_wins


# ──────────────────────────────────────────────
#  Main menu
# ──────────────────────────────────────────────

def main():
    header("⚔  RPG BATTLE GAME  ⚔")
    print("  Welcome, adventurer!\n")

    while True:
        print("  Select game mode:")
        print("    [1] Single Player")
        print("    [2] Player vs Player")
        print("    [3] Quit")
        mode = input("  Your choice: ").strip()

        if mode == "1":
            total_wins = single_player_game()
            print(f"\n  Game over! Final wins: {total_wins}")
        elif mode == "2":
            p1_wins, p2_wins = pvp_game()
            print(f"\n  Game over! Final scores — P1: {p1_wins}  P2: {p2_wins}")
        elif mode == "3":
            print("\n  Thanks for playing! Farewell, adventurer. ⚔\n")
            break
        else:
            print("  ✗ Invalid choice.\n")

        print()
        again = input("  Return to main menu? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing! Farewell, adventurer. ⚔\n")
            break


if __name__ == "__main__":
    main()