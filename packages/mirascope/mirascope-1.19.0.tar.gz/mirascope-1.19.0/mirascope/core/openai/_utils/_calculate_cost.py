"""Calculate the cost of a completion using the OpenAI API."""


def calculate_cost(
    input_tokens: int | float | None,
    cached_tokens: int | float | None,
    output_tokens: int | float | None,
    model: str = "gpt-3.5-turbo-16k",
) -> float | None:
    """Calculate the cost of a completion using the OpenAI API.

    https://openai.com/pricing

    Model                                     Input               Cached               Output
    gpt-4o                                    $2.50  / 1M tokens  $1.25 / 1M tokens   $10.00 / 1M tokens
    gpt-4o-2024-11-20                         $2.50  / 1M tokens  $1.25 / 1M tokens   $10.00 / 1M tokens
    gpt-4o-2024-08-06                         $2.50  / 1M tokens  $1.25 / 1M tokens   $10.00 / 1M tokens
    gpt-4o-2024-05-13                         $5.00  / 1M tokens  $2.50 / 1M tokens   $15.00 / 1M tokens
    gpt-4o-audio-preview                      $2.50  / 1M tokens  $1.25 / 1M tokens   $10.00 / 1M tokens
    gpt-4o-audio-preview-2024-12-17           $2.50  / 1M tokens  $1.25 / 1M tokens   $10.00 / 1M tokens
    gpt-4o-audio-preview-2024-10-01           $2.50  / 1M tokens  $1.25 / 1M tokens   $10.00 / 1M tokens
    gpt-4o-realtime-preview                   $5.00  / 1M tokens  $2.50 / 1M tokens   $20.00 / 1M tokens
    gpt-4o-realtime-preview-2024-12-17        $5.00  / 1M tokens  $2.50 / 1M tokens   $20.00 / 1M tokens
    gpt-4o-realtime-preview-2024-10-01        $5.00  / 1M tokens  $2.50 / 1M tokens   $20.00 / 1M tokens
    gpt-4o-mini                               $0.15  / 1M tokens  $0.08 / 1M tokens   $0.60  / 1M tokens
    gpt-4o-mini-2024-07-18                    $0.15  / 1M tokens  $0.08 / 1M tokens   $0.60  / 1M tokens
    gpt-4o-mini-audio-preview                 $0.15  / 1M tokens  $0.08 / 1M tokens   $0.60  / 1M tokens
    gpt-4o-mini-audio-preview-2024-12-17      $0.15  / 1M tokens  $0.08 / 1M tokens   $0.60  / 1M tokens
    gpt-4o-mini-realtime-preview              $0.60  / 1M tokens  $0.30 / 1M tokens   $2.40  / 1M tokens
    gpt-4o-mini-realtime-preview-2024-12-17   $0.60  / 1M tokens  $0.30 / 1M tokens   $2.40  / 1M tokens
    o1                                        $15.00 / 1M tokens  $7.50 / 1M tokens   $60.00 / 1M tokens
    o1-2024-12-17                             $15.00 / 1M tokens  $7.50 / 1M tokens   $60.00 / 1M tokens
    o1-preview-2024-09-12                     $15.00 / 1M tokens  $7.50 / 1M tokens   $60.00 / 1M tokens
    o3-mini                                   $1.10  / 1M tokens  $0.55 / 1M tokens   $4.40  / 1M tokens
    o3-mini-2025-01-31                        $1.10  / 1M tokens  $0.55 / 1M tokens   $4.40  / 1M tokens
    o1-mini                                   $1.10  / 1M tokens  $0.55 / 1M tokens   $4.40  / 1M tokens
    o1-mini-2024-09-12                        $1.10  / 1M tokens  $0.55 / 1M tokens   $4.40  / 1M tokens
    gpt-4-turbo                               $10.00 / 1M tokens                      $30.00 / 1M tokens
    gpt-4-turbo-2024-04-09                    $10.00 / 1M tokens                      $30.00 / 1M tokens
    gpt-3.5-turbo-0125	                      $0.50  / 1M tokens	                  $1.50  / 1M tokens
    gpt-3.5-turbo-1106	                      $1.00  / 1M tokens	                  $2.00  / 1M tokens
    gpt-4-1106-preview	                      $10.00 / 1M tokens                      $30.00 / 1M tokens
    gpt-4	                                  $30.00 / 1M tokens                      $60.00 / 1M tokens
    text-embedding-3-small	                  $0.02  / 1M tokens
    text-embedding-3-large	                  $0.13  / 1M tokens
    text-embedding-ada-0002	                  $0.10  / 1M tokens
    """
    pricing = {
        "gpt-4o": {
            "prompt": 0.000_002_5,
            "cached": 0.000_001_25,
            "completion": 0.000_01,
        },
        "gpt-4o-2024-11-20": {
            "prompt": 0.000_002_5,
            "cached": 0.000_001_25,
            "completion": 0.000_01,
        },
        "gpt-4o-2024-08-06": {
            "prompt": 0.000_002_5,
            "cached": 0.000_001_25,
            "completion": 0.000_01,
        },
        "gpt-4o-2024-05-13": {
            "prompt": 0.000_005,
            "cached": 0.000_002_5,
            "completion": 0.000_015,
        },
        "gpt-4o-audio-preview": {
            "prompt": 0.000_002_5,
            "cached": 0.000_001_25,
            "completion": 0.000_01,
        },
        "gpt-4o-audio-preview-2024-12-17": {
            "prompt": 0.000_002_5,
            "cached": 0.000_001_25,
            "completion": 0.000_01,
        },
        "gpt-4o-audio-preview-2024-10-01": {
            "prompt": 0.000_002_5,
            "cached": 0.000_001_25,
            "completion": 0.000_01,
        },
        "gpt-4o-realtime-preview": {
            "prompt": 0.000_005,
            "cached": 0.000_002_5,
            "completion": 0.000_02,
        },
        "gpt-4o-realtime-preview-2024-12-17": {
            "prompt": 0.000_005,
            "cached": 0.000_002_5,
            "completion": 0.000_02,
        },
        "gpt-4o-realtime-preview-2024-10-01": {
            "prompt": 0.000_005,
            "cached": 0.000_002_5,
            "completion": 0.000_02,
        },
        "gpt-4o-mini": {
            "prompt": 0.000_000_15,
            "cached": 0.000_000_08,
            "completion": 0.000_000_6,
        },
        "gpt-4o-mini-2024-07-18": {
            "prompt": 0.000_000_15,
            "cached": 0.000_000_08,
            "completion": 0.000_000_6,
        },
        "gpt-4o-mini-audio-preview": {
            "prompt": 0.000_000_15,
            "cached": 0.000_000_08,
            "completion": 0.000_000_6,
        },
        "gpt-4o-mini-audio-preview-2024-12-17": {
            "prompt": 0.000_000_15,
            "cached": 0.000_000_08,
            "completion": 0.000_000_6,
        },
        "gpt-4o-mini-realtime-preview": {
            "prompt": 0.000_000_6,
            "cached": 0.000_000_3,
            "completion": 0.000_002_4,
        },
        "gpt-4o-mini-realtime-preview-2024-12-17": {
            "prompt": 0.000_000_6,
            "cached": 0.000_000_3,
            "completion": 0.000_002_4,
        },
        "o1": {
            "prompt": 0.000_015,
            "cached": 0.000_007_5,
            "completion": 0.000_06,
        },
        "o1-2024-12-17": {
            "prompt": 0.000_015,
            "cached": 0.000_007_5,
            "completion": 0.000_06,
        },
        "o1-preview-2024-09-12": {
            "prompt": 0.000_015,
            "cached": 0.000_007_5,
            "completion": 0.000_06,
        },
        "o3-mini": {
            "prompt": 0.000_001_1,
            "cached": 0.000_000_55,
            "completion": 0.000_004_4,
        },
        "o3-mini-2025-01-31": {
            "prompt": 0.000_001_1,
            "cached": 0.000_000_55,
            "completion": 0.000_004_4,
        },
        "o1-mini": {
            "prompt": 0.000_001_1,
            "cached": 0.000_000_55,
            "completion": 0.000_004_4,
        },
        "o1-mini-2024-09-12": {
            "prompt": 0.000_001_1,
            "cached": 0.000_000_55,
            "completion": 0.000_004_4,
        },
        "gpt-4-turbo": {
            "prompt": 0.000_01,
            "cached": 0,
            "completion": 0.000_03,
        },
        "gpt-4-turbo-2024-04-09": {
            "prompt": 0.000_01,
            "cached": 0,
            "completion": 0.000_03,
        },
        "gpt-3.5-turbo-0125": {
            "prompt": 0.000_000_5,
            "cached": 0,
            "completion": 0.000_001_5,
        },
        "gpt-3.5-turbo-1106": {
            "prompt": 0.000_001,
            "cached": 0,
            "completion": 0.000_002,
        },
        "gpt-4-1106-preview": {
            "prompt": 0.000_01,
            "cached": 0,
            "completion": 0.000_03,
        },
        "gpt-4": {
            "prompt": 0.000_003,
            "cached": 0,
            "completion": 0.000_006,
        },
        "gpt-3.5-turbo-4k": {
            "prompt": 0.000_015,
            "cached": 0,
            "completion": 0.000_02,
        },
        "gpt-3.5-turbo-16k": {
            "prompt": 0.000_003,
            "cached": 0,
            "completion": 0.000_004,
        },
        "gpt-4-8k": {
            "prompt": 0.000_003,
            "cached": 0,
            "completion": 0.000_006,
        },
        "gpt-4-32k": {
            "prompt": 0.000_006,
            "cached": 0,
            "completion": 0.000_012,
        },
        "text-embedding-3-small": {
            "prompt": 0.000_000_02,
            "cached": 0,
            "completion": 0,
        },
        "text-embedding-ada-002": {
            "prompt": 0.000_000_1,
            "cached": 0,
            "completion": 0,
        },
        "text-embedding-3-large": {
            "prompt": 0.000_000_13,
            "cached": 0,
            "completion": 0,
        },
    }
    if input_tokens is None or output_tokens is None:
        return None

    if cached_tokens is None:
        cached_tokens = 0

    try:
        model_pricing = pricing[model]
    except KeyError:
        return None

    prompt_cost = input_tokens * model_pricing["prompt"]
    cached_cost = cached_tokens * model_pricing["cached"]
    completion_cost = output_tokens * model_pricing["completion"]
    total_cost = prompt_cost + cached_cost + completion_cost

    return total_cost
