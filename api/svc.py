import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import preprocessing

import utils as u

SVM_SAMPLE_SIZE = 2500
SVM_KERNEL_TYPE = "rbf"
DEFAULT_PAIR = "USDTIDR"
DEFAULT_GAMMA = 80
DEFAULT_C = 18

class SupportVectorClassifier:
  def __init__(self, data_source, data_sample_count=SVM_SAMPLE_SIZE, kernel_type=SVM_KERNEL_TYPE, pair=DEFAULT_PAIR, gamma=DEFAULT_GAMMA, C=DEFAULT_C, save_model=True):
    df = data_source
    df = df.drop(["Timestamp"], axis=1)
    df = df.head(data_sample_count)

    x = df.drop(["Trend"], axis=1)
    x = x.values
    y = df["Trend"]

    scalerX = preprocessing.StandardScaler().fit(x)
    x = scalerX.transform(x)

    self.x_train, self.x_test, y_train, self.y_test = train_test_split(x, y, test_size = 0.20)

    model_file_name = f"SVC_{kernel_type}-{data_sample_count}-{pair}-g{gamma}-C{C}.model"
    model_file_dir = f"{u.MODELS_FOLDER}/{model_file_name}"

    self.pair = pair
    self.gamma = gamma
    self.C = C
    self.data_sample_count = data_sample_count
    self.kernel_type = kernel_type

    print(f"[{pair}: gamma={gamma}/C={C} - {data_sample_count}] ", end='')

    if u.check_file_in_models_directory(model_file_name):
      print("Model Data Found! Using Cached Model.")
      self.classifier = u.load_pickle(model_file_dir)
    else:
      print("No Model Found! Constructing Model...")
      # self.classifier = SVC(kernel=kernel_type)
      self.classifier = SVC(kernel=kernel_type, gamma=gamma, C=C)
      self.classifier.fit(self.x_train, y_train)
      if save_model or data_sample_count >= 10000:
        u.save_pickle(self.classifier, model_file_dir)
  
  def predict(self, env):
    return self.classifier.predict(env)
  
  def get_predictions(self):
    return self.predict(self.x_test)

  def get_accuracy(self):
    predictions = self.predict(self.x_test)
    return accuracy_score(self.y_test, predictions) * 100
  
  def evaluate_classifier(self):
    predictions = self.predict(self.x_test)
    print(f"Accuracy -> {accuracy_score(self.y_test, predictions)*100} %")
    disp = ConfusionMatrixDisplay.from_estimator(
        self.classifier,
        self.x_test,
        self.y_test,
        display_labels=["Uptrend", "Sideways", "Downtrend"],
        cmap=plt.cm.Blues,
        normalize=None,
    )
    disp.ax_.set_title(f"SVM - Confusion Matrix - {self.pair}/{self.kernel_type.upper()}/gamma={self.gamma}/C={self.C}")

    plt.show()
