
### Get all dq channel.

less K1PEM*.ini | grep -e "^\[K1.*_DQ\]" | sed -r 's/\[(.*)\]/\1/'

