#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional


card_ranks = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': 9,
    'T': 8,
    '9': 7,
    '8': 6,
    '7': 5,
    '6': 4,
    '5': 3,
    '4': 2,
    '3': 1,
    '2': 0,
}

class Hand():
    def __init__(self, cards: str, id: Optional[str] = None, bet: int = -1) -> None:
        self.cards = cards
        self.id = cards if id is None else id
        self.bet = bet
    def to_dict(self) -> dict[str, int]:
        cd = {}
        for c in self.cards:
            if c not in cd:
                cd[c] = 0
            cd[c] = cd[c] + 1
        return cd
    def eyes(self) -> int:
        return max(self.to_dict().values())
    def same_of_kind(self, n: int) -> bool:
        return self.eyes() == n
    def is_two_pair(self) -> bool:
        cd = self.to_dict()
        pairs = 0
        for c in cd.keys():
            if cd[c] > 2:
                return False
            if cd[c] == 2:
                pairs += 1
        return pairs >= 2
    def is_full_house(self) -> bool:
        cd = self.to_dict()
        return len(cd) == 2 and not self.same_of_kind(4)
    def get_rank(self):
        assert ("J" not in self.cards) or (self.cards == self.id)
        ranks = [
            lambda c: c.same_of_kind(5),
            lambda c: c.same_of_kind(4),
            lambda c: c.is_full_house(),
            lambda c: c.same_of_kind(3),
            lambda c: c.is_two_pair(),
            lambda c: c.same_of_kind(2),
            lambda c: c.same_of_kind(1),
        ]
        for i in range(len(ranks)):
            if ranks[i](self):
                break
        return 6-i
    def tie_breaker(self, other: 'Hand') -> bool:
        for i in range(5):
            c  = self.id[i]
            oc = other.id[i]
            if c == oc:
                continue
            return card_ranks[c] < card_ranks[oc]
        return False
    def __lt__(self, other: 'Hand') -> bool:
        myrank = self.get_rank()
        otherrank = other.get_rank()
        if myrank == otherrank:
            return self.tie_breaker(other)
        return myrank < otherrank
    def __str__(self) -> str:
        nice_name = {
            6: "Five of a kind",
            5: "Four of a kind",
            4: "Full house",
            3: "Three of a kind",
            2: "Two pair",
            1: "One pair",
            0: "High Card",
        }
        return (f"{self.cards}|{self.id}|{self.get_rank()}|{nice_name[self.get_rank()]}")

def solution(l: list[Hand]) -> int:
    solution = 0
    for i in range(len(l)):
        solution += l[i].bet * (i+1)
    return solution

assert Hand("AAAAQ").get_rank() == 5
assert Hand("AAAAA").get_rank() == 6
assert Hand("AAAA2").get_rank() == 5
assert Hand("QQQ33").get_rank() == 4
assert Hand("AAA234").get_rank() == 3
assert Hand("QQAA45").get_rank() == 2
assert Hand("QQ2345").get_rank() == 1
assert Hand("234678").get_rank() == 0
assert Hand("2222Q") < Hand("2222A")
assert Hand("AAAAJ") < Hand("AAAAQ")

with open("input-7") as f:
    lines = f.readlines()
#     lines = """32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483""".splitlines()
    hands: list[Hand] = []
    for line in lines:
        card, bet = line.split(" ")
        hands.append(Hand(cards=card, id=card, bet=int(bet)))
    ranked_hands = sorted(hands)
    print(solution(sorted(ranked_hands)))
    # part2
    card_ranks["J"] = -1

    assert Hand("KKKK2", "JKKK2") < Hand("QQQQ2")
    assert Hand("Q2222") > Hand("Q2222", "Q2J22")
    def variation(cards: str):
        if "J" not in cards:
            return [cards]
        for i in range(len(cards)):
            c = cards[i]
            if c == "J":
                new_cards = []
                for rep in ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                    new_cards += variation(cards[0:i] + rep + cards[i+1:])
                return new_cards
        return []

    sub_ranking: list[Hand] = []
    for card in ranked_hands:
        new_cards = variation(card.cards)
        sub_ranking.append(max([Hand(cards=new_card, bet=card.bet, id=card.cards) for new_card in new_cards]))
    for card in sub_ranking:
        assert "J" not in card.cards
    print(solution(sorted(sub_ranking)))