def start_debate_example() : 
    return {
    200: {
        "description": "debate successfully made",
        "content": {
            "application/json": {
                "example": 
                    {
                        "debate_id": "64ea133ab146c72a4c61ba15",
                    }
            }
        }
    }}

def continue_debate_example() : 
    return {
    200: {
        "description": "reply by gpt",
        "content": {
            "application/json": {
                "example": 
                    {
                            "counter": "사용자의 입론 '유저 입론입니다'에 대한 gpt 반론입니다",
                            "arg": "gpt 입론입니다"
                        }
                
            }
        }
    }} 

def end_debate_example() : 
    return {
    200: {
        "description": "reply by gpt",
        "content": {
            "application/json": {
                "example": 
                    {
                            "counter": None,
                            "arg": "gpt 결론입니다"
                        }
                
            }
        }
    }} 