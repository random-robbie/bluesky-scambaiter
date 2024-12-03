#!/usr/bin/env python3
"""
Bluesky Scambaiter - A defensive cybersecurity tool for automated scam response
For authorized security testing and research purposes only.
"""

import os
import asyncio
import logging
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
import aiohttp
from atproto import Client, IdResolver, models
from dataclasses import dataclass
import yaml
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scambaiter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Config:
    bluesky_handle: str
    bluesky_password: str
    openrouter_api_key: str
    target_accounts: List[str]
    check_interval: int
    max_responses_per_hour: int
    response_probability: float
    prompt: str  # AI prompt text
    prompt_file: str  # Path to separate prompt file

@dataclass
class ConversationState:
    last_response_time: float = 0
    awaiting_reply: bool = False
    last_message_id: Optional[str] = None

class MessageDeduplicator:
    def __init__(self, max_size: int = 1000):
        self.seen_messages = set()
        self.max_size = max_size
    
    def is_duplicate(self, message_id: str) -> bool:
        if message_id in self.seen_messages:
            return True
        
        if len(self.seen_messages) >= self.max_size:
            # Remove oldest entries if we hit size limit
            self.seen_messages.clear()
            
        self.seen_messages.add(message_id)
        return False

class PromptMonitor:
    def __init__(self, config: Config):
        self.config = config
        self.last_modified_time = 0
        self.current_prompt = self.load_prompt()
    
    def load_prompt(self) -> str:
        """Load prompt from the prompt file"""
        try:
            with open(self.config.prompt_file, 'r') as f:
                prompt = f.read().strip()
                self.last_modified_time = os.path.getmtime(self.config.prompt_file)
                logger.info("Loaded new prompt from file")
                return prompt
        except Exception as e:
            logger.error(f"Failed to load prompt from file: {str(e)}")
            # Fall back to config prompt if file fails
            return self.config.prompt
    
    def check_for_updates(self) -> str:
        """Check if prompt file has been modified"""
        try:
            current_mtime = os.path.getmtime(self.config.prompt_file)
            if current_mtime > self.last_modified_time:
                self.current_prompt = self.load_prompt()
        except Exception as e:
            logger.error(f"Failed to check prompt file: {str(e)}")
        
        return self.current_prompt

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def acquire(self):
        now = time.time()
        
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time <= self.time_window]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = self.requests[0] + self.time_window - now
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                
        self.requests.append(now)

class BlueskyScambaiter:
    def __init__(self, config: Config):
        self.config = config
        self.client = Client()
        self.id_resolver = IdResolver()
        self.deduplicator = MessageDeduplicator()
        self.rate_limiter = RateLimiter(
            max_requests=config.max_responses_per_hour,
            time_window=3600
        )
        self.conversation_states: Dict[str, ConversationState] = {}
        self.prompt_monitor = PromptMonitor(config)
        
    def login(self):
        """Login to Bluesky"""
        try:
            self.client.login(
                self.config.bluesky_handle,
                self.config.bluesky_password
            )
            logger.info(f"Logged in as {self.config.bluesky_handle}")
            # Create DM client
            self.dm_client = self.client.with_bsky_chat_proxy()
            self.dm = self.dm_client.chat.bsky.convo
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise

    async def get_conversations(self):
        """Fetch conversations with monitored accounts"""
        try:
            # Get list of all conversations
            convo_list = self.dm.list_convos()
            logger.info(f'Found {len(convo_list.convos)} conversations')
            
            # Filter conversations with target accounts
            target_convos = []
            for convo in convo_list.convos:
                members = [member.handle for member in convo.members]
                if any(target in members for target in self.config.target_accounts):
                    target_convos.append(convo)
                    members_str = ', '.join(member.display_name for member in convo.members)
                    logger.info(f'Found target conversation: ID {convo.id} with members: {members_str}')
            
            return target_convos
        except Exception as e:
            logger.error(f"Failed to fetch conversations: {str(e)}")
            return []

    async def should_respond(self, convo_id: str, message) -> bool:
        """Determine if we should respond to a message"""
        if not hasattr(message, 'text'):
            return False

        state = self.conversation_states.get(convo_id)
        if not state:
            state = ConversationState()
            self.conversation_states[convo_id] = state

        # Skip deleted messages
        if message.py_type == 'app.bsky.feed.defs#deletedMessageView':
            return False

        # Don't respond to our own messages
        if message.sender.did == self.client.me.did:
            state.last_message_id = message.id
            state.awaiting_reply = True
            return False

        # If we're awaiting a reply, check if this is a new message
        if state.awaiting_reply:
            if message.id > state.last_message_id:
                state.awaiting_reply = False
                state.last_message_id = None
                return True
            return False

        # Check if message is new
        if self.deduplicator.is_duplicate(message.id):
            return False

        # Update state
        state.last_message_id = message.id
        
        # Apply response probability
        return random.random() < self.config.response_probability

    async def generate_response(self, message: str) -> str:
        """Generate response using OpenRouter API with Mythomax via OpenAI SDK"""
        try:
            # Check for prompt updates
            current_prompt = self.prompt_monitor.check_for_updates()
            
            client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.config.openrouter_api_key,
                default_headers={
                    "HTTP-Referer": "https://github.com/your-repo/bluesky-scambaiter",
                    "X-Title": "Bluesky Scambaiter"
                }
            )
            
            completion = await client.chat.completions.create(
                model="gryphe/mythomax-l2-13b:free",
                messages=[{
                    "role": "user", 
                    "content": current_prompt.format(message=message)
                }],
                max_tokens=150,
                temperature=0.8
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            return "Sorry, having some connection issues! I'll get back to you shortly."

    async def send_response(self, convo_id: str, response: str):
        """Send response and update conversation state"""
        try:
            await self.rate_limiter.acquire()
            
            result = self.dm.send_message(
                models.ChatBskyConvoSendMessage.Data(
                    convo_id=convo_id,
                    message=models.ChatBskyConvoDefs.MessageInput(
                        text=response
                    )
                )
            )
            
            # Update conversation state
            state = self.conversation_states.get(convo_id)
            if state:
                state.last_response_time = time.time()
                state.awaiting_reply = True
                if hasattr(result, 'id'):
                    state.last_message_id = result.id
            
            logger.info(f"Sent response to conversation {convo_id}: {response[:50]}...")
        except Exception as e:
            logger.error(f"Failed to send response: {str(e)}")

    async def run(self):
        """Main loop with improved message flow control"""
        self.login()
        
        while True:
            try:
                conversations = await self.get_conversations()
                
                for convo in conversations:
                    try:
                        messages_response = self.dm.get_messages({
                            'convoId': convo.id,
                            'limit': 50
                        })
                        
                        if hasattr(messages_response, 'messages'):
                            # Messages are already in reverse chronological order (newest first)
                            if messages_response.messages:
                                latest_message = messages_response.messages[0]
                                if await self.should_respond(convo.id, latest_message):
                                    response = await self.generate_response(latest_message.text)
                                    await self.send_response(convo.id, response)
                    
                    except Exception as e:
                        logger.error(f"Error processing conversation {convo.id}: {str(e)}")
                        continue
                
                await asyncio.sleep(self.config.check_interval)
                
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                await asyncio.sleep(60)  # Back off on error

def load_config(path: str = "config.yaml") -> Config:
    """Load configuration from YAML file"""
    try:
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
            return Config(**config_dict)
    except Exception as e:
        logger.error(f"Failed to load config: {str(e)}")
        raise

async def main():
    """Entry point"""
    config = load_config()
    scambaiter = BlueskyScambaiter(config)
    await scambaiter.run()

if __name__ == "__main__":
    asyncio.run(main())
