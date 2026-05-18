import random
import time
import os

SUITS = ['♠️', '♥️', '♦️', '♣️']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def create_deck():
    return [f'{rank}{suit}' for suit in SUITS for rank in RANKS]

def print_deck(deck, face_up=True, compact=True):
    if face_up:
        print(' '.join(deck))
    else:
        print(' '.join(['🂠' for _ in deck]))

def false_cut(deck):
    """Cut that keeps the deck's cyclic order, preserving key‑card/chosen‑card adjacency."""
    # Choose a cut point away from the very ends (but that's just for show)
    cut = random.randint(5, len(deck) - 5)
    return deck[cut:] + deck[:cut]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def dramatic_reveal(deck, key_card):
    """
    Simulates dealing cards face up until the key card appears.
    Then pauses dramatically, and reveals the very next card as the spectator's.
    """
    # Find the position of key_card (it's guaranteed to exist)
    key_pos = deck.index(key_card)
    # The chosen card is immediately after it (cyclic, but here it's just next index)
    chosen_pos = key_pos + 1
    if chosen_pos >= len(deck):
        chosen_pos = 0  # just in case, though our deck won't wrap because we cut afterwards
    chosen_card = deck[chosen_pos]

    print("\n🔮 The magician starts dealing cards face up, watching you intently...")
    print("He says: 'Keep a poker face. Don't react when you see your card.'\n")
    time.sleep(2)

    dealt = []
    for i, card in enumerate(deck):
        print(f"   {card}", end=' ', flush=True)
        time.sleep(0.35)
        dealt.append(card)

        # When we reach the key card, we know the next one is the spectator's.
        if card == key_card:
            print("  ← (Magician sees his key card)")  # subtle hint in terminal
            time.sleep(0.6)
            # Deal the next card (the chosen one) silently, but we will NOT show it as just another card.
            # Instead we stop, leaving it face down on top of the undealt portion.
            # We'll simulate that by breaking here and NOT dealing the next card.
            # So we pop the next card from the remaining deck and handle it manually.
            next_index = i + 1
            if next_index < len(deck):
                # We haven't printed the chosen card yet.
                # We'll act as if we are about to deal it.
                print("\n   (He pauses, leaving the next card face down on the table)")
                time.sleep(2)
                print('🧙 "The next card I turn over... will be yours."')
                time.sleep(1.5)
                # Now reveal it dramatically
                print(f'   🎴 He flips it: *{deck[next_index]}*')
                time.sleep(1)
                print(f'\n✨ Your card was the {deck[next_index]}! ✨')
            break

    # Return the found chosen card for verification
    return deck[next_index] if next_index < len(deck) else None

def play_trick():
    clear_screen()
    print("♠️ ♥️ ♣️ ♦️  The Key Card Trick  ♦️ ♣️ ♥️ ♠️")
    print("="*50)
    deck = create_deck()
    random.shuffle(deck)

    # --- Setup: Secret Key Card ---
    key_card = deck[-1]   # bottom card of the whole deck after shuffle
    print("\n1️⃣ The magician shuffles the deck and secretly notes the bottom card...")
    time.sleep(2)

    # --- Cut to two piles ---
    split = len(deck) // 2
    hand_A = deck[:split]   # top half, placed on table
    hand_B = deck[split:]   # bottom half, stays in hand (key_card is last here)

    print("\n2️⃣ He cuts the deck into two piles:")
    print("   📦 Table pile (top half) : ", end='')
    print_deck(hand_A, face_up=False)
    print("   🤚 Hand pile  (bottom half): ", end='')
    print_deck(hand_B, face_up=False)
    time.sleep(1.5)

    # --- Spectator's card ---
    chosen_card = hand_A[0]   # top card of the table pile
    print(f"\n3️⃣ He asks you to look at the top card of the table pile.")
    print(f"   👉 Your card is: *{chosen_card}*  (Memorize it!)")
    time.sleep(2)
    input("   Press Enter after you've memorized it...")

    # --- The Trap: hand B onto hand A ---
    deck = hand_B + hand_A
    print("\n4️⃣ He places his hand pile directly onto the table pile.")
    print("   (The key card is now secretly on top of your card.)")
    time.sleep(1.5)

    # --- False cuts for misdirection ---
    for i in range(3):
        print(f"   Doing a false cut ({i+1}/3)...")
        deck = false_cut(deck)
        time.sleep(0.8)

    # --- Dramatic reveal ---
    chosen_found = dramatic_reveal(deck, key_card)

    # --- Play again? ---
    print("\n" + "="*50)
    again = input("Play again? (y/n): ").strip().lower()
    if again == 'y':
        play_trick()
    else:
        print("Thanks for playing! 🃏")

if _name_ == "_main_":
    play_trick()
