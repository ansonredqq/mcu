def int16_to_bin_array(n):
    return [(n >> i) & 1 for i in range(15, -1, -1)]

print(int16_to_bin_array(2))