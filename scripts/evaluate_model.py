# ======== CONFIGURATION ========
MODEL_PATH = os.environ.get("MODEL_PATH", "models/disease/potato.keras")
TEST_DATASET_PATH = os.environ.get("TEST_DATASET_PATH", "dataset/test")
BATCH_SIZE = 32

# Default output paths (used if the user just presses Enter at the prompts below)
DEFAULT_CSV_OUTPUT_PATH = "results/evaluation"
DEFAULT_CONFUSION_MATRIX_OUTPUT_PATH = "results/confusion_matrices"
# ======== IMPORTS ========
import os
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ======== DEFINE CUSTOM ATTENTION LAYER ========
from tensorflow.keras.layers import Layer
from tensorflow.keras import backend as K

class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(
            name="att_weight", shape=(input_shape[-1], 1),
            initializer="random_normal", trainable=True
        )
        self.b = self.add_weight(
            name="att_bias", shape=(input_shape[1], 1),
            initializer="zeros", trainable=True
        )
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        e = K.tanh(K.dot(x, self.W) + self.b)
        a = K.softmax(e, axis=1)
        output = x * a
        return K.sum(output, axis=1)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])


# ======== ASK USER WHERE TO SAVE RESULTS ========
def ask_for_path(prompt_text, default_path, default_filename):
    """Ask the user to paste a save path. Press Enter to use the default.

    If the user pastes a folder (no filename with an extension, or an
    existing directory), the default_filename is appended automatically
    so we never try to open a directory as if it were a file.
    """
    user_input = input(f"{prompt_text}\n[Default: {default_path}]\n> ").strip().strip('"')
    chosen_path = user_input if user_input else default_path

    # If it's an existing directory, or has no file extension, treat it as
    # a folder and append the default filename.
    is_existing_dir = os.path.isdir(chosen_path)
    has_extension = bool(os.path.splitext(chosen_path)[1])
    if is_existing_dir or not has_extension:
        chosen_path = os.path.join(chosen_path, default_filename)

    # Make sure the destination folder exists
    folder = os.path.dirname(chosen_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    return chosen_path

print("[INFO] Please provide save locations for the results (or press Enter to use defaults).")
CSV_OUTPUT_PATH = ask_for_path(
    "📄 Paste the full path (including filename.csv, or just a folder) to save the classification report:",
    DEFAULT_CSV_OUTPUT_PATH,
    "classification_report.csv"
)
CONFUSION_MATRIX_OUTPUT_PATH = ask_for_path(
    "📊 Paste the full path (including filename.png, or just a folder) to save the confusion matrix:",
    DEFAULT_CONFUSION_MATRIX_OUTPUT_PATH,
    "confusion_matrix.png"
)

# ======== LOAD MODEL ========
print("[INFO] Loading CNN+Attention model...")
model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={"AttentionLayer": AttentionLayer}
)

# Auto-detect input size
_, img_height, img_width, _ = model.input_shape
IMG_SIZE = (img_height, img_width)
print(f"[INFO] Model expects input size: {IMG_SIZE}")

# ======== LOAD TEST DATASET ========
print("[INFO] Loading test dataset...")
raw_test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    TEST_DATASET_PATH,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
    label_mode="categorical"
)

class_names = raw_test_ds.class_names
print(f"[INFO] Classes: {class_names}")

# Normalize dataset
test_ds = raw_test_ds.map(lambda x, y: (x / 255.0, y))

# ======== EVALUATE MODEL ========
print("[INFO] Evaluating model...")
loss, accuracy = model.evaluate(test_ds)
print(f"\n✅ Final Test Accuracy: {accuracy * 100:.2f}%")
print(f"📉 Test Loss: {loss:.4f}")

# ======== PREDICTIONS ========
print("[INFO] Generating predictions...")
y_true = np.concatenate([y for x, y in test_ds], axis=0)
y_pred_probs = model.predict(test_ds)
y_pred = np.argmax(y_pred_probs, axis=1)
y_true = np.argmax(y_true, axis=1)

# ======== CLASSIFICATION REPORT ========
print("\n📊 Classification Report:")
report_text = classification_report(y_true, y_pred, target_names=class_names)
print(report_text)

# Save the classification report as a CSV file
report_dict = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
report_df.to_csv(CSV_OUTPUT_PATH, index=True)
print(f"[INFO] Classification report saved to: {CSV_OUTPUT_PATH}")

# ======== CONFUSION MATRIX ========
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")

# Save the confusion matrix image
plt.savefig(CONFUSION_MATRIX_OUTPUT_PATH, dpi=300, bbox_inches="tight")
print(f"[INFO] Confusion matrix saved to: {CONFUSION_MATRIX_OUTPUT_PATH}")

plt.show()