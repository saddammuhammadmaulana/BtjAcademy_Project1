# service.py
import numpy as np
import joblib
from api.predict.schemas import PredictionParams

PATH_MODEL = r'C:\Users\user\Documents\projectBTJ-academy\test-project\best_gmm (1).pkl'
MODEL = joblib.load(PATH_MODEL)

class Predict:
    def __init__(self, params: PredictionParams):
        self.params = params
        self.model = MODEL

    def _build_dynamic_mapping(self):
        """
        Buat mapping komponen GMM -> label Iris berdasarkan mean fitur.
        Asumsi: fitur = [sepal_length, sepal_width, petal_length, petal_width]
        """
        if not hasattr(self.model, "means_"):
            # Bukan GMM? fallback ke mapping statis, atau angkat error
            return {0: "Setosa", 1: "Virginica", 2: "VersiColor"}

        means = self.model.means_  # shape (n_components, 4)
        # Urutkan komponen berdasarkan petal_width (kolom index 3)
        order = np.argsort(means[:, 3])  # kecil → besar
        # kecil  -> Setosa, tengah -> VersiColor, besar -> Virginica
        mapping = {
            int(order[0]): "Setosa",
            int(order[1]): "VersiColor",
            int(order[2]): "Virginica"
        }
        return mapping

    def predict(self):
        pred_data = [[
            self.params.sepal_length,
            self.params.sepal_width,
            self.params.petal_length,
            self.params.petal_width
        ]]

        comp_idx = self.model.predict(pred_data).tolist()  # contoh: [2]
        mapping = self._build_dynamic_mapping()
        mapped = [mapping[int(i)] for i in comp_idx]

        return {
            "result": mapped,
            "data": "Prediction process for data"
        }