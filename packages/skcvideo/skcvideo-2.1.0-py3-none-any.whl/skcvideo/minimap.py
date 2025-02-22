import cv2
import numpy as np

from skcvideo.colors import WHITE
from skcvideo.field_model import create_field_objects
from skcvideo.utils import put_text

FIELD_COLOR = (65, 165, 113)


class Minimap:
    def __init__(self, box=None, pitch_length=105.0, pitch_width=68.0):
        if box is None:
            box = [200, 57, 740, 57 + 796]
        self.box = box
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width

        self.xc, self.yc = (self.box[1] + self.box[3]) / 2.0, (self.box[0] + self.box[2]) / 2.0
        self.w, self.h = self.box[3] - self.box[1], self.box[2] - self.box[0]
        self.pixel_per_meter = 5.0 * min(float(self.h) / 390.0, float(self.w) / 575.0)

    def build(self, image):
        field_objects = create_field_objects(
            pitch_length=self.pitch_length,
            pitch_width=self.pitch_width,
        )

        # Generate an inliers mask that is the size of the minimap
        self.inliers_mask = np.zeros((self.box[2] - self.box[0], self.box[3] - self.box[1], 3), dtype=np.uint8)
        xc, yc = (self.box[3] - self.box[1]) / 2.0, (self.box[2] - self.box[0]) / 2.0  # Lines centered on the mask

        # Draw the field lines on the inliers mask
        for _name, field_object in field_objects.items():
            if field_object["type"] == "line":
                start_x, start_y = self.switch_coords_meter_to_minimap(*field_object["start_point"], xc=xc, yc=yc)
                end_x, end_y = self.switch_coords_meter_to_minimap(*field_object["end_point"], xc=xc, yc=yc)
                cv2.line(
                    img=self.inliers_mask,
                    pt1=(start_x, start_y),
                    pt2=(end_x, end_y),
                    color=WHITE,
                    thickness=2,
                )
            elif field_object["type"] == "circle":
                x, y = self.switch_coords_meter_to_minimap(
                    field_object["x"],
                    field_object["y"],
                    xc=xc,
                    yc=yc,
                )
                radius = int(np.round(self.pixel_per_meter * field_object["radius"]))
                startAngle = int(np.round(180.0 * field_object["startAngle"] / np.pi))
                endAngle = int(np.round(180.0 * field_object["endAngle"] / np.pi))

                cv2.ellipse(
                    img=self.inliers_mask,
                    center=(x, y),
                    axes=(radius, radius),
                    angle=0,
                    startAngle=startAngle,
                    endAngle=endAngle,
                    color=WHITE,
                    thickness=2,
                )

        # Fill the area of the background corresponding to the field with the field color
        field_color_mask = np.array(FIELD_COLOR, dtype=np.uint8)[np.newaxis, np.newaxis, :]
        image[self.box[0] : self.box[2], self.box[1] : self.box[3]] = field_color_mask

        # Draw the field lines on the area of the background corresponding to the field
        white_mask = np.array(WHITE, dtype=np.uint8)[np.newaxis, np.newaxis, :]
        image[self.box[0] : self.box[2], self.box[1] : self.box[3]][self.inliers_mask[:, :, 0] != 0] = white_mask

    def switch_coords_meter_to_minimap(self, x, y, xc=None, yc=None):
        if xc is None:
            xc = self.xc
        if yc is None:
            yc = self.yc
        x_to_disp = np.round(x * self.pixel_per_meter + xc)
        y_to_disp = np.round(-y * self.pixel_per_meter + yc)
        x_to_disp, y_to_disp = map(int, [x_to_disp, y_to_disp])
        return x_to_disp, y_to_disp

    def refresh(self, image, data, info_mapping=lambda d: d):
        """
        info_mapping: a function taking d and returning a dict containing:
            {
                'x': float,
                'y': float,
                'radius': int,
                'color': (int, int, int),
                'second_color': (int, int, int),
                'text': str or None,
                'text_color': (int, int, int) or None,
            }
        """
        for d in data:
            info = info_mapping(d)
            x, y = self.switch_coords_meter_to_minimap(info["x"], info["y"])
            cv2.circle(image, (x, y), info["radius"], info["color"], thickness=-1)
            cv2.circle(image, (x, y), info["radius"], info["second_color"], thickness=1)
            if info["text"] is not None:
                put_text(
                    img=image,
                    text=info["text"],
                    org=(x, y),
                    fontScale=0.4,
                    color=info["text_color"],
                    align_x="center",
                    align_y="center",
                )
