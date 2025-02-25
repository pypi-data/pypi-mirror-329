import numpy as np
import cv2
import matplotlib.pyplot as plt


def main():
    labs, preds = zip(*[gen_lab_pred_pair(tp=3, fp=1, fn=0) for _ in range(16)])
    ## store to numpy file
    np.savez("exdata.npz", labs=np.array(labs), preds=np.array(preds))

    # imgs = [gen_sar_like_image(lab) for lab in labs]
    # overlap_grid(labs, preds, imgs)


def draw_ellipse(img, position, angle, size):
    """
    Draw an ellipse on the image.
    """
    # Get the ellipse parameters
    x0, y0 = position
    a, b = size
    # Generate the ellipse
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x = i - x0
            y = j - y0
            # Rotate the coordinates
            x_theta = x * np.cos(angle) + y * np.sin(angle)
            y_theta = -x * np.sin(angle) + y * np.cos(angle)
            # Check if the point is inside the ellipse
            if (x_theta / a) ** 2 + (y_theta / b) ** 2 <= 1:
                img[i, j] = 1
    return img


def gen_oil_spill_label(n_spills=3, resolution=256, return_instance_masks=False):
    """
    Generate a synthetic oil spill label image.
    Each spill is an ellipse with random orientation and size.
    The image is a binary image with 1s representing oil spills.
    """
    # Create an empty image
    img = np.zeros((resolution, resolution))
    instance_masks = []
    # Generate random ellipse parameters for each spill
    for _ in range(n_spills):
        position = np.random.randint(0, resolution, 2)
        size = np.random.randint(1, 16, 2)
        angle = np.random.rand() * np.pi
        instance_mask = np.zeros((resolution, resolution))
        instance_mask = draw_ellipse(instance_mask, position, angle, size)
        instance_masks.append(instance_mask)
        img += instance_mask

    # Threshold the image
    img[img > 0] = 1

    if return_instance_masks:
        return img, instance_masks

    return img


def overlap_grid(labs, preds, imgs, title=""):
    """
    Plot each label-prediction-img trio over one another in a grid. Labels and preds are transparent, but with colors according to
    the following rules:
        When both are 1, show in green, when positive in label and negative in prediction, show in red and vice versa in orange.
    The imgs are shown in the background.
    """
    alpha = 0.6
    n = int(np.ceil(np.sqrt(len(labs))))
    fig, axs = plt.subplots(n, n, figsize=(7, 7))
    axs = axs.flatten()
    for i, (lab, pred, img) in enumerate(zip(labs, preds, imgs)):
        ax = axs[i]
        lab = lab.numpy()
        pred = pred.numpy()

        tp = (lab == 1) & (pred >= 0.5)
        fn = (lab == 1) & (pred < 0.5)
        fp = (lab == 0) & (pred > 0.5)

        # background image
        ax.imshow(img, cmap="gray")

        ## transparent overlays
        tp_mask = np.ma.masked_where(~tp, tp).astype(float)
        fn_mask = np.ma.masked_where(~fn, fn).astype(float)
        fp_mask = np.ma.masked_where(~fp, fp).astype(float)

        tp_cmap = plt.get_cmap("Greens").copy()
        tp_cmap.set_bad(alpha=0)
        fn_cmap = plt.get_cmap("Reds").copy()
        fn_cmap.set_bad(alpha=0)
        fp_cmap = plt.get_cmap("Oranges").copy()
        fp_cmap.set_bad(alpha=0)

        ## show tp in transparent green, allowing the background image to fully show elsewhere
        ax.imshow(tp_mask, cmap=tp_cmap, alpha=alpha, vmin=0, vmax=1)
        ## show fn in transparent red
        ax.imshow(fn_mask, cmap=fn_cmap, alpha=alpha, vmin=0, vmax=1)
        ## show fp in transparent orange
        ax.imshow(fp_mask, cmap=fp_cmap, alpha=alpha, vmin=0, vmax=1)

        ax.axis("off")
    for ax in axs:
        ax.axis("off")
    fig.suptitle(title)
    plt.tight_layout()


def show_img(img):
    """
    Display an image.
    """
    import matplotlib.pyplot as plt

    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.show()


def show_img_grid(imgs):
    """
    Display a grid of images.
    """
    import matplotlib.pyplot as plt

    n = int(np.ceil(np.sqrt(len(imgs))))
    fig, axs = plt.subplots(n, n, figsize=(10, 10))
    for i, img in enumerate(imgs):
        ax = axs[i // n, i % n]
        ax.imshow(img, cmap="gray")
        ax.axis("off")
    for ax in axs.flat[i + 1 :]:
        ax.axis("off")
    plt.show()


def gen_sar_like_image(label):
    """
    Generate a synthetic SAR-like image from a binary label image.
    """
    ## assumed distribution of pixel values

    ## Large scale noise
    img = np.random.randn(*label.shape) * 0.4
    img = cv2.GaussianBlur(img, (5, 5), 0)

    ## add oil spill pixels
    img[label == 1] -= np.random.rand(*img[label == 1].shape) * 0.4
    img = cv2.GaussianBlur(img, (15, 15), 0)

    ## Create a background image
    img += np.random.randn(*label.shape) * 0.15
    return img


def gen_lab_pred_pair(
    tp=2, fn=1, fp=1, resolution=256, confidences=None, size_range=(10, 30)
):
    """
    Generate a synthetic label-prediction pair.
    """
    # Generate a label
    lab, instance_masks = gen_oil_spill_label(
        n_spills=tp + fn, return_instance_masks=True, resolution=resolution
    )
    if confidences is None:
        confidences = np.ones(tp + fp)

    pred = np.zeros_like(lab)
    for i, conf in zip(range(tp), confidences[:tp]):
        pred = np.where(instance_masks.pop(), conf, pred)

    for _, conf in zip(range(fp), confidences[tp:]):
        ellipse_mask = np.zeros_like(lab)
        draw_ellipse(
            ellipse_mask,
            np.random.randint(0, lab.shape[0], 2),
            np.random.rand() * np.pi,
            np.random.randint(*size_range, 2),
        )
        pred = np.where(ellipse_mask, conf, pred)

    return pred, lab


if __name__ == "__main__":
    main()
