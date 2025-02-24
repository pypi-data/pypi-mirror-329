import gzip
import logging
import os

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
import numpy as np
# make sure will take file lock for hdf5 file!
import h5py
import json
import tifffile as tiff
import cv2
from typing import List, Dict, Any, Sequence
from enum import Enum
# ide can not parse it...
from gefpy.cgef_adjust_cy import CgefAdjust
import pandas as pd


class ZlibCompressLevel(object):
    Z_BEST_SPEED: int = -1
    Z_NO_COMPRESSION: int = 0
    Z_BEST_COMPRESSION: int = 9


class GefFileKind(Enum):
    BgefKind = 1
    CgefKind = 2
    Unknown = 3


# init a global simple logger!
def generate_logger(log_name: str) -> logging.Logger:
    logger = logging.getLogger(log_name)
    log_format = logging.Formatter("%(asctime)s -%(filename)s[line:%(lineno)d] -%(levelname)s:%(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger


# define a simple logger!
logger = generate_logger("lazydog")


def convert_bin_size_string(bin_size_str: str) -> List[int]:
    try:
        split_bin_sizes = bin_size_str.split(",")
        for i in range(len(split_bin_sizes)):
            split_bin_sizes[i] = int(split_bin_sizes[i])
    except Exception as ex:
        raise RuntimeError from ex
    return split_bin_sizes


def create_dir_if_not_exist(file_dir: str) -> None:
    if not os.path.exists(file_dir):
        logger.info("create result dir {}".format(file_dir))
        os.makedirs(file_dir)


def check_write_file(file_path: str) -> None:
    if os.path.exists(file_path):
        return
    parent_dir = os.path.dirname(file_path)
    if parent_dir == "":
        # means that this is current relative path!
        logger.info("not need to check current relative directory!")
    else:
        create_dir_if_not_exist(parent_dir)


def generate_cell_mask_file(
    cellbin_file: str,
    output_image_file: str,
    ignore_when_exist: bool = False,
    fill_value: int = 255,
    compress_level: int = 6
) -> bool:
    """
    Args:
        cellbin_file:str,the input cell bin data file,if not exist,just raise exception!
        output_image_file:the output file of image
        fill_value:the fill pixel,default is 255,if zero,give warning!
    """
    if not os.path.exists(cellbin_file):
        error_string = "the given cellbin file {} is not exist,please check it!".format(cellbin_file)
        logger.error(error_string)
        return False

    if os.path.exists(output_image_file):
        logger.info("the image file {} is already exist!".format(output_image_file))
        if not ignore_when_exist:
            logger.info("not specify ignore it,so nothing to do!")
            return False
    else:
        # check whether the dir is valid!
        check_write_file(output_image_file)

    # check the fill value!
    min_pixel_value: int = 0
    max_pixel_value: int = 255
    if fill_value < min_pixel_value or max_pixel_value > 255:
        error_string = "the fill value is out of range,for 8bit image,the valid pixel range is [{},{}],but get {}".format(
            min_pixel_value, max_pixel_value, fill_value
        )
        logger.error(error_string)
        return False
    legacy_border_padding_value: int = 0
    border_padding_value: int = 32767

    with h5py.File(cellbin_file, mode="r", locking=False) as f:
        try:
            cell_border_path = "cellBin/cellBorder"
            cell_dataset_path = "cellBin/cell"
            cell_border_dataset = f[cell_border_path]
            cell_dataset = f[cell_dataset_path]
        except Exception as ex:
            error_string = "fail to get cell border/cell dataset caused by {}".format(str(ex))
            logger.error(error_string)
            return False

        # try to got the rect
        try:
            xmin = f.attrs["offsetX"][0]
            ymin = f.attrs["offsety"][0]
            xmax = f.attrs["maxX"][0]
            ymax = f.attrs["maxY"][0]
        except Exception as ex:
            logger.error("can not fetch rect from attrs with error {}...".format(str(ex)))
            return False

        cell_border_mat = cell_border_dataset[:]
        cell_center_xs = cell_dataset["x"]
        cell_center_ys = cell_dataset["y"]

    if xmin > xmax or ymin > ymax:
        logger.error("the range is invalid,while xmin={} xmax={} ymin={} ymax={}".format(xmin, xmax, ymin, ymax))
        return False

    height: int = ymax - ymin + 1
    width: int = xmax - xmin + 1
    cell_polygons = []

    cell_num, vertext_num, vertext_coor_num = cell_border_mat.shape
    if (vertext_coor_num) != 2:
        logger.error("the vertext of cell should be 2d,but get cell shape {}".format(cell_border_mat.shape))
        return False

    logger.info("we will generate cell mask with num {}".format(cell_num))
    if (len(cell_center_xs) != cell_num):
        logger.error(
            "the cell center num {} not equal to cell num {} which is invalid!".format(len(cell_center_xs), cell_num),
        )
        return False

    # got the padding mask
    valid_vertex_mask = (cell_border_mat != legacy_border_padding_value & cell_border_mat != border_padding_value)
    valid_vertex_mask = np.all(valid_vertex_mask, axis=2)

    for i in range(cell_num):
        polygon = cell_border_dataset[i][valid_vertex_mask[i]].astype(np.int32)
        polygon[:, 0] += cell_center_xs[i]
        polygon[:, 1] += cell_center_ys[i]
        cell_polygons.append(polygon)

    cell_image_mask = np.zeros(shape=(height, width), dtype=np.uint8)
    cv2.fillPoly(cell_image_mask, cell_polygons, fill_value)
    zlib_compress_args = {"level": compress_level}
    tiff.imwrite(
        output_image_file, cell_image_mask, compression="zlib", compressionargs=zlib_compress_args, bigtiff=True
    )


# define a simple func to get the file kind!
def get_gene_file_kind_with_path(file_path: str) -> GefFileKind:
    if h5py.is_hdf5(file_path):
        with h5py.File(file_path) as f:
            if "cellBin" in f:
                return GefFileKind.CgefKind
            elif "geneExp" in f:
                return GefFileKind.BgefKind
    return GefFileKind.Unknown


class ContourInfo(object):
    # contains two attr,label and coordinate,the coordinae should have n x 2 ...
    def __init__(self, contour_label: str, contour_coordinates: List[np.ndarray]) -> None:
        self.contour_label = contour_label
        self.contour_coordinates = contour_coordinates

    def __str__(self):
        return "label:{} coors:{}".format(self.contour_label, self.contour_coordinates)

    def __repr__(self) -> str:
        return self.__str__()


class CoordinateRange(object):
    # x1,y1,x2,y2
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def is_valid(self) -> bool:
        for v in [self.x1, self.y1, self.x2, self.y2]:
            if not isinstance(v, int):
                return False

        if self.x1 < 0 or self.y1 < 0:
            return False

        if self.x1 > self.x2 or self.y1 > self.y2:
            return False

        return True

    def get_height(self) -> int:
        return self.y2 - self.y1

    def get_width(self) -> int:
        return self.x2 - self.x1

    def __str__(self):
        return "CoorRange x1:{} y1:{} x2:{} y2:{}".format(self.x1, self.y1, self.x2, self.y2)

    def __repr__(self) -> str:
        return self.__str__()


def interval_binary_search_impl(search_intervals: Sequence[int], search_value: int) -> int:
    """
    Args:
        search_intervals:a sequence conteains the intervals of search values
            if we have 4 intervals,the size of search intervals should be 5,contain the last!
        search_value:int,the flat search value
    """
    n = len(search_intervals)
    left: int = 0
    # the right is require of end
    right: int = n - 1
    ret: int = -1
    while left < right:
        middle: int = (left + right) // 2
        # if value in this interval
        if search_intervals[middle] <= search_value and search_intervals[middle + 1] > search_value:
            # find it!
            ret = middle
            break
        # left of the interval
        elif search_intervals[middle] > search_value:
            right = middle
        else:
            # right of the interval
            left = middle + 1
    return ret


def parse_contours(contour_json_file: str = None) -> List[ContourInfo]:
    """
    parse the xxx.json of contours from map
    """
    ret = []
    if not os.path.exists(contour_json_file):
        error_string = "contour file {} is not exist!".format(contour_json_file)
    with open(contour_json_file, "r", encoding="utf-8") as f:
        try:
            data_dict: Dict[str, Any] = json.load(f)
            contour_infos = data_dict["geometries"]
            n = len(contour_infos)
            if n == 0:
                error_string = "the contour info is empty which is invalid!"
                logger.error(error_string)
                raise ValueError(error_string)
            for i in range(n):
                properties: Dict[str, Any] = contour_infos[i]["properties"]
                label_key = "label"
                uid_key = "uID"
                if label_key in properties:
                    label_str = str(properties[label_key])
                elif uid_key in properties:
                    label_str = str(properties[uid_key] + 1)
                else:
                    error_string = "you must speicfy a label with key {} or {},but we not find".format(
                        label_key, uid_key
                    )
                    logger.error(error_string)
                    raise ValueError(error_string)
                coordinates = contour_infos[i]["coordinates"]
                contours = len(coordinates)
                if contours == 0:
                    error_string = "the contour coordinates is invalid"
                    logger.error(error_string)
                    raise ValueError(error_string)
                contour_arrays = []
                for j in range(contours):
                    contour_arrays.append(np.array(coordinates[j], dtype=np.int32))
                ret.append(ContourInfo(contour_label=label_str, contour_coordinates=contour_arrays))
        # maybe got KeyError of it!
        except Exception as ex:
            error_string = "can not got the contours info with {}".format(str(ex))
            logger.error(error_string)
            raise RuntimeError from ex
    return ret


def generate_gene_compressed_csv_file(
    gene_file: str,
    output_csv_file: str,
    bin_size: int = 1,
    sep: str = "\t",
    compress_level: int = 6,
    batch_size: int = 65536,
    coor_range: CoordinateRange = None,
    sample_id: str = "",
    omics: str = "",
) -> None:
    """
    Args:
        gene_file:a str of input gene file
        output_csv_file:str,the output file,should be endswith gz to be recognized by others
        bin_size:int,which dataset we read
        sep:str,default is \t
        compress_level:int,the level used by zlib
        batch_size:int,used for expression,to reduce memory usage,for large chip,this is very useful!
    """
    if not coor_range:
        raise ValueError("coor range can not be empty")
    # the legacy gene dataset have gene offset count 3 columns
    LEGACY_GENE_DATASET_COLUMNS: int = 3

    # current gene dataset have gene_id,gene_name,offset,count 4 columns
    GENE_DATASET_COLUMNS: int = 4

    if not os.path.exists(gene_file):
        raise FileNotFoundError("gene file:{} is not exist!".format(gene_file))
    check_write_file(output_csv_file)

    # if output file name endswith gz and the compress level is not zero,
    if not output_csv_file.endswith("gz") and compress_level != 0:
        logger.warning(
            "we will write a compressed content to file,but file {} can not be recognized by others...".
            format(output_csv_file)
        )

    if output_csv_file.endswith("gz") and compress_level == 0:
        logger.warning(
            "the output file {} is not endswith gz,but you specify compress level = 0,this is not correct!".
            format(output_csv_file)
        )

    logger.info("generate csv file {} with file {}".format(output_csv_file, gene_file))
    gene_dataset_path = "geneExp/bin{}/gene".format(bin_size)
    expression_dataset_path = "geneExp/bin{}/expression".format(bin_size)
    # maybe have
    exon_dataset_path = "geneExp/bin{}/exon".format(bin_size)
    logger.info("we will use {} and {} dataset".format(gene_dataset_path, expression_dataset_path))

    f = h5py.File(gene_file, "r")
    gene_dataset = f[gene_dataset_path]
    expression_dataset = f[expression_dataset_path]
    exon_dataset = None
    if exon_dataset_path in f:
        logger.info("current file have exon dataset")
        exon_dataset = f[exon_dataset_path]
    gene_num = len(gene_dataset)
    expression_num = len(expression_dataset)
    logger.info("gene num:{} expression num:{}".format(gene_num, expression_num))

    # got the gene datas,usually,the gene data is not very large!
    gene_datas = gene_dataset[:]
    gene_dtype = gene_datas.dtype
    # check whether the columns is 4
    gene_columns: int = len(gene_dtype)
    # for legacy data
    if gene_columns == LEGACY_GENE_DATASET_COLUMNS:
        logger.info("the column of gene dataset is 3,trait as legacy gene data")
        # for legacy,only have gene names
        gene_ids = [item.decode() for item in gene_dataset["gene"]]
        gene_counts = [int(item) for item in gene_dataset["count"]]
        search_intervals = [0 for _ in range(gene_num)]
    elif gene_columns == GENE_DATASET_COLUMNS:
        logger.info("the column of gene dataset is 4,trait as current gene datas")
        gene_ids = [item.decode() for item in gene_dataset["geneID"]]
        gene_names = [item.decode() for item in gene_dataset["geneName"]]
        gene_counts = [int(item) for item in gene_dataset["count"]]
        search_intervals = [0 for _ in range(gene_num)]
        search_intervals[:gene_num] = [int(item) for item in gene_dataset["offset"]]
    else:
        error_string = "the column of gene dataset should be 3/4,but got {}".format(gene_columns)
        logger.error(error_string)
        raise ValueError(error_string)

    # the gene is small,so we can write it!
    batches = (expression_num + batch_size - 1) // batch_size

    expression_dtype = expression_dataset.dtype
    # define a buffer
    batch_expression = np.empty(shape=(batch_size, ), dtype=expression_dtype)

    exon_dtype = exon_dataset.dtype
    if exon_dataset is not None:
        batch_exon = np.empty(shape=(batch_size), dtype=exon_dtype)
        logger.info("allocate buffer for exon")

    if gene_columns == GENE_DATASET_COLUMNS:
        if exon_dataset is not None:
            column_names = ["geneID", "geneName", "x", "y", "MIDCount", "ExonCount"]
        else:
            column_names = ["geneID", "geneName", "x", "y", "MIDCount"]
    else:
        if exon_dataset is not None:
            column_names = ["geneID", "x", "y", "MIDCount", "ExonCount"]
        else:
            column_names = ["geneID", "x", "y", "MIDCount"]

    # write the head info of csv
    logger.info("add the head infos")
    if gene_columns == GENE_DATASET_COLUMNS:
        gem_header_info = "#FileFormat=GEMv0.2\n#SortedBy=None\n#BinType=Bin\n#BinSize={}\n#Omics={}\n#Stereo-seqChip={}\n#OffsetX={}\n#OffsetY={}\n".format(
            bin_size, omics, sample_id, coor_range.x1, coor_range.y1
        )
    else:
        gem_header_info = "#FileFormat=GEMv0.1\n#SortedBy=None\n#BinType=Bin\n#BinSize={}\n#Omics={}\n#Stereo-seqChip={}\n#OffsetX={}\n#OffsetY={}\n".format(
            bin_size, omics, sample_id, coor_range.x1, coor_range.y1
        )

    writer = gzip.open(output_csv_file, "wb", compresslevel=compress_level)
    writer.write(gem_header_info.encode())
    column_names = sep.join(column_names) + "\n"
    writer.write(column_names.encode())
    writer.close()

    # the compress args for df to csv!
    compress_args = {
        "method": "gzip",
        "compresslevel": compress_level,
    }
    logger.info("the compress args is {}".format(compress_args))

    left_search_gene_index = 0
    right_search_gene_index = 0

    # the first flat gene to process
    first_flat_gene_size: int = 0

    # the last flat gene to process
    last_flat_gene_size: int = 0
    # create the placeholder,to reuse the memory,and support slice assign!
    batch_flat_gene_ids = np.empty(shape=(batch_size, ), dtype=object)
    if gene_columns == GENE_DATASET_COLUMNS:
        batch_flat_gene_names = np.empty(shape=(batch_size, ), dtype=object)
    for i in range(batches - 1):
        # compute the range
        exp_left: int = i * batch_size
        exp_right: int = (i + 1) * batch_size
        expression_dataset.read_direct(batch_expression, source_sel=range(exp_left, exp_right))
        if exon_dataset is not None:
            exon_dataset.read_direct(batch_exon, source_sel=range(exp_left, exp_right))

        # find the last gene index
        right_search_gene_index = interval_binary_search_impl(search_intervals=search_intervals, search_value=exp_right)
        flat_gene_left: int = 0

        if gene_columns == GENE_DATASET_COLUMNS:
            if first_flat_gene_size > 0:
                batch_flat_gene_ids[:first_flat_gene_size] = gene_ids[left_search_gene_index]
                batch_flat_gene_names[:first_flat_gene_size] = gene_names[left_search_gene_index]
                flat_gene_left += first_flat_gene_size
                left_search_gene_index += 1

            for gene_index in range(left_search_gene_index, right_search_gene_index - 1):
                flat_gene_size: int = gene_counts[gene_index]
                flat_gene_right: int = flat_gene_left + flat_gene_size
                batch_flat_gene_ids[flat_gene_left:flat_gene_right] = gene_ids[gene_index]
                batch_flat_gene_names[flat_gene_left:flat_gene_right] = gene_names[gene_index]
                flat_gene_left = flat_gene_right

            # append the last flat size
            last_flat_gene_size = exp_right - search_intervals[right_search_gene_index]
            if last_flat_gene_size > 0:
                batch_flat_gene_ids[flat_gene_left:] = gene_ids[right_search_gene_index]
                batch_flat_gene_names[flat_gene_left:] = gene_names[right_search_gene_index]

            # update the remain size for next batch
            first_flat_gene_size = search_intervals[right_search_gene_index + 1] - exp_right

            # only need to search once!
            left_search_gene_index = right_search_gene_index

            if exon_dataset is not None:
                data_dict = {
                    "gene_id": batch_flat_gene_ids,
                    "gene_name": batch_flat_gene_names,
                    "x": batch_expression["x"],
                    "y": batch_expression["y"],
                    "count": batch_expression["count"],
                    "exon": batch_exon
                }
            else:
                data_dict = {
                    "gene_id": batch_flat_gene_ids,
                    "gene_name": batch_flat_gene_names,
                    "x": batch_expression["x"],
                    "y": batch_expression["y"],
                    "count": batch_expression["count"],
                }
        else:
            if first_flat_gene_size > 0:
                batch_flat_gene_ids[:first_flat_gene_size]
                flat_gene_left += first_flat_gene_size
                left_search_gene_index += 1

            # maybe process the last!
            for gene_index in range(left_search_gene_index, right_search_gene_index - 1):
                flat_gene_size: int = gene_counts[gene_index]
                flat_gene_right: int = flat_gene_left + flat_gene_size
                batch_flat_gene_ids[flat_gene_left:flat_gene_right] = gene_ids[gene_index]
                flat_gene_left = flat_gene_right

            # append the last flat size
            last_flat_gene_size = exp_right - search_intervals[right_search_gene_index]
            if last_flat_gene_size > 0:
                batch_flat_gene_ids[flat_gene_left:] = gene_ids[right_search_gene_index]
                batch_flat_gene_names[flat_gene_left:] = gene_names[right_search_gene_index]

            first_flat_gene_size = search_intervals[right_search_gene_index + 1] - exp_right

            # only need to search once!
            left_search_gene_index = right_search_gene_index

            if exon_dataset is not None:
                data_dict = {
                    "gene_id": batch_flat_gene_ids,
                    "x": batch_expression["x"],
                    "y": batch_expression["y"],
                    "count": batch_expression["count"],
                    "exon": batch_exon
                }
            else:
                data_dict = {
                    "gene_id": batch_flat_gene_ids,
                    "x": batch_expression["x"],
                    "y": batch_expression["y"],
                    "count": batch_expression["count"],
                }

        df = pd.DataFrame(data_dict)
        df.to_csv(output_csv_file, sep=sep, mode="a", compression=compress_args, header=False, index=False)
        logger.info("finish write compressed csv of {}/{}".format(i + 1, batches))

    # to last
    last_remain_size = expression_num - (batches - 1) * batch_size
    batch_expression = batch_expression[:last_remain_size]
    # loading...
    expression_dataset.read_direct(batch_expression, range((batches - 1) * batch_size, expression_num))
    if exon_dataset is not None:
        batch_exon = batch_exon[:last_remain_size]
        exon_dataset.read_direct(batch_exon, range((batches - 1) * batch_size, expression_num))

    flat_gene_left = 0
    if gene_columns == GENE_DATASET_COLUMNS:
        # this is very import,we need to adjust the index,point to the first!
        if first_flat_gene_size > 0:
            batch_flat_gene_ids[:first_flat_gene_size] = gene_ids[left_search_gene_index]
            batch_flat_gene_names[:first_flat_gene_size] = gene_ids[left_search_gene_index]
            flat_gene_left += first_flat_gene_size
            left_search_gene_index += 1

        for gene_index in range(left_search_gene_index, gene_num):
            flat_gene_size = gene_counts[gene_index]
            flat_gene_right = flat_gene_left + flat_gene_size
            batch_flat_gene_ids[flat_gene_left:flat_gene_right] = gene_ids[gene_index]
            batch_flat_gene_names[flat_gene_left:flat_gene_right] = gene_names[gene_index]
            flat_gene_left = flat_gene_right
        if exon_dataset is not None:
            data_dict = {
                "gene_id": batch_flat_gene_ids[:last_remain_size],
                "gene_name": batch_flat_gene_names[:last_remain_size],
                "x": batch_expression["x"],
                "y": batch_expression["y"],
                "count": batch_expression["count"],
                "exon": batch_exon
            }
        else:
            data_dict = {
                "gene_id": batch_flat_gene_ids[:last_remain_size],
                "gene_name": batch_flat_gene_names[:last_remain_size],
                "x": batch_expression["x"],
                "y": batch_expression["y"],
                "count": batch_expression["count"],
            }
    else:
        # this is very import,we need to adjust the index,point to the first!
        if first_flat_gene_size > 0:
            batch_flat_gene_ids[:first_flat_gene_size] = gene_ids[left_search_gene_index]
            flat_gene_left += first_flat_gene_size
            left_search_gene_index += 1

        for gene_index in range(left_search_gene_index, gene_num):
            flat_gene_size = gene_counts[gene_index]
            flat_gene_right = flat_gene_left + flat_gene_size
            batch_flat_gene_ids[flat_gene_left:flat_gene_right] = gene_ids[gene_index]
            flat_gene_left = flat_gene_right
        if exon_dataset is not None:
            data_dict = {
                "gene_id": batch_flat_gene_ids[:last_remain_size],
                "x": batch_expression["x"],
                "y": batch_expression["y"],
                "count": batch_expression["count"],
                "exon": batch_exon
            }
        else:
            data_dict = {
                "gene_id": batch_flat_gene_ids[:last_remain_size],
                "x": batch_expression["x"],
                "y": batch_expression["y"],
                "count": batch_expression["count"],
            }
    df = pd.DataFrame(data_dict)
    df.to_csv(output_csv_file, sep=sep, mode="a", compression=compress_args, header=False, index=False)
    logger.info("finish write compressed csv of {}/{}".format(batches, batches))


def parse_coor_range_from_bgef_file(gene_file: str) -> CoordinateRange:
    """
    read the height and width from file
    """
    coor_range = None
    try:
        with h5py.File(gene_file, "r") as f:
            exp_dataset_path = "/geneExp/bin1/expression"
            exp_dataset = f[exp_dataset_path]
            xmin = int(exp_dataset.attrs["minX"][0])
            ymin = int(exp_dataset.attrs["minY"][0])
            xmax = int(exp_dataset.attrs["maxX"][0])
            ymax = int(exp_dataset.attrs["maxY"][0])
            coor_range = CoordinateRange(x1=xmin, y1=ymin, x2=xmax, y2=ymax)
    except Exception as ex:
        raise RuntimeError from ex
    return coor_range


class LassoGenerator(object):

    def __init__(
        self,
        sample_id: str,
        input_gene_file: str,
        input_contour_file: str,
        result_dir: str,
        bin_sizes: List[int] = None,
        omics: str = "Transcriptomics",
        compress_level: int = 6,
        image_compress_level: int = 6,
        image_fill_value: int = 255,
        csv_sep: str = None
    ):
        if isinstance(bin_sizes, str):
            logger.warning(
                "the bin sizes {} got str type,we try to convert it to list with int,this is not recommded!".
                format(bin_sizes)
            )
            bin_sizes = convert_bin_size_string(bin_sizes)
        self.sample_id = sample_id
        self.csv_sep = csv_sep

        self._check_is_file_exist(input_gene_file)
        self.input_gene_file = input_gene_file

        self._check_is_file_exist(input_contour_file)
        self.input_contour_file = input_contour_file

        if not os.path.exists(result_dir):
            logger.info("create result dir {}".format(result_dir))
            os.makedirs(result_dir)
        else:
            sub_contents = os.listdir(result_dir)
            if len(sub_contents) > 0:
                warn_string = "the specify result dir {} is not empty".format(result_dir)
                logger.warning(warn_string)

        self.result_dir = result_dir
        self.omics = omics

        if not bin_sizes:
            error_string = "specify bin sizes {} is empty".format(bin_sizes)
            logger.error(error_string)
            raise ValueError(error_string)

        for index, bin_size in enumerate(bin_sizes):
            if not isinstance(bin_size, int):
                try:
                    bin_size = int(bin_size)
                except Exception as ex:
                    error_string = "got unexpected bin size {},and fail to convert it to int,error is {}".format(
                        bin_size, str(ex)
                    )
                    logger.error(error_string)
                    raise ValueError(error_string)
                finally:
                    bin_sizes[index] = bin_size

            if bin_size <= 0:
                error_string = "the bin size should be positive,but get {}".format(bin_size)
                logger.error(error_string)
                raise ValueError(error_string)
            self.bin_sizes = bin_size
        self.bin_sizes = bin_sizes

        if image_fill_value <= 0 or image_fill_value > 255:
            error_string = "specify fill value {} is not valid for 8bit image...".format(image_fill_value)
            logger.error(error_string)
            raise ValueError(error_string)
        self.image_fill_value = image_fill_value

        for _compress_level in [compress_level, image_compress_level]:
            if _compress_level < ZlibCompressLevel.Z_BEST_SPEED or _compress_level > ZlibCompressLevel.Z_BEST_COMPRESSION:
                error_string = "{} got unexpected compress level with zlib alg...".format(_compress_level)
                logger.error(error_string)
                raise ValueError(error_string)

        self.compress_level = compress_level
        self.image_compress_level = image_compress_level

    @staticmethod
    def _check_is_file_exist(file: str) -> None:
        if not os.path.exists(file):
            error_string = "file '{}' is not exist".format(file)
            logger.error(error_string)
            raise FileNotFoundError(error_string)

    def bgef_lasso_generate_with_contour_impl(self) -> bool:
        contour_infos = parse_contours(self.input_contour_file)
        if len(contour_infos) == 0:
            return False
        coor_range = parse_coor_range_from_bgef_file(self.input_gene_file)
        if not coor_range.is_valid():
            error_string = "the coordinate {}  is invalid".format(coor_range)
            logger.error(error_string)
            raise ValueError(error_string)
        height: int = coor_range.get_height()
        width: int = coor_range.get_width()

        for contour_info in contour_infos:
            label: str = contour_info.contour_label
            contours: List[np.ndarray] = contour_info.contour_coordinates

            # save the lasso bgef file
            lasso_label_dir = os.path.join(self.result_dir, label)
            create_dir_if_not_exist(lasso_label_dir)

            # save the csv and tiff file
            lasso_mask_result_dir = os.path.join(lasso_label_dir, "segmentation")
            create_dir_if_not_exist(lasso_mask_result_dir)

            if self.omics == "Transcriptomics":
                logger.info("generate lasso bgef for transcriptomics")
                output_file_name = "{}.{}.label.gef".format(self.sample_id, label)
            else:
                logger.info("generate for protein")
                output_file_name = "{}.{}.protein.label.gef".format(self.sample_id, label)

            output_file_path = os.path.join(lasso_label_dir, output_file_name)

            # convert param to flat
            flat_contours = []
            for contour in contours:
                flat_contours.append(contour.reshape(-1).tolist())

            # invoke cpp
            logger.info("generate bgef file with specify contours")
            _c_lasso_generator = CgefAdjust()
            generate_ok: bool = _c_lasso_generator.generate_region_bgef(
                self.input_gene_file, output_file_path, flat_contours, self.bin_sizes
            )

            if not generate_ok:
                logger.error("fail to generate bgef lasso file with cpp")
                return False
            logger.info("generate image of contour")

            fill_mask: np.ndarray = np.zeros(shape=(height, width), dtype=np.uint8)
            cv2.fillPoly(fill_mask, contours, self.image_fill_value)
            output_image_file = os.path.join(
                lasso_mask_result_dir, "{}.lasso.{}.mask.tif".format(self.sample_id, label)
            )
            tiff_zlib_compress_args = {"level": self.image_compress_level}
            tiff.imwrite(
                output_image_file, fill_mask, compression="zlib", compressionargs=tiff_zlib_compress_args, bigtiff=True
            )

            # generate csv file from hdf5!
            for bin_size in self.bin_sizes:
                output_csv_file = os.path.join(
                    lasso_mask_result_dir, "{}.lasso.bin{}.{}.gem.gz".format(self.sample_id, bin_size, label)
                )
                logger.info("generate csv {}".format(output_csv_file))
                generate_gene_compressed_csv_file(
                    gene_file=output_file_path,
                    output_csv_file=output_csv_file,
                    bin_size=bin_size,
                    sep=self.csv_sep,
                    compress_level=self.compress_level,
                    coor_range=coor_range,
                    sample_id=self.sample_id,
                    omics=self.omics,
                    batch_size=655360
                )
        return True

    def cgef_lasso_generate_with_contour_impl(self) -> bool:
        conotur_infos = parse_contours(self.input_gene_file)
        for contour_info in conotur_infos:
            label: str = contour_info.contour_label
            contours: List[np.ndarray] = contour_info.contour_coordinates

            lasso_label_dir = os.path.join(self.result_dir, label)
            create_dir_if_not_exist(lasso_label_dir)
            if self.omics == "Transcriptomics":
                output_file_name = "{}.{}.label.cellbin.gef".format(self.sample_id, label)
            else:
                output_file_name = "{}.{}.protein.label.cellbin.gef".format(self.sample_id, label)
            output_file_path = os.path.join(lasso_label_dir, output_file_name)

            flat_contours = []
            for contour in contours:
                flat_contours.append(contour.reshape(-1).tolist())

            _c_lasso_generator = CgefAdjust()
            generate_ok: bool = _c_lasso_generator.generate_region_cgef(
                self.input_gene_file, output_file_path, flat_contours
            )

            if not generate_ok:
                logger.error("fail to generate the lasso cellbin gef file")
                return False
            logger.info("try to generate cell mask!")
            output_image_file = os.path.join(
                lasso_label_dir, "{}.lasso.cellbin.{}.mask.tif".format(self.sample_id, label)
            )
            generate_cell_mask_file(
                cellbin_file=self.input_gene_file,
                output_image_file=output_image_file,
                ignore_when_exist=False,
                fill_value=self.image_fill_value,
                compress_level=self.image_compress_level
            )

        return True

    def lasso_generate_with_contour_impl(self) -> bool:
        file_kind: GefFileKind = get_gene_file_kind_with_path(self.input_gene_file)
        if file_kind == GefFileKind.BgefKind:
            logger.info("geneate lasso file with bgef kind...")
            self.bgef_lasso_generate_with_contour_impl()
        elif file_kind == GefFileKind.CgefKind:
            logger.info("generate lasso file with cgef kind...")
            self.cgef_lasso_generate_with_contour_impl()
        else:
            error_string = "sorry,not support file kind {}".format(file_kind)
            logger.error(error_string)
            return False
        return True

    def lasso_generate_with_contour(self) -> bool:
        return self.lasso_generate_with_contour_impl()

    def __call__(self) -> bool:
        return self.lasso_generate_with_contour_impl()


# legacy mode
class MaskSegmentation(object):

    def __init__(
        self,
        sample_id: str,
        contour_file: str,
        gene_file: str,
        result_dir: str,
        bin_sizes: List[int],
        omics: str = "Transcriptomics"
    ):
        logger.info(
            "recommend using {} to replace {},this class is only used for legacy!".format(
                LassoGenerator.__name__, MaskSegmentation.__name__
            )
        )
        logger.info("the compress level set to 6 and fill value set to 255")
        self.impl = LassoGenerator(
            sample_id=sample_id,
            input_gene_file=gene_file,
            input_contour_file=contour_file,
            result_dir=result_dir,
            bin_sizes=bin_sizes,
            omics=omics,
            compress_level=6,
            image_compress_level=6,
            image_fill_value=255
        )

    def run_cellMask(self) -> bool:
        ret: bool = self.impl.lasso_generate_with_contour_impl()
        return ret


def test_lasso_generator():
    sample_id = "lazydog"
    input_gene_file = "/home/lazydog/workspace/bgi_datas/gene_datas/bgef/C04144D5/C04144D5.raw.gef"
    contour_file = "/home/lazydog/workspace/bgi_datas/gene_datas/bgef/C04144D5/20240813094341.lasso.geojson"
    result_dir = "/home/lazydog/workspace/bgi_datas/gene_datas/bgef/C04144D5"
    bin_sizes = "1,20,50"
    # runner = LassoGenerator(
    #     sample_id=sample_id,
    #     input_gene_file=input_gene_file,
    #     input_contour_file=contour_file,
    #     result_dir=result_dir,
    #     compress_level=6,
    #     image_compress_level=6,
    #     image_fill_value=255,
    #     bin_sizes=[1, 20, 50]
    # )
    runner = MaskSegmentation(
        sample_id=sample_id,
        contour_file=contour_file,
        gene_file=input_gene_file,
        result_dir=result_dir,
        bin_sizes=bin_sizes
    )
    runner.run_cellMask()


if __name__ == "__main__":
    logger = generate_logger("fish")
    logger.info("today is Friday!")
    logger.info("the brownfox jumps over the lazydog!")
    logger.error("fly....")

    file_kind: GefFileKind = GefFileKind.BgefKind
    logger.info("current file is {}".format(file_kind))

    test_lasso_generator()
