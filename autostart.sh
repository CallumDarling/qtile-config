#! /bin/sh
#lxsession &
xlayoutdisplay &
#picom &
slstatus &
/usr/bin/emacs --daemon &
xinput set-prop 8 'libinput Accel Speed' -0.7 &
nitrogen --restore &
sxhkd ~/.config/sxhkd/sxhkdrc &
xss-lock --transfer-sleep-lock -- i3lock-fancy-multimonitor -p -n &
np-applet &
