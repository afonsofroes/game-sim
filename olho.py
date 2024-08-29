import random

card_values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'Joker']
card_order = {card: i for i, card in enumerate(card_values)}

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.rank = None

    def play_cards(self, current_play, is_first_round):
        valid_plays = self.get_valid_plays(current_play, is_first_round)
        if valid_plays:
            play = min(valid_plays, key=lambda x: max(card_order[card] for card in x))
            for card in play:
                self.hand.remove(card)
            return play
        return None

    def get_valid_plays(self, current_play, is_first_round):
        if not current_play:
            return self.get_lowest_set(is_first_round)
        
        play_size = len(current_play)
        valid_plays = []
        
        for i in range(len(self.hand) - play_size + 1):
            candidate = self.hand[i:i+play_size]
            if len(set(candidate)) == 1 and self.is_valid_play(candidate, current_play, is_first_round):
                valid_plays.append(candidate)
        
        return valid_plays

    def get_lowest_set(self, is_first_round):
        self.hand.sort(key=lambda x: card_order[x])
        for i in range(1, 5):  # Check for single, pair, triple, four of a kind
            for j in range(len(self.hand) - i + 1):
                if len(set(self.hand[j:j+i])) == 1:
                    set_cards = self.hand[j:j+i]
                    if not is_first_round or all(card not in ['2', 'Joker'] for card in set_cards):
                        return [set_cards]
        return []

    def is_valid_play(self, candidate, current_play, is_first_round):
        if is_first_round and any(card in ['2', 'Joker'] for card in candidate):
            return False
        if not current_play:
            return True
        if candidate[0] == 'Joker' or candidate[0] == '2':
            return True
        if current_play[0] == '7':
            return card_order[candidate[0]] <= card_order[current_play[0]]
        return card_order[candidate[0]] >= card_order[current_play[0]]

    def get_best_cards(self, count):
        return sorted(self.hand, key=lambda x: card_order[x], reverse=True)[:count]

    def remove_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def add_cards(self, cards):
        self.hand.extend(cards)

def setup_game(num_players):
    players = [Player(f"Player {i+1}") for i in range(num_players)]
    shuffled_deck = card_values * 4
    shuffled_deck.remove('Joker')
    shuffled_deck.remove('Joker')
    shuffled_deck.extend(['Joker', 'Joker'])
    random.shuffle(shuffled_deck)
    
    for i, card in enumerate(shuffled_deck):
        players[i % num_players].hand.append(card)
    
    return players

def swap_cards(players):
    n = len(players)
    if n < 3:
        return

    best_cards = players[-1].get_best_cards(2)
    players[-1].remove_cards(best_cards)
    players[0].add_cards(best_cards)
    worst_cards = players[0].get_best_cards(2)[::-1]  # Reverse to get worst cards
    players[0].remove_cards(worst_cards)
    players[-1].add_cards(worst_cards)

    if n > 3:
        best_card = players[-2].get_best_cards(1)
        players[-2].remove_cards(best_card)
        players[1].add_cards(best_card)
        worst_card = players[1].get_best_cards(1)[::-1]  # Reverse to get worst card
        players[1].remove_cards(worst_card)
        players[-2].add_cards(worst_card)

def play_game(players):
    current_player = -1  # Start with the last player from previous game
    current_play = []
    passes = 0
    is_first_round = True
    player_order = []
    schweppes_count = 0

    while len(player_order) < len(players):
        player = players[current_player]
        play = player.play_cards(current_play, is_first_round)

        if play:
            print(f"{player.name} plays {play}")
            if current_play and play[0] == current_play[0]:
                schweppes_count += 1
                print(f"Schweppes! {players[(current_player + 1) % len(players)].name} is skipped.")
                current_player = (current_player + 2) % len(players)
            else:
                current_player = (current_player + 1) % len(players)
            current_play = play
            passes = 0
            is_first_round = False
        else:
            print(f"{player.name} passes")
            passes += 1
            current_player = (current_player + 1) % len(players)

        if passes == len(players) - 1 or (current_play and current_play[0] in ['2', 'Joker']):
            print(f"Round ends. {players[(current_player - passes - 1) % len(players)].name} wins the round.")
            current_play = []
            passes = 0
            is_first_round = True

        if not player.hand and player not in player_order:
            player_order.append(player)
            print(f"{player.name} finishes in rank {len(player_order)}")

    # Assign ranks
    for i, player in enumerate(player_order):
        player.rank = i + 1

    print(f"Total Schweppes in this game: {schweppes_count}")
    return player_order

def full_game_cycle(num_players, num_games):
    players = setup_game(num_players)
    for game in range(num_games):
        print(f"\nStarting Game {game + 1}")
        print("Initial hands:")
        for player in players:
            print(f"{player.name}: {sorted(player.hand, key=lambda x: card_order[x])}")
        player_order = play_game(players)
        
        print("\nFinal Rankings:")
        for player in player_order:
            print(f"{player.name}: Rank {player.rank}")
        
        swap_cards(player_order)
        
        print("\nAfter card swapping:")
        for player in players:
            print(f"{player.name}: {sorted(player.hand, key=lambda x: card_order[x])}")

# Main game loop
num_players = 4  # You can change this to any number between 3 and 7
num_games = 3  # Number of games to play in a cycle
full_game_cycle(num_players, num_games)