#!/bin/bash

# (C) 2024 Massimo Girondi massimo@girondi.net GNU GPL v3
# This puts the second port of our NIC in a namespace
# So that we can use it as target for our experiments
# Without "localhost" replying for us

# The physical topology, when we need to just look at sender side, could then be:
#
#     +------------+
#     |            |       +------+
#     |         | 0|-----> |  OF  |
#     |     cx5|   |       |switch|
#     |         | 1|<----- |      |
#     |            |       +------+
#     +------------+
#


DEV0=cx5if0
DEV1=cx5if1
MACHINE=27

sudo ip netns add jail
sudo ip link  set netns jail dev $DEV1
sudo ip netns exec jail ip addr add 192.168.1${MACHINE}.1/16 dev $DEV1
sudo ip netns exec jail ip link set mtu 9000 dev $DEV1
sudo ip netns exec jail ip link set up dev $DEV1

sudo ip addr add 192.168.1${MACHINE}.0/16 dev $DEV0
sudo ip link set mtu 9000 dev $DEV0
sudo ip link set up dev $DEV0

