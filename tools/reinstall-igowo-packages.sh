#!/bin/bash
# -*- coding: utf-8 -*-

# Copyright 2006 - 2012 Philipp Wollermann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -u

pacman -Sy
pacman -Q | grep awstats && pacman -S --noconfirm awstats
pacman -Q | grep dovecot && pacman -S --noconfirm dovecot
pacman -Q | grep ejabberd-mod_admin_extra-svn && pacman -S --noconfirm ejabberd-mod_admin_extra-svn
pacman -Q | grep libaio && pacman -S --noconfirm libaio
pacman -Q | grep meld3 && pacman -S --noconfirm meld3
pacman -Q | grep mod_rpaf && pacman -S --noconfirm mod_rpaf
pacman -Q | grep nginx && pacman -S --noconfirm nginx
pacman -Q | grep perl-net-cidr && pacman -S --noconfirm perl-net-cidr
pacman -Q | grep qemu-kvm && pacman -S --noconfirm qemu-kvm
pacman -Q | grep ruby1.8 && pacman -S --noconfirm ruby1.8
pacman -Q | grep rubygems1.8 && pacman -S --noconfirm rubygems1.8
pacman -Q | grep spawn-fcgi && pacman -S --noconfirm spawn-fcgi
pacman -Q | grep supervisor && pacman -S --noconfirm supervisor
pacman -Q | grep unbound && pacman -S --noconfirm unbound
