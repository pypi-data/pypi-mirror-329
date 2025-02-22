import argparse
import csv
import io
import textwrap
from collections.abc import Callable, Sequence
from functools import partial
from pathlib import Path
from typing import Literal, Optional, cast

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
import pymupdf
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.text import Annotation
from matplotlib.transforms import Bbox
from PIL import Image
from tqdm import tqdm
from yaml import safe_load

from ithappens.card import Card
from ithappens.exceptions import ItHappensImageNotFoundError
from ithappens.utils import slugify


def text_with_wrap_autofit(
    ax: plt.Axes,
    txt: str,
    xy_size: tuple[float, float],
    width: float,
    height: float,
    *,
    min_font_size=None,
    bleed: Optional[float] = None,
    pad: Optional[float] = None,
    show_rect: bool = False,
    **kwargs,
):
    """Automatically fits the text to some axes.

    Args:
        ax: axes to put the text on.
        txt: text to display.
        xy: location to place the text.
        width: width of the text box in fractions.
        height: height of the text box in fractions.
        min_font_size: minimum acceptable font size.
        bleed: bleed of the figure.
        pad: padding of the box.
        **kwargs: keyword arguments passed to Axes.annotate.

    Returns:
        text artist.
    """

    #  Different alignments give different bottom left and top right anchors.
    x, y = xy_size
    if bleed is None:
        bleed = 0
    if pad:
        bleed += pad
        x -= 2 * pad
        y -= 2 * pad

    if show_rect:
        alpha = 0.3
    else:
        alpha = 0

    rect = Rectangle(
        (bleed + (1 - width) * x, bleed + (1 - height) * y),
        width * x,
        height * y,
        alpha=alpha,
    )
    ax.add_patch(rect)

    # Get transformation to go from display to data-coordinates.
    inv_data = ax.transData.inverted()

    fig: Figure = ax.get_figure()
    dpi = fig.dpi
    rect_height_inch = rect.get_height() / dpi

    # Initial fontsize according to the height of boxes
    fontsize = rect_height_inch * 72

    wrap_lines = 1
    xy = (bleed + 0.5 * x, bleed + 0.98 * y)
    while True:
        wrapped_txt = "\n".join(
            textwrap.wrap(txt, width=len(txt) // wrap_lines, break_long_words=False)
        )

        # For dramatic effect, place text after ellipsis on newline.
        wrapped_txt = wrapped_txt.replace("... ", "...\n")
        wrapped_txt = wrapped_txt.replace("… ", "...\n")
        text: Annotation = ax.annotate(wrapped_txt, xy, **kwargs)
        text.set_fontsize(fontsize)

        # Adjust the fontsize according to the box size.
        bbox: Bbox = text.get_window_extent()
        inv_text_bbox = inv_data.transform(bbox)
        width_text = inv_text_bbox[1][0] - inv_text_bbox[0][0]
        adjusted_size = fontsize * rect.get_width() / width_text
        if min_font_size is None or adjusted_size >= min_font_size:
            break
        text.remove()
        wrap_lines += 1
    text.set_fontsize(adjusted_size)

    return text


class ithappensArgs(argparse.Namespace):
    input_dir: str
    name: str
    merge: bool
    side: Literal["front", "back", "both"]
    format: Literal["pdf", "png"]
    workers: int
    chunks: int


def df_from_yaml(f):
    return pd.json_normalize(safe_load(f.getvalue()))


def df_from_csv(f):
    data = [row for row in csv.DictReader(f.getvalue().decode("utf-8").splitlines())]
    return pd.json_normalize(data)


def df_from_xlsx(f):
    return pd.read_excel(f)


def construct_df(f):
    for method in [df_from_yaml, df_from_csv, df_from_xlsx]:
        try:
            df = method(f)
            return df
        except Exception:
            pass
    else:
        raise ValueError("Could not parse input file.")


def open_input_file(input_path):
    try:
        with open(input_path, "rb") as f:
            return f
    except TypeError:
        return input_path


def parse_input_file(
    input_path: Path,
    image_dir: Path | None = None,
) -> pd.DataFrame:
    """Parse an input file.

    It must have two colums: descriptions along with their misery index.

    Args:
        intput_path: path of the input file (.csv or .xlsx)

    Returns:
        Pandas DataFrame with index, description, and misery index.
    """
    usecols = ["misery index", "situation", "image"]

    input_bytes = open_input_file(input_path)
    df = construct_df(input_bytes)

    try:
        df = df[usecols]
    except KeyError:
        print(f"Make sure {input_path} has {len(usecols)} columns named {usecols}.")
        exit()

    if image_dir:

        def _make_path(x: str, image_dir: Path) -> Path:
            if x is None:
                return None
            elif Path(x).is_absolute():
                return x
            else:
                return image_dir / x if x else None

        df["image"] = df["image"].apply(lambda x: _make_path(x, image_dir))

    return df


def plot_crop_marks(ax: Axes, bleed: float, factor: float = 0.6):
    """Plots crop marks on the given axis.
    The crop marks will mark the bleed. The crop mark size is adjustable with the factor.
    """
    crop_mark_len = factor * bleed
    fig = ax.get_figure()
    bbox: Bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    x_size, y_size = bbox.width, bbox.height

    # h, v - horizontal, vertical
    # u, d - up, down
    # l, r - left, right
    hul = (y_size - bleed, 0, crop_mark_len)
    hdl = (bleed, 0, crop_mark_len)
    hur = (y_size - bleed, x_size - crop_mark_len, x_size)
    hdr = (bleed, x_size - crop_mark_len, x_size)
    vul = (bleed, y_size - crop_mark_len, y_size)
    vdl = (bleed, 0, crop_mark_len)
    vur = (x_size - bleed, y_size - crop_mark_len, y_size)
    vdr = (x_size - bleed, 0, crop_mark_len)

    cropmarkstyle = {"color": "white", "linewidth": 1}

    for horizontal_mark in [hul, hdl, hur, hdr]:
        ax.hlines(*horizontal_mark, **cropmarkstyle)
    for vertical_mark in [vul, vdl, vur, vdr]:
        ax.vlines(*vertical_mark, **cropmarkstyle)


def plot_card_front(card: Card) -> Figure:
    # To be able to convert between centimeters and inches.
    cm_per_inch = 2.54

    # 62x88 mm for typical playing cards.
    x_size = 6.2 / cm_per_inch  # cm front and back
    y_size = 8.8 / cm_per_inch  # cm top to bottom

    # Add margin on all sides.
    bleed = 0.5 / cm_per_inch  # cm
    pad = 0.15 / cm_per_inch

    # Margin for image.
    image_pad = 0.08 / cm_per_inch

    x_total = x_size + 2 * bleed
    y_total = y_size + 2 * bleed
    xy_size = (x_total, y_total)

    plt.style.use("ithappens")
    fig, ax = plt.subplots()

    fig.set_size_inches(*xy_size)
    fig.set_facecolor("black")
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.axis("off")

    ax.set_xlim(0, x_total)
    ax.set_ylim(0, y_total)

    prop = fm.FontProperties(weight="extra bold")

    text_kwargs = dict(wrap=True, horizontalalignment="center", fontproperties=prop)

    # Front.
    situation_text = text_with_wrap_autofit(
        ax,
        card.desc.upper(),
        (x_size, y_size),
        1,
        0.4,
        **text_kwargs,
        bleed=bleed,
        pad=pad,
        min_font_size=11,
        va="top",
        weight="extra bold",
        color="#ffdc20",
    )

    mi_desc = card.misery_index_desc
    mi_desc_text = ax.text(
        x_total / 2,
        1.2 * y_size / 6 + bleed,
        mi_desc.upper(),
        **text_kwargs,
        color="#ffdc20",
        fontsize=13,
        weight="semibold",
        verticalalignment="center",
    )

    ax.figure.canvas.draw()
    situation_text_bbox = situation_text.get_window_extent()
    situation_text_bbox = ax.transAxes.inverted().transform(situation_text_bbox)
    bottom_situation_text = situation_text_bbox[0][1]

    mi_desc_bbox = mi_desc_text.get_window_extent()
    mi_desc_bbox = ax.transAxes.inverted().transform(mi_desc_bbox)
    top_mi_desc_bbox = mi_desc_bbox[1][1]

    image_height = bottom_situation_text - top_mi_desc_bbox - 2 * image_pad
    if card.image_path is not None:
        try:
            foreground = Image.open(card.image_path).convert("RGBA")
        except FileNotFoundError as e:
            raise ItHappensImageNotFoundError(card.image_path) from e
        image = Image.new("RGBA", foreground.size)
        image = Image.alpha_composite(image, foreground)
        image = image.convert("RGB")
        imageax = ax.inset_axes([0, top_mi_desc_bbox + image_pad, 1, image_height])
        imageax.imshow(image)
        imageax.axis("off")

    ax.text(
        x_total / 2,
        0.07 * y_size + bleed,
        card.misery_index,
        **text_kwargs,
        color="black",
        fontsize=45,
        weight="extra bold",
        verticalalignment="center",
    )

    mi_block = Rectangle(
        (bleed + x_size / 6, 0), 4 * x_size / 6, y_size / 6 + bleed, fc="#ffdc20"
    )
    ax.add_patch(mi_block)

    plot_crop_marks(ax, bleed)

    plt.close(fig)

    return fig


def plot_card_back(card: Card, expansion_logo_path: Path | None = None) -> Figure:
    # To be able to convert between centimeters and inches.
    cm_per_inch = 2.54

    # 62x88 mm for typical playing cards.
    x_size = 6.2 / cm_per_inch  # cm front and back
    y_size = 8.8 / cm_per_inch  # cm top to bottom

    # Add margin on all sides.
    bleed = 0.5 / cm_per_inch  # cm

    x_total = x_size + 2 * bleed
    y_total = y_size + 2 * bleed
    xy_size = (x_total, y_total)

    plt.style.use("ithappens")
    fig, ax = plt.subplots()

    fig.set_size_inches(*xy_size)
    fig.set_facecolor("black")
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.axis("off")

    prop_regular = fm.FontProperties(weight="regular")

    text_kwargs = dict(
        wrap=True, horizontalalignment="center", fontproperties=prop_regular
    )

    game_name = "It Happens"
    expansion_text = "edition"
    expansion_text_full = card.expansion_name + " " + expansion_text

    ax.text(
        x_size / 2 + bleed,
        0.9 * y_size + bleed,
        game_name.upper(),
        **text_kwargs,
        color="#ffdc20",
        fontsize=20,
        weight="regular",
        verticalalignment="center",
    )

    prop_light = fm.FontProperties(weight="regular")

    text_kwargs = dict(
        wrap=True, horizontalalignment="center", fontproperties=prop_light
    )

    ax.text(
        x_size / 2 + bleed,
        0.83 * y_size + bleed,
        expansion_text_full.upper(),
        **text_kwargs,
        color="#ffdc20",
        fontsize=14,
        fontstyle="italic",
        weight="ultralight",
        verticalalignment="center",
    )

    # Expansion logo
    if expansion_logo_path is None:
        parent_dir = Path(__file__).parent.resolve()
        expansion_logo_path = parent_dir / Path("images/expansion-logo.png")

    expansion_logo = Image.open(str(expansion_logo_path)).convert("RGBA")
    background = Image.new("RGBA", expansion_logo.size)
    expansion_logo = Image.alpha_composite(background, expansion_logo).convert("RGB")

    expansion_logoax = fig.add_axes([0.2, 0.1, 0.6, 0.6])
    expansion_logoax.imshow(
        expansion_logo,
    )
    expansion_logoax.axis("off")

    plot_crop_marks(ax, bleed)

    ax.set_xlim(0, x_total)
    ax.set_ylim(0, y_total)

    plt.close(fig)

    return fig


def save_card(
    card: Card,
    output_dir: Path,
    side: Literal["front", "back"],
    dpi: int = 300,
    format: str = "pdf",
) -> None:
    side_fn = "front" if side == "front" else "back"

    output_dir = output_dir / side_fn

    output_dir.mkdir(parents=True, exist_ok=True)

    fn = f"{card.misery_index}-{card.desc}"
    fn = slugify(fn)
    save_fn = (output_dir / fn).with_suffix("." + format)
    savefig_args = {
        "format": format,
        "pad_inches": 0,
        "dpi": dpi,
        "transparent": False,
    }

    if side == "front":
        card.front_save_fn = save_fn
        card.fig_front.savefig(save_fn, **savefig_args)
    elif side == "back":
        card.back_save_fn = save_fn
        card.fig_back.savefig(save_fn, **savefig_args)


def create_card(
    row,
    expansion_name,
    expansion_logo_path,
    output_dir,
    side,
    ext: Literal["pdf", "png"],
    misery_index_desc: str = "misery index",
) -> Card:
    try:
        image = row[1]["image"]
    except KeyError:
        image = None

    misery_index = float(str(row[1]["misery index"]).replace(",", "."))
    card = Card(
        row[1]["situation"],
        misery_index,
        expansion_name,
        image,
        misery_index_desc=misery_index_desc,
    )

    if side in ["front", "both"]:
        card.fig_front = plot_card_front(card)
        save_card(card, output_dir, "front", format=ext)
        card.fig_front = None  # Free up memory

    if side in ["back", "both"]:
        card.fig_back = plot_card_back(card, expansion_logo_path)
        save_card(card, output_dir, "back", format=ext)
        card.fig_back = None  # Free up memory

    return card


def create_cards(
    df: pd.DataFrame,
    expansion_name: str,
    expansion_logo_path: Path,
    output_dir: Path,
    merge: bool,
    side: Literal["front", "back", "both"],
    ext: Literal["pdf", "png"],
    workers: int,
    misery_index_desc: str = "misery_index",
    callbacks: Sequence[Callable] = [],
) -> None:
    nmax = df.shape[0]
    create_card_par = partial(
        create_card,
        expansion_name=expansion_name,
        expansion_logo_path=expansion_logo_path,
        output_dir=output_dir,
        side="front",
        ext=ext,
        misery_index_desc=misery_index_desc,
    )
    desc = "Plotting cards"
    from concurrent.futures import ProcessPoolExecutor, as_completed

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(create_card_par, row) for row in df.iterrows()]
        cards: list[Card] = []
        for future in tqdm(as_completed(futures), total=nmax, desc=desc):
            card = future.result()
            cards.append(card)
            for callback in callbacks:
                callback()

    # Because all the backs are duplicated, create it only once
    # and reference it for the others.
    if side in ["back", "both"]:
        cards[0].fig_back = plot_card_back(card, expansion_logo_path)
        fn = f"{card.misery_index}-{card.desc}"
        fn = slugify(fn)
        cards[0].back_save_fn = (output_dir / fn).with_suffix("." + ext)
        save_card(cards[0], output_dir, "back", format=ext)
        cards[0].fig_back = None
        for card in cards[1:]:
            card.back_save_fn = cards[0].back_save_fn

    if merge:
        if side in ["front", "both"]:
            front_output_dir = output_dir / "front"
            front_output_dir.mkdir(parents=True, exist_ok=True)
            merged_pdf = pymupdf.open()

            for card in cards:
                with pymupdf.open(card.front_save_fn) as front_pdf:
                    merged_pdf.insert_pdf(front_pdf)

            merged_pdf.save(str(front_output_dir / "merged.pdf"))

        if side in ["back", "both"]:
            back_output_dir = output_dir / "back"
            back_output_dir.mkdir(parents=True, exist_ok=True)
            merged_pdf = pymupdf.open()

            for card in cards:
                with pymupdf.open(card.back_save_fn) as back_pdf:
                    merged_pdf.insert_pdf(back_pdf)

            merged_pdf.save(back_output_dir / "merged.pdf")


def main(**args) -> None:
    input_file = args["input_file"]
    output_dir = Path(args["output_dir"])
    expansion_logo_path = (
        Path(args["expansion_logo_path"]) if args["expansion_logo_path"] else None
    )

    if args["name"]:
        expansion_name = args["name"]
    else:
        try:
            expansion_name = Path(input_file).stem
        except TypeError:  # In streamlit, the input_file is a file object.
            input_file = cast(io.BytesIO, input_file)
            expansion_name = Path(input_file.name).stem
        print(
            "Argument -n/--name not given. "
            f"Expansion name inferred to be {expansion_name}."
        )

    df = parse_input_file(input_file, args["image_dir"])

    callbacks = args.get("callbacks", [])

    create_cards(
        df,
        expansion_name,
        expansion_logo_path,
        output_dir,
        args["merge"],
        args["side"],
        args["format"],
        args["workers"],
        args["misery_index_desc"],
        callbacks,
    )


def main_cli(**kwargs):
    try:
        main(**kwargs)
    except KeyboardInterrupt:
        print("Interrupted.")


if __name__ == "__main__":
    main()
