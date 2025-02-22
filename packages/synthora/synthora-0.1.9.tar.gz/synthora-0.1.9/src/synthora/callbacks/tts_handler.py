import pyttsx3
from .base_handler import BaseCallBackHandler
from RealtimeSTT import AudioToTextRecorder
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from synthora.agents.vanilla_agent import VanillaAgent

class TTSHandler(BaseCallBackHandler):
    def __init__(self, agent: "VanillaAgent", rate: int=185):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.recorder = AudioToTextRecorder()
        self.agent = agent
        self.cache = "Yes, you can do your delivery next week. There are no public holidays in London the week after February 14th, so you’re good to go!"
        super().__init__()
    
    def on_llm_end(self, source, message, *args, **kwargs):
        self.recorder.stop()
        if self.cache:
            self.engine.say(self.cache)
            self.cache = ""
        self.engine.say(message.content)
        self.engine.runAndWait()
        self.engine.endLoop()