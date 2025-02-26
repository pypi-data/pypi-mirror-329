from typing import Tuple

import cv2
import torch


def draw_gravity_points(image: torch.Tensor,
                        annotation: torch.Tensor,
                        gravity_points: torch.Tensor,
                        output_path: str,
                        gravity_points_color: Tuple[int, int, int] = (0, 255, 255),
                        annotation_color: Tuple[int, int, int] = (0, 0, 255)):
    """
    Draw gravity points configuration on image and save

    :param image: image
    :param annotation: annotation
    :param gravity_points: gravity points
    :param output_path: path to save
    :param gravity_points_color: color of gravity points (default: yellow)
    :param annotation_color: color of annotation (default: red)
    """

    # delete ground truth padding
    annotation = annotation[annotation[:, 0] != -1]  # delete padding

    # draw each gravity points
    for gp in gravity_points:
        coord_x = int(gp[0])  # x
        coord_y = int(gp[1])  # y

        # draw gravity point (x, y)
        cv2.circle(image, (coord_x, coord_y), radius=0, color=gravity_points_color, thickness=1)

    for annotation in annotation:
        x = int(annotation[0].item())
        y = int(annotation[1].item())

        cv2.circle(image, (x, y), radius=0, color=annotation_color, thickness=1)

    # save image
    cv2.imwrite(output_path, image)
