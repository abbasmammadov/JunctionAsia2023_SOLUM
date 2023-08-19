def xywh2xyxy(box):
    x1 = box[0] - box[2]/2
    y1 = box[1] - box[3]/2
    x2 = box[0] + box[2]/2
    y2 = box[1] + box[3]/2

    return [x1, y1, x2, y2]

def calculate_iou(gt, pred):
    gt = xywh2xyxy(gt)
    pred = xywh2xyxy(pred)

    x_left = max(gt[0], pred[0])
    x_right = min(gt[2], pred[2])
    y_top = max(gt[1], pred[1])
    y_bottom = min(gt[3], pred[3])

    interior = max(0, x_right - x_left) * max(0, y_bottom - y_top)  
    outer = (gt[2] - gt[0]) * (gt[3] - gt[1]) + (pred[2] - pred[0]) * (pred[3] - pred[1]) - interior

    iou = interior / outer

    return iou