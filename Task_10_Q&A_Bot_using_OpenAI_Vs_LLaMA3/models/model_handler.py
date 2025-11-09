import time
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from utils.config import config

class ModelHandler:
    def __init__(self):
        # Initialize Groq (LLaMA3)
        if config.GROQ_API_KEY:
            self.llama3_client = ChatGroq(
                groq_api_key=config.GROQ_API_KEY,
                model_name=config.LLAMA3_MODEL,
                temperature=0.3,
                max_tokens=2048
            )
        else:
            self.llama3_client = None
        
        # Initialize OpenRouter
        if config.OPENROUTER_API_KEY:
            self.openrouter_client = ChatOpenAI(
                api_key=config.OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1",
                model=config.OPENROUTER_MODEL,
                temperature=0.3,
                max_tokens=2048
            )
        else:
            self.openrouter_client = None
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough: 4 chars per token)"""
        return len(text) // 4
    
    def query_openrouter(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Query OpenRouter model"""
        if not self.openrouter_client:
            return {
                "error": "OpenRouter client not initialized",
                "answer": "⚠️ OpenRouter API key missing",
                "latency": 0,
                "tokens": 0,
                "model": "OpenRouter"
            }
        
        start_time = time.time()
        
        try:
            response = self.openrouter_client.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ])
            
            answer = response.content if hasattr(response, 'content') else str(response)
            latency = round(time.time() - start_time, 2)
            
            # Estimate tokens
            tokens = self._estimate_tokens(system_prompt + user_prompt + answer)
            
            return {
                "answer": answer,
                "latency": latency,
                "tokens": tokens,
                "model": "OpenRouter"
            }
        except Exception as e:
            return {
                "error": str(e),
                "answer": f"❌ Error: {str(e)}",
                "latency": round(time.time() - start_time, 2),
                "tokens": 0,
                "model": "OpenRouter"
            }
    
    def query_llama3(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Query LLaMA3 via Groq"""
        if not self.llama3_client:
            return {
                "error": "Groq client not initialized",
                "answer": "⚠️ Groq API key missing",
                "latency": 0,
                "tokens": 0,
                "model": "LLaMA3"
            }
        
        start_time = time.time()
        
        try:
            response = self.llama3_client.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ])
            
            answer = response.content if hasattr(response, 'content') else str(response)
            latency = round(time.time() - start_time, 2)
            
            # Estimate tokens
            tokens = self._estimate_tokens(system_prompt + user_prompt + answer)
            
            return {
                "answer": answer,
                "latency": latency,
                "tokens": tokens,
                "model": "LLaMA3"
            }
        except Exception as e:
            return {
                "error": str(e),
                "answer": f"❌ Error: {str(e)}",
                "latency": round(time.time() - start_time, 2),
                "tokens": 0,
                "model": "LLaMA3"
            }
    
    def query_both(self, system_prompt: str, user_prompt: str) -> Dict[str, Dict[str, Any]]:
        """Query both models"""
        openrouter_result = self.query_openrouter(system_prompt, user_prompt)
        llama3_result = self.query_llama3(system_prompt, user_prompt)
        
        return {
            "openrouter": openrouter_result,
            "llama3": llama3_result
        }
