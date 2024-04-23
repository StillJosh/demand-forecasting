# gpt3_model.py
# Description: A brief description of what this file does.
# Author: Joshua Stiller
# Date: 27.12.23

from dotenv import load_dotenv
from openai import OpenAI
from src.model.utils import serialize_volume, deserialize_volume



class GPT3Model:
    """ API wrapper for the GPT-3 API. """

    def __init__(self, scaler=None):

        load_dotenv()
        self.client = OpenAI()

        self.scaler = scaler

    def predict(self, history, predict_frame=10):
        """
        Predicts the sales volumes for the next predict_frame days.
        Parameters
        ----------
        history: array-lie
            The historic sales volumes.
        predict_frame: int
            The number of days to predict.

        Returns
        -------
        forecast: list,
            The forecasted sales volumes as a list.
        completion: Completion,
            The GPT-3 completion of the prompt.
        """

        if self.scaler is not None:
            history = self.scaler.fit_transform(history.reshape(-1,1))

        input_str = serialize_volume(history, dec_sep=' ')

        chatgpt_sys_message = (f"You predict sales volumes. The user will provide a sequence of historic sales "
                               f"volumes and you will predict the remaining sequence. The decimal values of the "
                               f"volumes are separated by spaces and the different volumina are separated by commas.")
        extra_input = (f"Please continue the following sequence for {predict_frame} values without producing any "
                       f"additional text. Do not say anything like 'the next terms in the sequence are', just return "
                       f"the numbers split by commas. Sequence:\n")

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": chatgpt_sys_message},
                {"role": "user", "content": extra_input + input_str}
            ]
        )

        forecast = deserialize_volume(completion.choices[0].message.content)

        if self.scaler is not None:
            forecast = self.scaler.inverse_transform(forecast)

        return forecast[:predict_frame], completion


    def embed(self, history):
        """
        Embeds the input string.

        Parameters
        ----------
        history: array-like
            The historic sales volumes.

        Returns
        -------
        embedding: list,
            The embedding of the sales data.
        """

        if self.scaler is not None:
            history = self.scaler.fit_transform(history)

        input_str = serialize_volume(history)
        input_str = input_str.replace("\n", " ")
        embedding = self.client.embeddings.create(input=[input_str], model="text-embedding-ada-002").data[0].embedding

        return embedding
