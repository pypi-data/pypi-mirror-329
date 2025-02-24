import pytest
from functools import partial
import os
import json
from isd_tui.isd import (
    CustomInput,
    CustomSelectionList,
    DonationScreen,
    InteractiveSystemd,
    MainScreen,
)
from pathlib import Path
from textual.pilot import Pilot
from textual.widgets import RichLog, TabbedContent, Tabs
from xdg_base_dirs import xdg_data_home

os.environ["PATH"] = str(Path(__file__).parent.resolve()) + ":" + os.environ["PATH"]


def first_key(inp: str) -> str:
    return inp.split(",")[0]


def pilots_active_tab(pilot: Pilot) -> str:
    return pilot.app.query_one(TabbedContent).active


async def click_and_wait(pilot: Pilot, selector) -> None:
    await pilot.click(selector)
    await pilot.pause()


async def test_focus_ordering():
    app = InteractiveSystemd()
    async with app.run_test() as pilot:
        assert isinstance(pilot.app.screen, MainScreen)
        assert isinstance(pilot.app.focused, CustomInput)

        await pilot.press("tab")
        assert isinstance(pilot.app.focused, CustomSelectionList)

        await pilot.press("tab")
        assert isinstance(pilot.app.focused, RichLog)

        await pilot.press("tab")
        assert isinstance(pilot.app.focused, Tabs)

        await pilot.press("tab")
        assert isinstance(pilot.app.focused, CustomInput)

        await pilot.press("shift+tab")
        assert isinstance(pilot.app.focused, Tabs)


async def test_navigation_tabbed_content():
    app = InteractiveSystemd()
    settings = app.settings
    nav = settings.navigation_keybindings

    async with app.run_test() as pilot:
        pilot.app.query_one(Tabs).focus()
        right_key = first_key(nav.right)
        left_key = first_key(nav.left)

        prev_tab = pilots_active_tab(pilot)

        await pilot.press(left_key)
        assert pilots_active_tab(pilot) != prev_tab

        await pilot.press(right_key)
        assert pilots_active_tab(pilot) == prev_tab

        for ignored_key in [
            first_key(nav.up),
            first_key(nav.down),
            first_key(nav.page_up),
            first_key(nav.page_down),
            first_key(nav.page_left),
            first_key(nav.page_right),
        ]:
            await pilot.press(ignored_key)
            assert pilots_active_tab(pilot) == prev_tab


async def test_navigation_custom_selection():
    """
    A fairly long test that checks the behavior of the
    `navigation_keybindings` for each focusable widget on the
    `MainScreen`.
    If this test succeeds, I can be fairly certain that
    """
    app = InteractiveSystemd()
    settings = app.settings

    async with app.run_test() as pilot:
        assert isinstance(pilot.app.screen, MainScreen)
        pilot.app.query_one(CustomSelectionList).focus()

        prev_highlighted_unit = pilot.app.screen.highlighted_unit
        nav = settings.navigation_keybindings

        for horizontal_nav_keys in [nav.right, nav.left, nav.page_left, nav.page_right]:
            for horizontal_nav_key in horizontal_nav_keys.split(","):
                await pilot.press(horizontal_nav_key)
                assert pilot.app.screen.highlighted_unit == prev_highlighted_unit

        down_key = first_key(nav.down)
        up_key = first_key(nav.up)
        await pilot.press(down_key)
        assert pilot.app.screen.highlighted_unit != prev_highlighted_unit
        await pilot.press(up_key)
        assert pilot.app.screen.highlighted_unit == prev_highlighted_unit

        page_down_key = first_key(nav.page_down)
        page_up_key = first_key(nav.page_up)
        await pilot.press(page_down_key)
        assert pilot.app.screen.highlighted_unit != prev_highlighted_unit
        await pilot.press(page_up_key)
        assert pilot.app.screen.highlighted_unit == prev_highlighted_unit

        await pilot.press("space")
        assert prev_highlighted_unit in pilot.app.screen.ordered_selection


async def test_main_keybindings_change_preview_tab():
    app = InteractiveSystemd()
    settings = app.settings
    main_kbs = settings.main_keybindings
    async with app.run_test() as pilot:
        pilot.app.query_one(CustomSelectionList).focus()
        await pilot.pause()
        # Cannot be CustomInput, as it might otherwise eat the key shortcuts
        assert not isinstance(pilot.app.focused, CustomInput)
        prev_focus = pilot.app.focused
        initial_tab = pilots_active_tab(pilot)
        await pilot.press(first_key(main_kbs.previous_preview_tab))
        assert prev_focus == pilot.app.focused, (
            "Do not change focus when switching to a new preview tab."
        )
        new_tab = pilots_active_tab(pilot)
        assert initial_tab != new_tab
        await pilot.press(first_key(main_kbs.next_preview_tab))
        assert prev_focus == pilot.app.focused
        assert pilots_active_tab(pilot) == initial_tab


async def test_main_keybindings_input_shortcuts():
    app = InteractiveSystemd()
    settings = app.settings
    main_kbs = settings.main_keybindings
    async with app.run_test() as pilot:
        pilot.app.query_one(CustomInput).focus()
        await pilot.press("c")
        pilot.app.query_one(CustomSelectionList).focus()
        await pilot.press(first_key(main_kbs.clear_input))
        assert isinstance(pilot.app.focused, CustomInput)
        assert pilot.app.focused.value == ""

        await pilot.press("x")
        pilot.app.query_one(CustomSelectionList).focus()
        await pilot.press(first_key(main_kbs.jump_to_input))
        assert isinstance(pilot.app.focused, CustomInput)
        assert pilot.app.focused.value == "x"


async def test_selection_click():
    app = InteractiveSystemd()
    async with app.run_test() as pilot:
        pilot.app.query_exactly_one(CustomSelectionList).focus()
        assert isinstance(app.screen, MainScreen)
        assert len(app.screen.ordered_selection) == 0
        default_hl_unit = app.screen.highlighted_unit
        assert default_hl_unit is not None
        # first unit from the list
        assert default_hl_unit == "0-isd-example-unit-01.service"
        # Requires some x-offset to not only click on the outer non-selectable border.
        await pilot.click(CustomSelectionList, offset=(5, 2))
        assert app.screen.highlighted_unit == "0-isd-example-unit-02.service"
        assert len(app.screen.ordered_selection) == 0, (
            "Clicking on unit should not add it to the selection by default!"
        )


async def test_donation_screen_interaction():
    app = InteractiveSystemd(fake_startup_count=100)
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, DonationScreen)
        await pilot.press("enter")
        assert isinstance(app.screen, DonationScreen)
        await pilot.press(first_key(app.settings.navigation_keybindings.down))
        assert isinstance(app.screen, DonationScreen)
        await pilot.press("enter")
        assert isinstance(app.screen, DonationScreen)
        await pilot.press("tab")
        await pilot.press("enter")
        assert isinstance(app.screen, MainScreen)


async def test_usage_counter(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    assert xdg_data_home() == Path(tmp_path)

    p = Path(tmp_path) / "isd_tui" / "persistent_state.json"
    assert not p.exists()

    # The initialization updates the `startup_count`
    InteractiveSystemd(fake_startup_count=None)

    assert p.exists()
    assert json.loads(p.read_text())["startup_count"] == 1

    InteractiveSystemd(fake_startup_count=None)

    assert json.loads(p.read_text())["startup_count"] == 2

    # Using a fake startup counter should not change anything
    InteractiveSystemd(fake_startup_count=100)
    assert json.loads(p.read_text())["startup_count"] == 2


@pytest.mark.parametrize(
    "click_target",
    [
        "#--content-tab-status",
        "#--content-tab-journal",
        "#--content-tab-cat",
        "#--content-tab-dependencies",
        "#--content-tab-show",
        "#--content-tab-help",
    ],
)
def test_snap_preview(snap_compare, click_target: str):
    assert snap_compare(
        InteractiveSystemd(),
        run_before=partial(click_and_wait, selector=click_target),
    )


def test_snap_donation_screen(snap_compare):
    assert snap_compare(
        InteractiveSystemd(fake_startup_count=100),
        run_before=lambda pilot: pilot.pause(),
    )


def test_snap_systemctl_action(snap_compare):
    app = InteractiveSystemd()
    assert snap_compare(
        app, press=[first_key(app.settings.generic_keybindings.toggle_systemctl_modal)]
    )


def test_snap_toggled_mode(snap_compare):
    app = InteractiveSystemd()
    assert snap_compare(
        app, press=[first_key(app.settings.main_keybindings.toggle_mode)]
    )


def test_snap_height(snap_compare):
    app = InteractiveSystemd()

    async def run_before(pilot: Pilot):
        pilot.app.query_exactly_one(CustomSelectionList).focus()
        assert isinstance(pilot.app, InteractiveSystemd)
        await pilot.press(pilot.app.settings.main_keybindings.increase_widget_height)

    assert snap_compare(app, run_before=run_before)
