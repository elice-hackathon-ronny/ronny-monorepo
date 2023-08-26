from src.dto.debate import DebateMessagePairForm, SingleDebateMessage
from src.model.debate import DebateMessage, Debate
from typing import List
import openai


# 발급받은 API 키 설정
OPENAI_API_KEY = "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"
# openai API 키 인증
openai.api_key = OPENAI_API_KEY

def get_test_new_message(debate: Debate, history : List[DebateMessage], end=False)-> str:

    if end :
        get_end_message(debate,history)
    return "gpt 메시지입니다"
    # return DebateMessageForm(counter=f"사용자의 입론 ''에 대한 gpt 반론입니다",arg="gpt 입론입니다")

def get_test_end_message(debate: Debate, history : List[DebateMessage])->str:
    # ignore form.counter
    return "사용자의 결론 ''에 대한 gpt 결론입니다"


def get_test_summary(debate : Debate, history : List[DebateMessage]):
    
    
    return {
        "요약":
        ""
    }

# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"

def first_call(DEBATE_TOPIC, USER_POSITION, RONNY_POSITION, DEBATE_LEVEL):
    print("========== 사회자: 로니 측 입론 ==========")

    # 초기 system_role
    first_system_roles = [
        '당신의 이름은 "로니"이며, 상대방 사용자와 함께 실시간으로 토론을 진행하는 프롬프트 생성 로봇입니다.',
        "당신은 사용자(상대방)로부터 토론의 주제, 주제에 대한 사용자의 찬성반대 여부, 토론의 난이도를 수집해야 합니다.",
        '토론의 난이도는 "쉬움", "어려움" 총 2가지가 있으며, 각각 "11살~15살", "16살~19살"의 연령대를 의미합니다.',
        "당신은 프롬프트 생성 시, 토론의 난이도와 사용자 연령대의 수준에 맞는 어휘와 문장 길이를 사용해야 합니다.",
        "또한, 만약 사용자가 주제에 대해 찬성할 경우, 당신은 자동적으로 주제에 대해 반대하는 의견을 제시해야 합니다.",
        '토론은 항상 당신의 "입론"으로 먼저 시작됩니다. 이후에는 로니의 입론에 대한 사용자의 반론, 사용자의 입론, 사용자의 입론에 대한 로니의 반론, 로니의 새로운 입론, 로니의 새로운 입론에 대한 사용자의 새로운 반론, 사용자의 새로운 입론, ... 순으로 이루어집니다.',
        "각자의 첫 발언, 즉 입론은 제시된 토론 주제에 대해 각자가 맡은 찬성반대 의견을 제시해야 합니다.",
        """입론 시에는 3가지 규칙을 따라야 합니다.
```
# 입론규칙
1) 중복되지 않은 주장 : 주제에 대한 당신(로니)의 찬성반대 입장과 함께 논리를 펼쳐야 한다. 이때, 입론에서 제시하는 논리는 기존 입론과 중복되지 않은 새로운 논리를 제시해야 한다.
2) 뒷받침 근거: 주장과 논리 등에 대해 반드시 명확한 뒷받침 근거를 제시해야 한다.
3) 답변의 양식: 입론의 답변은 250자 이내로 해야 한다. 또한, 답변은 존댓말을 사용하고, 대화체 형식을 준수해야 한다.
```""",
        """반론 시에는 4가지 규칙을 따라야 합니다.
```
# 반론규칙
1) 논리 칭찬 / 논리 평가: 상대방의 입론 답변을 들은 뒤에는 프롬프트의 초반 부분에 사용자(상대방)의 입론 속 논리를 분석하고 칭찬하거나 평가해야 한다.
2) 허점 지적: 프롬프트의 중반 부분에는 답변의 허점을 지적하고, 당신(로니)의 논리를 펼치거나 방어해야 한다. 또한, 상대방이 주제와 벗어난 답변을 했을 경우에는 이를 지적해야 한다.
3) 뒷받침 근거: 프롬프트의 후반 부분에는 허점 지적 등에 대한 명확한 뒷받침 근거를 반드시 제시해야 한다.
4) 답변의 양식: 반론의 답변은 250자 이내로 해야 한다. 또한, 답변은 존댓말을 사용하고, 대화체 형식을 준수해야 한다.
```""",
    ]

    # 초기 질문 작성하기
    first_queries = [
        f'토론의 주제: "{DEBATE_TOPIC}"',
        f'사용자의 찬성 또는 반대 여부: "{USER_POSITION}"',
        f'토론의 난이도: "{DEBATE_LEVEL}"',
        f'답변은 "로니:"로 시작합니다.',
        f'당신("로니")의 답변은 토론 주제에 대해 "{RONNY_POSITION}"하는 주장을 프롬프트 답변으로 시작합니다.',
    ]

    # 초기 메시지 설정하기
    first_messages = [
        {"role": "system", "content": role} for role in first_system_roles
    ]
    first_messages.extend(
        [{"role": "user", "content": query} for query in first_queries]
    )

    # ChatGPT API 호출하기
    first_response = openai.ChatCompletion.create(model=model, messages=first_messages)
    first_answer = first_response["choices"][0]["message"]["content"]

    # 첫번째 대답
    if first_answer[0:2] == "로니":
        pass
    else:
        first_answer = f"로니: {first_answer}"

    return first_answer

def middle_call(history, DEBATE_TOPIC, USER_POSITION, RONNY_POSITION, DEBATE_LEVEL):
    """
    argument: 입론
    counter_argument: 반론
    conclusion: 결론
    """

    LAST_MESSAGE_AUTHOR = history[-1]['author']  # str : ('user', 'assistant')
    LAST_MESSAGE_TYPE = history[-1]['message_type']  # str : ('arg', 'counter')​

    user_argument_list, user_counter_argument_list, ronny_argument_list, ronny_counter_argument_list = [], [], [], []
    for debate_message in history:
        if debate_message['author'] == "user":
            if debate_message['message_type'] == "arg":
                user_argument_list.append(debate_message['message'])
            elif debate_message['message_type'] == "counter":
                user_counter_argument_list.append(debate_message['message'])
            else:
                print("debate_message.message_type ERROR")
        elif debate_message['author'] == "assistant":
            if debate_message['message_type'] == "arg":
                ronny_argument_list.append(debate_message['message'])
            elif debate_message['message_type'] == "counter":
                ronny_counter_argument_list.append(debate_message['message'])
            else:
                print("debate_message.message_type ERROR")
        else:
            print("debate_message.author ERROR")

    # 중반부 system_role
    middle_system_roles = [
        '당신의 이름은 "로니"이며, 상대방 사용자와 함께 실시간으로 토론을 진행하는 프롬프트 생성 로봇입니다.',
        f'토론의 주제는 "{DEBATE_TOPIC}"입니다.',
        f'당신은 토론 주제에 대해 "{RONNY_POSITION}" 입장을 가지며, 상대방 사용자는 주제에 대해 "{USER_POSITION}" 입장을 가지고 있습니다.',
        f'토론의 난이도는 "쉬움", "어려움" 총 2가지가 있으며, 각각 "11살~15살", "16살~19살"의 연령대를 의미합니다. 이번 토론의 난이도는 "{DEBATE_LEVEL}"입니다.',
        "당신은 프롬프트 생성 시, 토론의 난이도와 사용자 연령대의 수준에 맞는 어휘와 문장 길이를 사용해야 합니다.",
        '토론은 당신(로니)의 "입론", 로니의 입론에 대한 사용자의 반론, 사용자의 입론, 사용자의 입론에 대한 로니의 반론, 로니의 새로운 입론, 로니의 새로운 입론에 대한 사용자의 새로운 반론, 사용자의 새로운 입론, ... 순으로 이루어집니다.',
    ]
    middle_messages = [
        {"role": "system", "content": role} for role in middle_system_roles
    ]

    if LAST_MESSAGE_AUTHOR == "user" and LAST_MESSAGE_TYPE == "arg":  # 사용자 측 입론
        print("========== 사회자: 로니 측 반론 ==========")
        # 반론 system_role
        counter_argument_role = """반론 시에는 4가지 규칙을 따라야 합니다.
```
# 반론규칙
1) 논리 칭찬 / 논리 평가: 상대방의 입론 답변을 들은 뒤에는 프롬프트의 초반 부분에 사용자(상대방)의 입론 속 논리를 분석하고 칭찬하거나 평가해야 한다.
2) 허점 지적: 프롬프트의 중반 부분에는 답변의 허점을 지적하고, 당신(로니)의 논리를 펼치거나 방어해야 한다. 또한, 상대방이 주제와 벗어난 답변을 했을 경우에는 이를 지적해야 한다.
3) 뒷받침 근거: 프롬프트의 후반 부분에는 허점 지적 등에 대한 명확한 뒷받침 근거를 반드시 제시해야 한다.
4) 답변의 양식: 반론의 답변은 250자 이내로 해야 한다. 또한, 답변은 존댓말을 사용하고, 대화체 형식을 준수해야 한다.
```"""
        middle_counter_argument_messages = middle_messages.copy()
        middle_counter_argument_messages.append(
            {"role": "system", "content": counter_argument_role}
        )

        # for i in range(len(ronny_counter_argument_list)):
        #     middle_counter_argument_messages.append({"role": "assistant", "content": f"{ronny_argument_list[i]}"})
        #     middle_counter_argument_messages.append({"role": "user", "content": f"{user_counter_argument_list[i]}"})
        #     middle_counter_argument_messages.append({"role": "user", "content": f"{user_argument_list[i]}"})
        #     middle_counter_argument_messages.append({"role": "assistant", "content": f"{ronny_counter_argument_list[i]}"})
        # middle_counter_argument_messages.append({"role": "assistant", "content": f"{ronny_argument_role[len(ronny_counter_argument_list)+1]}"})
        # middle_counter_argument_messages.append({"role": "user", "content": f"{user_counter_argument_list[len(ronny_counter_argument_list)+1]}"})
        middle_counter_argument_messages.append(
            {
                "role": "user",
                "content": f'주제에 대한 상대방의 입론이 다음과 같을 때, 반론규칙을 준수하여 상대방의 입론에 대한 반론을 대화체로 서술하여 제시하세요. 답변은 "로니:"로 시작합니다. \n상대방 입론: {user_argument_list[-1]}',
            }
        )

        # ChatGPT API 호출하기
        middle_counter_argument_response = openai.ChatCompletion.create(
            model=model, messages=middle_counter_argument_messages
        )
        middle_counter_argument_answer = middle_counter_argument_response["choices"][0][
            "message"
        ]["content"]
        # 사용자 입론에 대한 로니의 반론
        if middle_counter_argument_answer[0:2] == "로니":
            pass
        else:
            middle_counter_argument_answer = f"로니: {middle_counter_argument_answer}"

        return middle_counter_argument_answer

    elif (
        LAST_MESSAGE_AUTHOR == "assistant" and LAST_MESSAGE_TYPE == "counter"
    ):  # 로니 측 반론 후 이어서 로니 측 입론
        print("========== 사회자: 로니 측 입론 ==========")
        # 입론 system_role
        argument_role = f"""입론 시에는 3가지 규칙을 따라야 합니다.
```
# 입론규칙
1) 중복되지 않은 주장 : 토론 주제에 대한 당신(로니)의 {RONNY_POSITION} 입장을 유지한 채로 논리를 펼쳐야 한다. 이때, 입론에서 제시하는 논리는 기존 입론, 그리고 상대방의 입론에 대한 당신의 반론과 중복되지 않은 새로운 논리를 제시해야 한다.
2) 뒷받침 근거: 주장과 논리 등에 대해 반드시 명확한 뒷받침 근거를 제시해야 한다.
3) 답변의 양식: 입론의 답변은 250자 이내로 해야 한다. 또한, 답변은 존댓말을 사용하고, 대화체 형식을 준수해야 한다.
```"""
        middle_argument_messages = middle_messages.copy()
        middle_argument_messages.append({"role": "system", "content": argument_role})

        for i in range(len(ronny_argument_list) - 1):
            middle_argument_messages.append(
                {"role": "assistant", "content": f"당신의 입론: {ronny_argument_list[i]}"}
            )
            # middle_argument_messages.append({"role": "user", "content": f"{user_counter_argument_list[i]}"})
            # middle_argument_messages.append({"role": "user", "content": f"{user_argument_list[i]}"})
            middle_argument_messages.append(
                {
                    "role": "assistant",
                    "content": f"상대방의 입론에 대한 당신의 반론: {ronny_counter_argument_list[i]}",
                }
            )
        middle_argument_messages.append(
            {"role": "assistant", "content": f"당신의 입론: {ronny_argument_list[-1]}"}
        )
        # middle_argument_messages.append({"role": "user", "content": f"{user_counter_argument_list[len(ronny_argument_list)]}"})
        # middle_argument_messages.append({"role": "user", "content": f"{user_argument_list[len(ronny_argument_list)]}"})
        middle_argument_messages.append(
            {
                "role": "user",
                "content": f'당신의 입론과 상대방의 입론에 대한 당신의 반론을 참고하여, 새로운 입론을 대화체로 서술하여 제시하세요. 이때, "{RONNY_POSITION}" 입장을 유지한 채, 입론규칙을 반드시 지켜야합니다. 답변은 "로니:"로 시작합니다.',
            }
        )

        # ChatGPT API 호출하기
        middle_argument_response = openai.ChatCompletion.create(
            model=model, messages=middle_argument_messages
        )
        middle_argument_answer = middle_argument_response["choices"][0]["message"][
            "content"
        ]
        # 로니의 새로운 입론
        if middle_argument_answer[0:2] == "로니":
            pass
        else:
            middle_argument_answer = f"로니: {middle_argument_answer}"
        ronny_argument_list.append(middle_argument_answer)

        return middle_argument_answer

def final_call(history, DEBATE_TOPIC, USER_POSITION, RONNY_POSITION, DEBATE_LEVEL):
    print("========== 사회자: 로니 측 최종 결론 ==========")

    ronny_argument_list = []
    for debate_message in history:
        if debate_message['author'] == "assistant":
            if debate_message['message_type'] == "arg":
                ronny_argument_list.append(debate_message['message'])

    # 마지막 system_role
    final_system_roles = [
        '당신의 이름은 "로니"이며, 상대방 사용자와 함께 실시간으로 토론을 진행하는 프롬프트 생성 로봇입니다.',
        f'토론의 주제는 "{DEBATE_TOPIC}"입니다.',
        f'당신은 토론 주제에 대해 "{RONNY_POSITION}" 입장을 가지며, 상대방 사용자는 주제에 대해 "{USER_POSITION}" 입장을 가지고 있습니다.',
        f'토론의 난이도는 "쉬움", "어려움" 총 2가지가 있으며, 각각 "11살~15살", "16살~19살"의 연령대를 의미합니다. 이번 토론의 난이도는 "{DEBATE_LEVEL}"입니다.',
        "당신은 프롬프트 생성 시, 토론의 난이도와 사용자 연령대의 수준에 맞는 어휘와 문장 길이를 사용해야 합니다.",
        '토론은 당신(로니)의 "입론", 로니의 입론에 대한 사용자의 반론, 사용자의 입론, 사용자의 입론에 대한 로니의 반론, 로니의 새로운 입론, 로니의 새로운 입론에 대한 사용자의 새로운 반론, 사용자의 새로운 입론, ... 순으로 이루어집니다.',
        """최종 결론 시에는 2가지 규칙을 따라야 합니다.
```
# 최종 결론 규칙
1) 입론의 요약 : 최종 결론을 제시할 때는 당신이 제시한 기존 입론들을 기반으로 결론을 생성해야 한다. 제시하지 않았던 새로운 논리를 제시해서는 안된다.
2) 답변의 양식: 반론의 답변은 250자 이내로 해야 한다. 또한, 답변은 존댓말을 사용하고, 대화체 형식을 준수해야 한다.
```""",
    ]
    final_messages = [
        {"role": "system", "content": role} for role in final_system_roles
    ]

    for i in range(len(ronny_argument_list)):
        final_messages.append(
            {"role": "assistant", "content": f"당신의 입론: {ronny_argument_list[i]}"}
        )

    # 마지막 질문 작성하기
    final_messages.append(
        {
            "role": "user",
            "content": f'여태까지 당신이 제시했던 당신의 입론들을 참고하여 최종 결론을 대화체로 서술하여 제시하세요. 이때, 최종 결론 규칙을 반드시 지켜야합니다. 답변은 "로니:"로 시작합니다.',
        }
    )

    # ChatGPT API 호출하기
    final_response = openai.ChatCompletion.create(model=model, messages=final_messages)
    final_answer = final_response["choices"][0]["message"]["content"]

    # 마지막 대답
    if final_answer[0:2] == "로니":
        pass
    else:
        final_answer = f"로니: {final_answer}"

    print(final_answer)
    return final_answer

def get_new_message(debate: Debate, history: List[DebateMessage], end=False):
    
    print(history)
    DEBATE_TOPIC = debate['subject']  # "안락사는 합법화되어야 한다."
    USER_POSITION = "찬성" if debate['position'] == "agree" else "반대"
    RONNY_POSITION = "반대" if USER_POSITION == "찬성" else "찬성"
    DEBATE_LEVEL = ["매우 쉬움", "쉬움", "어려움", "매우 어려움"][debate['level']]

    if len(history) == 0:
        first_answer = first_call(
            DEBATE_TOPIC, USER_POSITION, RONNY_POSITION, DEBATE_LEVEL
        )
        return first_answer

    elif end == True:
        ronny_conclusion = final_call(
            history, DEBATE_TOPIC, USER_POSITION, RONNY_POSITION, DEBATE_LEVEL
        )
        return ronny_conclusion

    else:
        answer = middle_call(
            history, DEBATE_TOPIC, USER_POSITION, RONNY_POSITION, DEBATE_LEVEL
        )
        return answer