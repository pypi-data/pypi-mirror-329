#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import os
import threading
import cv2
from PIL import Image
import json
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import torch
import transformers
import torchvision

from transformers import AutoImageProcessor, MaskFormerForInstanceSegmentation


class ImageTilesSplit:
  def __init__(self, image, name):
    self.image = image
    self.name = name

  def split(self, tile_size=(640, 640)):
    if self.image.shape[2] > 1:
        original_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
    else:
        original_image = Image.fromarray(self.image)
    original_width, original_height = original_image.size

    num_tiles_x = (original_width + tile_size[0] - 1) // tile_size[0]
    num_tiles_y = (original_height + tile_size[1] - 1) // tile_size[1]

    self.tiles_info = {
        'image': self.image,
        'original_image': original_image,
        'original_size': (original_width, original_height),
        'tile_size': tile_size,
        'num_tiles_x': num_tiles_x,
        'num_tiles_y': num_tiles_y,
        'tiles': {}
    }

    for i in range(num_tiles_x):
      for j in range(num_tiles_y):
        left = i * tile_size[0]
        upper = j * tile_size[1]
        right = min(left + tile_size[0], original_width)
        lower = min(upper + tile_size[1], original_height)

        tile = original_image.crop((left, upper, right, lower))

        tile_key = f'tile_{i}_{j}'
        self.tiles_info['tiles'][tile_key] = {
          'position': (i, j),
          'box': (left, upper, right, lower),
          'tile': tile,
          # 'cv2.tile': cv2.cvtColor(np.array(tile), cv2.COLOR_RGB2BGR)
          'cv2.tile': np.array(tile)
        }

    return self.tiles_info

  def join(self, tile_join_key="predicted"):
    joined = np.zeros((self.tiles_info['original_size'][1], self.tiles_info['original_size'][0], 1), dtype=np.uint8)
    for tile_key, tile_info in self.tiles_info['tiles'].items():
      box = tile_info['box']
      joined[box[1]:box[3], box[0]:box[2], 0] = tile_info[tile_join_key]
    joined = np.squeeze(joined, axis=-1)
    self.tiles_info[tile_join_key] = joined
    return joined

  def get_original_coordinates(self, tile_key, x, y):
    """
    Converts coordinates from a tile back to the original image.

    Args:
        tile_key (str): The key of the tile in the tiles_info dictionary.
        x (int): The x-coordinate in the tile.
        y (int): The y-coordinate in the tile.

    Returns:
        tuple: The coordinates (x_original, y_original) in the original image.
    """
    tile_data = self.tiles_info['tiles'][tile_key]
    left, upper, _, _ = tile_data['box']

    x_original = left + x
    y_original = upper + y

    return (x_original, y_original)

  def plot_tiles_with_grid(self):
    original_width, original_height = self.tiles_info['original_size']
    tile_width, tile_height = self.tiles_info['tile_size']
    num_tiles_x = self.tiles_info['num_tiles_x']
    num_tiles_y = self.tiles_info['num_tiles_y']

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.imshow(self.tiles_info['original_image'])

    for i in range(num_tiles_x + 1):
        x = i * tile_width
        ax.axvline(x=x, color='r', linestyle='--', linewidth=1)

    for j in range(num_tiles_y + 1):
        y = j * tile_height
        ax.axhline(y=y, color='r', linestyle='--', linewidth=1)

    ax.set_xlim(0, original_width)
    ax.set_ylim(original_height, 0)

    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            x_center = i * tile_width + tile_width / 2
            y_center = j * tile_height + tile_height / 2
            ax.text(x_center, y_center, f'{i},{j}', color=(0,1,0), fontsize=7, ha='center', va='center')

    plt.title(f"{self.name} Grid")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

  def plot_tiles_individually(self):
    num_tiles_x = self.tiles_info['num_tiles_x']
    num_tiles_y = self.tiles_info['num_tiles_y']

    fig, axes = plt.subplots(num_tiles_y, num_tiles_x, figsize=(15, 15))

    if num_tiles_x == 1 and num_tiles_y == 1:
        axes = [[axes]]
    elif num_tiles_x == 1:
        axes = [[ax] for ax in axes]
    elif num_tiles_y == 1:
        axes = [axes]

    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            tile_key = f'tile_{i}_{j}'
            tile = self.tiles_info['tiles'][tile_key]['tile']

            ax = axes[j][i]

            ax.imshow(tile, cmap='gray')
            ax.set_title(f'{i}.{j}', fontsize=8)
            ax.axis('off')

    plt.tight_layout()
    plt.show()


class MaskInstancePredictor:
  def __init__(self, cache_dir, device="cuda", colors=None):
    if colors is None:
      self.colors = [
        [0, 0, 255],
        [0, 255, 0],
        [255, 0, 0],
        [255, 255, 255]
      ]
    else:
      self.colors = colors

    self.device = device
    self.cache_dir = cache_dir

    self.processor = AutoImageProcessor.from_pretrained("facebook/maskformer-swin-base-ade")
    self.model = MaskFormerForInstanceSegmentation.from_pretrained(
      "facebook/maskformer-swin-base-ade",
      cache_dir=cache_dir
    ).to(self.device)

  def relabel_predictions(self, predictions, label_map, new_labels):
    relabeled = np.full_like(predictions, fill_value=-1)

    for label_id, label_name in label_map.items():
      if label_name in new_labels:
        relabeled[predictions == label_id] = new_labels[label_name]

    return relabeled

  def predict_one(self, image):
    inputs = self.processor(images=image, return_tensors="pt").to(self.device)
    with torch.no_grad():
      outputs = self.model(**inputs)

    predicted = self.processor.post_process_semantic_segmentation(outputs, target_sizes=[image.size[::-1]])[0]
    return predicted.to("cpu")

  def plot_mask(self, image, mask, alpha=0.5):
    color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8) # height, width, 3
    for label, color in enumerate(self.colors):
      color_mask[mask == label, :] = color
    color_mask = color_mask[..., ::-1] # Convert to BGR

    masked_image = np.array(image) * (1 - alpha) + color_mask * alpha
    masked_image = masked_image.astype(np.uint8)

    plt.figure(figsize=(15, 10))
    plt.imshow(masked_image)
    plt.show()


class UrbanPredictor:
  def __init__(self, name, cache_dir, device="cuda"):
    self.name = name
    self.device = device
    self.cache_dir = cache_dir

    self.predictor = MaskInstancePredictor(cache_dir, device=device)
    self._classes = {"artificial": 0, "natural": 1}
    self.ade_classes = {
      0: 'artificial', 1: 'artificial', 2: 'natural', 3: 'artificial', 4: 'natural', 5: 'artificial',6: 'artificial',7: 'artificial',8: 'artificial',9: 'natural',
      10: 'artificial',11: 'artificial',12: 'artificial',13: 'natural',14: 'artificial',15: 'artificial',16: 'natural',17: 'natural',18: 'artificial',19: 'artificial',
      20: 'artificial',21: 'natural',22: 'artificial',23: 'artificial',24: 'artificial',25: 'artificial',26: 'natural',27: 'artificial',28: 'artificial',29: 'natural',
      30: 'artificial',31: 'artificial',32: 'artificial',33: 'artificial',34: 'natural',35: 'artificial',36: 'artificial',37: 'artificial',38: 'artificial',39: 'artificial',
      40: 'artificial',41: 'artificial',42: 'artificial',43: 'artificial',44: 'artificial',45: 'artificial',46: 'natural',47: 'artificial',48: 'artificial',49: 'artificial',
      50: 'artificial',51: 'artificial',52: 'artificial',53: 'artificial',54: 'artificial',55: 'artificial',56: 'artificial',57: 'artificial',58: 'artificial',59: 'artificial',
      60: 'natural',61: 'artificial',62: 'artificial', 63: 'artificial', 64: 'artificial',65: 'artificial',66: 'natural',67: 'artificial',68: 'natural',69: 'artificial',
      70: 'artificial',71: 'artificial',72: 'natural',73: 'artificial',74: 'artificial',75: 'artificial',76: 'artificial',77: 'artificial',78: 'artificial',79: 'artificial',
      80: 'artificial',81: 'artificial',82: 'artificial',83: 'artificial',84: 'artificial',85: 'artificial',86: 'artificial',87: 'artificial',88: 'artificial',89: 'artificial',
      90: 'artificial',91: 'artificial',92: 'artificial',93: 'artificial',94: 'natural',95: 'artificial',96: 'artificial',97: 'artificial',98: 'artificial',99: 'artificial',
      100: 'artificial',101: 'artificial',102: 'artificial',103: 'artificial',104: 'artificial',105: 'artificial',106: 'artificial',107: 'artificial',108: 'artificial',109: 'artificial',
      110: 'artificial',111: 'artificial',112: 'artificial',113: 'natural',114: 'artificial',115: 'artificial',116: 'artificial',117: 'artificial',118: 'artificial',119: 'artificial',
      120: 'artificial',121: 'artificial',122: 'artificial',123: 'artificial',124: 'artificial',125: 'artificial',126: 'natural',127: 'artificial',128: 'natural',129: 'artificial',
      130: 'artificial',131: 'artificial',132: 'artificial',133: 'artificial',134: 'artificial',135: 'artificial',136: 'artificial',137: 'artificial',138: 'artificial',139: 'artificial',
      140: 'artificial',141: 'artificial',142: 'artificial',143: 'artificial',144: 'artificial',145: 'artificial',146: 'artificial',147: 'artificial',148: 'artificial',149: 'artificial'
      }
    # natural_labels = {
    #   'sky', 'tree', 'grass', 'mountain, mount', 'plant', 'water', 'earth, ground',
    #   'rock, stone', 'sand', 'flower', 'hill', 'palm, palm tree', 'river', 'sea',
    #   'field', 'land, ground, soil', 'falls', 'lake', 'animal'
    # }
    # self.ade_classes = {
    #   key: "natural" if value in natural_labels else "artificial"
    #   for key, value in self.predictor.model.config.id2label.items()
    # }

  def predict(self, image, w=512):
    self.tile_split = ImageTilesSplit(image, name=self.name)
    self.tile_split.split(tile_size=(w, w))

    n = 1
    l = len(self.tile_split.tiles_info['tiles'])
    for tile_key, tile_info in self.tile_split.tiles_info['tiles'].items():
      mask = self.predictor.predict_one(tile_info['tile'])
      mask = self.predictor.relabel_predictions(mask, self.ade_classes, self._classes)
      self.tile_split.tiles_info['tiles'][tile_key]['predicted'] = mask
      if n % 100 == 0:
          info(f"predict {self.name}", f"{n}/{l}", f"on {self.device}")
      n += 1

    self.tile_split.join(tile_join_key="predicted")

  def plot(self, alpha=0.5):
    self.predictor.plot_mask(self.tile_split.tiles_info['image'], self.tile_split.tiles_info['predicted'], alpha=alpha)

  def plot_tile(self, tile_key, alpha=0.5):
    self.predictor.plot_mask(self.tile_split.tiles_info['tiles'][tile_key]['tile'], self.tile_split.tiles_info['tiles'][tile_key]['predicted'], alpha=alpha)


class ThrPredictor:
  plot_lock = threading.Lock()

  def __init__(self, name, base_path, w, cache_dir, device):
    self.image = cv2.imread(os.path.join(base_path, name))
    self.name = name
    self.w = w
    self.cache_dir = cache_dir
    self.device = device

  def start(self):
    self.t = threading.Thread(target = self.run)
    self.t.start()

  def join(self):
    self.t.join()

  def plot(self, alpha=0.3):
    info("Plot", self.name)
    self.predictor.tile_split.plot_tiles_with_grid()
    self.predictor.plot(alpha=alpha)
    # self.predictor.plot_tile("tile_11_11", alpha=alpha)

  def run(self):
    try:
      self.predictor = UrbanPredictor(name=self.name, cache_dir=self.cache_dir, device=self.device)
      self.predictor.predict(self.image, w=self.w)
      with ThrPredictor.plot_lock:
        self.plot(alpha=0.3)
    except Exception as e:
      error(e)
