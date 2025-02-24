# the value for sampling,is same as cpp!
class SamplingPointKind(object):
    left_top: int = 0
    right_top: int = 1
    left_bottom: int = 2
    right_bottom: int = 3
    center: int = 5


def get_sampling_values_1d_size(
    start: int, end: int, stride: int, sampling_radius: int
) -> int:
    if sampling_radius >= stride:
        return 0

    if start >= end:
        return 0

    sampling_size = 0
    aligned_start: int = start
    if start % stride != 0:
        aligned_start = (start + stride - 1) // stride * stride
        value = start // stride * stride + sampling_radius
        if value >= start and value < end:
            sampling_size += 1

    # normal python divide maybe return a float!
    sampling_blocks: int = (end - aligned_start) // stride
    sampling_size += 2 * sampling_blocks

    if aligned_start + sampling_blocks * stride < end:
        samplign_size += 1

    if aligned_start + sampling_blocks * stride + sampling_radius < end:
        sampling_size += 1
    return sampling_size
