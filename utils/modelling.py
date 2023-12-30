# module for modelling utilities

# external imports
import gradio as gr


def prompt_limiter(
    tokenizer, message: str, history: list, system_prompt: str, knowledge: str = ""
):
    # initializing the prompt history empty
    prompt_history = []
    # getting the token count for the message, system prompt, and knowledge
    pre_count = (
        token_counter(tokenizer, message)
        + token_counter(tokenizer, system_prompt)
        + token_counter(tokenizer, knowledge)
    )

    # validating the token count
    # check if token count already too high
    if pre_count > 1024:

        # check if token count too high even without knowledge
        if (
            token_counter(tokenizer, message) + token_counter(tokenizer, system_prompt)
            > 1024
        ):

            # show warning and raise error
            gr.Warning("Message and system prompt are too long. Please shorten them.")
            raise RuntimeError(
                "Message and system prompt are too long. Please shorten them."
            )

        # show warning and remove knowledge
        gr.Warning("Knowledge is too long. It has been removed to keep model running.")
        return message, prompt_history, system_prompt, ""

    # if token count small enough, add history
    if pre_count < 800:
        # setting the count to the precount
        count = pre_count
        # reversing the history to prioritize recent conversations
        history.reverse()

        # iterating through the history
        for conversation in history:

            # checking the token count with the current conversation
            count += token_counter(tokenizer, conversation[0]) + token_counter(
                tokenizer, conversation[1]
            )

            # add conversation or break loop depending on token count
            if count < 1024:
                prompt_history.append(conversation)
            else:
                break

    # return the message, prompt history, system prompt, and knowledge
    return message, prompt_history, system_prompt, knowledge


# token counter function using the model tokenizer
def token_counter(tokenizer, text: str):
    # tokenize the text
    tokens = tokenizer(text, return_tensors="pt").input_ids
    # return the token count
    return len(tokens[0])
