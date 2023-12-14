from fastapi import APIRouter

from api_scripts.models import ClientData, BankDecisions
from scripts.model_scripts.predict import predict as model_predict

api_router = APIRouter()


@api_router.get("/")
async def root():
    return {"message": "Предсказание вероятности одобрения банком клиента. Используйте /predict."}


@api_router.post("/predict/")
def predict(client: ClientData) -> BankDecisions:
    """Предсказание вероятности одобрения банком клиента
    - **client**: данные клиента для оценивания
    :return: предсказание одобрения банками
    """
    predictions = model_predict(client)
    return predictions
