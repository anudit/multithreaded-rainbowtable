import hashlib
import timeit
from datetime import datetime

from Crypto.Hash import SHA256
from cryptography.hazmat.primitives import hashes


# Benchmarking pycryptodome
def pycryptodome_benchmark():
    current_dateTime = datetime.now()

    sha256 = SHA256.new()
    sha256.update(current_dateTime.isoformat().encode())
    sha256.digest()

# Benchmarking cryptography
def cryptography_benchmark():
    current_dateTime = datetime.now()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(current_dateTime.isoformat().encode())
    digest.finalize()

# Benchmarking hashlib
def hashlib_benchmark():
    current_dateTime = datetime.now()

    sha256 = hashlib.sha256()
    sha256.update(current_dateTime.isoformat().encode())
    sha256.digest()

# Run the benchmarks
num_iterations = 1_000_000

pycryptodome_time = timeit.timeit(pycryptodome_benchmark, number=num_iterations)
cryptography_time = timeit.timeit(cryptography_benchmark, number=num_iterations)
hashlib_time = timeit.timeit(hashlib_benchmark, number=num_iterations)

# Print the results
print(f"pycryptodome: {pycryptodome_time} seconds")
print(f"cryptography: {cryptography_time} seconds")
print(f"hashlib: {hashlib_time} seconds")
