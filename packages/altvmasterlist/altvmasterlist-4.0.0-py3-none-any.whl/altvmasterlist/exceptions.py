#!/usr/bin/env python3

class FetchError(Exception):
    """There has been an error while fetching remote data."""
    pass


class NoPublicID(Exception):
    """No valid data got fetched."""
    pass
