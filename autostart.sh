#! /bin/sh
killall udiskie &
#lxsession &
lxpolkit &
xlayoutdisplay &
picom &
/usr/bin/emacs --daemon &
xinput set-prop 'SteelSeries SteelSeries Sensei 310 eSports Mouse' 'libinput Accel Speed' -0.7 &
nitrogen --restore &
sxhkd ~/.config/sxhkd/sxhkdrc &
xss-lock --transfer-sleep-lock -- i3lock-fancy-multimonitor -p -n &
nm-applet &
udiskie --tray &
