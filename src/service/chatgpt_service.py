from src.dto.debate import DebateMessageForm
from src.model.debate import DebateMessage, Debate
from typing import List
def get_new_message(debate:Debate, history : List[DebateMessage]):
    return DebateMessageForm(counter=f"사용자의 입론 '{form.arg}'에 대한 gpt 반론입니다",arg="gpt 입론입니다")

def get_end_message(form: DebateMessageForm):
    # ignore form.counter
    return DebateMessageForm(arg=f"사용자의 결론 '{form.arg}'에 대한 gpt 결론입니다")


def get_new_message(debate: Debate, history : List[DebateMessage]):
    return DebateMessageForm(counter=f"사용자의 입론 '{form.arg}'에 대한 gpt 반론입니다",arg="gpt 입론입니다")