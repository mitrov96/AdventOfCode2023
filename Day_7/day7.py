from functools import cmp_to_key

# Parse input file
input = open("input_day_7.txt")

# Save the hands as a tuple of (cards, bid)
hands = []
for line in input:
    hands.append(line.strip().split())
    hands[-1][1] = int(hands[-1][1])
input.close()

# The ranking of the cards for pt. 1 and pt. 2, respectively
CARDS = 'AKQJT98765432'
CARDS2 = 'AKQT98765432J'


# Function for determining the ranking of a given hand
def classify_hand(hand, jokers):
    # Count how many of each card we have. Don't count Jokers if we have them (and are in pt. 2)
    cards = [[hand.count(card), card] for card in set(hand) if (jokers == False or card != 'J')]

    # Sort the cards so we know which card we have the most of
    cards.sort(reverse=True)

    # Replace the Jokers with the most prevalent card
    if jokers:
        joker_count = hand.count('J')
        # Special case for a hand with 5 Jokers
        if joker_count == 5:
            cards = [(5, 'J')]
        else:
            hand = hand.replace('J', cards[0][1])
            cards[0][0] += joker_count

    # Look for a Five-of-a-Kind
    if cards[0][0] == 5:
        return 7
    # Look for a Four-of-a-Kind
    elif cards[0][0] == 4:
        return 6
    # Look for a Full-House or a Three-of-a-Kind
    elif cards[0][0] == 3:
        if len(cards) == 2:
            return 5
        else:
            return 4
    # Look for a Two-Pair or One-Pair
    elif cards[0][0] == 2:
        if len(cards) == 3:
            return 3
        else:
            return 2
    # With 5 unique cards, we have a High Card
    else:
        return 1


# Comparison function for sorting the hands
def compare_hands(hand1, hand2, jokers=False):
    # We don't care about the bids, so just grab the hands themselves
    hand1 = hand1[0]
    hand2 = hand2[0]

    # Get the rank of both hands
    hand1_class = classify_hand(hand1, jokers)
    hand2_class = classify_hand(hand2, jokers)

    # Return -1 or 1 depending on which hand is a high rank
    if hand1_class < hand2_class:
        return -1
    elif hand1_class > hand2_class:
        return 1

    # If both cards are the same rank, start comparing cards in order until we find two that don't match
    else:
        hand1_card = None
        hand2_card = None
        for x in range(len(hand1)):
            if hand1[x] != hand2[x]:
                hand1_card = hand1[x]
                hand2_card = hand2[x]
                break
        if hand1_card == None:
            return 0
        else:
            return compare_cards(hand1_card, hand2_card, jokers)


# Comparison function for pt. 2, just calls the pt. 1 comparison function with jokers = True
def compare_hands_jokers(hand1, hand2):
    return compare_hands(hand1, hand2, True)


# Tiebreaker comparison function for finding the higher-value card
def compare_cards(card1, card2, jokers):
    # Different rankings for the cards depending on whether Js are Jokers or Jacks
    if not jokers:
        card1_index = CARDS.find(card1)
        card2_index = CARDS.find(card2)
    else:
        card1_index = CARDS2.find(card1)
        card2_index = CARDS2.find(card2)
    if card1_index > card2_index:
        return -1
    elif card1_index < card2_index:
        return 1
    else:
        return 0


# Pt. 1, where Js are Jacks
# cmp_to_key is a function that allows you to use a comparator between two values for the sorting key
hands.sort(key=cmp_to_key(compare_hands))
winnings = 0
for x in range(len(hands)):
    winnings += (x + 1) * (hands[x][1])
print("The total winnings for the J = Jacks Camel Cards is:", winnings)

# Pt. 2, where Js are Jokers
hands.sort(key=cmp_to_key(compare_hands_jokers))
winnings = 0
for x in range(len(hands)):
    winnings += (x + 1) * (hands[x][1])
print("The total winnings for the J = Jokers Camel Cards is:", winnings)