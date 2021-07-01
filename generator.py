import numpy as np
import mmap


def generate(size: int, filename: str):
    """Function for generating file with numbers uint32 written in big endian. Return sum of numbers, min and max number in array"""
    with open(filename, 'wb') as f_writer:
        generated_array = np.random.randint(0, 2**32, size//4, dtype=np.dtype('uint32')).newbyteorder()
        f_writer.write(generated_array.data)

def read_f(filename: str):
    with open(filename, 'rb') as f_reader:
        return np.frombuffer(f_reader.read(), dtype=np.dtype('uint32').newbyteorder('>'))

def read_mmap_f(size: int, filename: str):
    with open(filename, 'rb') as f_reader:
        mm_buf = mmap.mmap(f_reader .fileno(), length=size, offset=0, access=mmap.ACCESS_READ)
        return np.frombuffer(mm_buf, dtype=np.dtype('uint32').newbyteorder('>'))

def disp_res(min_elem: int, max_elem: int, sum_elems: int, ):
    print(f"Min: ", min_elem)
    print(f"Max: ", max_elem)
    print(f"Sum: ", sum_elems)
