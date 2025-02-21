from typing import Literal, TypedDict, assert_never, get_args

type BasicCardColor = Literal["red", "green", "blue", "yellow"]
basic_card_colors: tuple[BasicCardColor, ...] = get_args(BasicCardColor.__value__)


class NumberCard(TypedDict):
    id: str
    color: BasicCardColor
    type: Literal["number"]
    number: int


type FunctionCardEffect = Literal["skip", "+2", "reverse"]
function_card_effects: tuple[FunctionCardEffect, ...] = get_args(
    FunctionCardEffect.__value__
)


class FunctionCard(TypedDict):
    id: str
    color: BasicCardColor
    type: Literal["function"]
    effect: FunctionCardEffect


type WildCardEffect = Literal["+4", "color"]
wild_card_effects: tuple[WildCardEffect, ...] = get_args(WildCardEffect.__value__)
type WildCardColor = Literal["black"]
wild_card_color: WildCardColor = "black"


class WildCard(TypedDict):
    id: str
    color: WildCardColor
    type: Literal["wild"]
    effect: WildCardEffect


type Card = NumberCard | FunctionCard | WildCard
type Deck = list[Card]


def format_card(card: Card) -> str:
    if card["type"] == "number":
        return card["color"].title() + "_" + str(card["number"])
    elif card["type"] == "function":
        return card["color"].title() + "_" + card["effect"].title()
    elif card["type"] == "wild":
        return card["effect"].title()
    else:
        assert_never(card["type"])
