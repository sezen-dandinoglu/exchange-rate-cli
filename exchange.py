import requests
import argparse
import json
import os
from datetime import datetime

def main() -> None:

    parser = argparse.ArgumentParser(description="Fetch and display currency exchnage rate")
    parser.add_argument("--base", required=True, type=str, help="You must enter base currency {e.g. USD}")
    parser.add_argument("--target", required=True, type=str, help="You must enter target currency {e.g. EUR}")
    parser.add_argument("--amount", default=1, type=float, help="Amount of money to be exchanged")
    parser.add_argument("--output", type=str, help="result.json")
    
    args = parser.parse_args()

    base = args.base.strip().upper()
    target = args.target.strip().upper()

    URL=f'https://api.exchangerate-api.com/v4/latest/{base}'

    data = fetch_data(URL, target)

    if data is None:
        print("Invalid currency cide or request failed")
        return
    
    rate = data["rate"]
    time_last_updated  = data["time_last_updated"]
    
    if rate is None:
        print("Invalid target currency code")
        return

    converted_amount = rate * args.amount

    print_exchange_result(converted_amount, base, target, amount=args.amount)
    
    if args.output:
        formatted_time = datetime.fromtimestamp(time_last_updated).strftime('%Y-%m-%d %H:%M:%S')

        result = {"time_last_updated":formatted_time, 
                "base":base, 
                "target":target, 
                "amount":args.amount, 
                "rate":rate, 
                "converted_amount":converted_amount}
    
    save_to_json(result, args.output)


def fetch_data(url, target) -> dict | None:

    try:
        content = requests.get(url, timeout=5)
        content.raise_for_status()

        data = content.json()

        return{
            "rate": data.get("rates", {}).get(f"{target.upper()}"),
            "time_last_updated": data.get("time_last_updated", {})
        }
                
    except ValueError:
        print("Response is not valid JSON")
    except requests.exceptions.ConnectionError:
        print("Connection error")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    return None
    
def save_to_json(result: dict, filename: str) -> None:

    cur_path = os.path.dirname(__file__)
    filepath = os.path.join(cur_path, filename)

    existing_data = []
    
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                existing_data = json.load(file)

                if not isinstance(existing_data, list):
                    existing_data = []
        
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"File not found")
    
    existing_data.append(result)

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error occurred: {e}")


def print_exchange_result(calc_result, base, target, amount) -> None:

    print(f"{amount} {base.upper()} = {calc_result:.2f} {target.upper()}")

if __name__ == "__main__":
    main()