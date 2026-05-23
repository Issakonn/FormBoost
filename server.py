"""
FormBoost API Server — server.py
Run: uvicorn server:app --host 0.0.0.0 --port 8000
"""
import os, re, json, random, asyncio, logging, aiosqlite
