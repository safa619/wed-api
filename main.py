from fastapi import FastAPI
from x402.fastapi.middleware import require_payment

app = FastAPI()

app.middleware("http")(
    require_payment(
        price="$0.01",
        pay_to_address="0x055B85260Beb73c2268c7368863fDCB988E340B0",
        path="/hello",
    )
)

@app.get("/hello")
def hello():
    return {"message": "Hello from Wed.eth API"}
