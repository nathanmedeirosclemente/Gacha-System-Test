import random
from typing import List, Dict
from datetime import datetime


class Player:
    def __init__(self, name: str):
        self.name = name
        self.inventory = {"Mythic": [], "SSR": [], "SR": [], "R": []}
        self.total_pulls = 0
        self.pull_history = []
        self.stats = {"Mythic": 0, "SSR": 0, "SR": 0, "R": 0}


class GachaSystem:
    def __init__(self):
        # Updated rarity rates
        self.rates = {
            "Mythic": 0.1,  # 0.1%
            "SSR": 3,  # 3%
            "SR": 16,  # 16%
            "R": 80.9,  # 80.9%
        }

        # Updated WoW Items with Mythic tier
        self.items = {
            "Mythic": [
                "Atiesh, Greatstaff of the Guardian",
                "Val'anyr, Hammer of Ancient Kings",
                "Dragonwrath, Tarecgosa's Rest",
                "Fangs of the Father",
                "Thunderfury, Blessed Blade of the Windseeker",
            ],
            "SSR": [
                "Frostmourne",
                "Shadowmourne",
                "Warglaives of Azzinoth",
                "Thori'dal, the Stars' Fury",
                "Invincible's Reins",
                "Ashes of Al'ar",
                "Time-Lost Proto-Drake",
            ],
            "SR": [
                "Sulfuras, Hand of Ragnaros",
                "Val'anyr, Hammer of Ancient Kings",
                "Swift Spectral Tiger",
                "Mimiron's Head",
                "Reins of the Blue Drake",
                "Corrupted Ashbringer",
                "Zin'rokh, Destroyer of Worlds",
                "Swift Zulian Tiger",
                "Feldrake",
            ],
            "R": [
                "Swift White Ram",
                "Azure Whelpling",
                "Mechano-Hog",
                "Hearthstone",
                "Frostweave Bag",
                "Flask of the Titans",
                "Elixir of the Mongoose",
                "Deviate Fish",
                "Noggenfogger Elixir",
            ],
        }

        self.pity_counter = 0
        self.pity_limit = 110  # Guaranteed SSR after 110 pulls
        self.mythic_pity = 0  # Counter for Mythic pity
        self.mythic_pity_limit = 5000  # Guaranteed Mythic after 1000 pulls

        self.players = {}
        self.pull_logs = []

    def register_player(self, player_name: str) -> None:
        if player_name not in self.players:
            self.players[player_name] = Player(player_name)

    def get_rarity(self) -> str:
        self.pity_counter += 1
        self.mythic_pity += 1

        # Hard pity checks first
        if self.mythic_pity >= self.mythic_pity_limit:
            self.mythic_pity = 0
            self.pity_counter = 0
            return "Mythic"
        if self.pity_counter >= self.pity_limit:
            self.pity_counter = 0
            return "SSR"

        # Base roll calculation
        roll = random.uniform(0, 100)  # Usando float entre 0 e 100

        # Soft pity adjustments
        if self.mythic_pity >= 800:
            mythic_rate = self.rates["Mythic"] + (self.mythic_pity - 800) * 0.0001
        else:
            mythic_rate = self.rates["Mythic"]

        if self.pity_counter >= 75:
            ssr_rate = self.rates["SSR"] + (self.pity_counter - 75) * 0.05
        else:
            ssr_rate = self.rates["SSR"]

        # Check rarities in order from highest to lowest
        if roll < mythic_rate:
            self.mythic_pity = 0
            self.pity_counter = 0
            return "Mythic"
        elif roll < (mythic_rate + ssr_rate):
            self.pity_counter = 0
            return "SSR"
        elif roll < (mythic_rate + ssr_rate + self.rates["SR"]):
            return "SR"
        else:
            return "R"

    def pull_item(self, player_name: str) -> Dict[str, str]:
        if player_name not in self.players:
            self.register_player(player_name)

        player = self.players[player_name]
        player.total_pulls += 1

        # Get rarity first
        rarity = self.get_rarity()

        # Then create the result dictionary
        result = {
            "rarity": rarity,
            "item": random.choice(self.items[rarity]),
            "timestamp": datetime.now(),
            "pull_number": player.total_pulls,
        }

        # Update player inventory and stats
        player.inventory[result["rarity"]].append(result["item"])
        player.stats[result["rarity"]] += 1
        player.pull_history.append(result)

        return result

    def multi_pull(self, player_name: str, count: int = 10) -> List[Dict[str, str]]:
        return [self.pull_item(player_name) for _ in range(count)]

    def get_player_stats(self, player_name: str) -> Dict:
        if player_name not in self.players:
            return None

        player = self.players[player_name]
        return {
            "name": player.name,
            "total_pulls": player.total_pulls,
            "inventory": player.inventory,
            "stats": player.stats,
            "rarity_rates": {
                rarity: (
                    (count / player.total_pulls * 100) if player.total_pulls > 0 else 0
                )
                for rarity, count in player.stats.items()
            },
        }


if __name__ == "__main__":
    gacha = GachaSystem()
    current_player = input("Enter player name: ")

    while True:
        print(f"\n=== WoW Gacha System === [Player: {current_player}]")
        print("\n1. Single Pull")
        print("2. Multi Pull")
        print("3. View Stats")
        print("4. Change Player")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ")

        if choice == "1":
            result = gacha.pull_item(current_player)
            print(f"\nSingle Pull Result: {result['item']} ({result['rarity']})")

        elif choice == "2":
            try:
                pull_count = int(input("Enter number of pulls (1-10000): "))
                if 1 <= pull_count <= 10000:
                    results = gacha.multi_pull(current_player, pull_count)
                    print(f"\n{pull_count}x Pull Results:")
                    for i, result in enumerate(results, 1):
                        print(f"Pull {i}: {result['item']} ({result['rarity']})")
                else:
                    print("Please enter a number between 1 and 10000")
            except ValueError:
                print("Please enter a valid number")

        elif choice == "3":
            stats = gacha.get_player_stats(current_player)
            if stats:
                print(f"\nStats for {current_player}")
                print(f"Total Pulls: {stats['total_pulls']}")
                print("\nRarity Rates:")
                for rarity, rate in stats["rarity_rates"].items():
                    print(f"{rarity}: {rate:.2f}%")
                print("\nInventory:")
                for rarity, items in stats["inventory"].items():
                    if items:
                        print(f"\n{rarity}:")
                        item_count = {}
                        for item in items:
                            item_count[item] = item_count.get(item, 0) + 1
                        for item, count in item_count.items():
                            if count > 1:
                                print(f"- {item} x{count}")
                            else:
                                print(f"- {item}")
            else:
                print(f"No stats found for {current_player}")

        elif choice == "4":
            current_player = input("Enter new player name: ")
            print(f"\nSwitched to player: {current_player}")

        elif choice == "5":
            print("Thank you for playing!")
            break

        else:
            print("Invalid option. Please try again.")
