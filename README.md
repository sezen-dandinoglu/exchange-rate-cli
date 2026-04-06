# 💸 Exchange Rate CLI Tool

## Description

A simple Python CLI tool that fetches real-time currency exchange rates based on user input. It allows users to convert amounts between currencies and optionally export the results to a JSON file.

## Features

* CLI arguments:

  * `--base` (required): Base currency (e.g. USD)
  * `--target` (required): Target currency (e.g. TRY)
  * `--amount` (optional): Amount to convert (default = 1)
  * `--output` (optional): Save results to a JSON file
* Real-time exchange rate fetching via API
* JSON export for storing results
* Clean and readable terminal output

## API Used

ExchangeRate API:
https://api.exchangerate-api.com/v4/latest/{base}

## Usage

```bash
python exchange.py --base USD --target TRY --amount 100
```

```bash
python exchange.py --base EUR --target USD --output result.json
```

## Example Output (JSON)

```json
[
    {
        "time_last_updated": "2026-04-03 08:45:01",
        "base": "USD",
        "target": "TRY",
        "amount": 100.0,
        "rate": 44.58,
        "converted_amount": 4458.0
    },
    {
        "time_last_updated": "2026-04-03 08:45:01",
        "base": "USD",
        "target": "TRY",
        "amount": 50.0,
        "rate": 44.58,
        "converted_amount": 2229.0
    }
]
```
