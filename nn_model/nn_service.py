import modal
from modal import Image

app = modal.App("nn-service")
nn_image = (
    Image.debian_slim()
    .pip_install("torch", "scikit-learn", "joblib")
    .add_local_dir(".", remote_path="/root/nn_service")
)


@app.cls(image=nn_image, cpu=1.0, timeout=1800, scaledown_window=450, min_containers=0)
class ComplexityNN:
    @modal.enter()
    def setup(self):
        import joblib
        import torch
        import sys

        sys.path.append("/root/nn_service")
        from complexity_nn import NeuralNetwork

        self.scaler = joblib.load('/root/nn_service/artifacts/scaler.pkl')
        self.model = NeuralNetwork(input_size=7)
        self.model.load_state_dict(torch.load(
            '/root/nn_service/artifacts/neural_network.pth',
            map_location="cpu"
        ))
        self.model.eval()

    @modal.method()
    def predict(self, features: dict):
        import torch
        from normalise_features import normalise_features

        norm_result = normalise_features(features, self.scaler)['features']
        features_tensor = torch.tensor(norm_result, dtype=torch.float32)

        with torch.no_grad():
            prediction = self.model(features_tensor)
            raw_val = prediction[0].item()

            return round(raw_val, 2)
