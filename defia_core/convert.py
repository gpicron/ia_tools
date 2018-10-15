import json
import os
import os.path as osp

import cv2


def _best_interpol(inputsize, output_size):
    if inputsize[0] > output_size[0] and inputsize[1] > output_size[1]:
        return cv2.INTER_AREA
    else:
        return cv2.INTER_CUBIC


def convert_supervisely_to_yolo(supervisely_project_dir, yolo_outputdir, target_size=None):
    """
    This fonction convert a project in supervisely format to yolo format.
    Actually it is limited to convert supervisely "rectangle" annotations, in other words "bounding bounds".  Meanwhile,
    Supervisely provide a Data Transformation Tool that permits among other to transform any kind of annotation to bounding boxes.
    The function also convert the images to the JPG format and optionally resize the images.

    :param supervisely_project_dir: the project dir in Supervisely format
    :param yolo_outputdir: the target dir that will contains the images and the annotation txt file
    :param target_size: optional parameter if you want to resize the images
    """
    yolo_outputdir = osp.abspath(yolo_outputdir)

    print("Output directory: %s " % yolo_outputdir)

    os.makedirs(yolo_outputdir, exist_ok=True)

    project_dir = osp.abspath(supervisely_project_dir)

    with open(osp.join(project_dir, "meta.json"), "r", encoding="UTF-8") as read_file:
        project_meta = json.load(read_file)

    bb_classes = [cls['title'] for cls in project_meta['classes'] if cls['shape'] == 'rectangle']
    print('Input project meta: {} rectangle class(es). {}'.format(len(bb_classes), bb_classes))

    for dataset in [o for o in os.listdir(project_dir) if osp.isdir(osp.join(project_dir, o))]:
        print("Processing dataset %s..." % dataset)

        ann_path = osp.join(project_dir, dataset, 'ann')
        img_path = osp.join(project_dir, dataset, 'img')

        for img_file in [o for o in os.listdir(img_path)]:

            im = cv2.imread(osp.join(img_path, img_file))

            if im is None:
                print("+++++ Found %s in %s that is not an image. Skip" % (img_file, img_path))
                continue

            base_name = osp.splitext(img_file)[0]
            annot_file = base_name + '.json'

            base_out_name = dataset + "__" + base_name

            with open(osp.join(ann_path, annot_file), "r", encoding="UTF-8") as read_file:
                annotation = json.load(read_file)

            img_width = annotation['size']['width']
            img_height = annotation['size']['width']

            objects = [o for o in annotation['objects'] if o['classTitle'] in bb_classes]

            with open(osp.join(yolo_outputdir, base_out_name + '.txt'), "w", encoding="UTF-8") as yolo_ann:
                for object in objects:
                    classTitle = object['classTitle']
                    clazz = bb_classes.index(classTitle)
                    points = object['points']['exterior']
                    c1_x, c1_y = points[0][0], points[0][1]
                    c2_x, c2_y = points[1][0], points[1][1]

                    pos_x, pos_y = (c1_x + c2_x) / 2 / img_width, (c1_y + c2_y) / 2 / img_height
                    w, h = abs(c1_x - c2_x) / img_width, abs(c1_y - c2_y) / img_height

                    yolo_ann.write("%s %s %s %s %s\n" % (clazz, pos_x, pos_y, w, h))

            if target_size is not None:
                im = cv2.resize(im, target_size, interpolation=_best_interpol((img_width, img_height), target_size))

            cv2.imwrite(osp.join(yolo_outputdir, base_out_name + '.jpg'), im)

# TODO
# def convert_yolo_to_supervisely(yolo_dir, yolo_names_file, supervisely_project_outputdir, yolo_ann_dir=None, datasetname=None, target_size=None):
#     if datasetname is None:
#         datasetname = osp.basename(yolo_dir)
#
#     if yolo_ann_dir is None:
#         yolo_ann_dir = yolo_dir
#
#     supervisely_project_outputdir = osp.abspath(supervisely_project_outputdir)
#
#     os.makedirs(supervisely_project_outputdir, exist_ok=True)
#
#     # read labels
#     with open(yolo_names_file, "r", encoding="UTF-8") as yolo_labels:
#
#
#     for img_file in [o for o in os.listdir(yolo_dir)]:
#         im = cv2.imread(osp.join(yolo_dir, img_file))
#
#         # try loading to know if it is an image
#         if im is None:
#             continue
#
#         base_name = osp.splitext(img_file)[0]
#         annot_file = osp.join(yolo_ann_dir, base_name + '.txt')
#
#         with open(annot_file, "r", encoding="UTF-8") as yolo_ann:
