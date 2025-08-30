from fastapi import APIRouter, Body, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import numpy as np
import json
import orjson
import os
import io
import time
import pandas as pd
from .models import OptionParams, PricesResponse
from .black_scholes_pricer import black_scholes_call

# Load example JSON at startup
examples_file = os.path.join("examples", "random_options.json")
with open(examples_file) as f:
    OPTIONS_EXAMPLE = json.load(f)

router = APIRouter()


@router.post("/price", response_model=PricesResponse)
def price_options(options: List[OptionParams] = Body(..., example=OPTIONS_EXAMPLE)):
    
    spot = [opt.spot for opt in options]
    strike = [opt.strike for opt in options]
    maturity = [opt.maturity for opt in options]
    interest_rate = [opt.interest_rate for opt in options]
    volatility = [opt.volatility for opt in options]

    prices = black_scholes_call(spot, strike, maturity, interest_rate, volatility)
    return PricesResponse(prices=prices.tolist())

@router.post("/price-file")
async def price_options(
    file: UploadFile = File(None)
):
    """
    Calculate option prices from an uploaded JSON file.
    """
    start_time = time.time()  # start timer
    try:
        file_content = await file.read()
        df = pd.read_json(io.BytesIO(file_content))  # parse into DataFrame
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {e}")

    # Extract values

    spots = df["spot"].to_numpy()
    strikes = df["strike"].to_numpy()
    maturities = df["maturity"].to_numpy()
    interest_rates = df["interest_rate"].to_numpy()
    volatilities = df["volatility"].to_numpy()

    load_time = time.time()  # end timer
    print(f"Load time {load_time - start_time:.4f} seconds")

    # Compute prices
    prices = black_scholes_call(spots, strikes, maturities, interest_rates, volatilities)

    bs_time = time.time()  # end timer
    print(f"BS time {bs_time - load_time:.4f} seconds")

    # Prepare JSON file content
    json_bytes = io.BytesIO(orjson.dumps({"prices": prices.tolist()}, option=orjson.OPT_INDENT_2))

    outfile_time = time.time()  # end timer
    print(f"Outfile time {outfile_time - start_time:.4f} seconds")

    # Return as downloadable file
    return StreamingResponse(
        json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="prices.json"'}
    )