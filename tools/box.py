import numpy as np


def match_box(faces, heads):
    # TODO: match head & face
    return heads


def group_point(points):
    x = points[0]
    y = points[1]
    # TODO: group points
    return 0


def get_distance(pos_box, up_idx_list, in_idx_list):
    pos_2d_bottom = pos_box[:, :2][:5]
    pos_2d_top = pos_box[:, :2][5:]
    b_center = lambda idx: 0.5 * (pos_2d_bottom[idx] + pos_2d_bottom[idx + 1])
    t_center = lambda idx: 0.5 * (pos_2d_top[idx] + pos_2d_top[idx + 1])
    dis = lambda array1, array2: np.sqrt((array1[0] - array2[0]) ** 2 + (array1[1] - array2[1]) ** 2)
    upside_dis_list = []
    inside_dis_list = []
    if len(up_idx_list):
        for idx in up_idx_list:
            upside_dis_list.append(dis(b_center(idx), t_center(idx)))

    if len(in_idx_list):
        for idx in in_idx_list:
            inside_dis_list.append(dis(t_center(idx), t_center(idx+2)))
    return upside_dis_list, inside_dis_list


def box_angles(pos_box, turnround_sense=0.5, front_sense=(0.8, 1.2)):
    # TODO: get angles from pos_box
    pos_box = np.array(pos_box)
    upside_dis_list, inside_dis_list = get_distance(pos_box, [0, 2], [0, 1])
    is_front = front_sense[0] < inside_dis_list[0] / inside_dis_list[1] < front_sense[1]
    is_turnround = max(upside_dis_list) > (1.5-turnround_sense)*85 and not is_front
    return is_turnround, is_front