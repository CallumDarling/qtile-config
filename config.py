import os, subprocess
from typing import override
from libqtile import bar, layout, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras.bar import Bar
from qtile_extras.widget import modify
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call(home)

colours = [
    "#cad3f5", # normal text
    "#c6a0f6", # selected text and border
    "#24273a", # normal background (Base)
    "#363a4f", # selected bg
    "#d5aeea",  # pink
    "#F28FAD",  # red
    "#96CDFB", # blue
    "#18192600", # crust (transparent)
    "#5b6078", # crust
    "#b7bdf8", # lavender
]

mod = "mod4"
# terminal = guess_terminal()
terminal = "alacritty"
runLauncher = "dmenu_run"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is in the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Switch between screens
    Key([mod, "mod1"], "Right", lazy.next_screen(), desc="Move to the next screen"),
    Key([mod, "mod1"], "Left", lazy.prev_screen(), desc="Move to the previous screen"),
    Key([mod], "Space", lazy.next_screen(), desc="Move to the next screen"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes

    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "d", lazy.spawn(runLauncher), desc="Launch run menu"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control", "shift"], "c", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(border_focus=colours[1],
                     margin=3,
                     border_width=1,
                     single_border_width=0,
                     single_margin=0),
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    layout.Zoomy(),
]

widget_defaults = dict(
    #font="sans",
    font="Jetbrains Mono Bold",
    fontsize=11,
    padding=0,
    margin=0,
    background=colours[8],
    foreground=colours[2]
    #background='#0000000'
)
extension_defaults = widget_defaults.copy()

def initWidg(tray):
    c1=colours[2]
    c2=colours[0]
    # powerline = {
    #     "decorations": [
    #         PowerLineDecoration(path="forward_slash",size=8,)
    #     ]
    # }
    # plLeft = {
    #     "decorations": [
    #         PowerLineDecoration(path="arrow_right",size=8,)
    #     ]
    #}
    plRight = {
        "decorations": [
            PowerLineDecoration(path="arrow_left",size=8)
        ]
    }
    rect = {
        "decorations": [
            RectDecoration(colour=colours[4], radius=10, filled=True, padding_y=4, group=True,use_widget_background=True)
        ],
        "padding": 10,
    }
    colourLeft = colours[4]
    colourRight = colours[9]
    widgetsLeft = [
       widget.Spacer(length=5, background=colourLeft),
        widget.CurrentLayoutIcon(scale=0.6,background=colourLeft,foreground=colours[2],use_mask=True),
        widget.CurrentScreen(**plRight,background=colourLeft,active_color=colours[2],fmt=' {}',),
        widget.GroupBox2(
            background=colourRight,
            foreground=colours[4],
            text_colours=colours[2],
             font="Jetbrains Mono Bold",
             padding_x=5,
             margin_x=3,
            **plRight,
        ),
        widget.Spacer(length=1),
        widget.Prompt(),
        #widget.TextBox("|"),
        widget.WindowName(background=colours[8],foreground=colours[2],),
        widget.Chord(
            chords_colors={
                "launch": ("#ff0000", "#ffffff"),
            },
            name_transform=lambda name: name.upper(),
        ),
    ]
    widgetsRight = [
        widget.TextBox(fmt='CPU', background=colourLeft, **rect),
        widget.CPU(background=colourRight,
                   format='{freq_current}GHz {load_percent}% ',
                   **rect
                   ),
        widget.Spacer(length=1),
        widget.TextBox(fmt='MEM', background=colourLeft, **rect),
        widget.Memory(measure_mem='G',format='{MemUsed: .01f}G {MemPercent: .0f}% ',**rect,background=colourRight),
        widget.Spacer(length=1),
        widget.TextBox(fmt='CPU', background=colourLeft, **rect),
        widget.CheckUpdates(display_format='U: {Updates}',
                            no_update_string='U: 0 ',
                            background=colourRight,
                            **rect,
                            colour_have_updates=colours[2],
                            colour_no_updates=colours[2]
                            ),
        widget.Spacer(length=1),
        widget.TextBox(fmt='V', background=colourLeft, **rect),
        widget.Volume(emoji=False,fmt="{} ",**rect,background=colourRight),
        widget.Spacer(length=1),
        widget.TextBox(fmt='D', background=colourLeft, **rect),
        widget.Clock(format="%d/%m/%y | %a ",**rect,background=colourRight),
        widget.Spacer(length=1),
        widget.TextBox(fmt='T', background=colourLeft, **rect),
        widget.Clock(format="%H:%M",**rect,background=colourRight),
        widget.Spacer(length=1),
        widget.QuickExit(default_text='[X]', countdown_format='[{}]',**rect,background=colourRight),
    ]
    if tray:
        widgetsRight.insert(0, widget.Systray())

    return widgetsLeft + widgetsRight

bgcol = colours[8]
screens = [
    Screen(
        top=bar.Bar(
            widgets = initWidg(0),
            size = 31,
            border_width=[2, 2, 2, 2],  # Draw top and bottom borders
            #border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            border_color=[bgcol,bgcol,bgcol,bgcol],  # Borders are magenta
            background=bgcol
        ),
    ),
    Screen(
        top=bar.Bar(
            widgets = initWidg(1),
            size = 31,
            border_width=[2, 2, 2, 2],  # Draw top and bottom borders
            #border_color=['#00000000','#00000000','#00000000','#00000000',],  # Borders are magenta
            border_color=[bgcol,bgcol,bgcol,bgcol],  # Borders are magenta
            background=bgcol
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
