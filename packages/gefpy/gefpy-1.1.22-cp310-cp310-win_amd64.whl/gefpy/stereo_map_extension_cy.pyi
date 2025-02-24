from typing import List, Sequence


def py_create_gef_file_with_contour(
    input_file: str, output_file: str, flat_contours: List[Sequence[int]], export_bin_sizes: Sequence[int],
    exclude_file_bin_sizes: bool, matrix_chunk_size: int, apply_compress_for_bin1: bool, compress_level: int
) -> bool:
    """
    create gef file with given contour,the contour must be closed polygons...
    Args:
        input_file:the inut file of origianl gef,support raw.gef and others...
        output_file:the output file path of result,we will overwite it if exist,if the parent dir is
            not exist,we will create it!
        flat_contours:the flatten contours,the layout of contour is [[x1,y1,x2,y2.....],[x1,y1,x2,y2...],...],first is x,next is y,etc...
        export_bin_sizes:we will default export bin 1,and you can speicfy other bin sizes,if gifen [50,100],will export 1,50,100
        matrix_chunk_size:a chunk size to process the large matrix,also,if you specify compress,we will use this to compress matrix
            but if the size is not in [2048,8192] we will clipp it to expected interval
        apply_compress_for_bin1:bool,whether compress bin1,if can compress,we will use zlib,maybe support other compress in the future!
        compress_level:the level to compress,recommend 2
    """
    ...


def py_create_gef_file_with_coordinates(
    input_file: str,
    output_file: str,
    flat_coordinates: Sequence[int],
    export_bin_sizes: Sequence[int],
    exclude_file_bin_sizes: bool,
    matrix_chunk_size: int,
    apply_compress_for_bin1: bool,
    compress_level: int,
) -> bool:
    """
    create gef file with given contour,the contour must be closed polygons...
    Args:
        input_file:the inut file of origianl gef,support raw.gef and others...
        output_file:the output file path of result,we will overwite it if exist,if the parent dir is
            not exist,we will create it!
        flat_coordinates:the flatten coordiantes,the layout of coordiantes is [x1,y1,x2,y2.....],first is x,next is y,etc...
        export_bin_sizes:we will default export bin 1,and you can speicfy other bin sizes,if gifen [50,100],will export 1,50,100
        matrix_chunk_size:a chunk size to process the large matrix,also,if you specify compress,we will use this to compress matrix
            but if the size is not in [2048,8192] we will clipp it to expected interval
        apply_compress_for_bin1:bool,whether compress bin1,if can compress,we will use zlib,maybe support other compress in the future!
        compress_level:the level to compress,recommend 2
    """
    ...


def py_create_gef_file_with_contour_and_coordinates(
    input_file: str,
    output_file: str,
    flat_contours: List[Sequence[int]],
    flat_coordinates: Sequence[int],
    export_bin_sizes: Sequence[int],
    exclude_file_bin_sizes: bool,
    matrix_chunk_size: int,
    apply_compress_for_bin1: bool,
    compress_level: int,
) -> bool:
    """
    create gef file with given contour,the contour must be closed polygons...
    Args:
        input_file:the inut file of origianl gef,support raw.gef and others...
        output_file:the output file path of result,we will overwite it if exist,if the parent dir is
            not exist,we will create it!
        flat_contours:the flatten contours,the layout of contour is [[x1,y1,x2,y2.....],[x1,y1,x2,y2...],...],first is x,next is y,etc...
        flat_coordinates:the flatten coordiantes,the layout of coordiantes is [x1,y1,x2,y2.....],first is x,next is y,etc...
        export_bin_sizes:we will default export bin 1,and you can speicfy other bin sizes,if gifen [50,100],will export 1,50,100
        matrix_chunk_size:a chunk size to process the large matrix,also,if you specify compress,we will use this to compress matrix
            but if the size is not in [2048,8192] we will clipp it to expected interval
        apply_compress_for_bin1:bool,whether compress bin1,if can compress,we will use zlib,maybe support other compress in the future!
        compress_level:the level to compress,recommend 2
    """
    ...
