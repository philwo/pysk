#!/bin/bash

set -e
set -u

pacman -Sy
pacman -Q | grep awstats && pacman -S --noconfirm awstats
pacman -Q | grep ejabberd-mod_admin_extra-svn && pacman -S --noconfirm ejabberd-mod_admin_extra-svn
pacman -Q | grep libaio && pacman -S --noconfirm libaio
pacman -Q | grep meld3 && pacman -S --noconfirm meld3
pacman -Q | grep mod_rpaf && pacman -S --noconfirm mod_rpaf
pacman -Q | grep nginx && pacman -S --noconfirm nginx
pacman -Q | grep qemu-kvm && pacman -S --noconfirm qemu-kvm
pacman -Q | grep ruby1.8 && pacman -S --noconfirm ruby1.8
pacman -Q | grep rubygems1.8 && pacman -S --noconfirm rubygems1.8
pacman -Q | grep spawn-fcgi && pacman -S --noconfirm spawn-fcgi
pacman -Q | grep supervisor && pacman -S --noconfirm supervisor
pacman -Q | grep unbound && pacman -S --noconfirm unbound

