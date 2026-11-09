from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.server import x402ResourceServer

PAY_TO = "0x055B85260Beb73c2268c7368863fDCB988E340B0"
NETWORK = "eip155:84532"  # Base Sepolia (تجريبي)

app = FastAPI()

facilitator = HTTPFacilitatorClient(
    FacilitatorConfig(url="https://x402.org/facilitator")
)
server = x402ResourceServer(facilitator)
server.register(NETWORK, ExactEvmServerScheme())

routes: dict[str, RouteConfig] = {
    "GET /hello": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=PAY_TO,
                price="$0.01",
                network=NETWORK,
            )
        ],
        mime_type="application/json",
        description="Hello from Wed.eth API",
    ),
}

app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)

# vAPI يطلب كشف هيدرات الدفع عبر CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["PAYMENT-REQUIRED", "PAYMENT-RESPONSE"],
)

@app.get("/hello")
async def hello():
    return {"message": "Hello from Wed.eth API"}
