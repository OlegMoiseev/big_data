import numpy as np


def generate_rand_int48():
    randByte1 = np.random.randint(1,255).to_bytes(1, byteorder='little')
    randByte2 = np.random.randint(1,255).to_bytes(1, byteorder='little')
    randByte3 = np.random.randint(1,255).to_bytes(1, byteorder='little')
    randByte4 = np.random.randint(1,255).to_bytes(1, byteorder='little')
    randByte5 = np.random.randint(1,255).to_bytes(1, byteorder='little')
    randByte6 = np.random.randint(1,255).to_bytes(1, byteorder='little')

    randBytes = randByte1 + randByte2 + randByte3 + randByte4 + randByte5 + randByte6
    randInt48 = int.from_bytes(randBytes, byteorder='little')

    return randInt48


def create_file_with_int48(num_int, f_name):
    with open(f_name, 'w') as file_writer:
        generated_array = np.array([generate_rand_int48() for _ in range(num_int)])
        np.savetxt(file_writer, generated_array, fmt="%u")


def read_f(f_name):
    with open(f_name, 'rb') as f_reader:
        return np.fromiter(f_reader.readlines(), dtype=np.dtype('u8'))
