def ip_wild_card_check(ip_address, wild_card_mask):
    """
    Checks an IP address against a wild card mask.
    Example: 192.168.1.100 passes with a mask of 192.168.%
    :param ip_address: #.#.#.# formatted IP address
    :param wild_card_mask: #.#.#.# formatted mask where % represents a wild card
    :return:
    """
    ip_parts = ip_address.split(".")
    wc_parts = wild_card_mask.split(".")
    for i in range(4):
        if wc_parts[i] == "%":
            return True
        if not ip_parts[i] == wc_parts[i]:
            return False
    return True
