from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import utils as u

SVM_SAMPLE_SIZE = 50000
SVM_KERNEL_TYPE = "rbf"

class SupportVectorClassifier:
  def __init__(self, data_source, data_sample_count=SVM_SAMPLE_SIZE, kernel_type=SVM_KERNEL_TYPE):
    df = data_source
    df = df.drop(["Timestamp"], axis=1)
    df = df.head(SVM_SAMPLE_SIZE)

    x = df.drop(["Trend"], axis=1)
    x = x.values
    y = df["Trend"]
    
    x_train, self.x_test, y_train, self.y_test = train_test_split(x, y, test_size = 0.20)

    model_file_name = f"SVC_{kernel_type}-{data_sample_count}.model"
    model_file_dir = f"{u.MODELS_FOLDER}/{model_file_name}"


    if u.check_file_in_models_directory(model_file_name):
      print("Model Data Found! Using Cached Model.")
      self.classifier = u.load_pickle(model_file_dir)
    else:
      print("No Model Found! Constructing Model...")
      self.classifier = SVC(kernel=kernel_type)
      self.classifier.fit(x_train, y_train)
      u.save_pickle(self.classifier, model_file_dir)

    self.evaluate_classifier()
  
  def predict(self, env):
    return self.classifier.predict(env)
  
  def evaluate_classifier(self):
    predictions = self.predict(self.x_test)
    print(f"Accuracy -> {accuracy_score(self.y_test, predictions)*100} %")
