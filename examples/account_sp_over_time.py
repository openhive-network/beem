#!/usr/bin/python
import sys
import datetime as dt
from beem.amount import Amount
from beem.utils import parse_time, formatTimeString, addTzInfo
from beem.instance import set_shared_hive_instance
from beem import Hive
from beem.snapshot import AccountSnapshot
import matplotlib as mpl
# mpl.use('Agg')
# mpl.use('TkAgg')
import matplotlib.pyplot as plt


if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("ERROR: command line parameter mismatch!")
        # print("usage: %s [account]" % (sys.argv[0]))
        account = "thecrazygm"
    else:
        account = sys.argv[1]
    acc_snapshot = AccountSnapshot(account)
    acc_snapshot.get_account_history()
    acc_snapshot.build()
    # acc_snapshot.build(only_ops=["producer_reward"])
    # acc_snapshot.build(only_ops=["curation_reward"])
    # acc_snapshot.build(only_ops=["author_reward"])
    acc_snapshot.build_hp_arrays()
    timestamps = acc_snapshot.timestamps
    own_hp = acc_snapshot.own_hp
    eff_hp = acc_snapshot.eff_hp

    plt.figure(figsize=(12, 6))
    opts = {'linestyle': '-', 'marker': '.'}
    plt.plot_date(timestamps[1:], own_hp[1:], label="Own HP", **opts)
    plt.plot_date(timestamps[1:], eff_hp[1:], label="Effective HP", **opts)
    plt.grid()
    plt.legend()
    plt.title("HP over time - @%s" % (account))
    plt.xlabel("Date")
    plt.ylabel("HivePower (HP)")
    # plt.show()
    plt.savefig("hp_over_time-%s.png" % (account))

    print("last effective HP: %.1f HP" % (eff_hp[-1]))
    print("last own HP: %.1f HP" % (own_hp[-1]))
