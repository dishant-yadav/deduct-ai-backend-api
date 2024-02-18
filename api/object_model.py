from teachable_machine import TeachableMachine

URL = "https://teachablemachine.withgoogle.com/models/l-rA90AwJ/"
model_path = URL + "model.json"
metadata_path = URL + "metadata.json"

model = TeachableMachine(model_path=model_path, metadata_path=metadata_path)
print(model)
