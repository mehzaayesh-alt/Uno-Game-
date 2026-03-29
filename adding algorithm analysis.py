import random 

COLORS = ["Red", "Blue", "Green", "Yellow"]
NUMBERS = list(range(10))
SKIP = "Skip"

PLAYER_NAMES = {
    0: "Player 1 (Minimax - Defensive)",
    1: "Player 2 (Expectimax - Offensive)",
    2: "Player 3"
}

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def is_skip(self):
        return self.value == SKIP

    def __repr__(self):
        return f"{self.color} {self.value}"

def build_deck():
    deck = []
    for color in COLORS:
        for num in NUMBERS:
            deck.append(Card(color, num))
        deck.append(Card(color, SKIP))
        deck.append(Card(color, SKIP))
    random.shuffle(deck)
    return deck


def draw_card(deck, discard):
    if not deck: #checking if the deck is not epmty 
        if len(discard) <= 1: #reshuffle not possible if deck has 0,1 cards, cant shuffle the top card 
            raise Exception("no cards left")
        top = discard[-1] #last card in list,top card
        rest = discard[:-1] #take all except the last element(top card)
        random.shuffle(rest)  
        deck.extend(rest) #adding all items of rest in deck(putting rest of the cards back in deck)
        discard.clear() #remove everyhting from discard pile
        discard.append(top) #placing top card baxk on top
    return deck.pop()

def get_valid_moves(hand, top):
    valid_moves = []

    for c in hand:
        if c.color == top.color or c.value == top.value:
            valid_moves.append(c)

    return valid_moves
#  def max-value(state):
#      if terminal: return utility
#      v = -inf
#      for each successor:
#          v = max(v, min-value(successor))
#      return v
#
#  def min-value(state):
#      if terminal: return utility
#      v = +inf
#      for each successor:
#          v = min(v, max-value(successor))
#      return v

def max_value(state, depth, player_id):
    if state.is_terminal() or depth == 0: #gameover or depth limit reaxhed 
        return evaluate(state, player_id, "defensive")

    v = float("-inf")

    moves = get_valid_moves(state.hands[state.current], state.top)
    if len(moves) == 0:
        moves = ["draw"]

    for move in moves:
        successor = apply_move(state, move)
        result    = min_value(successor, depth - 1, player_id)

        if result > v:
            v = result

    return v


def min_value(state, depth, player_id):
    if state.is_terminal() or depth == 0:
        return evaluate(state, player_id, "defensive")

    v = float("+inf")

    moves = get_valid_moves(state.hands[state.current], state.top)
    if len(moves) == 0:
        moves = ["draw"]

    for move in moves:
        successor = apply_move(state, move)
        result    = max_value(successor, depth - 1, player_id)

        if result < v:
            v = result

    return v

def exp_value(state, depth, player_id):
  
    if not state.deck:
        return evaluate(state, player_id, "offensive")

    total   = 0
    n_cards = len(state.deck)
    p_each  = 1.0 / n_cards

    for card in state.deck:
        sim = state.clone()
        sim.hands[sim.current].append(card)
        sim.current = sim.next_player()
        total += p_each * expectimax_value(sim, depth, player_id)

    return total


def expectimax_value(state, depth, player_id):
        #MAX node if it is our turn
        #EXP node if it is an opponent turn (average, not worst-case)
    
    if state.is_terminal() or depth == 0:
        return evaluate(state, player_id, "offensive")

    current = state.current

    if current == player_id: #our turn => max node 
        v     = float("-inf")
        moves = get_valid_moves(state.hands[current], state.top)
        if len(moves) == 0:
            moves = ["draw"]

        for move in moves:
            if move == "draw":
                result = exp_value(state, depth - 1, player_id)
            else:
                successor = apply_move(state, move)
                result    = expectimax_value(successor, depth - 1, player_id)
            if result > v:
                v = result
        return v

    # opponent turn => average over their legal moves
    else:
        moves = get_valid_moves(state.hands[current], state.top)
        if len(moves) == 0:
            moves = ["draw"]

        total = 0
        for move in moves:
            successor = apply_move(state, move)
            total    += expectimax_value(successor, depth - 1, player_id)

        return total / len(moves)


class ExpectimaxAgent:
    def __init__(self, pid, depth=3):
        self.pid   = pid
        self.depth = depth

    def choose_move(self, state):
        moves = get_valid_moves(state.hands[self.pid], state.top)
        if len(moves) == 0:
            moves = ["draw"]

        best_move  = moves[0]
        best_score = float("-inf")
        scored     = []

        for move in moves:
            if move == "draw":
                score = exp_value(state, self.depth - 1, self.pid)
            else:
                successor = apply_move(state, move)
                score     = expectimax_value(successor, self.depth - 1, self.pid)

            scored.append((str(move), round(score, 2)))
            if score > best_score:
                best_score = score
                best_move  = move

        return best_move, scored

print("Expectimax agent defined.")
print("Implements: expectimax_value() router + exp_value() chance node")
print("Strategy  : Offensive (weights: own=-4, opp=+3, skip=+2)")

# running 35 games for anaylsis  
N_GAMES = 35
wins    = {0: 0, 1: 0, 2: 0}
turns_per_game  = []
p1_avg_hand     = []
p2_avg_hand     = []

print(f"Running {N_GAMES} simulated games...")

for seed in range(N_GAMES):
    random.seed(seed)
    s, hlog, mlog, _ = run_game(seed=seed, verbose=False)
    w = s.winner()
    if w is not None:
        wins[w] += 1
    turns_per_game.append(len(mlog))
    if hlog[0]:
        p1_avg_hand.append(sum(hlog[0]) / len(hlog[0]))
        p2_avg_hand.append(sum(hlog[1]) / len(hlog[1]))

print("Done.")
print()
print(f"{'Player':<30} {'Wins':>6} {'Win %':>8}")
print("-" * 46)
for pid in [0, 1, 2]:
    pct = wins[pid] / N_GAMES * 100
    print(f"{PLAYER_NAMES[pid]:<30} {wins[pid]:>6}   {pct:>6.1f}%")

print()
print(f"Average turns per game : {sum(turns_per_game)/len(turns_per_game):.1f}")
print(f"P1 avg hand size       : {sum(p1_avg_hand)/len(p1_avg_hand):.2f} cards")
print(f"P2 avg hand size       : {sum(p2_avg_hand)/len(p2_avg_hand):.2f} cards")

# Both algorithms were tested over multiple game simulations.

# MINIMAX (Player 1 - Defensive):
# - Minimax assumes the worst case scenario at every step
# - It treats opponents as if they are always trying to hurt P1
# - This makes it very careful and conservative
# - It holds onto skip cards and avoids risky moves
# - The problem is that opponents dont actually play against P1 they play for themselves, so minimax is too pessimistic
# - It wins less often because it plays too safe

# EXPECTIMAX (Player 2 - Offensive):
# - Expectimax is more realistic than minimax
# - When drawing a card it calculates the expected value
#   over all cards in the deck instead of assuming worst card
# - Opponents are modelled as random not adversarial which is closer to how they actually play
# - This makes it more aggressive in shedding cards
# - It wins more often because it targets the win condition directly

# WHICH IS BETTER:
# Expectimax performed better in most simulations
# The main reason is that UNO has real randomness (drawing cards)
# and Expectimax handles that randomness properly using probability
# Minimax ignores the probability and just assumes bad luck every time
# For a game like UNO, Expectimax is the more suitable algorithm

# CONCLUSION:
# Minimax = safer but slower to win
# Expectimax = more realistic and wins more games
# If i had to pick one for UNO i would pick Expectimax
