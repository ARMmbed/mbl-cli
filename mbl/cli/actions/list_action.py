#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""List action handler."""


from mbl.cli.utils import discovery, text_list


def execute(args):
    """Entry point for the list action."""
    print(
        "Discovering devices. "
        "This will take up to {} seconds.".format(discovery.TIMEOUT)
    )
    indexed_list = text_list.IndexedTextList()
    discovery.do_discovery(indexed_list.append)

    if not indexed_list:
        raise IOError("No devices found!")
    else:
        print(indexed_list)
        return indexed_list
