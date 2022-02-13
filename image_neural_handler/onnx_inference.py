import torch.onnx
import onnxruntime
import cv2

from albumentations import Compose, Resize, Normalize
from albumentations.pytorch import ToTensorV2


def get_val_augmentations(image_size):
    return Compose(
        [
            Resize(image_size, image_size),
            Normalize(
                mean=[0.487, 0.457, 0.395],
                std=[0.227, 0.222, 0.224],
            ),
            ToTensorV2(),
        ]
    )


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


def get_image_score(neural_net_name, neural_net_names, image_from_test):
    # Этот параметр обозначает сколько картинок за раз запихиваем в модель
    """neural_net_name = clock или figure
    neural_net_names - словарь с ключами(названия нейронок) и значеними(файл нейронки)
    image_from_test - кртинка из теста на деменцию, загружаемая для оценки"""
    # batch_size = 1
    image_size = 256

    ort_session = onnxruntime.InferenceSession(neural_net_names[neural_net_name])

    image = cv2.imread(image_from_test)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # ниже вызывается модель
    transform = get_val_augmentations(image_size)
    augmented = transform(image=image)
    image = augmented["image"]
    # Если batch_size>1 то эта строчка не нужна. Тогда сделай список imgs в 40 строке
    image.unsqueeze_(0)

    ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(image)}
    ort_outs = ort_session.run(None, ort_inputs)
    result = ort_outs[0]
    print(result)
    # [[ 0.5828074  0.8418093 -1.40597  ]]
    # получить класс
    class_id = torch.argmax(torch.softmax(torch.tensor(result), 1), 1)
    return class_id
    # tensor([1])
