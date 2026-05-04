#!/usr/bin/env python3
"""Simulated tokmon demo for terminal recording."""
import time, sys, os

os.environ["TERM"] = "xterm-256color"

def c(code, text):
    return f"\033[{code}m{text}\033[0m"

def slow(text, delay=0.012):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    print()

def section(text):
    print(c("1;36", f"\n  {text}"))
    print(c("36", f"  {'─'*56}"))

print(c("1;33", """
  ████████╗ ██████╗ ██╗  ██╗███╗   ███╗ ██████╗ ███╗   ██╗
  ╚══██╔══╝██╔═══██╗██║ ██╔╝████╗ ████║██╔═══██╗████╗  ██║
     ██║   ██║   ██║█████╔╝ ██╔████╔██║██║   ██║██╔██╗ ██║
     ██║   ██║   ██║██╔═██╗ ██║╚██╔╝██║██║   ██║██║╚██╗██║
     ██║   ╚██████╔╝██║  ██╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
     ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝"""))

time.sleep(0.2)
print(c("2", "  v0.1.0 • LLM token & cost tracker — decorator, dashboards, alerts"))
time.sleep(0.4)

# Show decorator usage
section("1 · Drop-in Decorator")
time.sleep(0.2)

code_lines = [
    "  from tokmon import track_cost",
    "",
    "  @track_cost(budget=0.50, model='gpt-4o')",
    "  def summarize(text: str) -> str:",
    "      return openai.chat(model='gpt-4o', ...)",
    "",
    "  result = summarize(long_document)",
]
for line in code_lines:
    col = "35" if any(kw in line for kw in ["from", "def", "return"]) else "37"
    if "@" in line: col = "33"
    if "import" in line: col = "35"
    print(c(col, line))
    time.sleep(0.05)

time.sleep(0.4)

section("2 · Running Agent Pipeline")
time.sleep(0.3)

calls = [
    ("planner",  "gpt-4o",     "1,240", "0.012",  "0.8s"),
    ("executor", "gpt-4o",     "3,400", "0.034",  "1.2s"),
    ("executor", "gpt-4o",     "2,100", "0.021",  "0.9s"),
    ("observer", "gpt-4o-mini","  480", "0.001",  "0.3s"),
    ("synth",    "gpt-4o",     "  890", "0.009",  "0.5s"),
]

print(f"\n  {c('1','Step'):14s} {c('1','Model'):16s} {c('1','Tokens'):>8s} {c('1','Cost'):>8s} {c('1','Latency'):>8s}")
print(f"  {'─'*14} {'─'*16} {'─'*8} {'─'*8} {'─'*8}")

running_cost = 0.0
for step, model, tok, cost, lat in calls:
    running_cost += float(cost)
    bar_len = int(float(cost) * 600)
    bar = c("33", "█" * bar_len) + c("2", "░" * (20 - bar_len))
    print(f"  {c('37',step):22s} {c('36',model):24s} {c('33',tok):>16s} {c('1;33',f'${cost}'):>16s} {c('2',lat):>16s}")
    time.sleep(0.2)

print(f"\n  {'─'*56}")
print(f"  {c('1','TOTAL'):14s} {'':16s} {c('1;33','8,110'):>8s} {c('1;33','$0.077'):>8s} {c('2','3.7s'):>8s}")

time.sleep(0.4)

# Budget alert
section("3 · Budget Alert")
time.sleep(0.2)

print(f"  Budget: {c('1','$0.50')} / session")
print(f"  Spent:  {c('33','$0.077')} ({c('32','15.4%')})")
print()
bar = c("32", "█" * 8) + c("2", "░" * 44)
print(f"  [{bar}] {c('32','15.4%')}")
print(f"  {c('2','~6 more runs before budget limit')}")
time.sleep(0.3)

# Session dashboard
section("4 · Session Dashboard")
time.sleep(0.2)

print(f"\n  {c('1','Last 5 requests:')}")
print(f"  {'─'*56}")
reqs = [
    ("14:23:01", "summarize",       "gpt-4o",     "3,400", "$0.034"),
    ("14:23:04", "classify_intent", "gpt-4o-mini","  680", "$0.001"),
    ("14:23:05", "generate_reply",  "gpt-4o",     "2,200", "$0.022"),
    ("14:23:08", "translate",       "gpt-4o",     "1,100", "$0.011"),
    ("14:23:10", "summarize",       "gpt-4o",     "3,600", "$0.036"),
]
for ts, func, model, tok, cost in reqs:
    print(f"  {c('2',ts)}  {c('37',func):22s} {c('36',model):22s} {tok:>6s}  {c('33',cost)}")
    time.sleep(0.1)

print(f"\n  {c('1','Session total')}: {c('1;33','11,980 tokens')} • {c('1;33','$0.104')} • {c('2','5 requests')}")

time.sleep(0.4)
print(c("1;36", f"\n  {'─'*56}"))
print(c("1;32", "  ✓ Zero-config • Works with any LLM provider"))
print(c("2",    "    pip install tokmon-ai"))
print(c("1;36", f"  {'─'*56}\n"))
time.sleep(1.0)
