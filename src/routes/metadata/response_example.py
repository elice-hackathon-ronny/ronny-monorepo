def start_debate_example() : 
    return {
    200: {
        "description": "debate successfully made",
        "content": {
            "application/json": {
                "example": 
                    {
                        "debate_id": "64ea133ab146c72a4c61ba15",
                        "message" : {
                            "message":"메시지 내용",
                            "message_type":"arg",
                            "author":"assistant",
                        }
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
                            "message": "사용자의 입론 '유저 입론입니다'에 대한 gpt 반론입니다",
                            "message_type": "counter",
                            "author":"assistant"
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

def get_debate_summary_example() : 
    return {
    200: {
        "description": "debate summary",
        "content": {
            "application/json": {
                "example": 
                        {
                            "ronny_summary": "this is ai_summary",
                            "user_summary" : "this is user_summary",
                            "eval":"this is final evaluation"
                        }
                
            }
        }
    }} 