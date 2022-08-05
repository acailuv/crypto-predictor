import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import preprocessing

import utils as u

SVM_SAMPLE_SIZE = 50000
SVM_KERNEL_TYPE = "rbf"
UPPER_BOUND_PRICE = 1000000000

class SupportVectorClassifier:
  def __init__(self, data_source, data_sample_count=SVM_SAMPLE_SIZE, kernel_type=SVM_KERNEL_TYPE):
    df = data_source
    df = df.drop(["Timestamp"], axis=1)
    df = df.head(data_sample_count)

    x = df.drop(["Trend"], axis=1)
    x = x.values
    y = df["Trend"]

    scalerX = preprocessing.StandardScaler().fit(x)
    x = scalerX.transform(x)

    self.x_train, self.x_test, y_train, self.y_test = train_test_split(x, y, test_size = 0.20)

    model_file_name = f"SVC_{kernel_type}-{data_sample_count}.model"
    model_file_dir = f"{u.MODELS_FOLDER}/{model_file_name}"


    if u.check_file_in_models_directory(model_file_name):
      print("Model Data Found! Using Cached Model.")
      self.classifier = u.load_pickle(model_file_dir)
    else:
      print("No Model Found! Constructing Model...")
      # self.classifier = SVC(kernel=kernel_type)
      self.classifier = SVC(kernel=kernel_type, gamma=100, C=100)
      self.classifier.fit(self.x_train, y_train)
      u.save_pickle(self.classifier, model_file_dir)
  
  def predict(self, env):
    return self.classifier.predict(env)
  
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
    disp.ax_.set_title(f"SVM - Confusion Matrix")

    plt.show()
