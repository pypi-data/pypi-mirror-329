from typing import Final

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from tuno.client.components.CardColorLabel import CardColorLabel
from tuno.client.components.CardLabel import CardLabel
from tuno.shared.sse_events import GameStateEvent


class Sidebar(VerticalScroll):

    __CLASS_GAME_STATUS_STARTED: Final = "started"
    __CLASS_GAME_STATUS_PENDING: Final = "pending"
    __CLASS_CURRENT_PLAYER_ACTIVE: Final = "active"
    __CLASS_CURRENT_PLAYER_WAITING: Final = "waiting"

    BORDER_TITLE = "Game Info"
    DEFAULT_CSS = """
    Sidebar {
        row-span: 2;
        height: 100%;
        padding: 1 2;

        .sidebar-info-section {
            width: 100%;
            height: 3;
            align-horizontal: center;
            content-align-horizontal: center;
            color: $foreground-muted;
            border-title-color: $foreground;
            border-title-align: center;
            border: solid $surface;

            .sidebar-info-split {
                color: $text-muted 20%;
                margin: 0 1;
            }
        }

        #sidebar-info-status {
            &.started {
                color: $text-success;
            }
            &.pending {
                color: $text-warning;
            }
        }

        #sidebar-info-current-player {
            color: $foreground-muted;

            &.active {
                color: $text-success;
            }
            &.waiting {
                color: $text-accent;
            }
        }

        #sidebar-info-pile-size {
            #sidebar-info-pile-size-draw {
                color: $text-success;
            }

            #sidebar-info-pile-size-discard {
                color: $text-error;
            }
        }

        #sidebar-info-counters {
            #sidebar-info-draw-counter, #sidebar-info-skip-counter {
                color: $foreground;
            }
        }

        #sidebar-info-lead-color-container, #sidebar-info-lead-card-container {
            padding: 0 1;
        }
    }
    """

    game_state: reactive[GameStateEvent.DataType | None] = reactive(None)

    def compose(self) -> ComposeResult:

        label_status = Label(
            "...",
            id="sidebar-info-status",
            classes="sidebar-info-section",
        )
        label_status.border_title = "Game Status"
        yield label_status

        label_capacity = Label(
            "-/-",
            id="sidebar-info-capacity",
            classes="sidebar-info-section",
        )
        label_capacity.border_title = "Capacity"
        yield label_capacity

        label_direction = Label(
            "-/-",
            id="sidebar-info-direction",
            classes="sidebar-info-section",
        )
        label_direction.border_title = "Direction"
        yield label_direction

        label_current_player = Label(
            "-/-",
            id="sidebar-info-current-player",
            classes="sidebar-info-section",
        )
        label_current_player.border_title = "Current"
        yield label_current_player

        label_draw_pile_size = Label(
            "-",
            id="sidebar-info-pile-size-draw",
        )
        label_draw_pile_size.tooltip = "Draw pile."
        label_discard_pile_size = Label(
            "-",
            id="sidebar-info-pile-size-discard",
        )
        label_discard_pile_size.tooltip = "Discard pile."
        container_pile_size = Horizontal(
            label_draw_pile_size,
            Label("|", classes="sidebar-info-split"),
            label_discard_pile_size,
            id="sidebar-info-pile-size",
            classes="sidebar-info-section",
        )
        container_pile_size.border_title = "Pile Size"
        yield container_pile_size

        label_draw_counter = Label(
            "-",
            id="sidebar-info-draw-counter",
        )
        label_draw_counter.tooltip = "Draw counter."
        label_skip_counter = Label(
            "-",
            id="sidebar-info-skip-counter",
        )
        label_skip_counter.tooltip = "Skip counter."
        container_counters = Horizontal(
            label_draw_counter,
            Label("|", classes="sidebar-info-split"),
            label_skip_counter,
            id="sidebar-info-counters",
            classes="sidebar-info-section",
        )
        container_counters.border_title = "Draw/Skip"
        yield container_counters

        widget_lead_color = Widget(
            CardColorLabel(id="sidebar-info-lead-color"),
            id="sidebar-info-lead-color-container",
            classes="sidebar-info-section",
        )
        widget_lead_color.border_title = "Lead Color"
        yield widget_lead_color

        widget_lead_card = Widget(
            CardLabel(id="sidebar-info-lead-card"),
            id="sidebar-info-lead-card-container",
            classes="sidebar-info-section",
        )
        widget_lead_card.border_title = "Lead Card"
        yield widget_lead_card

    def watch_game_state(
        self,
        game_state: GameStateEvent.DataType | None,
    ) -> None:

        from tuno.client.UnoApp import UnoApp

        app = self.app
        assert isinstance(app, UnoApp)
        assert app.client is not None

        # -- Game Status --
        label_game_status = self.query_exactly_one(
            "#sidebar-info-status",
            Label,
        )
        if game_state:
            if game_state["started"]:
                game_status_display = "Started"
                label_game_status.add_class(self.__CLASS_GAME_STATUS_STARTED)
                label_game_status.remove_class(self.__CLASS_GAME_STATUS_PENDING)
            else:
                game_status_display = "Pending"
                label_game_status.remove_class(self.__CLASS_GAME_STATUS_STARTED)
                label_game_status.add_class(self.__CLASS_GAME_STATUS_PENDING)
        else:
            game_status_display = "..."
            label_game_status.remove_class(
                self.__CLASS_GAME_STATUS_STARTED,
                self.__CLASS_GAME_STATUS_PENDING,
            )
        label_game_status.update(game_status_display)

        # -- Player Capacity --
        label_player_capacity = self.query_exactly_one(
            "#sidebar-info-capacity",
            Label,
        )
        if game_state:
            player_count = len(game_state["players"])
            player_capacity = game_state["rules"]["player_capacity"]
            label_player_capacity.update(f"{player_count}/{player_capacity}")
        else:
            label_player_capacity.update("-/-")

        # -- Direction --
        label_direction = self.query_exactly_one(
            "#sidebar-info-direction",
            Label,
        )
        if game_state and game_state["started"]:
            direction = f"{game_state['direction']:+d}"
            label_direction.update(direction)
        else:
            label_direction.update("N/A")

        # -- Current Player --
        label_current_player = self.query_exactly_one(
            "#sidebar-info-current-player",
            Label,
        )
        current_player_name = "N/A"
        if game_state and game_state["started"]:
            current_player_index = game_state["current_player_index"]
            players = game_state["players"]
            if 0 <= current_player_index < len(players):
                current_player_name = players[current_player_index]["name"]
            else:
                self.log.error(
                    "Invalid value for `current_player_index`:",
                    current_player_index,
                )
            if current_player_name == app.client.player_name:
                label_current_player.add_class(self.__CLASS_CURRENT_PLAYER_ACTIVE)
                label_current_player.remove_class(self.__CLASS_CURRENT_PLAYER_WAITING)
            else:
                label_current_player.remove_class(self.__CLASS_CURRENT_PLAYER_ACTIVE)
                label_current_player.add_class(self.__CLASS_CURRENT_PLAYER_WAITING)
        else:
            label_current_player.remove_class(
                self.__CLASS_CURRENT_PLAYER_ACTIVE,
                self.__CLASS_CURRENT_PLAYER_WAITING,
            )
        label_current_player.update(current_player_name)

        # -- Pile Size --
        label_draw_pile_size = self.query_exactly_one(
            f"#sidebar-info-pile-size-draw",
            Label,
        )
        label_discard_pile_size = self.query_exactly_one(
            f"#sidebar-info-pile-size-discard",
            Label,
        )
        if game_state and game_state["started"]:
            label_draw_pile_size.update(str(game_state["draw_pile_size"]))
            label_discard_pile_size.update(str(game_state["discard_pile_size"]))
        else:
            label_draw_pile_size.update("-")
            label_discard_pile_size.update("-")

        # -- Draw/Skip Counters --
        label_draw_count = self.query_exactly_one(
            f"#sidebar-info-draw-counter",
            Label,
        )
        label_skip_count = self.query_exactly_one(
            f"#sidebar-info-skip-counter",
            Label,
        )
        if game_state and game_state["started"]:
            label_draw_count.update(str(game_state["draw_counter"]))
            label_skip_count.update(str(game_state["skip_counter"]))
        else:
            label_draw_count.update("-")
            label_skip_count.update("-")

        # -- Lead Color --
        widget_lead_color = self.query_exactly_one(
            f"#sidebar-info-lead-color",
            CardColorLabel,
        )
        widget_lead_color.data = game_state and game_state["lead_color"]

        # -- Lead Card --
        widget_lead_card = self.query_exactly_one(
            f"#sidebar-info-lead-card",
            CardLabel,
        )
        widget_lead_card.data = game_state and game_state["lead_card"]
