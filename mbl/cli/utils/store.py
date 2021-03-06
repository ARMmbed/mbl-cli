#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Manage persistent storage locations used with device provisioning.

A "persistent storage location" consists of a directory on disk containing
a file named `config.json`. The persistent storage location is used to hold
credentials and certificates which are used to provision devices for use with
Pelion Device Management.
The `config.json` file holds information about the stored items and other
metadata (including paths to any objects in the persistent storage location
stored as files).
MBL-CLI also creates/accepts a file named `.mbl-stores.json`.
`.mbl-stores.json` is referred to as the STORE_LOCATIONS_FILE.
This is where known storage types and locations are saved as key/value pairs.

The `Store` class contained in this module provides the public interface to
access objects in a persistent storage location and save new items to the
store.
The `Store` class is basically a thin wrapper around a dict built from the
store's config.json.

* `Store` class representing a storage location on disk.
* `StoreLocationsRecord` class is an interface for STORE_LOCATIONS_FILE i/o.

Exceptions:
----
* `StoreNoteFoundError` Specified store location does not exist.
"""

import pathlib
import shutil
from . import file_handler

DEFAULT_STORE_RECORD = {
    "user": str(pathlib.Path().home() / pathlib.Path(".mbl-store", "user")),
    "team": str(pathlib.Path().home() / pathlib.Path(".mbl-store", "team")),
}


class Store:
    """This class is an abstraction of a storage location on disk.

    The store holds a `_config` dict. `_config` holds metadata
    about the store itself, and information on objects within the store.

    This object provides an interface to access the store config file data.
    """

    def __init__(self, store_type):
        """Build a store object from a path based on the store_type.

        The path_to_store on disk must exist before instantiating this class.

        :params str store_type: The type of store to build (team or user).
        """
        path_to_store = _get_or_create_store(store_type)
        self._config = file_handler.from_json(path_to_store / "config.json")
        if not self._config:
            self._config = dict(
                location=str(path_to_store), api_key="", dev_certs=dict()
            )

    @property
    def api_key(self):
        """Return the API key held in the store.

        :returns str: API key
        """
        return self._config["api_key"]

    @api_key.setter
    def api_key(self, key):
        self._config["api_key"] = key.strip()

    @property
    def certificate_paths(self):
        """List of all developer certificate binary files in the store.

        :returns dict: developer cert file paths in the form
        `{name: [bin_path_1, bin_path_2 ...]}`
        """
        return self._config["dev_certs"]

    @property
    def config_path(self):
        """Path to the store config file."""
        return pathlib.Path(self._config["location"], "config.json")

    def save(self):
        """Save config data to a file."""
        file_handler.to_json(self.config_path, **self._config)

    def add_certificate(self, name, certificate):
        """Add a certificate object to the store as a set of binary files.

        :param str name: name of the dev certificate.
        :param dict credentials: credentials object.
        """
        p_list = []
        for item in certificate:
            c_path = pathlib.Path(self._config["location"], name)
            c_path.mkdir(exist_ok=True, parents=True)
            c_path = c_path / "{}.bin".format(item)
            file_handler.to_binary_file(c_path, certificate[item])
            p_list.append(str(c_path))
        self.certificate_paths[name] = p_list
        self.save()

    def delete_certificate(self, name):
        """Delete a certificate from the store."""
        if name not in self.certificate_paths.keys():
            raise ValueError(
                "Certificate '{}' not found in the store, so could not be"
                " deleted.".format(name)
            )
        try:
            shutil.rmtree(
                str(pathlib.Path(self._config["location"], name).resolve())
            )
        except OSError:
            raise OSError(
                "There was an error removing the certificate files."
                " The certificate has been removed from the store config."
                " Please check and delete the files manually."
            )
        finally:
            del self.certificate_paths[name]
            self.save()


class StoreLocationsRecord:
    """Class represents the Store Locations Record.

    This class provides an interface to update and read the
    STORE_LOCATIONS_FILE.

    The store types and locations in the STORE_LOCATIONS_FILE are held as JSON
    key-value pairs which map directly to this object's internal dictionary.
    """

    STORE_LOCATIONS_FILE_PATH = pathlib.Path().home() / ".mbl-stores.json"

    def __init__(self):
        """Initialise `_data` dict with data from STORE_LOCATIONS_FILE."""
        self._data = file_handler.from_json(
            config_file_path=self.STORE_LOCATIONS_FILE_PATH
        )
        if not self._data:
            # STORE_LOCATIONS_FILE was empty.
            # write DEFAULT_STORE_RECORD to it.
            file_handler.to_json(
                config_file_path=self.STORE_LOCATIONS_FILE_PATH,
                **DEFAULT_STORE_RECORD
            )
            self._data = DEFAULT_STORE_RECORD

    def update(self, store_type, location):
        """Write a new store UID and storage location to the record.

        Prevent setting a known UID's location.
        """
        self._data[store_type] = location
        file_handler.to_json(
            config_file_path=self.STORE_LOCATIONS_FILE_PATH, **self._data
        )

    def get(self, store_type):
        """Look up a store by store_type and return the location.

        Verify the storage location is valid & exists on disk.

        :param str store_type:
        :returns Path: file path to the storage location.
        """
        try:
            loc = pathlib.Path(self._data.get(store_type, None))
        except TypeError:
            raise StoreNotFoundError(
                "Store Type not recognised. Only User and Team supported."
            )
        return loc


class StoreNotFoundError(Exception):
    """The specified store does not exist."""


def _get_or_create_store(store_type):
    """Get the store path from the StoreLocationsRecord.

    Create the path if it doesn't exist.

    We expect the storage location and config.json to be automatically
    created in the scenario where a user is saving to the store for
    the first time.

    :param str store_type: type of store to get/create.
    """
    store_path = StoreLocationsRecord().get(store_type)
    mode = 0o700 if store_type == "user" else 0o750
    store_path.mkdir(mode=mode, parents=True, exist_ok=True)
    return store_path
